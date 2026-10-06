// 3. INTERACTIVE 81-PROVINCE TOUCH PAN & PINCH-ZOOM MAP ENGINE
const MapEngine = {
    selectedCityIdx: 0,
    isSelectingNextRoute: false,
    
    // Smooth Touch Pan & Zoom State
    scale: 1.8,
    panX: 0,
    panY: 0,
    isPanning: false,
    startX: 0,
    startY: 0,
    startPanX: 0,
    startPanY: 0,
    dragDistance: 0,
    
    init() {
        this.renderPins();
        this.highlightProvinces();
        this.bindEvents();
        
        // Initial Camera Setup: Center active city or Turkey overview
        const curIdx = SaveManager.data.currentCityIdx || 0;
        if (SaveManager.data.hasSelectedStartCity) {
            this.focusOnCity(curIdx, 1.8);
        } else {
            this.panCameraTo(550, 250, 1.0);
        }
    },

    renderPins() {
        const pinsLayer = document.getElementById('city-pins-layer');
        if (!pinsLayer) return;
        let html = '';
        CITIES.forEach((c, idx) => {
            const isCurrent = idx === SaveManager.data.currentCityIdx;
            const isCompleted = SaveManager.data.completedProvinces.includes(c.plate);
            
            const fillClass = isCurrent ? 'current' : (isCompleted ? 'completed' : 'unlocked');
            
            // 52px Hitbox (r=26) for generous thumb touch targets on mobile
            html += `<g class="city-pin-node ${fillClass}" data-idx="${idx}" onclick="MapEngine.handlePinClick(${idx})" transform="translate(${c.cx}, ${c.cy})">
                <circle class="pin-hitbox" r="26" fill="transparent" />
                <circle class="city-pin-circle ${fillClass}" r="${isCurrent ? 10 : (isCompleted ? 8 : 6)}" />
                <text class="city-pin-text" y="1">${isCompleted ? '✓' : (c.plate < 10 ? '0' + c.plate : c.plate)}</text>
                <text class="city-label-text" y="${isCurrent ? -14 : -11}">${c.name}</text>
            </g>`;
        });
        pinsLayer.innerHTML = html;
    },

    highlightProvinces() {
        document.querySelectorAll('.province-path').forEach(el => {
            const plate = parseInt(el.dataset.plate);
            const cityIdx = CITIES.findIndex(c => c.plate === plate);
            el.classList.remove('active-city', 'completed', 'locked');
            
            if (cityIdx === SaveManager.data.currentCityIdx) {
                el.classList.add('active-city');
            } else if (SaveManager.data.completedProvinces.includes(plate)) {
                el.classList.add('completed');
            }
        });
    },

    bindEvents() {
        const stage = document.getElementById('map-stage-wrapper');
        if (stage) {
            stage.addEventListener('pointerdown', (e) => this.onPointerDown(e));
            window.addEventListener('pointermove', (e) => this.onPointerMove(e));
            window.addEventListener('pointerup', (e) => this.onPointerUp(e));
            window.addEventListener('pointercancel', (e) => this.onPointerUp(e));
            
            // Desktop Wheel Zoom
            stage.addEventListener('wheel', (e) => {
                e.preventDefault();
                const delta = e.deltaY < 0 ? 1.18 : 0.85;
                this.setZoom(this.scale * delta, e.clientX, e.clientY);
            }, { passive: false });
        }

        document.querySelectorAll('.province-path').forEach(el => {
            el.addEventListener('click', () => {
                if (this.dragDistance > 8) return;
                const plate = parseInt(el.dataset.plate);
                const cityIdx = CITIES.findIndex(c => c.plate === plate);
                if (cityIdx !== -1) MapEngine.selectCity(cityIdx);
            });
        });
    },

    onPointerDown(e) {
        if (e.target.closest('#map-city-card') || e.target.closest('.map-controls-floating')) return;
        
        // If clicking outside on the map, dismiss card and unfocus
        if (!e.target.closest('.city-pin-node') && !e.target.closest('.province-path')) {
            this.closeCard();
        }
        
        this.isPanning = true;
        this.startX = e.clientX;
        this.startY = e.clientY;
        this.startPanX = this.panX;
        this.startPanY = this.panY;
        this.dragDistance = 0;
        
        const viewport = document.getElementById('map-viewport');
        if (viewport) viewport.style.transition = 'none';
    },

    onPointerMove(e) {
        if (!this.isPanning) return;
        const dx = e.clientX - this.startX;
        const dy = e.clientY - this.startY;
        this.dragDistance = Math.hypot(dx, dy);
        
        this.panX = this.startPanX + dx;
        this.panY = this.startPanY + dy;
        this.applyTransform(false);
    },

    onPointerUp(e) {
        if (!this.isPanning) return;
        this.isPanning = false;
        this.applyTransform(true);
    },

    handlePinClick(idx) {
        if (this.dragDistance > 8) return; 
        this.selectCity(idx);
    },

    zoomIn() {
        this.setZoom(Math.min(3.8, this.scale * 1.3));
    },

    zoomOut() {
        this.setZoom(Math.max(0.65, this.scale / 1.3));
    },

    resetCamera() {
        const curIdx = SaveManager.data.currentCityIdx || 0;
        this.focusOnCity(curIdx, 2.0);
    },

    setZoom(newScale, focalX, focalY) {
        const container = document.getElementById('map-stage-wrapper') || document.getElementById('map-viewport')?.parentElement || document.body;
        const vpW = container.clientWidth || 360;
        const vpH = container.clientHeight || 500;
        
        const focusX = (focalX !== undefined) ? focalX : (vpW / 2);
        const focusY = (focalY !== undefined) ? focalY : (vpH / 2);

        // Keep focal point stationary during zoom
        const mapX = (focusX - this.panX) / this.scale;
        const mapY = (focusY - this.panY) / this.scale;

        this.scale = Math.max(0.65, Math.min(3.8, newScale));
        this.panX = focusX - (mapX * this.scale);
        this.panY = focusY - (mapY * this.scale);
        this.applyTransform(true);
        this.updateZoomClasses();
    },

    applyTransform(smooth = false) {
        const viewport = document.getElementById('map-viewport');
        if (!viewport) return;
        viewport.style.transition = smooth ? 'transform 0.5s cubic-bezier(0.25, 1, 0.5, 1)' : 'none';
        viewport.style.transform = `translate3d(${this.panX}px, ${this.panY}px, 0) scale(${this.scale})`;
    },

    updateZoomClasses() {
        const svg = document.getElementById('turkey-map-svg');
        if (!svg) return;
        if (this.scale <= 1.25) {
            svg.classList.add('zoomed-out');
        } else {
            svg.classList.remove('zoomed-out');
        }
    },

    panCameraTo(cx, cy, scale = 2.0) {
        const container = document.getElementById('map-stage-wrapper') || document.getElementById('map-viewport')?.parentElement || document.body;
        this.scale = scale;
        this.panX = (container.clientWidth / 2) - (cx * scale);
        this.panY = (container.clientHeight / 2) - (cy * scale);
        this.applyTransform(true);
        this.updateZoomClasses();
    },

    focusOnCity(idx, customScale) {
        if (idx < 0 || idx >= CITIES.length) return;
        const city = CITIES[idx];
        const path = document.querySelector(`.province-path[data-plate="${city.plate}"]`);
        
        let centerX = city.cx;
        let centerY = city.cy;
        
        if (path) {
            const bbox = path.getBBox();
            centerX = bbox.x + bbox.width / 2;
            centerY = bbox.y + bbox.height / 2;
        }
        
        const container = document.getElementById('map-stage-wrapper') || document.getElementById('map-viewport')?.parentElement || document.body;
        const scale = customScale || 2.0;
        
        const targetX = (container.clientWidth / 2) - (centerX * scale);
        const targetY = (container.clientHeight / 2) - (centerY * scale);
        
        this.scale = scale;
        this.panX = targetX;
        this.panY = targetY;
        this.applyTransform(true);
        this.updateZoomClasses();
        
        // Visual focus styling
        const svg = document.getElementById('turkey-map-svg');
        if (svg) {
            svg.classList.add('has-focus');
            document.querySelectorAll('.province-path').forEach(el => el.classList.remove('focused'));
            if (path) path.classList.add('focused');
        }
    },

    selectCity(idx) {
        if (idx < 0 || idx >= CITIES.length) return;
        this.selectedCityIdx = idx;
        const city = CITIES[idx];
        const isCurrent = idx === SaveManager.data.currentCityIdx;
        const isCompleted = SaveManager.data.completedProvinces.includes(city.plate);
        const hasStarted = SaveManager.data.hasSelectedStartCity;
        
        // Populate card
        document.getElementById('card-city-plate').innerText = city.plate < 10 ? '0' + city.plate : city.plate;
        document.getElementById('card-city-name').innerText = city.name;
        
        const curCity = CITIES[SaveManager.data.currentCityIdx] || CITIES[0];
        const isCurCompleted = SaveManager.data.completedProvinces.includes(curCity.plate);
        
        const descEl = document.getElementById('card-city-desc');
        if (isCompleted) {
            descEl.innerHTML = `<span style="color:#10b981; font-weight:bold;">✓ Vilayet Keşif Mührü Alındı</span><br>${city.name} ilimizin 5 mekanındaki 25 bulmacayı başarıyla tamamladın. Koleksiyon kartpostalın mühürlendi.`;
        } else if (isCurrent && hasStarted) {
            const sub = SaveManager.data.currentSubLevel;
            const m = Math.floor(sub / 5) + 1;
            const b = (sub % 5) + 1;
            descEl.innerHTML = `<span style="color:#f59e0b; font-weight:bold;">📍 Aktif Sefer</span> • Keşif: Mekan ${m}/5 — Bölüm ${b}/5<br>${city.name} ilindeki yolculuğun devam ediyor (${sub + 1}/25).`;
        } else if (!hasStarted) {
            descEl.innerHTML = `5 Mekan • 25 Bölüm • Altın Keşif Mührü<br>${city.name} ilini başlangıç noktan olarak seç ve maceraya başla!`;
        } else if (this.isSelectingNextRoute || isCurCompleted) {
            descEl.innerHTML = `5 Mekan • 25 Bölüm • Altın Keşif Mührü<br>Yeni rotanı ${city.name} olarak belirle ve keşfe başla!`;
        } else {
            descEl.innerHTML = `<span style="color:#ef4444; font-weight:bold;">🔒 Kilitli İl</span> • 5 Mekan • 25 Bölüm<br>Bu ile geçebilmek için önce aktif ilin olan <strong>${curCity.name}</strong> ilindeki 25 bulmacayı tamamlamalısın!`;
        }

        // Action button state & text
        const actionBtn = document.getElementById('card-action-btn') || document.querySelector('#map-city-card button.btn-3d');
        if (actionBtn) {
            actionBtn.style.pointerEvents = 'auto';

            if (!hasStarted) {
                actionBtn.innerText = "YOLCULUĞA BURADAN BAŞLA ➔";
                actionBtn.style.opacity = '1';
                actionBtn.onclick = () => MapEngine.startAtCity(idx);
            } else if (isCurrent) {
                actionBtn.innerText = isCompleted ? "TEKRAR OYNA ➔" : "OYUNA DEVAM ET ➔";
                actionBtn.style.opacity = '1';
                actionBtn.onclick = () => MapEngine.playSelectedCity();
            } else if (isCompleted) {
                actionBtn.innerText = "TEKRAR OYNA ➔";
                actionBtn.style.opacity = '1';
                actionBtn.onclick = () => MapEngine.travelToCity(idx);
            } else if (this.isSelectingNextRoute || isCurCompleted) {
                actionBtn.innerText = "BURAYA SEYAHAT ET ➔";
                actionBtn.style.opacity = '1';
                actionBtn.onclick = () => MapEngine.travelToCity(idx);
            } else {
                actionBtn.innerText = `🔒 KİLİTLİ (Önce ${curCity.name})`;
                actionBtn.style.opacity = '0.65';
                actionBtn.onclick = () => MapEngine.showLockedToast(curCity.name);
            }
        }

        document.getElementById('map-city-card').classList.add('active');

        // Smoothly focus camera on selected city using the exact mathematical center formula
        this.focusOnCity(idx, 2.0);
    },

    showLockedToast(cityName) {
        if (window.AudioEngine) AudioEngine.playWrong();
        let toast = document.getElementById('map-locked-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'map-locked-toast';
            toast.className = 'map-locked-toast';
            document.body.appendChild(toast);
        }
        toast.innerHTML = `🔒 <strong>Bu il kilitli!</strong><br>Önce <strong>${cityName}</strong> ilindeki 25 bulmacayı tamamlamalısın!`;
        toast.classList.add('active');
        setTimeout(() => toast.classList.remove('active'), 2500);
    },

    startAtCity(idx) {
        SaveManager.data.hasSelectedStartCity = true;
        SaveManager.data.currentCityIdx = idx;
        SaveManager.data.currentSubLevel = 0;
        SaveManager.save();
        this.closeCard();
        App.updateUI();
        App.goToScreen('screen-game');
    },

    travelToCity(targetIdx) {
        const fromIdx = SaveManager.data.currentCityIdx;
        this.closeCard();
        
        if (fromIdx === targetIdx) {
            this.playSelectedCity();
            return;
        }

        this.animateTravel(fromIdx, targetIdx, () => {
            SaveManager.data.currentCityIdx = targetIdx;
            SaveManager.data.currentSubLevel = 0;
            SaveManager.save();
            MapEngine.isSelectingNextRoute = false;
            App.updateUI();
            App.goToScreen('screen-game');
        });
    },

    closeCard() {
        const card = document.getElementById('map-city-card');
        if (card) card.classList.remove('active');
        const svg = document.getElementById('turkey-map-svg');
        if (svg) {
            svg.classList.remove('has-focus');
            document.querySelectorAll('.province-path').forEach(el => el.classList.remove('focused'));
        }
    },

    playSelectedCity() {
        SaveManager.data.currentCityIdx = this.selectedCityIdx;
        SaveManager.save();
        this.closeCard();
        App.goToScreen('screen-game');
    },

    animateTravel(fromIdx, toIdx, callback) {
        const fromCity = CITIES[fromIdx];
        const toCity = CITIES[toIdx];
        const route = document.getElementById('travel-route');
        const carrier = document.getElementById('travel-carrier');

        if (!fromCity || !toCity || !route || !carrier) {
            if (callback) callback();
            return;
        }

        // Curved route (quadratic bezier) with dashed golden line
        const midX = (fromCity.cx + toCity.cx) / 2;
        const midY = Math.min(fromCity.cy, toCity.cy) - 60;
        const d = `M ${fromCity.cx} ${fromCity.cy} Q ${midX} ${midY} ${toCity.cx} ${toCity.cy}`;
        route.setAttribute('d', d);
        route.style.opacity = '1';
        carrier.style.opacity = '1';

        const totalLen = route.getTotalLength();
        let start = null;
        const duration = 1500;
        const container = document.getElementById('map-stage-wrapper') || document.getElementById('map-viewport')?.parentElement || document.body;
        const scale = 2.0;

        const self = this;
        function step(ts) {
            if (!start) start = ts;
            const elapsed = ts - start;
            const progress = Math.min(elapsed / duration, 1);
            
            // easeInOutQuad
            const ease = progress < 0.5 ? 2 * progress * progress : -1 + (4 - 2 * progress) * progress;
            const pt = route.getPointAtLength(ease * totalLen);
            carrier.setAttribute('transform', `translate(${pt.x}, ${pt.y}) scale(1.5)`);

            // Smooth camera follow tracking the carrier in center
            self.panX = (container.clientWidth / 2) - (pt.x * scale);
            self.panY = (container.clientHeight / 2) - (pt.y * scale);
            self.scale = scale;
            self.applyTransform(false);

            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                setTimeout(() => {
                    route.style.opacity = '0';
                    carrier.style.opacity = '0';
                    if (callback) callback();
                }, 250);
            }
        }
        requestAnimationFrame(step);
    }
};
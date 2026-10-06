// 3. INTERACTIVE 81-PROVINCE TOUCH PAN & PINCH-ZOOM MAP ENGINE
const MapEngine = {
    selectedCityIdx: 0,
    isSelectingNextRoute: false,
    
    // ViewBox state (Initial viewBox 0 0 1100 500)
    vbX: 0,
    vbY: 0,
    vbW: 1100,
    vbH: 500,
    
    targetVbX: 0,
    targetVbY: 0,
    targetVbW: 1100,
    targetVbH: 500,

    isPanning: false,
    startX: 0,
    startY: 0,
    startVbX: 0,
    startVbY: 0,
    dragDistance: 0,
    
    rafId: null,
    
    init() {
        this.renderPins();
        this.highlightProvinces();
        this.bindEvents();
        
        // Start continuous viewBox lerp loop
        this.startLerpLoop();
    },

    startLerpLoop() {
        const step = () => {
            // Cubic-bezier smooth lerping
            this.vbX += (this.targetVbX - this.vbX) * 0.1;
            this.vbY += (this.targetVbY - this.vbY) * 0.1;
            this.vbW += (this.targetVbW - this.vbW) * 0.1;
            this.vbH += (this.targetVbH - this.vbH) * 0.1;
            
            const svg = document.getElementById('turkey-map-svg');
            if (svg) {
                svg.setAttribute('viewBox', `${this.vbX} ${this.vbY} ${this.vbW} ${this.vbH}`);
                if (this.vbW > 700) {
                    svg.classList.add('zoomed-out');
                } else {
                    svg.classList.remove('zoomed-out');
                }
            }
            this.rafId = requestAnimationFrame(step);
        };
        if (!this.rafId) step();
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
        const svg = document.getElementById('turkey-map-svg');
        if (svg) {
            svg.addEventListener('pointerdown', (e) => this.onPointerDown(e));
            window.addEventListener('pointermove', (e) => this.onPointerMove(e));
            window.addEventListener('pointerup', (e) => this.onPointerUp(e));
            window.addEventListener('pointercancel', (e) => this.onPointerUp(e));
            
            // Desktop Wheel Zoom
            svg.addEventListener('wheel', (e) => {
                e.preventDefault();
                const delta = e.deltaY < 0 ? 0.85 : 1.15;
                this.setZoom(delta, e);
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
        
        // If they click outside the card on the map, close the card and remove focus
        if (!e.target.closest('.city-pin-node') && !e.target.closest('.province-path')) {
             this.closeCard();
        }
        
        this.isPanning = true;
        this.startX = e.clientX;
        this.startY = e.clientY;
        this.startVbX = this.targetVbX;
        this.startVbY = this.targetVbY;
        this.dragDistance = 0;
    },

    onPointerMove(e) {
        if (!this.isPanning) return;
        const dx = e.clientX - this.startX;
        const dy = e.clientY - this.startY;
        this.dragDistance = Math.hypot(dx, dy);
        
        // Convert screen pixel delta to viewBox units
        const stage = document.getElementById('map-stage-wrapper');
        const vpW = stage.clientWidth || 1;
        const ratio = this.targetVbW / vpW;
        
        this.targetVbX = this.startVbX - dx * ratio;
        this.targetVbY = this.startVbY - dy * ratio;
        this.clampBounds();
    },

    onPointerUp(e) {
        if (!this.isPanning) return;
        this.isPanning = false;
        this.clampBounds();
    },

    handlePinClick(idx) {
        if (this.dragDistance > 8) return; 
        this.selectCity(idx);
    },

    setZoom(delta, e) {
        const svg = document.getElementById('turkey-map-svg');
        const rect = svg.getBoundingClientRect();
        
        // Pointer position relative to SVG element
        const px = e.clientX - rect.left;
        const py = e.clientY - rect.top;
        
        // Convert to percentage of current viewBox
        const pxPct = px / rect.width;
        const pyPct = py / rect.height;
        
        // Focal point in viewBox coordinates
        const focalX = this.targetVbX + (this.targetVbW * pxPct);
        const focalY = this.targetVbY + (this.targetVbH * pyPct);
        
        let newVbW = this.targetVbW * delta;
        let newVbH = this.targetVbH * delta;
        
        // Constrain Zoom
        if (newVbW < 150) { newVbW = 150; newVbH = 150 * (500/1100); }
        if (newVbW > 1100) { newVbW = 1100; newVbH = 500; }
        
        this.targetVbW = newVbW;
        this.targetVbH = newVbH;
        this.targetVbX = focalX - (newVbW * pxPct);
        this.targetVbY = focalY - (newVbH * pyPct);
        this.clampBounds();
    },

    zoomIn() {
        this.targetVbW *= 0.75;
        this.targetVbH *= 0.75;
        this.targetVbX += (this.vbW - this.targetVbW) / 2;
        this.targetVbY += (this.vbH - this.targetVbH) / 2;
        this.clampBounds();
    },

    zoomOut() {
        this.targetVbW *= 1.33;
        this.targetVbH *= 1.33;
        this.targetVbX -= (this.targetVbW - this.vbW) / 2;
        this.targetVbY -= (this.targetVbH - this.vbH) / 2;
        this.clampBounds();
    },

    resetCamera() {
        const curIdx = SaveManager.data.currentCityIdx;
        this.focusOnCity(curIdx);
    },

    clampBounds() {
        // Constrain width
        if (this.targetVbW > 1100) { this.targetVbW = 1100; this.targetVbH = 500; }
        if (this.targetVbW < 150) { this.targetVbW = 150; this.targetVbH = 150 * (500/1100); }
        
        // Constrain position (padding around edges)
        const minX = -100;
        const maxX = 1100 - this.targetVbW + 100;
        const minY = -100;
        const maxY = 500 - this.targetVbH + 100;
        
        if (this.targetVbX < minX) this.targetVbX = minX;
        if (this.targetVbX > maxX) this.targetVbX = maxX;
        if (this.targetVbY < minY) this.targetVbY = minY;
        if (this.targetVbY > maxY) this.targetVbY = maxY;
    },

    focusOnCity(idx) {
        if (idx < 0 || idx >= CITIES.length) return;
        const city = CITIES[idx];
        const path = document.querySelector(`.province-path[data-plate="${city.plate}"]`);
        if (!path) {
            // Fallback to center point
            this.targetVbW = 300;
            this.targetVbH = 136;
            this.targetVbX = city.cx - this.targetVbW/2;
            this.targetVbY = city.cy - this.targetVbH/2;
            this.clampBounds();
            return;
        }

        const bbox = path.getBBox();
        const stage = document.getElementById('map-stage-wrapper');
        const aspect = (stage.clientWidth || 360) / (stage.clientHeight || 500);
        
        // 35% padding inside the box
        const padW = bbox.width * 1.70;
        const padH = bbox.height * 1.70;
        
        let newW, newH;
        if (padW / padH > aspect) {
            newW = padW;
            newH = padW / aspect;
        } else {
            newH = padH;
            newW = padH * aspect;
        }
        
        // Enforce max limits
        if (newW > 1100) {
            newW = 1100;
            newH = 1100 / aspect;
        }
        
        const cx = bbox.x + bbox.width / 2;
        const cy = bbox.y + bbox.height / 2;
        
        this.targetVbW = newW;
        this.targetVbH = newH;
        this.targetVbX = cx - newW / 2;
        this.targetVbY = cy - newH / 2;
        this.clampBounds();
        
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

        // Smoothly focus camera on selected city using true SVG BBox
        this.focusOnCity(idx);
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

        // Animate viewBox lerp tracking the zeppelin
        const initialVbX = this.targetVbX;
        const initialVbY = this.targetVbY;

        const stage = document.getElementById('map-stage-wrapper');
        const aspect = (stage.clientWidth || 360) / (stage.clientHeight || 500);
        this.targetVbW = 400; // Zoom in for travel tracking
        this.targetVbH = 400 / aspect;

        const self = this;
        function step(ts) {
            if (!start) start = ts;
            const elapsed = ts - start;
            const progress = Math.min(elapsed / duration, 1);
            
            // easeInOutQuad
            const ease = progress < 0.5 ? 2 * progress * progress : -1 + (4 - 2 * progress) * progress;
            const pt = route.getPointAtLength(ease * totalLen);
            carrier.setAttribute('transform', `translate(${pt.x}, ${pt.y}) scale(1.5)`);

            // Camera tracks the carrier
            self.targetVbX = pt.x - self.targetVbW / 2;
            self.targetVbY = pt.y - self.targetVbH / 2;
            self.clampBounds();

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
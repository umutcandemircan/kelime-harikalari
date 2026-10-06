// 3. INTERACTIVE 81-PROVINCE TOUCH PAN & PINCH-ZOOM MAP ENGINE
const MapEngine = {
    selectedCityIdx: 0,
    isSelectingNextRoute: false,
    
    // Smooth Touch Pan & Zoom State
    scale: 1.6,
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
                const delta = e.deltaY < 0 ? 1.15 : 0.87;
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
        this.clampBounds();
        this.applyTransform(true);
    },

    handlePinClick(idx) {
        if (this.dragDistance > 8) return; // Ignore drag release on pins
        this.selectCity(idx);
    },

    zoomIn() {
        this.setZoom(Math.min(3.8, this.scale * 1.3));
    },

    zoomOut() {
        this.setZoom(Math.max(0.75, this.scale / 1.3));
    },

    resetCamera() {
        const cur = CITIES[SaveManager.data.currentCityIdx] || CITIES[0];
        this.panCameraTo(cur.cx, cur.cy, 1.8);
    },

    setZoom(newScale, focalX, focalY) {
        const stage = document.getElementById('map-stage-wrapper');
        const vpW = stage ? stage.clientWidth : 360;
        const vpH = stage ? stage.clientHeight : 500;
        
        const focusX = (focalX !== undefined) ? focalX : (vpW / 2);
        const focusY = (focalY !== undefined) ? focalY : (vpH / 2);

        // Keep focal point stationary during zoom
        const svgX = (focusX - this.panX) / this.scale;
        const svgY = (focusY - this.panY) / this.scale;

        this.scale = Math.max(0.75, Math.min(3.8, newScale));
        this.panX = focusX - (svgX * this.scale);
        this.panY = focusY - (svgY * this.scale);
        this.clampBounds();
        this.applyTransform(true);
    },

    clampBounds() {
        const stage = document.getElementById('map-stage-wrapper');
        const vpW = stage ? stage.clientWidth : 360;
        const vpH = stage ? stage.clientHeight : 500;
        
        const mapW = 1100 * this.scale;
        const mapH = 500 * this.scale;
        
        const minX = vpW - mapW - 100;
        const maxX = 100;
        const minY = vpH - mapH - 100;
        const maxY = 100;

        if (mapW > vpW) {
            this.panX = Math.min(maxX, Math.max(minX, this.panX));
        }
        if (mapH > vpH) {
            this.panY = Math.min(maxY, Math.max(minY, this.panY));
        }
    },

    applyTransform(smooth = false) {
        const viewport = document.getElementById('map-viewport');
        if (!viewport) return;
        viewport.style.transition = smooth ? 'transform 0.5s cubic-bezier(0.25, 1, 0.5, 1)' : 'none';
        viewport.style.transform = `translate3d(${this.panX}px, ${this.panY}px, 0) scale(${this.scale})`;
    },

    panCameraTo(cx, cy, scale) {
        const stage = document.getElementById('map-stage-wrapper');
        if (!stage) return;
        
        const vpW = stage.clientWidth || 360;
        const vpH = stage.clientHeight || 500;
        
        this.scale = scale || this.scale || 1.8;
        this.panX = (vpW / 2) - (cx * this.scale);
        this.panY = (vpH / 2) - (cy * this.scale);
        this.clampBounds();
        this.applyTransform(true);
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
        
        const totalLevels = city.levels ? city.levels.length : 10;
        const starInfo = SaveManager.getCityStars(idx, totalLevels);
        
        const descEl = document.getElementById('card-city-desc');
        if (isCompleted) {
            descEl.innerHTML = `<span style="color:#10b981; font-weight:bold;">✓ Mühürlendi</span> • ⭐ ${starInfo.earned}/${starInfo.max} Yıldız<br>${city.name} ilimizin 5 mekanındaki 10 bulmacayı başarıyla tamamladın.`;
        } else if (isCurrent && hasStarted) {
            const sub = SaveManager.data.currentSubLevel;
            const m = Math.floor(sub / 2) + 1;
            const b = (sub % 2) + 1;
            descEl.innerHTML = `<span style="color:#f59e0b; font-weight:bold;">📍 Aktif Sefer</span> • Mekan ${m}/5 • Bulmaca ${b}/2<br>${city.name} ilindeki yolculuğun devam ediyor.`;
        } else {
            descEl.innerHTML = `5 Mekan • 10 Bulmaca • ⭐ 0/${totalLevels * 3} Yıldız<br>${city.name} ilinin tarihi ve kültürel güzelliklerini keşfet.`;
        }

        // Action button state & text
        const actionBtn = document.getElementById('card-action-btn') || document.querySelector('#map-city-card button.btn-3d');
        if (actionBtn) {
            actionBtn.style.opacity = '1';
            actionBtn.style.pointerEvents = 'auto';

            if (!hasStarted) {
                actionBtn.innerText = "YOLCULUĞA BURADAN BAŞLA ➔";
                actionBtn.onclick = () => MapEngine.startAtCity(idx);
            } else if (this.isSelectingNextRoute || (isCompleted && !isCurrent) || (!isCompleted && !isCurrent)) {
                actionBtn.innerText = isCompleted ? "TEKRAR OYNA ➔" : "BURAYA SEYAHAT ET ➔";
                actionBtn.onclick = () => MapEngine.travelToCity(idx);
            } else {
                actionBtn.innerText = isCompleted ? "TEKRAR OYNA ➔" : "OYUNA DEVAM ET ➔";
                actionBtn.onclick = () => MapEngine.playSelectedCity();
            }
        }

        document.getElementById('map-city-card').classList.add('active');

        // Smoothly focus camera on selected city
        this.panCameraTo(city.cx, city.cy, 2.2);
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

        // Animate curved travel route and then enter game
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

        // Curved route (quadratic bezier)
        const midX = (fromCity.cx + toCity.cx) / 2;
        const midY = Math.min(fromCity.cy, toCity.cy) - 40;
        const d = `M ${fromCity.cx} ${fromCity.cy} Q ${midX} ${midY} ${toCity.cx} ${toCity.cy}`;
        route.setAttribute('d', d);
        route.style.opacity = '1';
        carrier.style.opacity = '1';

        const totalLen = route.getTotalLength();
        let start = null;
        const duration = 1400;

        const panStartCx = fromCity.cx;
        const panStartCy = fromCity.cy;
        const panEndCx = toCity.cx;
        const panEndCy = toCity.cy;

        const self = this;
        function step(ts) {
            if (!start) start = ts;
            const elapsed = ts - start;
            const progress = Math.min(elapsed / duration, 1);
            const ease = progress < 0.5 ? 2 * progress * progress : -1 + (4 - 2 * progress) * progress;
            const pt = route.getPointAtLength(ease * totalLen);
            carrier.setAttribute('transform', `translate(${pt.x}, ${pt.y})`);

            // Smooth camera follow
            const curCx = panStartCx + (panEndCx - panStartCx) * ease;
            const curCy = panStartCy + (panEndCy - panStartCy) * ease;
            self.panCameraTo(curCx, curCy, 2.0);

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
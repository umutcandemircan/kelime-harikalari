// 3. INTERACTIVE 3D WORLD ATLAS & CITY MAP ENGINE
const MapEngine = {
    selectedCityIdx: 0,
    selectedWorldCity: null,
    isWorldCitySelected: false,
    isSelectingNextRoute: false,
    
    // Smooth Touch Pan & Zoom State
    scale: 1.2,
    panX: 0,
    panY: 0,
    isPanning: false,
    startX: 0,
    startY: 0,
    startPanX: 0,
    startPanY: 0,
    dragDistance: 0,
    
    // Pinch to Zoom
    isPinching: false,
    startPinchDist: 0,
    startPinchScale: 1,

    init() {
        this.renderWorldCities();
        this.renderTurkeyPins();
        this.highlightProvinces();
        this.bindEvents();
        
        // Initial setup
        const curIdx = SaveManager.data.currentCityIdx || 0;
        if (SaveManager.data.hasSelectedStartCity) {
            this.focusOnTurkeyCity(curIdx, 1.8);
        } else {
            this.panCameraTo(550, 250, 1.1, true);
        }
    },

    // RENDER WORLD CITIES (PARIS, ROME, TOKYO, NEW YORK, CAIRO, ETC.)
    renderWorldCities() {
        const layer = document.getElementById('world-cities-layer');
        if (!layer || typeof WORLD_CITIES === 'undefined') return;
        
        let html = '';
        WORLD_CITIES.forEach((country, cIdx) => {
            (country.cities || []).forEach((city, cityIdx) => {
                html += `<g class="city-pin-node world-city-node" data-cidx="${cIdx}" data-cityidx="${cityIdx}" onclick="MapEngine.selectWorldCity(${cIdx}, ${cityIdx})" transform="translate(${city.cx}, ${city.cy})">
                    <circle class="pin-hitbox" r="28" fill="transparent" />
                    <circle class="city-pin-circle world-pin-circle" r="8" fill="#1e293b" stroke="#d4af37" stroke-width="2" />
                    <text class="city-pin-text" y="1" font-size="9" fill="#d4af37">🔒</text>
                    <text class="city-label-text" y="-12" font-size="11" font-weight="700" fill="#FAF4E6">${city.name}</text>
                    <text y="18" text-anchor="middle" font-size="8" fill="#94a3b8">${country.flag} ${country.country}</text>
                </g>`;
            });
        });
        layer.innerHTML = html;
    },

    // RENDER TURKEY 81 PROVINCES
    renderTurkeyPins() {
        const pinsLayer = document.getElementById('city-pins-layer');
        if (!pinsLayer || typeof CITIES === 'undefined') return;
        
        let html = '';
        CITIES.forEach((c, idx) => {
            const isCurrent = idx === SaveManager.data.currentCityIdx;
            const isCompleted = SaveManager.data.completedProvinces.includes(c.plate);
            const fillClass = isCurrent ? 'current' : (isCompleted ? 'completed' : 'unlocked');
            
            html += `<g class="city-pin-node ${fillClass}" data-idx="${idx}" onclick="MapEngine.selectTurkeyCity(${idx})" transform="translate(${c.cx}, ${c.cy})">
                <circle class="pin-hitbox" r="28" fill="transparent" />
                <circle class="city-pin-circle ${fillClass}" r="${isCurrent ? 11 : (isCompleted ? 8 : 6.5)}" />
                <text class="city-pin-text" y="1">${isCompleted ? '✓' : (c.plate < 10 ? '0' + c.plate : c.plate)}</text>
                <text class="city-label-text" y="${isCurrent ? -15 : -11}">${c.name}</text>
            </g>`;
        });
        pinsLayer.innerHTML = html;
    },

    highlightProvinces() {
        if (typeof CITIES === 'undefined') return;
        document.querySelectorAll('.province-path').forEach(el => {
            const plate = parseInt(el.dataset.plate);
            const cityIdx = CITIES.findIndex(c => c.plate === plate);
            el.classList.remove('active-city', 'completed', 'locked', 'focused');
            
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
            stage.addEventListener('touchstart', (e) => this.onTouchStart(e), { passive: false });
            stage.addEventListener('touchmove', (e) => this.onTouchMove(e), { passive: false });
            stage.addEventListener('touchend', (e) => this.onTouchEnd(e), { passive: false });
            stage.addEventListener('touchcancel', (e) => this.onTouchEnd(e), { passive: false });
            
            stage.addEventListener('pointerdown', (e) => { if(e.pointerType === 'mouse') this.onPointerDown(e); });
            window.addEventListener('pointermove', (e) => { if(e.pointerType === 'mouse') this.onPointerMove(e); });
            window.addEventListener('pointerup', (e) => { if(e.pointerType === 'mouse') this.onPointerUp(e); });
            
            stage.addEventListener('wheel', (e) => {
                e.preventDefault();
                const delta = e.deltaY < 0 ? 1.18 : 0.85;
                this.setZoom(this.scale * delta, e.clientX, e.clientY);
            }, { passive: false });
        }

        // Bind clicks to province paths
        document.querySelectorAll('.province-path').forEach(el => {
            el.addEventListener('click', (e) => {
                if (this.dragDistance > 18) return;
                const plate = parseInt(el.dataset.plate);
                const cityIdx = CITIES.findIndex(c => c.plate === plate);
                if (cityIdx !== -1) MapEngine.selectTurkeyCity(cityIdx);
            });
        });
    },

    onTouchStart(e) {
        if (e.target.closest('#map-city-card') || e.target.closest('.map-controls-floating') || e.target.closest('.top-navbar')) return;
        if (!e.target.closest('.city-pin-node') && !e.target.closest('.province-path')) {
            this.closeCard();
        }
        
        if (e.touches.length === 2) {
            e.preventDefault();
            this.isPinching = true;
            this.isPanning = false;
            const dx = e.touches[0].clientX - e.touches[1].clientX;
            const dy = e.touches[0].clientY - e.touches[1].clientY;
            this.startPinchDist = Math.hypot(dx, dy);
            this.startPinchScale = this.scale;
        } else if (e.touches.length === 1) {
            this.isPanning = true;
            this.isPinching = false;
            this.startX = e.touches[0].clientX;
            this.startY = e.touches[0].clientY;
            this.startPanX = this.panX;
            this.startPanY = this.panY;
            this.dragDistance = 0;
        }
        const viewport = document.getElementById('map-viewport');
        if (viewport) viewport.style.transition = 'none';
    },

    onTouchMove(e) {
        if (this.isPinching && e.touches.length === 2) {
            e.preventDefault();
            const dx = e.touches[0].clientX - e.touches[1].clientX;
            const dy = e.touches[0].clientY - e.touches[1].clientY;
            const dist = Math.hypot(dx, dy);
            const centerX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
            const centerY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
            const newScale = this.startPinchScale * (dist / this.startPinchDist);
            this.setZoom(newScale, centerX, centerY, false);
            
        } else if (this.isPanning && e.touches.length === 1) {
            e.preventDefault();
            const dx = e.touches[0].clientX - this.startX;
            const dy = e.touches[0].clientY - this.startY;
            this.dragDistance = Math.hypot(dx, dy);
            this.panX = this.startPanX + dx;
            this.panY = this.startPanY + dy;
            this.applyTransform(false);
        }
    },

    onTouchEnd(e) {
        if (this.isPinching && e.touches.length < 2) {
            this.isPinching = false;
            if (e.touches.length === 1) {
                this.isPanning = true;
                this.startX = e.touches[0].clientX;
                this.startY = e.touches[0].clientY;
                this.startPanX = this.panX;
                this.startPanY = this.panY;
            }
        } else if (this.isPanning && e.touches.length === 0) {
            this.isPanning = false;
            this.applyTransform(true);
            // Reset dragDistance shortly after click events process
            setTimeout(() => { this.dragDistance = 0; }, 60);
        }
    },

    onPointerDown(e) {
        if (e.target.closest('#map-city-card') || e.target.closest('.map-controls-floating') || e.target.closest('.top-navbar')) return;
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
        setTimeout(() => { this.dragDistance = 0; }, 60);
    },

    zoomIn() {
        this.setZoom(Math.min(4.5, this.scale * 1.3));
    },

    zoomOut() {
        this.setZoom(Math.max(0.7, this.scale / 1.3));
    },

    resetCamera() {
        const curIdx = SaveManager.data.currentCityIdx || 0;
        this.focusOnTurkeyCity(curIdx, 1.6);
    },

    setZoom(newScale, focalX, focalY, smooth = true) {
        const container = document.getElementById('map-stage-wrapper') || document.body;
        const vpW = container.clientWidth || 360;
        const vpH = container.clientHeight || 500;
        
        const focusX = (focalX !== undefined) ? focalX : (vpW / 2);
        const focusY = (focalY !== undefined) ? focalY : (vpH / 2);

        const mapX = (focusX - this.panX) / this.scale;
        const mapY = (focusY - this.panY) / this.scale;

        this.scale = Math.max(0.7, Math.min(4.5, newScale));
        this.panX = focusX - (mapX * this.scale);
        this.panY = focusY - (mapY * this.scale);
        this.applyTransform(smooth);
        this.updateZoomClasses();
    },

    applyTransform(smooth = false) {
        const viewport = document.getElementById('map-viewport');
        if (!viewport) return;
        
        const container = document.getElementById('map-stage-wrapper') || document.body;
        const vpW = container.clientWidth;
        const vpH = container.clientHeight;
        const mapW = 1100 * this.scale;
        const mapH = 500 * this.scale;
        
        const minX = vpW - mapW - 120;
        const maxX = 120;
        const minY = vpH - mapH - 120;
        const maxY = 120;
        
        if (this.panX > maxX) this.panX = maxX;
        if (this.panX < minX) this.panX = minX;
        if (this.panY > maxY) this.panY = maxY;
        if (this.panY < minY) this.panY = minY;
        
        viewport.style.transition = smooth ? 'transform 0.45s cubic-bezier(0.2, 0.9, 0.3, 1)' : 'none';
        viewport.style.transform = `translate3d(${this.panX}px, ${this.panY}px, 0) scale(${this.scale})`;
    },

    updateZoomClasses() {
        const svg = document.getElementById('turkey-map-svg');
        if (!svg) return;
        if (this.scale <= 1.1) {
            svg.classList.add('zoomed-out');
        } else {
            svg.classList.remove('zoomed-out');
        }
    },

    panCameraTo(targetX, targetY, targetScale = 1.8, smooth = true) {
        const container = document.getElementById('map-stage-wrapper') || document.body;
        const vpW = container.clientWidth || 360;
        const vpH = container.clientHeight || 500;
        
        this.scale = Math.max(0.7, Math.min(4.5, targetScale));
        this.panX = (vpW / 2) - (targetX * this.scale);
        this.panY = (vpH / 2) - (targetY * this.scale);
        
        this.applyTransform(smooth);
        this.updateZoomClasses();
    },

    focusOnTurkeyCity(cityIdx, zoomScale = 2.2) {
        const city = CITIES[cityIdx];
        if (!city) return;
        
        const path = document.querySelector(`.province-path[data-plate="${city.plate}"]`);
        let centerX = city.cx;
        let centerY = city.cy;
        
        if (path && typeof path.getBBox === 'function') {
            try {
                const bbox = path.getBBox();
                if (bbox.width > 0 && bbox.height > 0) {
                    centerX = bbox.x + bbox.width / 2;
                    centerY = bbox.y + bbox.height / 2;
                }
            } catch(e) {}
        }
        
        this.panCameraTo(centerX, centerY, zoomScale, true);
    },

    // 1. SELECT TURKEY CITY (FULLY PLAYABLE)
    selectTurkeyCity(idx) {
        if (this.dragDistance > 18) return;
        this.isWorldCitySelected = false;
        this.selectedCityIdx = idx;
        const city = CITIES[idx];
        if (!city) return;

        this.focusOnTurkeyCity(idx, 2.2);

        // Highlight province
        const paths = document.querySelectorAll('.province-path');
        paths.forEach(p => { p.classList.remove('active-city', 'focused'); });
        const p = document.querySelector(`.province-path[data-plate="${city.plate}"]`);
        if (p) { p.classList.add('active-city', 'focused'); }

        const card = document.getElementById('map-city-card');
        const flagEl = document.getElementById('card-city-flag');
        const nameEl = document.getElementById('card-city-name');
        const plateEl = document.getElementById('card-city-plate');
        const countryEl = document.getElementById('card-city-country');
        const descEl = document.getElementById('card-city-desc');
        const landmarksGrid = document.getElementById('card-city-landmarks');
        const actionBtn = document.getElementById('card-action-btn');

        if (flagEl) flagEl.innerText = "🇹🇷";
        if (nameEl) nameEl.innerText = city.name;
        if (plateEl) {
            plateEl.style.display = 'inline-block';
            plateEl.innerText = city.plate < 10 ? '0' + city.plate : city.plate;
        }
        if (countryEl) countryEl.innerText = "Türkiye • 1. Sefer (Aktif)";

        // 5 Iconic Landmarks
        const rawLms = (city.levels || []).map(l => l.landmark).filter(Boolean);
        const uniqueLms = [...new Set(rawLms)].slice(0, 5);
        if (landmarksGrid) {
            landmarksGrid.innerHTML = uniqueLms.map(l => `<div class="landmark-badge">🏛️ ${l}</div>`).join('');
        }

        const isCurrent = idx === SaveManager.data.currentCityIdx;
        const isCompleted = SaveManager.data.completedProvinces.includes(city.plate);
        
        if (descEl) {
            if (isCompleted) {
                descEl.innerHTML = `🟢 <strong>Tamamlandı:</strong> ${city.name} ilinin tüm 5 mekanını fethettin ve altın mührü kazandın!`;
            } else if (isCurrent) {
                const sub = SaveManager.data.currentSubLevel;
                descEl.innerHTML = `🌟 <strong>Aktif Sefer:</strong> ${city.name} seferin devam ediyor! İlerlemen: Bulmaca ${sub + 1}/25.`;
            } else {
                descEl.innerHTML = `✨ <strong>Keşfe Hazır:</strong> 5 simgesel mekan ve 25 kelime bulmacasıyla bu şehri fethet.`;
            }
        }

        if (actionBtn) {
            actionBtn.style.background = "linear-gradient(180deg, #FAF0D7 0%, #D4AF37 60%, #9E7D1E 100%)";
            actionBtn.style.color = "#181512";
            if (!SaveManager.data.hasSelectedStartCity) {
                actionBtn.innerText = "YOLCULUĞA BURADAN BAŞLA ➔";
            } else if (isCurrent) {
                actionBtn.innerText = "YOLCULUĞA DEVAM ET ➔";
            } else if (isCompleted) {
                actionBtn.innerText = "TEKRAR OYNA ➔";
            } else {
                actionBtn.innerText = "BU İLE SEYAHAT ET ➔";
            }
        }

        if (card) card.classList.add('visible');
    },

    // 2. SELECT WORLD CITY (COMING SOON PREVIEW)
    selectWorldCity(countryIdx, cityIdx) {
        if (this.dragDistance > 18) return;
        this.isWorldCitySelected = true;
        const country = WORLD_CITIES[countryIdx];
        if (!country) return;
        const city = country.cities[cityIdx];
        if (!city) return;
        this.selectedWorldCity = { ...city, country: country.country, flag: country.flag };

        this.panCameraTo(city.cx, city.cy, 1.8, true);

        // Remove province focus
        document.querySelectorAll('.province-path').forEach(p => p.classList.remove('focused'));

        const card = document.getElementById('map-city-card');
        const flagEl = document.getElementById('card-city-flag');
        const nameEl = document.getElementById('card-city-name');
        const plateEl = document.getElementById('card-city-plate');
        const countryEl = document.getElementById('card-city-country');
        const descEl = document.getElementById('card-city-desc');
        const landmarksGrid = document.getElementById('card-city-landmarks');
        const actionBtn = document.getElementById('card-action-btn');

        if (flagEl) flagEl.innerText = country.flag;
        if (nameEl) nameEl.innerText = city.name;
        if (plateEl) plateEl.style.display = 'none';
        if (countryEl) countryEl.innerText = `${country.country} • Dünya Seferi`;

        // 5 Landmarks
        if (landmarksGrid) {
            landmarksGrid.innerHTML = (city.landmarks || []).map(l => `<div class="landmark-badge">🏛️ ${l}</div>`).join('');
        }

        if (descEl) {
            descEl.innerHTML = `🔒 <strong>Çok Yakında:</strong> ${city.name} şehrinin 5 simgesel mekanı keşif seferine hazırlanıyor. Türkiye Seferi'ni tamamlayarak vize kazan!`;
        }

        if (actionBtn) {
            actionBtn.innerText = "ÇOK YAKINDA (KEŞİF HAZIRLIĞI)";
            actionBtn.style.background = "linear-gradient(180deg, #334155 0%, #1e293b 100%)";
            actionBtn.style.color = "#a8a29e";
        }

        if (card) card.classList.add('visible');
    },

    closeCard() {
        const card = document.getElementById('map-city-card');
        if (card) card.classList.remove('visible');
        document.querySelectorAll('.province-path').forEach(p => p.classList.remove('focused'));
    },

    handleCityAction() {
        if (this.isWorldCitySelected) {
            const wc = this.selectedWorldCity;
            alert(`"${wc ? wc.name : 'Bu Şehir'}" çok yakında eklenecektir! Şu an aktif olan Türkiye Seferi'nin 81 ilini çözerek hazırlıklarını tamamla.`);
            return;
        }

        this.playSelectedTurkeyCity();
    },

    playSelectedTurkeyCity() {
        const city = CITIES[this.selectedCityIdx];
        if (!city) return;

        if (!SaveManager.data.hasSelectedStartCity) {
            SaveManager.data.hasSelectedStartCity = true;
            SaveManager.data.currentCityIdx = this.selectedCityIdx;
            SaveManager.data.currentSubLevel = 0;
            SaveManager.save();
            App.updateUI();
            this.closeCard();
            App.goToScreen('screen-game');
            return;
        }

        if (this.selectedCityIdx !== SaveManager.data.currentCityIdx) {
            this.animateTravelCarrier(SaveManager.data.currentCityIdx, this.selectedCityIdx, () => {
                SaveManager.data.currentCityIdx = this.selectedCityIdx;
                SaveManager.data.currentSubLevel = 0;
                SaveManager.save();
                App.updateUI();
                this.closeCard();
                App.goToScreen('screen-game');
            });
        } else {
            this.closeCard();
            App.goToScreen('screen-game');
        }
    },

    animateTravelCarrier(fromIdx, toIdx, onComplete) {
        const fromCity = CITIES[fromIdx];
        const toCity = CITIES[toIdx];
        if (!fromCity || !toCity) { if (onComplete) onComplete(); return; }

        const carrier = document.getElementById('travel-carrier');
        const route = document.getElementById('travel-route');
        if (!carrier || !route) { if (onComplete) onComplete(); return; }

        const midX = (fromCity.cx + toCity.cx) / 2;
        const midY = (fromCity.cy + toCity.cy) / 2 - 40;
        const pathData = `M ${fromCity.cx} ${fromCity.cy} Q ${midX} ${midY} ${toCity.cx} ${toCity.cy}`;
        route.setAttribute('d', pathData);
        route.style.display = 'block';

        carrier.style.display = 'block';
        carrier.setAttribute('transform', `translate(${fromCity.cx}, ${fromCity.cy})`);

        let progress = 0;
        const startTime = performance.now();
        const duration = 850;

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            progress = Math.min(elapsed / duration, 1);
            
            const t = progress;
            const curX = (1 - t) * (1 - t) * fromCity.cx + 2 * (1 - t) * t * midX + t * t * toCity.cx;
            const curY = (1 - t) * (1 - t) * fromCity.cy + 2 * (1 - t) * t * midY + t * t * toCity.cy;
            carrier.setAttribute('transform', `translate(${curX}, ${curY})`);

            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                carrier.style.display = 'none';
                route.style.display = 'none';
                if (onComplete) onComplete();
            }
        };

        requestAnimationFrame(animate);
    }
};

if (typeof window !== 'undefined') {
    window.MapEngine = MapEngine;
}

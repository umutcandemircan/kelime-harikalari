// TURKEY 81-PROVINCE CARTOGRAPHIC SVG MAP CONTROLLER (V2)
const CountryMap = {
    selectedCityIdx: 0,
    
    // Pan & Zoom State
    scale: 1.25,
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
        this.renderTurkeyPins();
        this.highlightProvinces();
        this.bindEvents();
        
        // Initial camera center
        const curIdx = SaveManager?.data?.currentCityIdx || 0;
        if (SaveManager?.data?.hasSelectedStartCity) {
            this.focusOnCity(curIdx, 1.8);
        } else {
            this.panCameraTo(550, 250, 1.15, true);
        }
    },

    renderTurkeyPins() {
        const pinsLayer = document.getElementById('city-pins-layer');
        if (!pinsLayer || typeof CITIES === 'undefined') return;
        
        let html = '';
        CITIES.forEach((c, idx) => {
            const isCurrent = idx === SaveManager.data.currentCityIdx;
            const isCompleted = SaveManager.data.completedProvinces.includes(c.plate);
            const fillClass = isCurrent ? 'current' : (isCompleted ? 'completed' : 'unlocked');
            
            html += `<g class="city-pin-node ${fillClass}" data-idx="${idx}" onclick="CountryMap.selectCity(${idx})" transform="translate(${c.cx}, ${c.cy})" role="button" aria-label="${c.name} İli">
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
            
            stage.addEventListener('pointerdown', (e) => { if (e.pointerType === 'mouse') this.onPointerDown(e); });
            window.addEventListener('pointermove', (e) => { if (e.pointerType === 'mouse') this.onPointerMove(e); });
            window.addEventListener('pointerup', (e) => { if (e.pointerType === 'mouse') this.onPointerUp(e); });
            
            stage.addEventListener('wheel', (e) => {
                e.preventDefault();
                const delta = e.deltaY < 0 ? 1.18 : 0.85;
                this.setZoom(this.scale * delta, e.clientX, e.clientY);
            }, { passive: false });
        }

        // SVG Path clicks
        document.querySelectorAll('.province-path').forEach(el => {
            el.addEventListener('click', () => {
                if (this.dragDistance > 18) return;
                const plate = parseInt(el.dataset.plate);
                const cityIdx = CITIES.findIndex(c => c.plate === plate);
                if (cityIdx !== -1) this.selectCity(cityIdx);
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
            this.setZoom(newScale, centerX, centerY);
        } else if (this.isPanning && e.touches.length === 1) {
            const dx = e.touches[0].clientX - this.startX;
            const dy = e.touches[0].clientY - this.startY;
            this.dragDistance = Math.hypot(dx, dy);
            this.panX = this.startPanX + dx;
            this.panY = this.startPanY + dy;
            this.clampPan();
            this.applyTransform();
        }
    },

    onTouchEnd(e) {
        this.isPinching = false;
        this.isPanning = false;
        setTimeout(() => { this.dragDistance = 0; }, 60);
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
        this.clampPan();
        this.applyTransform();
    },

    onPointerUp() {
        this.isPanning = false;
        setTimeout(() => { this.dragDistance = 0; }, 60);
    },

    setZoom(targetScale, clientX, clientY) {
        const minScale = 0.95;
        const maxScale = 4.2;
        const nextScale = Math.max(minScale, Math.min(maxScale, targetScale));
        
        const stage = document.getElementById('map-stage-wrapper');
        const rect = stage.getBoundingClientRect();
        const pivotX = (clientX !== undefined ? clientX : rect.left + rect.width / 2) - rect.left;
        const pivotY = (clientY !== undefined ? clientY : rect.top + rect.height / 2) - rect.top;
        
        const scaleRatio = nextScale / this.scale;
        this.panX = pivotX - (pivotX - this.panX) * scaleRatio;
        this.panY = pivotY - (pivotY - this.panY) * scaleRatio;
        this.scale = nextScale;
        
        this.clampPan();
        this.applyTransform();
    },

    clampPan() {
        const stage = document.getElementById('map-stage-wrapper');
        if (!stage) return;
        const w = stage.clientWidth;
        const h = stage.clientHeight;
        const mapW = 1050 * this.scale;
        const mapH = 500 * this.scale;
        
        const minX = Math.min(0, w - mapW - 100);
        const maxX = Math.max(0, 100);
        const minY = Math.min(0, h - mapH - 100);
        const maxY = Math.max(0, 100);
        
        this.panX = Math.max(minX, Math.min(maxX, this.panX));
        this.panY = Math.max(minY, Math.min(maxY, this.panY));
    },

    applyTransform(smooth = false) {
        const viewport = document.getElementById('map-viewport');
        if (!viewport) return;
        if (smooth) {
            viewport.style.transition = 'transform 0.45s cubic-bezier(0.16, 1, 0.3, 1)';
        } else {
            viewport.style.transition = 'none';
        }
        viewport.style.transform = `translate3d(${this.panX.toFixed(1)}px, ${this.panY.toFixed(1)}px, 0) scale(${this.scale.toFixed(3)})`;
    },

    panCameraTo(svgX, svgY, scale = 1.8, smooth = true) {
        const stage = document.getElementById('map-stage-wrapper');
        if (!stage) return;
        this.scale = Math.max(1.0, Math.min(4.0, scale));
        this.panX = (stage.clientWidth / 2) - (svgX * this.scale);
        this.panY = (stage.clientHeight / 2) - (svgY * this.scale);
        this.clampPan();
        this.applyTransform(smooth);
    },

    focusOnCity(cityIdx, zoomScale = 2.0) {
        const city = CITIES[cityIdx];
        if (!city) return;
        
        let focusX = city.cx;
        let focusY = city.cy;
        const pathEl = document.getElementById(`p${city.plate}`);
        if (pathEl && pathEl.getBBox) {
            try {
                const bbox = pathEl.getBBox();
                if (bbox.width > 0 && bbox.height > 0) {
                    focusX = bbox.x + bbox.width / 2;
                    focusY = bbox.y + bbox.height / 2;
                }
            } catch (_) {}
        }
        this.panCameraTo(focusX, focusY, zoomScale, true);
    },

    selectCity(cityIdx) {
        if (this.dragDistance > 18) return;
        const city = CITIES[cityIdx];
        if (!city) return;
        
        this.selectedCityIdx = cityIdx;
        AudioEngine.playPop(1);
        this.focusOnCity(cityIdx, 2.1);
        
        document.querySelectorAll('.province-path').forEach(p => p.classList.remove('focused'));
        const path = document.getElementById(`p${city.plate}`);
        if (path) path.classList.add('focused');
        
        this.showCard(city);
    },

    showCard(city) {
        const card = document.getElementById('map-city-card');
        if (!card) return;
        
        const isCurrent = this.selectedCityIdx === SaveManager.data.currentCityIdx;
        const isCompleted = SaveManager.data.completedProvinces.includes(city.plate);
        
        const title = document.getElementById('map-card-title');
        const plate = document.getElementById('map-card-plate');
        const badge = document.getElementById('map-card-badge');
        const desc = document.getElementById('map-card-desc');
        const landmarkThumb = document.getElementById('map-card-landmark-thumb');
        const landmarkName = document.getElementById('map-card-landmark-name');
        const btn = document.getElementById('map-card-action-btn');
        
        if (title) title.innerText = city.name;
        if (plate) plate.innerText = `${city.plate < 10 ? '0' + city.plate : city.plate} • Vilayet`;
        
        const firstLm = city.landmarks?.[0] || { name: 'Tarihi Merkez', bg: '' };
        if (landmarkName) landmarkName.innerText = `1. ${firstLm.name}`;
        if (landmarkThumb && firstLm.bg) landmarkThumb.style.backgroundImage = `url('${firstLm.bg}')`;
        
        if (desc) {
            desc.innerText = firstLm.desc || `${city.name} ilimizin tarihi ve doğal güzellikleri.`;
        }
        
        if (badge) {
            if (isCompleted) {
                badge.innerText = 'Tamamlandı ✓';
                badge.className = 'status-badge completed';
            } else if (isCurrent) {
                badge.innerText = 'Aktif Sefer';
                badge.className = 'status-badge active';
            } else {
                badge.innerText = 'Keşfedilmeyi Bekliyor';
                badge.className = 'status-badge unlocked';
            }
        }
        
        if (btn) {
            btn.innerText = 'Şehri Keşfet (5 Mekân)';
            btn.onclick = () => {
                this.closeCard();
                CityExploration.openCity(this.selectedCityIdx);
            };
        }
        
        card.classList.remove('hidden');
        card.classList.add('visible');
    },

    closeCard() {
        const card = document.getElementById('map-city-card');
        if (card) {
            card.classList.add('hidden');
            card.classList.remove('visible');
        }
    },

    zoomIn() { this.setZoom(this.scale * 1.35); },
    zoomOut() { this.setZoom(this.scale / 1.35); },
    resetView() {
        this.panCameraTo(550, 250, 1.25, true);
        this.closeCard();
    }
};

if (typeof window !== 'undefined') {
    window.CountryMap = CountryMap;
    // Alias for backward compatibility
    window.MapEngine = CountryMap;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CountryMap;
}

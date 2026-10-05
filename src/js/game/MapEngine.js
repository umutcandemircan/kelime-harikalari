// 3. INTERACTIVE 81-PROVINCE MAP ENGINE
const MapEngine = {
    selectedCityIdx: 0,
    
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
            const isUnlocked = idx <= SaveManager.data.unlockedCityIdx;
            const isCurrent = idx === SaveManager.data.currentCityIdx;
            const isCompleted = SaveManager.data.completedProvinces.includes(c.plate);
            
            const r = isCurrent ? 10 : (isCompleted ? 7 : (isUnlocked ? 6 : 4));
            const fillClass = isCurrent ? 'current' : (isCompleted ? 'completed' : (isUnlocked ? 'unlocked' : 'locked'));
            
            html += `<g class="city-pin-node ${fillClass}" data-idx="${idx}" onclick="MapEngine.selectCity(${idx})" transform="translate(${c.cx}, ${c.cy})">
                <circle class="city-pin-circle" r="${r}" />
                <text class="city-pin-text" y="0">${c.plate < 10 ? '0' + c.plate : c.plate}</text>
                ${isUnlocked ? `<text class="city-label-text" y="-12">${c.name}</text>` : ''}
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
            } else if (cityIdx > SaveManager.data.unlockedCityIdx) {
                el.classList.add('locked');
            }
        });
    },

    bindEvents() {
        document.querySelectorAll('.province-path').forEach(el => {
            el.addEventListener('click', () => {
                const plate = parseInt(el.dataset.plate);
                const cityIdx = CITIES.findIndex(c => c.plate === plate);
                if (cityIdx !== -1) MapEngine.selectCity(cityIdx);
            });
        });
    },

    selectCity(idx) {
        if (idx < 0 || idx >= CITIES.length) return;
        this.selectedCityIdx = idx;
        const city = CITIES[idx];
        const isUnlocked = idx <= SaveManager.data.unlockedCityIdx;
        const isCompleted = SaveManager.data.completedProvinces.includes(city.plate);
        
        // Populate card
        document.getElementById('card-city-plate').innerText = city.plate < 10 ? '0' + city.plate : city.plate;
        document.getElementById('card-city-name').innerText = city.name;
        
        const totalLevels = city.levels ? city.levels.length : 1;
        const starInfo = SaveManager.getCityStars(idx, totalLevels);
        
        const descEl = document.getElementById('card-city-desc');
        if (isCompleted) {
            descEl.innerHTML = `<span style="color:#10b981; font-weight:bold;">✓ Tamamlandı</span> • ⭐ ${starInfo.earned}/${starInfo.max} Yıldız<br>${city.name} ilimizin tüm tarihi mekanlarını keşfettin.`;
        } else if (isUnlocked) {
            descEl.innerHTML = `⭐ ${starInfo.earned}/${starInfo.max} Yıldız • ${totalLevels} Bölüm<br>${city.name} ilinde keşfedilecek simgesel mekanlar seni bekliyor.`;
        } else {
            descEl.innerHTML = `<span style="color:#ef4444; font-weight:bold;">🔒 Kilitli</span><br>Bu ili açmak için önceki şehirleri tamamlamalısın.`;
        }

        // Action button state
        const actionBtn = document.querySelector('#map-city-card button.btn-3d');
        if (actionBtn) {
            if (isUnlocked) {
                actionBtn.innerText = isCompleted ? "TEKRAR OYNA ➔" : "KEŞFE BAŞLA ➔";
                actionBtn.style.opacity = '1';
                actionBtn.style.pointerEvents = 'auto';
                actionBtn.onclick = () => MapEngine.playSelectedCity();
            } else {
                actionBtn.innerText = "KİLİTLİ 🔒";
                actionBtn.style.opacity = '0.5';
                actionBtn.style.pointerEvents = 'none';
            }
        }

        document.getElementById('map-city-card').classList.add('active');

        // Animate Route & Pan/Zoom Camera
        this.panCameraTo(city.cx, city.cy, 2.2);
    },

    panCameraTo(cx, cy, scale) {
        const viewport = document.getElementById('map-viewport');
        const stage = document.getElementById('map-stage-wrapper');
        if (!viewport || !stage) return;
        
        const vpW = stage.clientWidth || 360;
        const vpH = stage.clientHeight || 500;
        
        const tx = (vpW / 2) - (cx * scale);
        const ty = (vpH / 2) - (cy * scale);
        viewport.style.transform = `translate3d(${tx}px, ${ty}px, 0) scale(${scale})`;
    },

    closeCard() {
        const card = document.getElementById('map-city-card');
        if (card) card.classList.remove('active');
    },

    playSelectedCity() {
        // Strict Progression Guard
        if (this.selectedCityIdx > SaveManager.data.unlockedCityIdx) {
            console.warn(`[ProgressionGuard] City index ${this.selectedCityIdx} is locked!`);
            return;
        }
        SaveManager.data.currentCityIdx = this.selectedCityIdx;
        SaveManager.data.currentSubLevel = 0;
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

        // Quadratic bezier curved route
        const midX = (fromCity.cx + toCity.cx) / 2;
        const midY = Math.min(fromCity.cy, toCity.cy) - 30;
        const d = `M ${fromCity.cx} ${fromCity.cy} Q ${midX} ${midY} ${toCity.cx} ${toCity.cy}`;
        route.setAttribute('d', d);
        route.style.opacity = '1';
        carrier.style.opacity = '1';

        const totalLen = route.getTotalLength();
        let start = null;
        const duration = 1200;

        function step(ts) {
            if (!start) start = ts;
            const elapsed = ts - start;
            const progress = Math.min(elapsed / duration, 1);
            const ease = progress < 0.5 ? 2 * progress * progress : -1 + (4 - 2 * progress) * progress;
            const pt = route.getPointAtLength(ease * totalLen);
            carrier.setAttribute('transform', `translate(${pt.x}, ${pt.y})`);

            if (progress < 1) {
                requestAnimationFrame(step);
            } else {
                setTimeout(() => {
                    route.style.opacity = '0';
                    carrier.style.opacity = '0';
                    if (callback) callback();
                }, 200);
            }
        }
        requestAnimationFrame(step);
    }
};
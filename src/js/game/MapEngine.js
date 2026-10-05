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
                let html = '';
                CITIES.forEach((c, idx) => {
                    const isUnlocked = idx <= SaveManager.data.unlockedCityIdx;
                    const isCurrent = idx === SaveManager.data.currentCityIdx;
                    const r = isCurrent ? 10 : (isUnlocked ? 7 : 4);
                    
                    html += `<g class="city-pin-node ${isCurrent ? 'current' : ''}" data-idx="${idx}" onclick="MapEngine.selectCity(${idx})" transform="translate(${c.cx}, ${c.cy})">
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
                    el.classList.remove('active-city', 'completed');
                    if (cityIdx === SaveManager.data.currentCityIdx) {
                        el.classList.add('active-city');
                    } else if (cityIdx < SaveManager.data.unlockedCityIdx) {
                        el.classList.add('completed');
                    }
                });
            },
            bindEvents() {
                document.querySelectorAll('.province-path').forEach(el => {
                    el.addEventListener('click', (e) => {
                        const plate = parseInt(el.dataset.plate);
                        const cityIdx = CITIES.findIndex(c => c.plate === plate);
                        if (cityIdx !== -1) MapEngine.selectCity(cityIdx);
                    });
                });
            },
            selectCity(idx) {
                this.selectedCityIdx = idx;
                const city = CITIES[idx];
                
                // Show sliding card
                document.getElementById('card-city-plate').innerText = city.plate < 10 ? '0' + city.plate : city.plate;
                document.getElementById('card-city-name').innerText = city.name;
                const landmarkCount = city.landmarks ? city.landmarks.length : 1;
                document.getElementById('card-city-desc').innerText = `${city.name} ilinde keşfedilecek ${landmarkCount} simgesel mekan bulunuyor.`;
                document.getElementById('map-city-card').classList.add('active');

                // Animate Route & Pan/Zoom Camera
                this.panCameraTo(city.cx, city.cy, 2.2);
            },
            panCameraTo(cx, cy, scale) {
                const viewport = document.getElementById('map-viewport');
                const stage = document.getElementById('map-stage-wrapper');
                const vpW = stage.clientWidth;
                const vpH = stage.clientHeight;
                
                const tx = (vpW / 2) - (cx * scale);
                const ty = (vpH / 2) - (cy * scale);
                viewport.style.transform = `translate3d(${tx}px, ${ty}px, 0) scale(${scale})`;
            },
            closeCard() {
                document.getElementById('map-city-card').classList.remove('active');
            },
            playSelectedCity() {
                if (this.selectedCityIdx > SaveManager.data.unlockedCityIdx) {
                    App.showModal('modal-insufficient-gold'); // Can repurpose as locked modal
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

                // Draw quadratic bezier curved route
                const midX = (fromCity.cx + toCity.cx) / 2;
                const midY = Math.min(fromCity.cy, toCity.cy) - 30;
                const d = `M ${fromCity.cx} ${fromCity.cy} Q ${midX} ${midY} ${toCity.cx} ${toCity.cy}`;
                route.setAttribute('d', d);
                route.style.opacity = '1';
                carrier.style.opacity = '1';

                // Glide carrier along route over 1.2s
                const totalLen = route.getTotalLength();
                let start = null;
                const duration = 1200;

                function step(ts) {
                    if (!start) start = ts;
                    const elapsed = ts - start;
                    const progress = Math.min(elapsed / duration, 1);
                    // EaseInOut
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

        
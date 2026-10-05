// 6. MAIN APPLICATION STATE MACHINE
        const App = {
            init() {
                SaveManager.load();
                if ('serviceWorker' in navigator) {
                    window.addEventListener('load', () => {
                        navigator.serviceWorker.register('./sw.js').then(reg => {
                            console.log('SW registered:', reg.scope);
                        }).catch(err => console.log('SW registration failed:', err));
                    });
                }

                this.updateUI();
                MapEngine.init();

                // Pointer Events for gameplay wheel
                const wheel = document.getElementById('wheel-assembly');
                wheel.addEventListener('pointerdown', (e) => GameEngine.handleDown(e));
                window.addEventListener('pointermove', (e) => GameEngine.handleMove(e));
                window.addEventListener('pointerup', (e) => GameEngine.handleUp(e));

                this.goToScreen('screen-hub');
            },

            updateUI() {
                const coins = SaveManager.data.coins;
                ['hub-coins', 'map-coins', 'game-coins', 'idiom-coins'].forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.innerText = coins;
                });
                const curCity = CITIES[SaveManager.data.unlockedCityIdx];
                if (curCity) {
                    document.getElementById('hub-progress-badge').innerText = `İl ${curCity.plate < 10 ? '0' + curCity.plate : curCity.plate}/81`;
                }
            },

            goToScreen(screenId) {
                document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
                const target = document.getElementById(screenId);
                if (target) target.classList.add('active');

                if (screenId === 'screen-map') {
                    const curIdx = SaveManager.data.currentCityIdx;
                    const c = CITIES[curIdx];
                    setTimeout(() => MapEngine.panCameraTo(c.cx, c.cy, 2.2), 100);
                    MapEngine.highlightProvinces();
                } else if (screenId === 'screen-game') {
                    GameEngine.loadLevel();
                } else if (screenId === 'screen-idiom') {
                    IdiomEngine.init();
                }
            },

            showModal(id) {
                const m = document.getElementById(id);
                if (m) m.classList.add('active');
            },

            hideModal(id) {
                const m = document.getElementById(id);
                if (m) m.classList.remove('active');
            },

            showSettings() {
                this.showModal('modal-settings');
            },

            showDailyModal() {
                document.getElementById('daily-date-str').innerText = new Date().toISOString().split('T')[0];
                this.showModal('modal-daily');
            },

            startDailyChallenge() {
                this.hideModal('modal-daily');
                this.goToScreen('screen-game');
            },

            claim2xReward() {
                this.showRewardedAd('2x');
                this.hideModal('modal-postcard');
                this.advanceLevel();
            },

            continueAfterWin() {
                this.hideModal('modal-postcard');
                this.advanceLevel();
            },

            advanceLevel() {
                const curCityIdx = SaveManager.data.currentCityIdx;
                const city = CITIES[curCityIdx];
                SaveManager.data.currentSubLevel++;

                if (SaveManager.data.currentSubLevel >= (city.levels ? city.levels.length : 1)) {
                    // City completed! Advance to next province
                    SaveManager.data.currentSubLevel = 0;
                    const nextCityIdx = (curCityIdx + 1) % CITIES.length;
                    
                    if (curCityIdx === SaveManager.data.unlockedCityIdx) {
                        SaveManager.data.unlockedCityIdx = nextCityIdx;
                    }
                    
                    this.goToScreen('screen-map');
                    setTimeout(() => {
                        MapEngine.animateTravel(curCityIdx, nextCityIdx, () => {
                            SaveManager.data.currentCityIdx = nextCityIdx;
                            SaveManager.save();
                            MapEngine.renderPins();
                            MapEngine.highlightProvinces();
                            MapEngine.selectCity(nextCityIdx);
                        });
                    }, 400);

                    // Show interstitial ad every 3 cities
                    if (nextCityIdx % 3 === 0) this.showInterstitialAd();
                } else {
                    // Next landmark in same city
                    SaveManager.save();
                    GameEngine.loadLevel();
                }
            },

            // MONETIZATION HOOKS (PLAY STORE / CAPACITOR)
            showRewardedAd(type) {
                console.log('AD HOOK: showRewardedAd', type);
                if (window.Capacitor && window.AdMob) {
                    // Native rewarded ad call
                }
                if (type === '2x') {
                    SaveManager.addCoins(40);
                } else if (type === 'hint') {
                    SaveManager.addCoins(100);
                    this.hideModal('modal-insufficient-gold');
                }
            },

            watchAdForGold() {
                this.showRewardedAd('hint');
            },

            showInterstitialAd() {
                console.log('AD HOOK: showInterstitialAd');
                if (window.Capacitor && window.AdMob) {
                    // Native interstitial call
                }
            }
        };

        window.onload = () => App.init();
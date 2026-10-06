// 6. MAIN APPLICATION STATE MACHINE & SCREEN CONTROLLER
const App = {
    // Bank of deterministic daily challenge crosswords (strictly validated)
    DAILY_POOL: [
        {
            words: [
                { word: "BAHAR", row: 1, col: 1, dir: "H" },
                { word: "HARA", row: 0, col: 2, dir: "V" },
                { word: "BAR", row: 0, col: 4, dir: "V" },
                { word: "ARA", row: 3, col: 0, dir: "H" }
            ],
            letters: ["A", "B", "H", "R"],
            wheel: ["A", "B", "H", "R"]
        },
        {
            words: [
                { word: "DENİZ", row: 2, col: 0, dir: "H" },
                { word: "DİZ", row: 2, col: 0, dir: "V" },
                { word: "DİN", row: 0, col: 2, dir: "V" }
            ],
            letters: ["D", "E", "İ", "N", "Z"],
            wheel: ["D", "E", "İ", "N", "Z"]
        },
        {
            words: [
                { word: "KİTAP", row: 2, col: 0, dir: "H" },
                { word: "TAKİP", row: 0, col: 0, dir: "V" },
                { word: "PAK", row: 1, col: 3, dir: "V" }
            ],
            letters: ["A", "İ", "K", "P", "T"],
            wheel: ["A", "İ", "K", "P", "T"]
        },
        {
            words: [
                { word: "ROMA", row: 2, col: 0, dir: "H" },
                { word: "ORAN", row: 1, col: 0, dir: "V" },
                { word: "ROMAN", row: 0, col: 2, dir: "V" }
            ],
            letters: ["A", "M", "N", "O", "R"],
            wheel: ["A", "M", "N", "O", "R"]
        }
    ],

    init() {
        SaveManager.load();
        this.updateUI();
        MapEngine.init();

        // Register Service Worker for offline PWA
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('./sw.js').then(reg => {
                    console.log('[PWA] Service Worker registered:', reg.scope);
                }).catch(err => {
                    console.warn('[PWA] Service Worker registration failed:', err);
                });
            });
        }

        // Global wheel pointer events
        const asm = document.getElementById('wheel-assembly');
        if (asm) {
            asm.addEventListener('pointerdown', (e) => GameEngine.handleDown(e));
            window.addEventListener('pointermove', (e) => GameEngine.handleMove(e));
            window.addEventListener('pointerup', (e) => GameEngine.handleUp(e));
        }

        this.goToScreen('screen-hub');
    },

    startJourney() {
        if (!SaveManager.data.hasSelectedStartCity) {
            this.goToScreen('screen-map');
            this.showModal('modal-start-city');
            const banner = document.getElementById('map-guidance-banner');
            if (banner) banner.innerText = "🗺️ Başlamak istediğin ili haritadan seç!";
        } else {
            this.goToScreen('screen-game');
        }
    },

    onCityCompletedTravel() {
        this.hideModal('modal-city-completed');
        MapEngine.isSelectingNextRoute = true;
        this.goToScreen('screen-map');
        const banner = document.getElementById('map-guidance-banner');
        if (banner) banner.innerText = "✨ Sıradaki Hedefini Seç: Haritadan yeni bir il seç!";
    },

    updateUI() {
        const coins = SaveManager.data.coins;
        ['hub-coins', 'map-coins', 'game-coins', 'idiom-coins'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.innerText = coins;
        });

        // Update total stars indicator in Hub
        const totalStars = SaveManager.getTotalStars();
        const hubStarsSummary = document.getElementById('hub-stars-summary');
        if (hubStarsSummary) {
            hubStarsSummary.innerText = `⭐ ${totalStars} Yıldız Toplandı`;
        }

        const completedCount = SaveManager.data.completedProvinces ? SaveManager.data.completedProvinces.length : 0;
        const footerProgress = document.getElementById('hub-footer-progress');
        if (footerProgress) {
            footerProgress.innerText = `Keşfedilen: ${completedCount}/81 İl | Toplam Yıldız: ⭐ ${totalStars}`;
        }

        // Update Hub "Yolculuğa Başla" card status
        const progressBadge = document.getElementById('hub-progress-badge');
        const journeySub = document.getElementById('hub-journey-subtitle');
        if (!SaveManager.data.hasSelectedStartCity) {
            if (progressBadge) progressBadge.innerText = "Başlangıç";
            if (journeySub) journeySub.innerText = "Yolculuğa başlamak için bir il seç";
        } else {
            const curCity = CITIES[SaveManager.data.currentCityIdx] || CITIES[0];
            const sub = SaveManager.data.currentSubLevel;
            const m = Math.floor(sub / 5) + 1;
            const b = (sub % 5) + 1;
            if (progressBadge) progressBadge.innerText = `${curCity.name} (${sub + 1}/25)`;
            if (journeySub) journeySub.innerText = `Mekan ${m}/5 • Bulmaca ${b}/5 — Devam Et`;
        }

        // Update province map pins
        if (window.MapEngine && typeof MapEngine.highlightProvinces === 'function') {
            MapEngine.highlightProvinces();
        }
    },

    goToScreen(screenId) {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        const target = document.getElementById(screenId);
        if (target) {
            target.classList.add('active');
            window.scrollTo(0, 0);

            if (screenId === 'screen-map') {
                MapEngine.renderPins();
                MapEngine.highlightProvinces();
                const cur = CITIES[SaveManager.data.currentCityIdx] || CITIES[0];
                if (cur) MapEngine.panCameraTo(cur.cx, cur.cy, 1.8);
                
                const banner = document.getElementById('map-guidance-banner');
                if (banner && !MapEngine.isSelectingNextRoute) {
                    if (!SaveManager.data.hasSelectedStartCity) {
                        banner.innerText = "🗺️ Başlamak istediğin ili haritadan seç!";
                    } else {
                        banner.innerText = "🗺️ Türkiye Turu • Keşfetmek istediğin ile dokun";
                    }
                }
            } else if (screenId === 'screen-game') {
                if (!GameEngine.isDailyMode) {
                    GameEngine.loadLevel();
                }
            } else if (screenId === 'screen-idiom') {
                IdiomEngine.init();
            }
        }
        this.updateUI();
    },

    showModal(modalId) {
        const m = document.getElementById(modalId);
        if (m) m.classList.add('active');
    },

    hideModal(modalId) {
        const m = document.getElementById(modalId);
        if (m) m.classList.remove('active');
    },

    showSettings() {
        document.getElementById('setting-sound').checked = SaveManager.data.soundEnabled;
        document.getElementById('setting-vibrate').checked = SaveManager.data.hapticEnabled;
        this.showModal('modal-settings');
    },

    resetProgress() {
        if (confirm("Tüm oyun ilerlemen sıfırlanacak ve haritadan başlangıç ili seçimine dönülecektir. Onaylıyor musun?")) {
            localStorage.clear();
            SaveManager.init();
            this.hideModal('modal-settings');
            this.goToScreen('screen-hub');
            this.updateUI();
        }
    },

    showDailyModal() {
        const todayStr = new Date().toISOString().split('T')[0];
        const state = SaveManager.getDailyState(todayStr);

        document.getElementById('daily-date-str').innerText = todayStr;
        
        const actionBtn = document.querySelector('#modal-daily button.btn-3d-turquoise');
        const descP = document.querySelector('#modal-daily p');

        if (state.completedToday) {
            actionBtn.innerText = "BUGÜN TAMAMLANDI ✓";
            actionBtn.style.opacity = '0.6';
            actionBtn.style.pointerEvents = 'none';
            if (descP) descP.innerHTML = `<span style="color:#10b981; font-weight:bold;">Tebrikler!</span> Bugünün bulmacasını çözdün.<br>Mevcut Seri: <strong style="color:#f59e0b;">${state.streak} Gün</strong>. Yarın yeni bulmaca için bekleriz!`;
        } else {
            actionBtn.innerText = "GÜNÜN BULMACASINI OYNA ➔";
            actionBtn.style.opacity = '1';
            actionBtn.style.pointerEvents = 'auto';
            if (descP) descP.innerHTML = `Özel yıldızlı kelimeleri çözerek takvim serini artır ve ekstra <strong>50 Altın</strong> kazan!<br>Mevcut Seri: <strong style="color:#f59e0b;">${state.streak} Gün</strong>`;
        }

        this.showModal('modal-daily');
    },

    startDailyChallenge() {
        const todayStr = new Date().toISOString().split('T')[0];
        const state = SaveManager.getDailyState(todayStr);
        if (!state.canPlay) return;

        this.hideModal('modal-daily');
        
        // Deterministic level selection based on date string
        let seed = 0;
        for (let i = 0; i < todayStr.length; i++) {
            seed = (seed * 31 + todayStr.charCodeAt(i)) & 0xFFFFFFFF;
        }
        const dailyIndex = Math.abs(seed) % this.DAILY_POOL.length;
        const dailyLvl = this.DAILY_POOL[dailyIndex];

        GameEngine.loadDailyLevel(dailyLvl);
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
        if (GameEngine.isDailyMode) {
            GameEngine.isDailyMode = false;
            this.goToScreen('screen-hub');
            return;
        }

        const curCityIdx = SaveManager.data.currentCityIdx;
        const city = CITIES[curCityIdx];
        const levels = city.levels || [];
        SaveManager.data.currentSubLevel++;

        if (SaveManager.data.currentSubLevel >= levels.length) {
            SaveManager.data.currentSubLevel = levels.length - 1;
            SaveManager.save();
            this.onCityCompletedTravel();
        } else {
            SaveManager.save();
            GameEngine.loadLevel();
        }
    },

    // REWARDED ADS & MONETIZATION
    showRewardedAd(type) {
        console.info(`[AdSense/Monetization] Playing rewarded ad for: ${type}`);
        // Procedural ad simulation (instant reward)
        if (type === '2x') {
            SaveManager.addCoins(25);
        } else if (type === 'coins') {
            SaveManager.addCoins(100);
        }
        AudioEngine.playVictory();
    },

    watchAdForGold() {
        this.hideModal('modal-insufficient-gold');
        this.showRewardedAd('coins');
    }
};

window.onload = () => App.init();
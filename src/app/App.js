// MAIN APPLICATION CONTROLLER & LIFECYCLE COORDINATOR (V2)
const App = {
    APP_VERSION: '2.0.0',

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
        // Check GitHub Pages maintenance / Alpha preparation overlay
        try {
            const isGitHub = typeof window !== 'undefined' && window.location.hostname.indexOf('github.io') !== -1;
            const isBypass = typeof window !== 'undefined' && window.location.search.indexOf('preview=1') !== -1;
            const maintenanceEl = document.getElementById('maintenance-overlay');
            if (maintenanceEl) {
                if (isGitHub && !isBypass) {
                    maintenanceEl.classList.remove('hidden');
                } else {
                    maintenanceEl.classList.add('hidden');
                }
            }
        } catch(e) {}

        SaveManager.init();
        InputManager.init();
        WordValidator.init();
        AudioEngine.init();

        this.updateUI();

        // Register Service Worker for offline PWA
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('./sw.js').then(reg => {
                    console.log('[PWA] Service Worker registered for scope:', reg.scope);
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

        // Initialize 3D Globe
        if (window.Globe3D) {
            Globe3D.init();
        }

        // Initialize 81-city CountryMap
        if (window.CountryMap) {
            CountryMap.init();
        }

        // Initialize Onboarding
        if (window.OnboardingModal && typeof OnboardingModal.init === 'function') {
            OnboardingModal.init();
        }

        // Check Onboarding
        if (!SaveManager.data.onboardingCompleted) {
            OnboardingModal.open();
        } else {
            // Check Release Notes ("Neler Yeni?")
            ReleaseNotesModal.checkAndShow();
        }

        ScreenRouter.goTo('screen-hub');
    },

    updateUI() {
        const coins = SaveManager.data.coins;
        document.querySelectorAll('.currency-val').forEach(el => {
            el.innerText = coins;
        });

        const completedCount = SaveManager.data.completedProvinces ? SaveManager.data.completedProvinces.length : 0;
        
        const hubStarsSummary = document.getElementById('hub-stars-summary');
        if (hubStarsSummary) {
            hubStarsSummary.innerText = `📜 ${completedCount}/81 Vilayet Mührü`;
        }

        const footerProgress = document.getElementById('hub-footer-progress');
        if (footerProgress) {
            footerProgress.innerText = `Keşfedilen: ${completedCount}/81 İl | Kazanılan Mühür: ${completedCount}`;
        }

        // Update Hub "Yolculuğa Başla" status
        const progressBadge = document.getElementById('hub-progress-badge');
        const journeySub = document.getElementById('hub-journey-subtitle');
        if (!SaveManager.data.hasSelectedStartCity) {
            if (progressBadge) progressBadge.innerText = "Başlangıç";
            if (journeySub) journeySub.innerText = "Yolculuğa başlamak için bir il seç";
        } else {
            const curCity = (typeof CITIES !== 'undefined' ? CITIES[SaveManager.data.currentCityIdx] : null) || (window.CITIES ? window.CITIES[0] : null);
            if (curCity) {
                const sub = SaveManager.data.currentSubLevel || 0;
                const m = Math.floor(sub / 5) + 1;
                const b = (sub % 5) + 1;
                if (progressBadge) progressBadge.innerText = `${curCity.name} (${sub + 1}/25)`;
                if (journeySub) journeySub.innerText = `Mekân ${m}/5 • Bölüm ${b}/5 — Devam Et`;
            }
        }
    },

    startJourney() {
        if (!SaveManager.data.hasSelectedStartCity) {
            ScreenRouter.goTo('screen-country');
        } else {
            ScreenRouter.goTo('screen-city', { cityIdx: SaveManager.data.currentCityIdx });
        }
    },

    openGlobe() {
        ScreenRouter.goTo('screen-globe');
    },

    openCountryMap() {
        ScreenRouter.goTo('screen-country');
    },

    openDailyChallenge() {
        const todayIdx = Math.floor(Date.now() / (1000 * 60 * 60 * 24)) % this.DAILY_POOL.length;
        const dailyLvl = this.DAILY_POOL[todayIdx];
        ScreenRouter.goTo('screen-game', { daily: dailyLvl });
    },

    openIdiomMode() {
        ScreenRouter.goTo('screen-idiom');
        if (window.IdiomEngine) {
            IdiomEngine.loadQuestion();
        }
    },

    showModal(modalId) {
        const m = document.getElementById(modalId);
        if (m) m.classList.remove('hidden');
    },

    hideModal(modalId) {
        const m = document.getElementById(modalId);
        if (m) m.classList.add('hidden');
    }
};

if (typeof window !== 'undefined') {
    window.App = App;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = App;
}

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

    // Adres taşıma ayarları
    OLD_HOST: 'umutcandemircan.github.io',
    NEW_URL: 'https://www.harfiye.com/',
    TRANSFER_PARAM: 'aktar',

    init() {
        // Yeni adreste: eski adresten gelen ilerlemeyi içe aktar (SaveManager yüklenmeden önce)
        this.importTransferredSave();

        SaveManager.init();

        // Eski adreste: yalnızca taşınma bildirimini göster, oyunu başlatma
        if (this.showMovedNotice()) return;

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

    // ---------- ADRES TAŞIMA ----------

    _progressScore(save) {
        if (!save || typeof save !== 'object') return -1;
        const provinces = Array.isArray(save.completedProvinces) ? save.completedProvinces.length : 0;
        const landmarks = Array.isArray(save.completedLandmarks) ? save.completedLandmarks.length : 0;
        const sub = Number(save.currentSubLevel) || 0;
        return provinces * 10000 + landmarks * 100 + sub;
    },

    _encodeSave(obj) {
        const json = JSON.stringify(obj);
        const b64 = btoa(unescape(encodeURIComponent(json)));
        return b64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
    },

    _decodeSave(str) {
        let b64 = str.replace(/-/g, '+').replace(/_/g, '/');
        while (b64.length % 4) b64 += '=';
        return JSON.parse(decodeURIComponent(escape(atob(b64))));
    },

    importTransferredSave() {
        try {
            const hash = window.location.hash || '';
            const prefix = `#${this.TRANSFER_PARAM}=`;
            if (!hash.startsWith(prefix)) return;

            const incoming = this._decodeSave(hash.slice(prefix.length));
            // Adres çubuğundan veriyi hemen temizle
            history.replaceState(null, '', window.location.pathname + window.location.search);

            if (!incoming || typeof incoming !== 'object' || !Array.isArray(incoming.completedProvinces)) return;

            let existing = null;
            try { existing = JSON.parse(localStorage.getItem(SaveManager.KEY) || 'null'); } catch (e) {}

            // Yerelde daha ileri bir kayıt varsa üzerine yazma
            if (existing && this._progressScore(existing) >= this._progressScore(incoming)) return;

            localStorage.setItem(SaveManager.KEY, JSON.stringify(incoming));
            console.info('[Taşıma] Eski adresten gelen ilerleme içe aktarıldı.');
        } catch (e) {
            console.warn('[Taşıma] İlerleme içe aktarılamadı:', e);
        }
    },

    showMovedNotice() {
        if (typeof window === 'undefined' || window.location.hostname !== this.OLD_HOST) return false;

        const overlay = document.getElementById('moved-overlay');
        if (!overlay) return false;

        // Mevcut ilerlemeyi bağlantıya ekle
        let targetUrl = this.NEW_URL;
        const save = SaveManager.data;
        const score = this._progressScore(save);
        const hasProgress = score > 0 || (save && save.coins !== SaveManager.defaultData.coins);
        if (hasProgress) {
            try {
                targetUrl = `${this.NEW_URL}#${this.TRANSFER_PARAM}=${this._encodeSave(save)}`;
            } catch (e) {}
        }

        const goBtn = document.getElementById('moved-go-btn');
        if (goBtn) goBtn.href = targetUrl;

        const note = document.getElementById('moved-progress-note');
        if (note) {
            if (hasProgress) {
                const provinces = (save.completedProvinces || []).length;
                note.innerHTML = `İlerlemen (<strong>${provinces}/81 vilayet</strong>, <strong>${save.coins} altın</strong>) bu butonla Harfiye'ye otomatik taşınır. Yer imlerini de güncellemeyi unutma.`;
            } else {
                note.textContent = 'Yer imlerini yeni adresle güncellemeyi unutma.';
            }
        }

        const copyBtn = document.getElementById('moved-copy-btn');
        if (copyBtn) {
            copyBtn.addEventListener('click', () => {
                const done = () => {
                    copyBtn.textContent = 'Bağlantı Kopyalandı';
                    setTimeout(() => { copyBtn.textContent = 'Bağlantıyı Kopyala'; }, 2200);
                };
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(this.NEW_URL).then(done).catch(() => window.prompt('Yeni adres:', this.NEW_URL));
                } else {
                    window.prompt('Yeni adres:', this.NEW_URL);
                }
            });
        }

        // Arka plandaki oyun ekranlarını erişilebilirlik ağacından ve etkileşimden çıkar
        document.querySelectorAll('body > *:not(#moved-overlay):not(script)').forEach(el => {
            el.setAttribute('aria-hidden', 'true');
            el.setAttribute('inert', '');
        });

        document.title = 'Harfiye — Yeni Adresimiz';

        // Hareket azaltma tercihinde SVG (SMIL) yelkenli animasyonunu durdur
        if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            overlay.querySelectorAll('svg').forEach(svg => {
                if (typeof svg.pauseAnimations === 'function') svg.pauseAnimations();
            });
        }

        overlay.classList.remove('hidden');
        return true;
    },

    updateUI() {
        const coins = SaveManager.data.coins;
        document.querySelectorAll('.currency-val').forEach(el => {
            el.innerText = coins;
        });

        const completedCount = SaveManager.data.completedProvinces ? SaveManager.data.completedProvinces.length : 0;
        
        const hubStarsSummary = document.getElementById('hub-stars-summary');
        if (hubStarsSummary) {
            hubStarsSummary.innerText = `${completedCount}/81 Vilayet Mührü`;
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

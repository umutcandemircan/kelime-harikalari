// SAVE MANAGER WITH SCHEMA VERSIONING & MULTI-VERSION MIGRATION PIPELINE
const SaveManager = {
    KEY: 'sozcukSeferi_v2_save',
    LEGACY_KEYS: ['sozcukSeferi_v1_save', 'sozcukSeferi_save', 'kelimeHarikalari_save'],
    CURRENT_SCHEMA_VERSION: 4,
    CURRENT_APP_VERSION: '2.0.0',
    
    defaultData: {
        schemaVersion: 4,
        appVersion: '2.0.0',
        lastSeenVersion: '2.0.0',
        coins: 250,
        hasSelectedStartCity: false,
        onboardingCompleted: false,
        currentCountry: 'tr',
        currentCityIdx: 0,
        currentLandmarkIdx: 0,
        unlockedCityIdx: 80,
        currentSubLevel: 0,
        completedProvinces: [],
        completedLandmarks: [],
        stars: {}, // "cityIdx_subLevel": 1 | 2 | 3
        bonusChest: 0,
        settings: {
            soundEnabled: true,
            hapticEnabled: true,
            reducedMotion: false
        },
        daily: {
            lastDate: null,
            streak: 0,
            completedToday: false
        },
        feedbackHistory: []
    },
    
    data: null,
    
    init() {
        this.data = JSON.parse(JSON.stringify(this.defaultData));
        this.load();
    },

    load() {
        try {
            let raw = localStorage.getItem(this.KEY);
            
            // Check legacy keys
            if (!raw) {
                for (const oldKey of this.LEGACY_KEYS) {
                    const oldRaw = localStorage.getItem(oldKey);
                    if (oldRaw) {
                        console.info(`[SaveManager] Found legacy save in ${oldKey}, initiating migration...`);
                        raw = oldRaw;
                        break;
                    }
                }
            }
            
            if (!raw) {
                this.save();
                return;
            }
            
            const parsed = JSON.parse(raw);
            this.data = this.migrateAndNormalize(parsed);
            this.save();
        } catch (e) {
            console.error('[SaveManager] Save recovery triggered due to corruption:', e);
            this.data = JSON.parse(JSON.stringify(this.defaultData));
            this.save();
        }
    },

    migrateAndNormalize(input) {
        const out = JSON.parse(JSON.stringify(this.defaultData));
        if (typeof input !== 'object' || input === null) return out;

        // 1. Coins
        if (typeof input.coins === 'number' && !isNaN(input.coins)) {
            out.coins = Math.max(0, Math.min(999999, Math.floor(input.coins)));
        }

        // 2. Start city & onboarding
        out.hasSelectedStartCity = Boolean(input.hasSelectedStartCity);
        out.onboardingCompleted = Boolean(input.onboardingCompleted || input.hasSelectedStartCity);

        // 3. Country & City Indices
        if (typeof input.currentCountry === 'string') {
            out.currentCountry = input.currentCountry;
        }
        if (typeof input.currentCityIdx === 'number' && !isNaN(input.currentCityIdx)) {
            out.currentCityIdx = Math.max(0, Math.min(80, Math.floor(input.currentCityIdx)));
        }
        if (typeof input.currentLandmarkIdx === 'number' && !isNaN(input.currentLandmarkIdx)) {
            out.currentLandmarkIdx = Math.max(0, Math.min(4, Math.floor(input.currentLandmarkIdx)));
        }
        if (typeof input.unlockedCityIdx === 'number' && !isNaN(input.unlockedCityIdx)) {
            out.unlockedCityIdx = Math.max(0, Math.min(80, Math.floor(input.unlockedCityIdx)));
        }

        // 4. SubLevel (0 to 24)
        if (typeof input.currentSubLevel === 'number' && !isNaN(input.currentSubLevel)) {
            out.currentSubLevel = Math.max(0, Math.min(24, Math.floor(input.currentSubLevel)));
        }

        // 5. Completed Provinces (1 to 81)
        if (Array.isArray(input.completedProvinces)) {
            out.completedProvinces = [...new Set(
                input.completedProvinces
                    .filter(p => typeof p === 'number' && p >= 1 && p <= 81)
                    .map(p => Math.floor(p))
            )];
        }

        // 6. Completed Landmarks
        if (Array.isArray(input.completedLandmarks)) {
            out.completedLandmarks = [...new Set(input.completedLandmarks.filter(s => typeof s === 'string'))];
        }

        // 7. Stars
        if (typeof input.stars === 'object' && input.stars !== null) {
            out.stars = {};
            for (const [k, v] of Object.entries(input.stars)) {
                if (typeof v === 'number' && v >= 1 && v <= 3) {
                    out.stars[k] = Math.floor(v);
                }
            }
        }

        // 8. Settings
        if (typeof input.settings === 'object' && input.settings !== null) {
            out.settings.soundEnabled = input.settings.soundEnabled !== false;
            out.settings.hapticEnabled = input.settings.hapticEnabled !== false;
            out.settings.reducedMotion = Boolean(input.settings.reducedMotion);
        } else {
            // Check flat legacy flags
            if (typeof input.soundEnabled === 'boolean') out.settings.soundEnabled = input.soundEnabled;
            if (typeof input.hapticEnabled === 'boolean') out.settings.hapticEnabled = input.hapticEnabled;
        }

        // 9. Versioning
        out.lastSeenVersion = typeof input.lastSeenVersion === 'string' ? input.lastSeenVersion : (typeof input.version === 'string' ? input.version : '1.0.0');
        out.schemaVersion = this.CURRENT_SCHEMA_VERSION;
        out.appVersion = this.CURRENT_APP_VERSION;

        // 10. Daily challenge
        if (typeof input.daily === 'object' && input.daily !== null) {
            out.daily.lastDate = input.daily.lastDate || null;
            out.daily.streak = typeof input.daily.streak === 'number' ? Math.max(0, input.daily.streak) : 0;
            out.daily.completedToday = Boolean(input.daily.completedToday);
        }

        return out;
    },

    save() {
        try {
            if (!this.data) this.data = JSON.parse(JSON.stringify(this.defaultData));
            this.data.schemaVersion = this.CURRENT_SCHEMA_VERSION;
            this.data.appVersion = this.CURRENT_APP_VERSION;
            localStorage.setItem(this.KEY, JSON.stringify(this.data));
        } catch (e) {
            console.error('[SaveManager] Failed to write to localStorage:', e);
        }
    },

    addCoins(amount) {
        if (typeof amount !== 'number' || isNaN(amount) || amount <= 0) return;
        this.data.coins = Math.min(999999, this.data.coins + Math.floor(amount));
        this.save();
    },

    spendCoins(amount) {
        if (typeof amount !== 'number' || isNaN(amount) || amount <= 0) return false;
        const cost = Math.floor(amount);
        if (this.data.coins >= cost) {
            this.data.coins -= cost;
            this.save();
            return true;
        }
        return false;
    },

    completeProvince(plate) {
        if (typeof plate !== 'number') return;
        if (!this.data.completedProvinces.includes(plate)) {
            this.data.completedProvinces.push(plate);
            this.save();
        }
    },

    recordFeedback(report) {
        if (!Array.isArray(this.data.feedbackHistory)) {
            this.data.feedbackHistory = [];
        }
        this.data.feedbackHistory.push(report);
        if (this.data.feedbackHistory.length > 20) {
            this.data.feedbackHistory.shift();
        }
        this.save();
    }
};

if (typeof window !== 'undefined') {
    window.SaveManager = SaveManager;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SaveManager;
}

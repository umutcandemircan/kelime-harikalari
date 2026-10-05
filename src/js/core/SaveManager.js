// 1. SAVE MANAGER (LOCALSTORAGE) WITH VERSIONING AND CORRUPTION FALLBACK
const SaveManager = {
    KEY: 'sozcukSeferi_save',
    CURRENT_VERSION: 2,
    
    // The canonical schema for version 2
    defaultData: {
        version: 2,
        coins: 250,
        currentCityIdx: 0,
        unlockedCityIdx: 0,
        currentSubLevel: 0,
        completedProvinces: [],
        stars: {}, // Format: "cityIdx_subLevel": 1|2|3
        bonusChest: 0,
        soundEnabled: true,
        hapticEnabled: true,
        dailyStreak: 0,
        lastDailyTimestamp: null,
        totalPlayTime: 0
    },
    
    data: null,
    
    init() {
        this.data = JSON.parse(JSON.stringify(this.defaultData));
        this.load();
    },

    load() {
        try {
            const s = localStorage.getItem(this.KEY);
            if (!s) return;
            
            let parsed = JSON.parse(s);
            
            // Migration pipeline
            if (!parsed.version || parsed.version < this.CURRENT_VERSION) {
                console.warn(`[SaveManager] Migrating save file from version ${parsed.version || 1} to ${this.CURRENT_VERSION}`);
                parsed = this.migrate(parsed);
            }
            
            // Schema validation (corruption fallback)
            if (this.validateSchema(parsed)) {
                this.data = { ...this.defaultData, ...parsed };
            } else {
                throw new Error("Invalid save schema");
            }
        } catch (e) {
            console.error("[SaveManager] Save file corrupted or missing. Falling back to default data.", e);
            this.data = JSON.parse(JSON.stringify(this.defaultData));
            this.save();
        }
    },
    
    migrate(oldData) {
        let newData = { ...this.defaultData };
        // V1 to V2 mapping
        if (oldData.coins !== undefined) newData.coins = oldData.coins;
        if (oldData.currentCityIdx !== undefined) newData.currentCityIdx = oldData.currentCityIdx;
        if (oldData.unlockedCityIdx !== undefined) newData.unlockedCityIdx = oldData.unlockedCityIdx;
        if (oldData.currentSubLevel !== undefined) newData.currentSubLevel = oldData.currentSubLevel;
        if (oldData.completedProvinces !== undefined) newData.completedProvinces = oldData.completedProvinces;
        if (oldData.soundEnabled !== undefined) newData.soundEnabled = oldData.soundEnabled;
        if (oldData.hapticEnabled !== undefined) newData.hapticEnabled = oldData.hapticEnabled;
        if (oldData.dailyStreak !== undefined) newData.dailyStreak = oldData.dailyStreak;
        newData.version = this.CURRENT_VERSION;
        return newData;
    },
    
    validateSchema(data) {
        // Strict typing check
        if (typeof data !== 'object' || data === null) return false;
        if (typeof data.coins !== 'number' || data.coins < 0) return false;
        if (typeof data.currentCityIdx !== 'number') return false;
        if (!Array.isArray(data.completedProvinces)) return false;
        return true;
    },

    save() {
        try {
            this.data.version = this.CURRENT_VERSION;
            localStorage.setItem(this.KEY, JSON.stringify(this.data));
        } catch (e) {
            console.error("[SaveManager] Quota exceeded or permission denied", e);
        }
    },

    addCoins(amount) {
        if (amount <= 0) return;
        this.data.coins += amount;
        this.save();
        App.updateUI();
    },

    spendCoins(amount) {
        if (amount <= 0) return false;
        if (this.data.coins >= amount) {
            this.data.coins -= amount;
            this.save();
            App.updateUI();
            return true;
        }
        App.showModal('modal-insufficient-gold');
        return false;
    },
    
    saveStar(cityIdx, subLevel, stars) {
        const key = `${cityIdx}_${subLevel}`;
        const currentStars = this.data.stars[key] || 0;
        if (stars > currentStars) {
            this.data.stars[key] = stars;
            this.save();
        }
    },
    
    getStars(cityIdx, subLevel) {
        return this.data.stars[`${cityIdx}_${subLevel}`] || 0;
    },

    setHaptic(val) {
        this.data.hapticEnabled = !!val;
        this.save();
    },
    
    setSound(val) {
        this.data.soundEnabled = !!val;
        this.save();
    }
};

// Initialize early
SaveManager.init();
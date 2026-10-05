// 1. SAVE MANAGER (LOCALSTORAGE) WITH STRICT SCHEMA VALIDATION & CORRUPTION RECOVERY
const SaveManager = {
    KEY: 'sozcukSeferi_v2_save',
    LEGACY_KEYS: ['sozcukSeferi_v1_save', 'sozcukSeferi_save', 'kelimeHarikalari_save'],
    CURRENT_VERSION: 2,
    
    defaultData: {
        version: 2,
        coins: 250,
        currentCityIdx: 0,
        unlockedCityIdx: 0,
        currentSubLevel: 0,
        completedProvinces: [],
        stars: {}, // Format: "cityIdx_subLevel": 1 | 2 | 3
        bonusChest: 0,
        soundEnabled: true,
        hapticEnabled: true,
        daily: {
            lastDate: null,
            streak: 0,
            completedToday: false
        }
    },
    
    data: null,
    
    init() {
        this.data = JSON.parse(JSON.stringify(this.defaultData));
        this.load();
    },

    load() {
        try {
            let raw = localStorage.getItem(this.KEY);
            
            // Check legacy migration if current key is missing
            if (!raw) {
                for (const oldKey of this.LEGACY_KEYS) {
                    const oldRaw = localStorage.getItem(oldKey);
                    if (oldRaw) {
                        console.info(`[SaveManager] Found legacy save in ${oldKey}, migrating...`);
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
            this.data = this.normalizeAndValidate(parsed);
            this.save(); // Write back normalized data
        } catch (e) {
            console.error('[SaveManager] Save corruption detected. Restoring defaults.', e);
            this.data = JSON.parse(JSON.stringify(this.defaultData));
            this.save();
        }
    },
    
    normalizeAndValidate(input) {
        const out = JSON.parse(JSON.stringify(this.defaultData));
        if (typeof input !== 'object' || input === null) return out;
        
        // 1. Coins validation: integer between 0 and 99999
        if (typeof input.coins === 'number' && !isNaN(input.coins)) {
            out.coins = Math.max(0, Math.min(99999, Math.floor(input.coins)));
        }
        
        // 2. City index bounds: 0 to 80 (81 provinces)
        if (typeof input.currentCityIdx === 'number' && !isNaN(input.currentCityIdx)) {
            out.currentCityIdx = Math.max(0, Math.min(80, Math.floor(input.currentCityIdx)));
        }
        if (typeof input.unlockedCityIdx === 'number' && !isNaN(input.unlockedCityIdx)) {
            out.unlockedCityIdx = Math.max(0, Math.min(80, Math.floor(input.unlockedCityIdx)));
        }
        
        // Ensure currentCityIdx cannot exceed unlockedCityIdx
        if (out.currentCityIdx > out.unlockedCityIdx) {
            out.currentCityIdx = out.unlockedCityIdx;
        }
        
        // 3. SubLevel bounds: integer between 0 and 10
        if (typeof input.currentSubLevel === 'number' && !isNaN(input.currentSubLevel)) {
            out.currentSubLevel = Math.max(0, Math.min(10, Math.floor(input.currentSubLevel)));
        }
        
        // 4. Completed provinces: array of unique numbers between 1 and 81
        if (Array.isArray(input.completedProvinces)) {
            out.completedProvinces = [...new Set(
                input.completedProvinces
                    .filter(p => typeof p === 'number' && p >= 1 && p <= 81)
                    .map(p => Math.floor(p))
            )];
        }
        
        // 5. Stars validation: dictionary of "city_sub" -> 1..3
        if (typeof input.stars === 'object' && input.stars !== null) {
            out.stars = {};
            for (const [k, v] of Object.entries(input.stars)) {
                if (typeof v === 'number' && v >= 1 && v <= 3) {
                    out.stars[k] = Math.floor(v);
                }
            }
        }
        
        // 6. Bonus chest: 0 to 5
        if (typeof input.bonusChest === 'number' && !isNaN(input.bonusChest)) {
            out.bonusChest = Math.max(0, Math.min(5, Math.floor(input.bonusChest)));
        }
        
        // 7. Settings
        out.soundEnabled = typeof input.soundEnabled === 'boolean' ? input.soundEnabled : true;
        out.hapticEnabled = typeof input.hapticEnabled === 'boolean' ? input.hapticEnabled : true;
        
        // 8. Daily Challenge State
        if (typeof input.daily === 'object' && input.daily !== null) {
            out.daily.lastDate = typeof input.daily.lastDate === 'string' ? input.daily.lastDate : null;
            out.daily.streak = typeof input.daily.streak === 'number' ? Math.max(0, Math.floor(input.daily.streak)) : 0;
            out.daily.completedToday = typeof input.daily.completedToday === 'boolean' ? input.daily.completedToday : false;
        } else if (typeof input.lastDaily === 'string') {
            // Legacy daily field migration
            out.daily.lastDate = input.lastDaily;
            out.daily.streak = typeof input.dailyStreak === 'number' ? Math.max(0, Math.floor(input.dailyStreak)) : 0;
        }
        
        out.version = this.CURRENT_VERSION;
        return out;
    },

    save() {
        try {
            this.data.version = this.CURRENT_VERSION;
            localStorage.setItem(this.KEY, JSON.stringify(this.data));
        } catch (e) {
            console.error('[SaveManager] Save failed or quota exceeded', e);
        }
    },

    addCoins(amount) {
        if (typeof amount !== 'number' || isNaN(amount) || amount <= 0) return;
        this.data.coins = Math.min(99999, this.data.coins + Math.floor(amount));
        this.save();
        if (window.App && typeof App.updateUI === 'function') App.updateUI();
    },

    spendCoins(amount) {
        if (typeof amount !== 'number' || isNaN(amount) || amount <= 0) return false;
        const cost = Math.floor(amount);
        if (this.data.coins >= cost) {
            this.data.coins -= cost;
            this.save();
            if (window.App && typeof App.updateUI === 'function') App.updateUI();
            return true;
        }
        if (window.App && typeof App.showModal === 'function') App.showModal('modal-insufficient-gold');
        return false;
    },
    
    saveStar(cityIdx, subLevel, stars) {
        const key = `${cityIdx}_${subLevel}`;
        const currentStars = this.data.stars[key] || 0;
        if (stars > currentStars && stars <= 3) {
            this.data.stars[key] = stars;
            this.save();
        }
    },
    
    getStars(cityIdx, subLevel) {
        return this.data.stars[`${cityIdx}_${subLevel}`] || 0;
    },
    
    getCityStars(cityIdx, totalLevels) {
        let earned = 0;
        for (let i = 0; i < totalLevels; i++) {
            earned += this.getStars(cityIdx, i);
        }
        return { earned, max: totalLevels * 3 };
    },
    
    getTotalStars() {
        return Object.values(this.data.stars).reduce((sum, s) => sum + s, 0);
    },

    getDailyState(todayStr) {
        if (!this.data.daily.lastDate) {
            return { canPlay: true, streak: 0, completedToday: false };
        }
        
        if (this.data.daily.lastDate === todayStr) {
            return { canPlay: false, streak: this.data.daily.streak, completedToday: true };
        }
        
        // Calculate date difference for streak
        const last = new Date(this.data.daily.lastDate);
        const today = new Date(todayStr);
        const diffDays = Math.round((today - last) / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) {
            // Consecutive day
            return { canPlay: true, streak: this.data.daily.streak, completedToday: false };
        } else {
            // Missed one or more days -> streak resets
            return { canPlay: true, streak: 0, completedToday: false };
        }
    },
    
    recordDailyCompletion(todayStr, rewardCoins = 50) {
        const state = this.getDailyState(todayStr);
        const newStreak = state.streak + 1;
        this.data.daily.lastDate = todayStr;
        this.data.daily.streak = newStreak;
        this.data.daily.completedToday = true;
        this.addCoins(rewardCoins);
        this.save();
        return newStreak;
    },

    setHaptic(val) {
        this.data.hapticEnabled = Boolean(val);
        this.save();
    },
    
    setSound(val) {
        this.data.soundEnabled = Boolean(val);
        this.save();
    }
};

SaveManager.init();
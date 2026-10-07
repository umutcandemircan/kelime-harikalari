// SCREEN ROUTER & NAVIGATION CONTROLLER (V2)
const ScreenRouter = {
    currentScreen: 'screen-hub',
    screenHistory: [],

    goTo(screenId, params = {}) {
        const screens = document.querySelectorAll('.screen');
        screens.forEach(s => s.classList.remove('active'));

        const target = document.getElementById(screenId);
        if (target) {
            target.classList.add('active');
            if (this.currentScreen !== screenId) {
                this.screenHistory.push(this.currentScreen);
                this.currentScreen = screenId;
            }
        }

        // Screen specific hooks
        if (screenId === 'screen-globe') {
            if (window.Globe3D) {
                Globe3D.resume();
                Globe3D.resize();
            }
        } else {
            if (window.Globe3D) {
                Globe3D.pause();
            }
        }
        
        if (screenId === 'screen-country') {
            if (window.CountryMap) {
                CountryMap.init();
            }
        } else if (screenId === 'screen-city') {
            if (window.CityExploration && params.cityIdx !== undefined) {
                CityExploration.openCity(params.cityIdx);
            } else if (window.CityExploration) {
                CityExploration.renderCityView();
            }
        } else if (screenId === 'screen-game') {
            if (window.GameEngine) {
                if (params.daily) {
                    GameEngine.loadDailyLevel(params.daily);
                } else if (!GameEngine.level) {
                    GameEngine.loadLevel();
                }
            }
        }

        if (window.App && typeof App.updateUI === 'function') {
            App.updateUI();
        }

        Telemetry.log('screen_navigation', { screenId, params });
    },

    handleBack() {
        if (this.currentScreen === 'screen-game') {
            this.goTo('screen-city');
        } else if (this.currentScreen === 'screen-city') {
            this.goTo('screen-country');
        } else if (this.currentScreen === 'screen-country') {
            this.goTo('screen-globe');
        } else if (this.currentScreen === 'screen-globe') {
            this.goTo('screen-hub');
        } else if (this.screenHistory.length > 0) {
            const prev = this.screenHistory.pop();
            this.goTo(prev);
        } else {
            this.goTo('screen-hub');
        }
    }
};

if (typeof window !== 'undefined') {
    window.ScreenRouter = ScreenRouter;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ScreenRouter;
}

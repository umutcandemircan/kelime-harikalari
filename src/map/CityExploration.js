// CITY EXPLORATION SCREEN CONTROLLER (5 SIMGE MEKÂN × 5 BÖLÜM)
const CityExploration = {
    currentCity: null,
    currentCityIdx: 0,

    openCity(cityIdx) {
        this.currentCityIdx = cityIdx;
        const city = (typeof CITIES !== 'undefined' ? CITIES[cityIdx] : null) || window.CITIES?.[cityIdx];
        if (!city) return;
        this.currentCity = city;

        // Save current city index
        SaveManager.data.currentCityIdx = cityIdx;
        SaveManager.data.hasSelectedStartCity = true;
        SaveManager.save();

        this.renderCityView();
        if (window.ScreenRouter) {
            ScreenRouter.goTo('screen-city');
        }
    },

    renderCityView() {
        if (!this.currentCity) {
            const cityIdx = SaveManager?.data?.currentCityIdx || 0;
            this.currentCity = (typeof CITIES !== 'undefined' ? CITIES[cityIdx] : null) || window.CITIES?.[cityIdx];
            this.currentCityIdx = cityIdx;
        }
        const city = this.currentCity;
        if (!city) return;

        // 1. City Header Info
        const titleEl = document.getElementById('city-explore-title');
        const plateEl = document.getElementById('city-explore-plate');
        const progressEl = document.getElementById('city-explore-progress');
        const sealBadgeEl = document.getElementById('city-explore-seal-badge');

        if (titleEl) titleEl.innerText = city.name;
        if (plateEl) plateEl.innerText = `${city.plate < 10 ? '0' + city.plate : city.plate} • Vilayet`;

        const isCityCompleted = SaveManager.data.completedProvinces.includes(city.plate);
        if (sealBadgeEl) {
            if (isCityCompleted) {
                sealBadgeEl.innerHTML = `<span>Vilayet Mührü Kazanıldı</span>`;
                sealBadgeEl.className = 'city-seal-badge completed';
            } else {
                sealBadgeEl.innerHTML = `<span>Keşif Sürüyor</span>`;
                sealBadgeEl.className = 'city-seal-badge ongoing';
            }
        }

        // Sublevel progress for this city (0..24)
        // If current city is the active save city, use currentSubLevel
        const isActiveCity = SaveManager.data.currentCityIdx === this.currentCityIdx;
        const activeSubLevel = isActiveCity ? (SaveManager.data.currentSubLevel || 0) : (isCityCompleted ? 25 : 0);
        
        if (progressEl) {
            progressEl.innerText = `${activeSubLevel}/25 Bölüm Çözüldü`;
        }

        // 2. Render 5 Landmark Exploration Cards
        const container = document.getElementById('city-landmarks-container');
        if (!container) return;

        const landmarks = city.landmarks || [];
        let html = '';

        landmarks.forEach((lm, lmIdx) => {
            const landmarkNo = lmIdx + 1;
            const startLevel = lmIdx * 5;     // e.g. 0, 5, 10, 15, 20
            const endLevel = startLevel + 4;  // e.g. 4, 9, 14, 19, 24

            let landmarkCompleted = false;
            let landmarkUnlocked = false;
            let currentLevelInLandmark = 1;

            if (isCityCompleted) {
                landmarkCompleted = true;
                landmarkUnlocked = true;
                currentLevelInLandmark = 5;
            } else if (activeSubLevel > endLevel) {
                landmarkCompleted = true;
                landmarkUnlocked = true;
                currentLevelInLandmark = 5;
            } else if (activeSubLevel >= startLevel && activeSubLevel <= endLevel) {
                landmarkCompleted = false;
                landmarkUnlocked = true;
                currentLevelInLandmark = (activeSubLevel - startLevel) + 1;
            } else {
                landmarkCompleted = false;
                landmarkUnlocked = false;
                currentLevelInLandmark = 1;
            }

            const stateClass = landmarkCompleted ? 'completed' : (landmarkUnlocked ? 'active' : 'locked');

            html += `
            <div class="landmark-card ${stateClass}" onclick="CityExploration.selectLandmark(${lmIdx})" tabindex="0" role="button" aria-label="${lm.name}">
                <div class="landmark-card-media" style="background-image: url('${lm.bg || ''}')">
                    <div class="landmark-media-overlay"></div>
                    <span class="landmark-number-pill">Mekân ${landmarkNo}/5</span>
                    <span class="landmark-status-badge">
                        ${landmarkCompleted ? '✓ Tamamlandı' : (landmarkUnlocked ? `Bölüm ${currentLevelInLandmark}/5` : 'Kilitli')}
                    </span>
                </div>
                <div class="landmark-card-body">
                    <h3 class="landmark-card-title">${lm.name}</h3>
                    <p class="landmark-card-desc">${lm.desc || 'Tarihi ve kültürel simge mekân.'}</p>
                    <div class="landmark-card-footer">
                        <div class="landmark-level-dots">
                            ${[0, 1, 2, 3, 4].map(dotIdx => {
                                const dotLevel = startLevel + dotIdx;
                                const isDone = activeSubLevel > dotLevel || isCityCompleted;
                                const isCur = activeSubLevel === dotLevel && !isCityCompleted;
                                return `<span class="level-dot ${isDone ? 'done' : (isCur ? 'current' : '')}"></span>`;
                            }).join('')}
                        </div>
                        <button class="landmark-action-btn ${stateClass}">
                            ${landmarkCompleted ? 'Tekrar Oyna' : (landmarkUnlocked ? 'Keşfe Başla' : 'Kilitli')}
                        </button>
                    </div>
                </div>
            </div>`;
        });

        container.innerHTML = html;
    },

    selectLandmark(lmIdx) {
        AudioEngine.playPop(lmIdx);
        const startLevel = lmIdx * 5;
        
        // Update SaveManager active landmark
        SaveManager.data.currentLandmarkIdx = lmIdx;
        
        // If current city is active, resume from subLevel if it's in this landmark, else jump to start of this landmark
        if (SaveManager.data.currentCityIdx === this.currentCityIdx) {
            const cur = SaveManager.data.currentSubLevel || 0;
            if (cur < startLevel || cur > startLevel + 4) {
                SaveManager.data.currentSubLevel = startLevel;
                SaveManager.save();
            }
        } else {
            SaveManager.data.currentCityIdx = this.currentCityIdx;
            SaveManager.data.currentSubLevel = startLevel;
            SaveManager.save();
        }

        // Launch Game Engine with selected level
        if (window.GameEngine) {
            GameEngine.loadCityLevel(this.currentCityIdx, SaveManager.data.currentSubLevel);
        }
        if (window.ScreenRouter) {
            ScreenRouter.goTo('screen-game');
        }
    }
};

if (typeof window !== 'undefined') {
    window.CityExploration = CityExploration;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CityExploration;
}

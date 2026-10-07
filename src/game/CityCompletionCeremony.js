// CITY COMPLETION GRAND CEREMONY (LEVEL 25 FINALE)
// Sequence: Grid fades out -> Panoramic visual -> 5 Landmark Seals stamp down ->
// Golden Provincial Seal unlocks -> Postcard awarded -> Return to map
const CityCompletionCeremony = {
    active: false,

    start(city, onFinishCallback) {
        this.active = true;
        const modal = document.getElementById('modal-city-ceremony');
        if (!modal) {
            if (typeof onFinishCallback === 'function') onFinishCallback();
            return;
        }

        // 1. Setup UI details
        const titleEl = document.getElementById('ceremony-city-name');
        const plateEl = document.getElementById('ceremony-city-plate');
        const sealsContainer = document.getElementById('ceremony-seals-grid');
        const bannerImg = document.getElementById('ceremony-hero-img');

        if (titleEl) titleEl.innerText = city.name.toUpperCase();
        if (plateEl) plateEl.innerText = `${city.plate < 10 ? '0' + city.plate : city.plate} NOLU VİLAYET TAMAMLANDI!`;
        
        // Landmark photo for hero banner
        const heroBg = city.landmarks?.[4]?.bg || city.landmarks?.[0]?.bg || '';
        if (bannerImg && heroBg) bannerImg.style.backgroundImage = `url('${heroBg}')`;

        // Render 5 landmark seal slots
        if (sealsContainer) {
            let sealsHtml = '';
            (city.landmarks || []).slice(0, 5).forEach((lm, i) => {
                sealsHtml += `
                <div class="ceremony-seal-slot" id="ceremony-seal-${i}">
                    <div class="seal-stamp-ring">
                        <span class="seal-number">${i + 1}</span>
                        <span class="seal-icon">✦</span>
                    </div>
                    <span class="seal-lm-name">${lm.name}</span>
                </div>`;
            });
            sealsContainer.innerHTML = sealsHtml;
        }

        // Show ceremony screen
        modal.classList.remove('hidden');
        modal.classList.add('active');

        // Play celebration fanfare
        AudioEngine.playFanfare();

        // 2. Animate 5 seals stamping down one-by-one with resonant audio
        (city.landmarks || []).slice(0, 5).forEach((_, i) => {
            setTimeout(() => {
                const sealSlot = document.getElementById(`ceremony-seal-${i}`);
                if (sealSlot) {
                    sealSlot.classList.add('stamped');
                    AudioEngine.playStamp();
                }
            }, 600 + i * 400);
        });

        // Mark province completed in SaveManager immediately so progress is never lost
        SaveManager.completeProvince(city.plate);
        SaveManager.addCoins(100);

        // 3. Unlock Grand Provincial Badge after all 5 seals stamp down
        setTimeout(() => {
            const grandBadge = document.getElementById('ceremony-grand-badge');
            if (grandBadge) {
                grandBadge.classList.add('unlocked');
                AudioEngine.playVictory();
            }
            AudioEngine.playCoin();
        }, 600 + 5 * 400 + 400);

        // Bind finish button
        const continueBtn = document.getElementById('ceremony-continue-btn');
        if (continueBtn) {
            continueBtn.onclick = () => {
                modal.classList.remove('active');
                modal.classList.add('hidden');
                this.active = false;
                if (typeof onFinishCallback === 'function') {
                    onFinishCallback();
                } else if (window.ScreenRouter) {
                    ScreenRouter.goTo('screen-country');
                }
            };
        }
    }
};

if (typeof window !== 'undefined') {
    window.CityCompletionCeremony = CityCompletionCeremony;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CityCompletionCeremony;
}

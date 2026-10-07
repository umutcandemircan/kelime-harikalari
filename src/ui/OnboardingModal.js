// ONBOARDING / FIRST-TIME USER EXPERIENCE (V2)
// 4-step modern interactive carousel with skip option & bug report introduction
const OnboardingModal = {
    currentStep: 0,
    totalSteps: 4,

    steps: [
        {
            icon: '🧭',
            title: 'Sözcük Seferî’ne Hoş Geldin',
            desc: 'Kadim Anadolu topraklarından başlayıp tüm dünyaya uzanacak büyüleyici bir kelime ve kültür seferine çıkıyorsun.'
        },
        {
            icon: '🌍',
            title: '3B Dünya Küresi & 81 İl',
            desc: 'Dünya küresinden Türkiye’yi seç, 81 vilayeti ve zengin tarihi coğrafyayı adım adım keşfet.'
        },
        {
            icon: '🏛️',
            title: '5 Simge Mekân × 5 Bölüm',
            desc: 'Her şehirde 5 simge tarihi/doğal mekân seni bekliyor. Harfleri birleştir, kelimeleri çöz, 25 bölümü tamamlayarak Vilayet Mührü’nü kazan!'
        },
        {
            icon: '💬',
            title: 'Hata & Geri Bildirim',
            desc: 'Her ekranda görebileceğin "Hata Bildir" butonundan tek dokunuşla öneri, eksik veya hata bildirebilirsin. Katkılarınla oyun daha da güzelleşiyor!'
        }
    ],

    init() {
        // Keyboard support: Enter/Space advances or finishes, Escape skips
        window.addEventListener('keydown', (e) => {
            const modal = document.getElementById('modal-onboarding');
            if (modal && !modal.classList.contains('hidden')) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.next();
                } else if (e.key === 'Escape') {
                    e.preventDefault();
                    this.skip();
                }
            }
        });
    },

    open() {
        const modal = document.getElementById('modal-onboarding');
        if (!modal) return;
        this.currentStep = 0;
        this.renderStep();
        modal.classList.remove('hidden');
        modal.setAttribute('aria-hidden', 'false');
    },

    close() {
        const modal = document.getElementById('modal-onboarding');
        if (modal) {
            modal.classList.add('hidden');
            modal.setAttribute('aria-hidden', 'true');
        }
        SaveManager.data.onboardingCompleted = true;
        SaveManager.save();
    },

    next() {
        if (this.currentStep < this.totalSteps - 1) {
            this.currentStep++;
            this.renderStep();
            if (window.AudioEngine && typeof AudioEngine.playPop === 'function') {
                AudioEngine.playPop(this.currentStep);
            }
        } else {
            this.finish();
        }
    },

    finish() {
        this.close();
        if (window.AudioEngine && typeof AudioEngine.playFanfare === 'function') {
            AudioEngine.playFanfare();
        }
        // Navigate cleanly to Hub screen
        if (window.ScreenRouter && typeof ScreenRouter.goTo === 'function') {
            ScreenRouter.goTo('screen-hub');
        }
    },

    skip() {
        this.close();
        if (window.ScreenRouter && typeof ScreenRouter.goTo === 'function') {
            ScreenRouter.goTo('screen-hub');
        }
    },

    renderStep() {
        const step = this.steps[this.currentStep];
        const iconEl = document.getElementById('onboard-icon');
        const titleEl = document.getElementById('onboard-title');
        const descEl = document.getElementById('onboard-desc');
        const dotsEl = document.getElementById('onboard-dots');
        const btnNext = document.getElementById('onboard-btn-next');

        if (iconEl) iconEl.innerText = step.icon;
        if (titleEl) titleEl.innerText = step.title;
        if (descEl) descEl.innerText = step.desc;

        if (dotsEl) {
            dotsEl.innerHTML = this.steps.map((_, i) => 
                `<span class="onboard-dot ${i === this.currentStep ? 'active' : ''}" aria-label="Adım ${i + 1}"></span>`
            ).join('');
        }

        if (btnNext) {
            btnNext.innerText = this.currentStep === this.totalSteps - 1 ? 'SEFER BAŞLASIN! 🚀' : 'İlerle →';
        }
    }
};

if (typeof window !== 'undefined') {
    window.OnboardingModal = OnboardingModal;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OnboardingModal;
}

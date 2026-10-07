// FEEDBACK & BUG REPORT SYSTEM (V2)
// Frictionless, privacy-first diagnostic reporting with automatic context enrichment
const FeedbackModal = {
    selectedCategory: 'bug',

    open() {
        const modal = document.getElementById('modal-feedback');
        if (!modal) return;

        // Auto-populate diagnostic context preview
        const diagEl = document.getElementById('feedback-diag-preview');
        const context = this.getDiagnostics();
        if (diagEl) {
            diagEl.innerText = `Sistem Bilgisi: Sürüm: ${context.appVersion} | Ekran: ${context.viewport} | Konum: ${context.location}`;
        }

        // Reset inputs
        const textarea = document.getElementById('feedback-message-input');
        if (textarea) textarea.value = '';

        const successNotice = document.getElementById('feedback-success-notice');
        if (successNotice) successNotice.classList.add('hidden');

        const formBody = document.getElementById('feedback-form-body');
        if (formBody) formBody.classList.remove('hidden');

        modal.classList.remove('hidden');
    },

    close() {
        const modal = document.getElementById('modal-feedback');
        if (modal) modal.classList.add('hidden');
    },

    setCategory(cat) {
        this.selectedCategory = cat;
        document.querySelectorAll('.feedback-cat-pill').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.cat === cat);
        });
        AudioEngine.playPop(1);
    },

    getDiagnostics() {
        const currentCity = typeof CITIES !== 'undefined' ? CITIES[SaveManager.data.currentCityIdx] : null;
        const cityName = currentCity ? currentCity.name : 'Genel';
        const sub = SaveManager.data.currentSubLevel || 0;
        const m = Math.floor(sub / 5) + 1;
        const b = (sub % 5) + 1;

        return {
            appVersion: SaveManager.CURRENT_APP_VERSION || '2.0.0',
            schemaVersion: SaveManager.CURRENT_SCHEMA_VERSION || 4,
            viewport: `${window.innerWidth}x${window.innerHeight}`,
            deviceClass: InputManager.isTouchDevice ? 'Dokunmatik (Mobil/Tablet)' : 'İşaretçi (Masaüstü/Laptop)',
            userAgent: navigator.userAgent,
            timestamp: new Date().toISOString(),
            location: `${cityName} (Mekân ${m}, Bölüm ${b})`,
            currentScreen: window.ScreenRouter ? ScreenRouter.currentScreen : 'Bilinmiyor'
        };
    },

    submit() {
        const textarea = document.getElementById('feedback-message-input');
        const message = textarea ? textarea.value.trim() : '';

        if (!message) {
            if (textarea) {
                textarea.style.borderColor = '#ef4444';
                textarea.focus();
                setTimeout(() => textarea.style.borderColor = '', 1500);
            }
            return;
        }

        const report = {
            id: 'fb-' + Date.now(),
            category: this.selectedCategory,
            message,
            diagnostics: this.getDiagnostics()
        };

        // Record locally in SaveManager
        SaveManager.recordFeedback(report);
        Telemetry.log('feedback_submitted', { category: this.selectedCategory });
        AudioEngine.playVictory();

        // Show success state
        const formBody = document.getElementById('feedback-form-body');
        const successNotice = document.getElementById('feedback-success-notice');
        if (formBody) formBody.classList.add('hidden');
        if (successNotice) successNotice.classList.remove('hidden');

        setTimeout(() => {
            this.close();
        }, 1800);
    }
};

if (typeof window !== 'undefined') {
    window.FeedbackModal = FeedbackModal;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FeedbackModal;
}

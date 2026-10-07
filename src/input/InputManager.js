// MULTI-DEVICE UNIFIED INPUT MANAGER
// Supports Touch (mobile/tablet), Pointer/Mouse (desktop), Wheel, and Keyboard (smartboards & laptops)
const InputManager = {
    isTouchDevice: false,

    init() {
        this.detectDevice();
        this.bindKeyboard();
    },

    detectDevice() {
        this.isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
        if (this.isTouchDevice) {
            document.documentElement.classList.add('touch-device');
        } else {
            document.documentElement.classList.add('pointer-device');
        }
    },

    bindKeyboard() {
        window.addEventListener('keydown', (e) => {
            // Ignore if active inside an input or textarea (e.g. feedback form)
            if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
                return;
            }

            const key = e.key;

            // Global Escape: Close top active modal or go back
            if (key === 'Escape') {
                e.preventDefault();
                this.handleEscape();
                return;
            }

            // Game screen keyboard controls
            const gameScreen = document.getElementById('screen-game');
            if (gameScreen && gameScreen.classList.contains('active')) {
                if (key === 'Enter') {
                    e.preventDefault();
                    if (window.GameEngine && typeof GameEngine.submitCurrentWord === 'function') {
                        GameEngine.submitCurrentWord();
                    }
                } else if (key === 'Backspace') {
                    e.preventDefault();
                    if (window.GameEngine && typeof GameEngine.popLastLetter === 'function') {
                        GameEngine.popLastLetter();
                    }
                } else if (key === ' ') {
                    e.preventDefault();
                    if (window.GameEngine && typeof GameEngine.shuffleWheel === 'function') {
                        GameEngine.shuffleWheel();
                    }
                } else if (/^[a-zA-ZçğıöşüÇĞİÖŞÜ]$/i.test(key)) {
                    // Typed a letter: find in current wheel
                    const char = ContentPolicy.normalize(key);
                    if (window.GameEngine && typeof GameEngine.typeLetter === 'function') {
                        GameEngine.typeLetter(char);
                    }
                }
            }
        });
    },

    handleEscape() {
        // Find visible modals
        const visibleModal = document.querySelector('.modal-overlay:not(.hidden)');
        if (visibleModal) {
            visibleModal.classList.add('hidden');
            return;
        }

        // Screen routing back
        if (window.ScreenRouter) {
            ScreenRouter.handleBack();
        }
    }
};

if (typeof window !== 'undefined') {
    window.InputManager = InputManager;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = InputManager;
}

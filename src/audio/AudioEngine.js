// PROCEDURAL WEB AUDIO SYNTHESIZER & SOUND FX
const AudioEngine = {
    ctx: null,

    init() {
        if (!this.ctx) {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (AudioCtx) this.ctx = new AudioCtx();
        }
    },

    isEnabled() {
        return Boolean(SaveManager?.data?.settings?.soundEnabled ?? true);
    },

    toggleSound(val) {
        if (!SaveManager?.data?.settings) return;
        SaveManager.data.settings.soundEnabled = Boolean(val);
        SaveManager.save();
    },

    playTone(freq, type = 'sine', duration = 0.2, vol = 0.2) {
        if (!this.isEnabled()) return;
        this.init();
        if (!this.ctx) return;
        try {
            if (this.ctx.state === 'suspended') {
                this.ctx.resume();
            }
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
            gain.gain.setValueAtTime(vol, this.ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, this.ctx.currentTime + duration);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start();
            osc.stop(this.ctx.currentTime + duration);
        } catch (_) {}
    },

    playLetter(idx = 0) {
        const scale = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25];
        this.playTone(scale[idx % scale.length], 'sine', 0.18, 0.22);
        this.triggerHaptic(12);
    },

    playPop(idx = 0) {
        this.playLetter(idx);
    },

    playWordCorrect() {
        [523.25, 659.25, 783.99].forEach((f, i) => {
            setTimeout(() => this.playTone(f, 'triangle', 0.35, 0.25), i * 60);
        });
        this.triggerHaptic([25, 40, 30]);
    },

    playWrong() {
        this.playTone(140, 'sawtooth', 0.28, 0.25);
        this.triggerHaptic(80);
    },

    playVictory() {
        const notes = [523.25, 659.25, 783.99, 1046.50];
        notes.forEach((f, i) => {
            setTimeout(() => this.playTone(f, 'sine', 0.4, 0.25), i * 140);
        });
        this.triggerHaptic([30, 60, 100]);
    },

    playStamp() {
        // Deep resonant stamp thud
        this.playTone(95, 'triangle', 0.25, 0.4);
        setTimeout(() => this.playTone(190, 'sine', 0.15, 0.2), 30);
        this.triggerHaptic([45, 70]);
    },

    playFanfare() {
        // Grand 5-tone fanfare for city completion
        const fanfare = [392.00, 523.25, 659.25, 783.99, 1046.50];
        fanfare.forEach((f, i) => {
            setTimeout(() => this.playTone(f, 'triangle', 0.5, 0.3), i * 120);
        });
        this.triggerHaptic([50, 80, 50, 120]);
    },

    playCoin() {
        this.playTone(987.77, 'sine', 0.12, 0.25);
        setTimeout(() => this.playTone(1318.51, 'sine', 0.2, 0.25), 80);
        this.triggerHaptic(15);
    },

    triggerHaptic(pattern) {
        if (!SaveManager?.data?.settings?.hapticEnabled) return;
        if (typeof navigator !== 'undefined' && navigator.vibrate) {
            try { navigator.vibrate(pattern); } catch (_) {}
        }
    }
};

if (typeof window !== 'undefined') {
    window.AudioEngine = AudioEngine;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AudioEngine;
}

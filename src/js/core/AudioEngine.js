// 2. PROCEDURAL WEB AUDIO SYNTHESIZER
const AudioEngine = {
    ctx: null,
    enabled: true,

    init() {
        if (!this.ctx) {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (AudioCtx) this.ctx = new AudioCtx();
        }
    },

    toggleSound(val) {
        this.enabled = Boolean(val);
        SaveManager.data.soundEnabled = this.enabled;
        SaveManager.save();
    },

    playTone(freq, type = 'sine', duration = 0.2, vol = 0.2) {
        if (!this.enabled) return;
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
            gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start();
            osc.stop(this.ctx.currentTime + duration);
        } catch (e) {
            // Audio error swallowed gracefully
        }
    },

    playLetter(idx = 0) {
        const scale = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25];
        this.playTone(scale[idx % scale.length], 'sine', 0.18, 0.22);
        if (SaveManager.data.hapticEnabled && navigator.vibrate) {
            try { navigator.vibrate(12); } catch (_) {}
        }
    },

    playPop(idx = 0) {
        this.playLetter(idx);
    },

    playWordCorrect() {
        [523.25, 659.25, 783.99].forEach((f, i) => {
            setTimeout(() => this.playTone(f, 'triangle', 0.35, 0.25), i * 60);
        });
        if (SaveManager.data.hapticEnabled && navigator.vibrate) {
            try { navigator.vibrate([25, 40, 30]); } catch (_) {}
        }
    },

    playWrong() {
        this.playTone(140, 'sawtooth', 0.28, 0.25);
        if (SaveManager.data.hapticEnabled && navigator.vibrate) {
            try { navigator.vibrate(80); } catch (_) {}
        }
    },

    playVictory() {
        const notes = [523.25, 659.25, 783.99, 1046.50];
        notes.forEach((f, i) => {
            setTimeout(() => this.playTone(f, 'sine', 0.4, 0.25), i * 140);
        });
    }
};
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
                this.enabled = val;
                SaveManager.data.soundEnabled = val;
                SaveManager.save();
            },
            playTone(freq, type='sine', duration=0.2, vol=0.2) {
                if (!this.enabled) return;
                this.init();
                if (!this.ctx) return;
                try {
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
                } catch (e) {}
            },
            playLetter(idx) {
                const scale = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25];
                this.playTone(scale[idx % scale.length], 'sine', 0.18, 0.22);
                if (SaveManager.data.hapticEnabled && navigator.vibrate) navigator.vibrate(12);
            },
            playWordCorrect() {
                // Chime chord
                [523.25, 659.25, 783.99].forEach((f, i) => {
                    setTimeout(() => this.playTone(f, 'triangle', 0.35, 0.25), i * 60);
                });
                if (SaveManager.data.hapticEnabled && navigator.vibrate) navigator.vibrate([25, 40, 30]);
            },
            playWrong() {
                this.playTone(140, 'sawtooth', 0.28, 0.25);
                if (SaveManager.data.hapticEnabled && navigator.vibrate) navigator.vibrate(80);
            },
            playVictory() {
                const notes = [523.25, 659.25, 783.99, 1046.50];
                notes.forEach((f, i) => {
                    setTimeout(() => this.playTone(f, 'sine', 0.4, 0.25), i * 140);
                });
            }
        };

        
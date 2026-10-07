// 5. DEYİM AVCISI MINI-MODE (PREMIUM PARCHMENT THEME & BUG-FREE ENGINE)
const IdiomEngine = {
    currentIdx: 0,
    idiom: null,
    letters: [],
    selectedIndices: [],
    isDragging: false,

    init() {
        if (typeof IDIOMS === 'undefined' || !IDIOMS || IDIOMS.length === 0) return;
        this.currentIdx = Math.floor(Math.random() * IDIOMS.length);
        this.loadIdiom();
        this.bindEvents();
    },

    loadIdiom() {
        if (typeof IDIOMS === 'undefined' || !IDIOMS || IDIOMS.length === 0) return;
        this.idiom = IDIOMS[this.currentIdx];
        if (!this.idiom) return;

        // Cleanly format missing idiom phrase
        const rawText = this.idiom.text || this.idiom.clue || 'Deyimi tamamla: ___';
        const formattedClue = rawText.replace('___', '<span class="idiom-blank">[ &nbsp;?&nbsp; ]</span>');
        
        const clueEl = document.getElementById('idiom-clue-box');
        if (clueEl) clueEl.innerHTML = formattedClue;

        const meaningEl = document.getElementById('idiom-meaning-box');
        if (meaningEl) meaningEl.innerText = this.idiom.meaning ? `“${this.idiom.meaning}”` : '';

        // Build target answer cells
        const board = document.getElementById('idiom-board');
        if (board) {
            board.innerHTML = '';
            for (let i = 0; i < this.idiom.answer.length; i++) {
                const cell = document.createElement('div');
                cell.className = 'grid-cell idiom-cell';
                cell.id = `id-cell-${i}`;
                cell.innerText = '';
                board.appendChild(cell);
            }
        }

        // Shuffle letters on wheel
        this.letters = this.idiom.answer.split('');
        for (let i = this.letters.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.letters[i], this.letters[j]] = [this.letters[j], this.letters[i]];
        }
        this.drawWheel();
        this.updateDragLine(null);
        this.updatePreview();
    },

    drawWheel() {
        const container = document.getElementById('idiom-letters-container');
        if (!container) return;
        container.innerHTML = '';
        const count = this.letters.length;
        if (count === 0) return;

        const asm = document.getElementById('idiom-wheel-assembly');
        const w = asm ? (asm.clientWidth || 270) : 270;
        const cx = w / 2;
        const cy = w / 2;
        const radius = (w / 2) - 38;
        const step = (2 * Math.PI) / count;

        this.letters.forEach((char, i) => {
            const angle = i * step - Math.PI / 2;
            const x = cx + radius * Math.cos(angle);
            const y = cy + radius * Math.sin(angle);

            const node = document.createElement('div');
            node.className = 'letter-node';
            node.style.left = x + 'px';
            node.style.top = y + 'px';
            node.innerText = char;
            node.dataset.idx = i;
            node.dataset.x = x;
            node.dataset.y = y;
            container.appendChild(node);
        });
    },

    bindEvents() {
        const wheel = document.getElementById('idiom-wheel-assembly');
        if (!wheel) return;

        wheel.addEventListener('pointerdown', (e) => {
            const node = e.target.closest('.letter-node');
            if (node) {
                this.isDragging = true;
                this.selectedIndices = [parseInt(node.dataset.idx)];
                node.classList.add('selected');
                this.updatePreview();
                this.updateDragLine(e);
                if (window.AudioEngine) AudioEngine.playPop();
            }
        });

        window.addEventListener('pointermove', (e) => {
            if (!this.isDragging) return;
            const el = document.elementFromPoint(e.clientX, e.clientY);
            if (el) {
                const node = el.closest('#idiom-wheel-assembly .letter-node');
                if (node) {
                    const idx = parseInt(node.dataset.idx);
                    if (!this.selectedIndices.includes(idx)) {
                        this.selectedIndices.push(idx);
                        node.classList.add('selected');
                        this.updatePreview();
                        if (window.AudioEngine) AudioEngine.playPop();
                    } else if (this.selectedIndices.length > 1 && idx === this.selectedIndices[this.selectedIndices.length - 2]) {
                        // Undo last letter if moving backwards
                        const popped = this.selectedIndices.pop();
                        const poppedNode = document.querySelector(`#idiom-wheel-assembly .letter-node[data-idx="${popped}"]`);
                        if (poppedNode) poppedNode.classList.remove('selected');
                        this.updatePreview();
                        if (window.AudioEngine) AudioEngine.playPop();
                    }
                }
            }
            this.updateDragLine(e);
        });

        window.addEventListener('pointerup', () => {
            if (!this.isDragging) return;
            this.isDragging = false;
            const word = this.selectedIndices.map(i => this.letters[i]).join('');
            const normWord = typeof ContentPolicy !== 'undefined' ? ContentPolicy.normalize(word) : word;
            
            // Content policy check
            if (typeof ContentPolicy !== 'undefined' && !ContentPolicy.check(normWord).allowed) {
                if (window.AudioEngine) AudioEngine.playWrong();
                this.selectedIndices = [];
                document.querySelectorAll('#idiom-wheel-assembly .letter-node').forEach(n => n.classList.remove('selected'));
                this.updateDragLine(null);
                this.updatePreview();
                return;
            }

            if (this.idiom && normWord === this.idiom.answer) {
                if (window.AudioEngine) AudioEngine.playVictory();
                SaveManager.addCoins(50);
                
                for (let i = 0; i < word.length; i++) {
                    const c = document.getElementById(`id-cell-${i}`);
                    if (c) {
                        c.innerText = word[i];
                        c.classList.add('solved');
                    }
                }

                // Show celebration and advance to next idiom
                const clueEl = document.getElementById('idiom-clue-box');
                if (clueEl) {
                    clueEl.innerHTML = `<span style="color:#10b981;">✓ Doğru: ${this.idiom.answer}!</span>`;
                }

                setTimeout(() => {
                    this.currentIdx = (this.currentIdx + 1) % IDIOMS.length;
                    this.loadIdiom();
                }, 1400);
            } else if (word.length > 0) {
                if (window.AudioEngine) AudioEngine.playWrong();
            }

            this.selectedIndices = [];
            document.querySelectorAll('#idiom-wheel-assembly .letter-node').forEach(n => n.classList.remove('selected'));
            this.updateDragLine(null);
            this.updatePreview();
        });
    },

    updateDragLine(pos) {
        const poly = document.getElementById('idiom-drag-line');
        if (!poly) return;
        if (!this.isDragging || this.selectedIndices.length === 0) {
            poly.setAttribute('points', '');
            return;
        }

        const asm = document.getElementById('idiom-wheel-assembly');
        if (!asm) return;
        const asmRect = asm.getBoundingClientRect();

        const pts = this.selectedIndices.map(idx => {
            const node = document.querySelector(`#idiom-wheel-assembly .letter-node[data-idx="${idx}"]`);
            if (node) {
                const r = node.getBoundingClientRect();
                return `${r.left - asmRect.left + r.width / 2},${r.top - asmRect.top + r.height / 2}`;
            }
            return '0,0';
        });

        if (pos) {
            pts.push(`${pos.clientX - asmRect.left},${pos.clientY - asmRect.top}`);
        }
        poly.setAttribute('points', pts.join(' '));
    },

    updatePreview() {
        const pill = document.getElementById('idiom-preview-pill');
        if (!pill) return;
        if (this.selectedIndices.length > 0) {
            pill.innerText = this.selectedIndices.map(i => this.letters[i]).join('');
            pill.classList.add('active');
        } else {
            pill.innerText = '';
            pill.classList.remove('active');
        }
    }
};
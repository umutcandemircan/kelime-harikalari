// 5. DEYİM AVCISI MINI-MODE
        const IdiomEngine = {
            currentIdx: 0,
            idiom: null,
            letters: [],
            selectedIndices: [],
            isDragging: false,

            init() {
                this.currentIdx = Math.floor(Math.random() * IDIOMS.length);
                this.loadIdiom();
                this.bindEvents();
            },
            loadIdiom() {
                this.idiom = IDIOMS[this.currentIdx];
                document.getElementById('idiom-clue-box').innerText = this.idiom.clue;
                document.getElementById('idiom-meaning-box').innerText = this.idiom.meaning;

                const board = document.getElementById('idiom-board');
                board.innerHTML = '';
                for (let i = 0; i < this.idiom.answer.length; i++) {
                    const cell = document.createElement('div');
                    cell.className = 'grid-cell';
                    cell.style.position = 'relative';
                    cell.id = `id-cell-${i}`;
                    board.appendChild(cell);
                }

                this.letters = this.idiom.answer.split('');
                for (let i = this.letters.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [this.letters[i], this.letters[j]] = [this.letters[j], this.letters[i]];
                }
                this.drawWheel();
            },
            drawWheel() {
                const container = document.getElementById('idiom-letters-container');
                container.innerHTML = '';
                const radius = 95, cx = 135, cy = 135;
                const step = (2 * Math.PI) / this.letters.length;

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
                wheel.addEventListener('pointerdown', (e) => {
                    if (e.target.classList.contains('letter-node')) {
                        this.isDragging = true;
                        this.selectedIndices = [e.target.dataset.idx];
                        e.target.classList.add('selected');
                        this.updatePreview();
                        AudioEngine.playLetter(0);
                    }
                });
                window.addEventListener('pointermove', (e) => {
                    if (!this.isDragging) return;
                    const el = document.elementFromPoint(e.clientX, e.clientY);
                    if (el && el.classList.contains('letter-node') && el.closest('#idiom-wheel-assembly')) {
                        const idx = el.dataset.idx;
                        if (!this.selectedIndices.includes(idx)) {
                            this.selectedIndices.push(idx);
                            el.classList.add('selected');
                            this.updatePreview();
                            AudioEngine.playLetter(this.selectedIndices.length - 1);
                        }
                    }
                });
                window.addEventListener('pointerup', () => {
                    if (!this.isDragging) return;
                    this.isDragging = false;
                    const word = this.selectedIndices.map(i => this.letters[i]).join('');
                    if (word === this.idiom.answer) {
                        AudioEngine.playVictory();
                        SaveManager.addCoins(50);
                        for (let i = 0; i < word.length; i++) {
                            const c = document.getElementById(`id-cell-${i}`);
                            c.innerText = word[i];
                            c.classList.add('solved');
                        }
                        setTimeout(() => {
                            this.currentIdx = (this.currentIdx + 1) % IDIOMS.length;
                            this.loadIdiom();
                        }, 1500);
                    } else {
                        AudioEngine.playWrong();
                    }
                    this.selectedIndices = [];
                    document.querySelectorAll('#idiom-wheel-assembly .letter-node').forEach(n => n.classList.remove('selected'));
                    this.updatePreview();
                });
            },
            updatePreview() {
                const pill = document.getElementById('idiom-preview-pill');
                if (this.selectedIndices.length > 0) {
                    pill.innerText = this.selectedIndices.map(i => this.letters[i]).join('');
                    pill.classList.add('active');
                } else {
                    pill.classList.remove('active');
                }
            }
        };

        
// 4. CROSSWORD & GAMEPLAY ENGINE
const GameEngine = {
    city: null,
    level: null,
    gridCells: [],
    words: [],
    foundWords: new Set(),
    letters: [],
    selectedIndices: [],
    isDragging: false,
    targetModeActive: false,
    
    // Performance & Scoring
    mistakes: 0,
    hintsUsed: 0,
    difficulty: 'EASY', // EASY | MEDIUM | HARD

    loadLevel() {
        const cityIdx = SaveManager.data.currentCityIdx;
        const subIdx = SaveManager.data.currentSubLevel;
        this.city = CITIES[cityIdx];
        this.level = this.city.levels[subIdx % this.city.levels.length];
        
        document.getElementById('game-city-label').innerText = `${trUpper(this.city.name)} (${this.city.plate < 10 ? '0' + this.city.plate : this.city.plate})`;
        document.getElementById('game-landmark-label').innerText = this.level.landmark || this.city.name;
        document.getElementById('game-bg-img').src = this.level.bg || '';

        this.foundWords.clear();
        this.words = this.level.words;
        this.letters = [...this.level.letters];
        
        // Reset Scoring
        this.mistakes = 0;
        this.hintsUsed = 0;
        this.difficulty = this.calculateDifficulty(this.level);
        
        this.buildCrossword();
        this.shuffleLetters();
    },

    calculateDifficulty(level) {
        const wordCount = level.words.length;
        const totalLen = level.words.reduce((sum, w) => sum + w.word.length, 0);
        const avgLen = totalLen / wordCount;
        
        if (wordCount < 4 && avgLen <= 4.5) return 'EASY';
        if (wordCount > 6 || avgLen > 5.5) return 'HARD';
        return 'MEDIUM';
    },

    buildCrossword() {
        const container = document.getElementById('crossword-container');
        container.innerHTML = '';
        this.gridCells = [];

        if (this.words.length === 0) return;

        let minR = Math.min(...this.words.map(w => w.row));
        let maxR = Math.max(...this.words.map(w => w.dir === 'V' ? w.row + w.word.length - 1 : w.row));
        let minC = Math.min(...this.words.map(w => w.col));
        let maxC = Math.max(...this.words.map(w => w.dir === 'H' ? w.col + w.word.length - 1 : w.col));

        const rows = maxR - minR + 1;
        const cols = maxC - minC + 1;
        
        // Ensure minimum 4x4 for visual padding
        const maxDim = Math.max(rows, cols, 4);

        container.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
        container.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
        container.style.aspectRatio = `${cols}/${rows}`;

        const gridMap = {};
        this.words.forEach(w => {
            for (let i = 0; i < w.word.length; i++) {
                const r = w.row - minR + (w.dir === 'V' ? i : 0);
                const c = w.col - minC + (w.dir === 'H' ? i : 0);
                const char = w.word[i];
                gridMap[`${r},${c}`] = char;
            }
        });

        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                const char = gridMap[`${r},${c}`];
                if (char) {
                    const cell = document.createElement('div');
                    cell.className = 'grid-cell';
                    cell.onclick = () => this.handleCellClick(cell);
                    container.appendChild(cell);
                    this.gridCells.push({ r, c, char, el: cell, solved: false });
                } else {
                    const empty = document.createElement('div');
                    container.appendChild(empty);
                }
            }
        }
    },

    shuffleLetters() {
        for (let i = this.letters.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.letters[i], this.letters[j]] = [this.letters[j], this.letters[i]];
        }
        this.drawWheel();
    },

    drawWheel() {
        const svg = document.getElementById('wheel-svg');
        const labels = document.getElementById('wheel-labels');
        labels.innerHTML = '';
        
        const count = this.letters.length;
        const r = 100;
        const cx = 150;
        const cy = 150;

        for (let i = 0; i < count; i++) {
            const angle = (i * 2 * Math.PI) / count - Math.PI / 2;
            const x = cx + r * Math.cos(angle);
            const y = cy + r * Math.sin(angle);

            const node = document.createElement('div');
            node.className = 'letter-node';
            node.innerText = this.letters[i];
            node.style.left = `${x}px`;
            node.style.top = `${y}px`;
            node.dataset.idx = i;
            node.dataset.x = x;
            node.dataset.y = y;

            labels.appendChild(node);
        }

        const asm = document.getElementById('wheel-assembly');
        asm.onpointerdown = this.handleDown.bind(this);
        asm.onpointermove = this.handleMove.bind(this);
        asm.onpointerup = this.handleUp.bind(this);
        asm.onpointercancel = this.handleUp.bind(this);
    },

    handleDown(e) {
        if (e.target.classList.contains('letter-node')) {
            this.isDragging = true;
            this.selectedIndices = [parseInt(e.target.dataset.idx)];
            e.target.classList.add('selected');
            this.updateDragLine(e);
            this.updatePreview();
            AudioEngine.playPop();
        }
    },

    handleMove(e) {
        if (!this.isDragging) return;
        e.preventDefault();

        const clientX = e.clientX !== undefined ? e.clientX : (e.touches && e.touches[0].clientX);
        const clientY = e.clientY !== undefined ? e.clientY : (e.touches && e.touches[0].clientY);
        
        if (clientX === undefined) return;

        const el = document.elementFromPoint(clientX, clientY);
        if (el && el.classList.contains('letter-node')) {
            const idx = parseInt(el.dataset.idx);
            if (!this.selectedIndices.includes(idx)) {
                this.selectedIndices.push(idx);
                el.classList.add('selected');
                this.updatePreview();
                AudioEngine.playPop();
            } else if (this.selectedIndices.length > 1 && idx === this.selectedIndices[this.selectedIndices.length - 2]) {
                const popped = this.selectedIndices.pop();
                document.querySelector(`.letter-node[data-idx="${popped}"]`).classList.remove('selected');
                this.updatePreview();
                AudioEngine.playPop();
            }
        }
        this.updateDragLine({ clientX, clientY });
    },

    handleUp(e) {
        if (!this.isDragging) return;
        this.isDragging = false;
        const word = this.selectedIndices.map(i => this.letters[i]).join('');
        this.validateWord(word);

        this.selectedIndices = [];
        document.querySelectorAll('.letter-node').forEach(n => n.classList.remove('selected'));
        this.updateDragLine(null);
        this.updatePreview();
    },

    updateDragLine(e) {
        const poly = document.getElementById('wheel-drag-line');
        if (this.selectedIndices.length === 0) {
            poly.setAttribute('points', '');
            return;
        }
        let pts = [];
        this.selectedIndices.forEach(idx => {
            const el = document.querySelector(`.letter-node[data-idx="${idx}"]`);
            pts.push(`${el.dataset.x},${el.dataset.y}`);
        });
        if (e) {
            const rect = document.getElementById('wheel-assembly').getBoundingClientRect();
            const x = (e.clientX !== undefined ? e.clientX : e.touches[0].clientX) - rect.left;
            const y = (e.clientY !== undefined ? e.clientY : e.touches[0].clientY) - rect.top;
            pts.push(`${x},${y}`);
        }
        poly.setAttribute('points', pts.join(' '));
    },

    updatePreview() {
        const pill = document.getElementById('word-preview-pill');
        if (this.selectedIndices.length > 0) {
            pill.innerText = this.selectedIndices.map(i => this.letters[i]).join('');
            pill.classList.add('active');
            pill.style.background = 'rgba(13, 148, 136, 0.95)';
        } else {
            pill.classList.remove('active');
        }
    },

    validateWord(word) {
        if (!word || word.length < 2) return;
        let matched = false;

        this.words.forEach(w => {
            if (w.word === word) {
                if (!this.foundWords.has(word)) {
                    this.foundWords.add(word);
                    matched = true;
                    AudioEngine.playWordCorrect();
                    this.revealWord(w);
                }
            }
        });

        if (!matched) {
            this.mistakes++;
            AudioEngine.playWrong();
            const pill = document.getElementById('word-preview-pill');
            pill.style.background = 'rgba(220, 38, 38, 0.95)';
            pill.classList.add('active');
            setTimeout(() => pill.classList.remove('active'), 500);

            // Add to bonus chest if it's a valid word in TDK dictionary but not in puzzle
            if (TDK_DICT_FULL.includes(word)) {
                SaveManager.data.bonusChest = (SaveManager.data.bonusChest || 0) + 1;
                if (SaveManager.data.bonusChest >= 5) {
                    SaveManager.data.bonusChest = 0;
                    SaveManager.addCoins(30);
                    AudioEngine.playVictory();
                }
                SaveManager.save();
                document.getElementById('bonus-chest-text').innerText = `${SaveManager.data.bonusChest}/5`;
                // Show floating text "Bonus!"
            }
        }
    },

    revealWord(w) {
        let minR = Math.min(...this.words.map(ww => ww.row));
        let minC = Math.min(...this.words.map(ww => ww.col));

        for (let i = 0; i < w.word.length; i++) {
            const r = w.row - minR + (w.dir === 'V' ? i : 0);
            const c = w.col - minC + (w.dir === 'H' ? i : 0);
            const cell = this.gridCells.find(gc => gc.r === r && gc.c === c);
            if (cell && !cell.solved) {
                cell.solved = true;
                setTimeout(() => {
                    cell.el.innerText = cell.char;
                    cell.el.classList.add('solved');
                    cell.el.style.transform = 'scale(1.1) rotateX(180deg)';
                    setTimeout(() => cell.el.style.transform = 'scale(1) rotateX(0deg)', 150);
                }, i * 80);
            }
        }
        setTimeout(() => this.checkWinCondition(), w.word.length * 80 + 350);
    },

    calculateStars() {
        // Dynamic scoring based on difficulty
        const totalWords = this.words.length;
        
        let stars = 3;
        if (this.hintsUsed > 0) {
            stars = 2;
        }
        if (this.hintsUsed > 2 || this.mistakes > totalWords * 1.5) {
            stars = 1;
        }
        if (this.hintsUsed === 0 && this.mistakes === 0) {
            stars = 3; // Perfect
        }
        return stars;
    },

    checkWinCondition() {
        if (this.foundWords.size === this.words.length) {
            AudioEngine.playVictory();
            
            const stars = this.calculateStars();
            let baseReward = 20;
            if (this.difficulty === 'MEDIUM') baseReward = 30;
            if (this.difficulty === 'HARD') baseReward = 50;
            
            const finalReward = baseReward + (stars * 5);
            SaveManager.addCoins(finalReward);
            
            SaveManager.saveStar(SaveManager.data.currentCityIdx, SaveManager.data.currentSubLevel, stars);
            
            // Show Postcard
            const pc = this.level.postcard || {
                landmark: this.level.landmark || this.city.name,
                desc: `${this.city.name} ilimizin eşsiz güzelliklerini ${stars} yıldızla başarıyla keşfettin!`,
                bg: this.level.bg
            };
            document.getElementById('post-landmark-title').innerText = pc.landmark;
            document.getElementById('post-story-text').innerText = pc.desc;
            document.getElementById('post-photo-img').src = pc.bg || '';
            
            // Render stars in postcard (we need to inject this into the UI)
            const pcStars = document.getElementById('post-stars') || document.createElement('div');
            pcStars.id = 'post-stars';
            pcStars.innerHTML = '⭐'.repeat(stars) + '☆'.repeat(3 - stars);
            pcStars.style.fontSize = '24px';
            pcStars.style.textAlign = 'center';
            pcStars.style.margin = '10px 0';
            
            const titleEl = document.getElementById('post-landmark-title');
            if (!document.getElementById('post-stars')) {
                titleEl.parentNode.insertBefore(pcStars, titleEl.nextSibling);
            }
            
            App.showModal('modal-postcard');
        }
    },

    // POWERUPS
    useBulb() {
        let cost = 30;
        if (SaveManager.spendCoins(cost)) {
            this.hintsUsed++;
            const unsolved = this.gridCells.filter(c => !c.solved);
            if (unsolved.length > 0) {
                const target = unsolved[Math.floor(Math.random() * unsolved.length)];
                target.solved = true;
                target.el.innerText = target.char;
                target.el.classList.add('solved');
                AudioEngine.playWordCorrect();
                this.checkWinCondition();
            }
        }
    },

    useTarget() {
        if (this.targetModeActive) return;
        let cost = 60;
        if (SaveManager.spendCoins(cost)) {
            this.hintsUsed++;
            this.targetModeActive = true;
            this.gridCells.filter(c => !c.solved).forEach(c => {
                c.el.classList.add('target-mode');
                c.el.style.animation = 'pulse 1s infinite';
            });
        }
    },

    handleCellClick(el) {
        if (!this.targetModeActive) return;
        const cell = this.gridCells.find(c => c.el === el);
        if (cell && !cell.solved) {
            cell.solved = true;
            cell.el.innerText = cell.char;
            cell.el.classList.add('solved');
            this.targetModeActive = false;
            this.gridCells.forEach(c => {
                c.el.classList.remove('target-mode');
                c.el.style.animation = 'none';
            });
            AudioEngine.playWordCorrect();
            this.checkWinCondition();
        }
    },

    useBomb() {
        let cost = 90;
        if (SaveManager.spendCoins(cost)) {
            this.hintsUsed += 3;
            const unsolved = this.gridCells.filter(c => !c.solved);
            const count = Math.min(3, unsolved.length);
            for (let i = 0; i < count; i++) {
                const target = unsolved[i];
                target.solved = true;
                setTimeout(() => {
                    target.el.innerText = target.char;
                    target.el.classList.add('solved');
                    target.el.style.transform = 'scale(1.2)';
                    setTimeout(() => target.el.style.transform = 'scale(1)', 200);
                }, i * 150);
            }
            AudioEngine.playVictory();
            setTimeout(() => this.checkWinCondition(), count * 150 + 300);
        }
    }
};
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
    isDailyMode: false,
    dailyLevel: null,
    
    // Performance & Scoring
    mistakes: 0,
    hintsUsed: 0,
    difficulty: 'EASY', // EASY | MEDIUM | HARD

    loadLevel() {
        this.isDailyMode = false;
        const cityIdx = SaveManager.data.currentCityIdx;
        const subIdx = SaveManager.data.currentSubLevel;
        this.city = CITIES[cityIdx];
        const levels = this.city.levels || [];
        this.level = levels[subIdx % levels.length];
        
        const plateStr = this.city.plate < 10 ? '0' + this.city.plate : this.city.plate;
        const mekanNo = this.level.mekan_no || (Math.floor(subIdx / 5) + 1);
        const bulmacaNo = this.level.bulmaca_no || ((subIdx % 5) + 1);
        const landmarkName = this.level.landmark || this.city.name;

        // Top bar format: [İl Adı] (Plaka) — Mekan X/5: [Mekan Adı] — Bulmaca Y/5
        const cityLabel = document.getElementById('game-city-label');
        if (cityLabel) {
            cityLabel.innerText = `${trUpper(this.city.name)} (${plateStr}) — Mekan ${mekanNo}/5: ${landmarkName} — Bulmaca ${bulmacaNo}/5`;
        }

        const landmarkLabel = document.getElementById('game-landmark-label');
        if (landmarkLabel) landmarkLabel.innerText = landmarkName;

        const currentStars = SaveManager.getStars(cityIdx, subIdx);
        const starsLabel = document.getElementById('game-stars-label');
        if (starsLabel) {
            starsLabel.innerText = currentStars > 0 ? '★'.repeat(currentStars) + '☆'.repeat(3 - currentStars) : '⭐⭐⭐';
        }

        const bgImg = document.getElementById('game-bg-img');
        if (bgImg) {
            setupPhotoWithFallback(bgImg, this.level.bg, document.getElementById('screen-game'));
        }

        this.initLevelCommon();
    },

    loadDailyLevel(dailyLvl) {
        this.isDailyMode = true;
        this.dailyLevel = dailyLvl;
        this.level = dailyLvl;
        this.city = { name: "Günün Bulmacası", plate: 0 };

        document.getElementById('game-city-label').innerText = "GÜNLÜK BULMACA";
        const landmarkLabel = document.getElementById('game-landmark-label');
        if (landmarkLabel) landmarkLabel.innerText = "Günün Özel Meydan Okuması";
        const bgImg = document.getElementById('game-bg-img');
        if (bgImg) bgImg.src = "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=1280&q=80";

        this.initLevelCommon();
    },

    initLevelCommon() {
        this.foundWords.clear();
        this.words = this.level.words || [];
        
        // Robust wheel/letters extraction
        const rawLetters = this.level.letters || this.level.wheel || [];
        this.letters = [...rawLetters];
        
        // Reset Scoring
        this.mistakes = 0;
        this.hintsUsed = 0;
        this.difficulty = this.calculateDifficulty(this.level);
        
        this.buildCrossword();
        this.shuffleLetters();
    },

    calculateDifficulty(level) {
        const words = level.words || [];
        if (words.length === 0) return 'EASY';
        const wordCount = words.length;
        const totalLen = words.reduce((sum, w) => sum + (w.word ? w.word.length : 0), 0);
        const avgLen = totalLen / wordCount;
        
        if (wordCount <= 3 && avgLen <= 4.0) return 'EASY';
        if (wordCount >= 5 || avgLen >= 5.0) return 'HARD';
        return 'MEDIUM';
    },

    buildCrossword() {
        const container = document.getElementById('crossword-board');
        if (!container) return;
        container.innerHTML = '';
        this.gridCells = [];

        if (this.words.length === 0) return;

        let minR = Math.min(...this.words.map(w => w.row));
        let maxR = Math.max(...this.words.map(w => w.dir === 'V' ? w.row + w.word.length - 1 : w.row));
        let minC = Math.min(...this.words.map(w => w.col));
        let maxC = Math.max(...this.words.map(w => w.dir === 'H' ? w.col + w.word.length - 1 : w.col));

        const rows = maxR - minR + 1;
        const cols = maxC - minC + 1;

        // Auto-fit math for non-overflowing crossword grid
        const vp = document.getElementById('crossword-viewport');
        const availW = vp && vp.clientWidth > 0 ? (vp.clientWidth - 24) : 340;
        const availH = vp && vp.clientHeight > 0 ? (vp.clientHeight - 24) : 280;
        const gap = 5;
        const sizeW = Math.floor((availW - (cols - 1) * gap) / cols);
        const sizeH = Math.floor((availH - (rows - 1) * gap) / rows);
        let cellSize = Math.min(sizeW, sizeH, 46);
        if (cellSize < 24) cellSize = 24;

        container.style.setProperty('--cell-size', `${cellSize}px`);
        container.style.gridTemplateColumns = `repeat(${cols}, var(--cell-size, ${cellSize}px))`;
        container.style.gridTemplateRows = `repeat(${rows}, var(--cell-size, ${cellSize}px))`;
        container.style.aspectRatio = `${cols}/${rows}`;

        const totalW = cols * cellSize + (cols - 1) * gap;
        const totalH = rows * cellSize + (rows - 1) * gap;
        if (totalW > availW || totalH > availH) {
            const scale = Math.min(availW / totalW, availH / totalH);
            container.style.transform = `scale(${scale})`;
            container.style.transformOrigin = 'center center';
        } else {
            container.style.transform = 'none';
        }

        const gridMap = {};
        this.words.forEach(w => {
            for (let i = 0; i < w.word.length; i++) {
                const r = w.row - minR + (w.dir === 'V' ? i : 0);
                const c = w.col - minC + (w.dir === 'H' ? i : 0);
                gridMap[`${r},${c}`] = w.word[i];
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
        const labels = document.getElementById('wheel-letters-container');
        if (!labels) return;
        labels.innerHTML = '';
        
        const count = this.letters.length;
        if (count === 0) return;
        
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
        if (asm) {
            asm.onpointerdown = this.handleDown.bind(this);
            asm.onpointermove = this.handleMove.bind(this);
            asm.onpointerup = this.handleUp.bind(this);
            asm.onpointercancel = this.handleUp.bind(this);
        }
    },

    handleDown(e) {
        if (e.target && e.target.classList.contains('letter-node')) {
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
                const node = document.querySelector(`.letter-node[data-idx="${popped}"]`);
                if (node) node.classList.remove('selected');
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
        if (!poly) return;
        if (this.selectedIndices.length === 0) {
            poly.setAttribute('points', '');
            return;
        }
        let pts = [];
        this.selectedIndices.forEach(idx => {
            const el = document.querySelector(`.letter-node[data-idx="${idx}"]`);
            if (el) pts.push(`${el.dataset.x},${el.dataset.y}`);
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
        if (!pill) return;
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
            if (pill) {
                pill.style.background = 'rgba(220, 38, 38, 0.95)';
                pill.classList.add('active');
                setTimeout(() => pill.classList.remove('active'), 500);
            }

            // Bonus word check in TDK dictionary
            if (typeof TDK_DICT_FULL !== 'undefined' && TDK_DICT_FULL.includes(word)) {
                SaveManager.data.bonusChest = (SaveManager.data.bonusChest || 0) + 1;
                if (SaveManager.data.bonusChest >= 5) {
                    SaveManager.data.bonusChest = 0;
                    SaveManager.addCoins(30);
                    AudioEngine.playVictory();
                }
                SaveManager.save();
                const bonusEl = document.getElementById('bonus-chest-text');
                if (bonusEl) bonusEl.innerText = `${SaveManager.data.bonusChest}/5`;
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

    

    checkWinCondition() {
        if (this.foundWords.size === this.words.length) {
            AudioEngine.playVictory();
            
            if (this.isDailyMode) {
                // Daily Challenge win
                const todayStr = new Date().toISOString().split('T')[0];
                const streak = SaveManager.recordDailyCompletion(todayStr, 50);
                
                document.getElementById('post-landmark-title').innerText = "GÜNLÜK BULMACA TAMAMLANDI!";
                document.getElementById('post-story-text').innerText = `Tebrikler! Günün bulmacasını başarıyla çözdün.\nSerin: ${streak} Gün! (+50 Altın)`;
                document.getElementById('post-photo-img').src = "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=1280&q=80";
                
                
                
                App.showModal('modal-postcard');
                return;
            }
            
            // Regular Level win
            const stars = 3;
            let baseReward = 20;
            if (this.difficulty === 'MEDIUM') baseReward = 30;
            if (this.difficulty === 'HARD') baseReward = 50;
            
            const finalReward = baseReward + (stars * 5);
            SaveManager.addCoins(finalReward);
            
            const subIdx = SaveManager.data.currentSubLevel;
            SaveManager.saveStar(SaveManager.data.currentCityIdx, subIdx, stars);

            const isCityCompleted = (subIdx === 24 || subIdx >= (this.city.levels.length - 1));

            if (isCityCompleted) {
                // Major City Completion: 25/25 puzzles solved!
                SaveManager.addCoins(100);
                if (!SaveManager.data.completedProvinces.includes(this.city.plate)) {
                    SaveManager.data.completedProvinces.push(this.city.plate);
                }
                SaveManager.save();

                const compTitle = document.getElementById('completed-city-title');
                if (compTitle) compTitle.innerText = `${trUpper(this.city.name)} TAMAMLANDI!`;

                const compImg = document.getElementById('completed-city-img');
                if (compImg) {
                    setupPhotoWithFallback(compImg, this.level.bg, document.querySelector('#modal-city-completed .postcard-photo-frame'));
                }

                const compStory = document.getElementById('completed-city-story');
                if (compStory) {
                    compStory.innerHTML = `Tebrikler! <strong>${this.city.name}</strong> ilimizin 5 simgesel mekanındaki 25 bulmacayı başarıyla çözdün ve altın zafer mührünü kazandın!`;
                }

                App.showModal('modal-city-completed');
                return;
            }
            
            // Show Normal Postcard for sub-levels (1-24)
            const pc = this.level.postcard || {
                landmark: this.level.landmark || this.city.name,
                desc: `${this.city.name} ilimizin eşsiz güzelliklerini başarıyla keşfettin!`,
                bg: this.level.bg
            };
            document.getElementById('post-landmark-title').innerText = pc.landmark || this.city.name;
            document.getElementById('post-story-text').innerText = pc.desc || '';
            const pcPhoto = document.getElementById('post-photo-img');
            if (pcPhoto) {
                setupPhotoWithFallback(pcPhoto, pc.bg || this.level.bg, document.querySelector('#modal-postcard .postcard-photo-frame'));
            }
            
            // Render stars
            
            
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
            this.gridCells.forEach(c => c.el.classList.remove('target-mode'));
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
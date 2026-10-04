// Words of Wonders (WoW) Studio Engine - 100 TDK Levels
class WoWGame {
  constructor() {
    this.storageKey = 'wow_tr_save_v2';
    this.secretSalt = 'wow_pure_tdk_2026';

    // State
    this.state = this.loadSecureState();
    this.currentWord = "";
    this.selectedNodes = [];
    this.isDragging = false;
    this.isHammerMode = false;

    // Crossword Grid Tracking
    this.cellMap = new Map(); // "r,c" => { el, char, words: [wId], revealed: bool }
    this.solvedWords = new Set();
    this.bonusWordsFound = new Set();

    // DOM Elements
    this.boardEl = document.getElementById('crossword-board');
    this.letterWheel = document.getElementById('letter-wheel');
    this.wheelSvg = document.getElementById('wheel-lines');
    this.wordPreview = document.getElementById('current-word-preview');
    this.levelDisplay = document.getElementById('level-display');
    this.locationBadge = document.getElementById('location-badge');
    this.coinCount = document.getElementById('coin-count');
    this.jarCountEl = document.getElementById('jar-count');
    this.jarModalCountEl = document.getElementById('jar-modal-count');

    // Modals
    this.modalVictory = document.getElementById('modal-victory');
    this.modalShop = document.getElementById('modal-shop');
    this.modalJar = document.getElementById('modal-jar');
    this.modalQr = document.getElementById('modal-qr');

    // Confetti
    this.canvas = document.getElementById('confetti-canvas');
    this.ctx = this.canvas.getContext('2d');
    this.confettiParticles = [];

    this.init();
  }

  loadSecureState() {
    const raw = localStorage.getItem(this.storageKey);
    const defaultState = {
      levelIndex: 0,
      coins: 120,
      jarCount: 0,
      noAds: false
    };

    if (!raw) return defaultState;

    try {
      const data = JSON.parse(raw);
      const computedHash = this.computeHash(data.levelIndex, data.coins, data.jarCount);
      if (data.checksum !== computedHash) {
        return defaultState;
      }
      return {
        levelIndex: Math.max(0, data.levelIndex || 0),
        coins: Math.max(0, data.coins || 120),
        jarCount: Math.max(0, data.jarCount || 0),
        noAds: !!data.noAds
      };
    } catch (e) {
      return defaultState;
    }
  }

  saveSecureState() {
    const checksum = this.computeHash(this.state.levelIndex, this.state.coins, this.state.jarCount);
    const payload = {
      ...this.state,
      checksum: checksum
    };
    localStorage.setItem(this.storageKey, JSON.stringify(payload));
    this.coinCount.textContent = this.state.coins;
    this.jarCountEl.textContent = `${this.state.jarCount}/5`;
    this.jarModalCountEl.textContent = `${this.state.jarCount} / 5 Kelime`;
  }

  computeHash(lvl, coins, jar) {
    const str = `${lvl}-${coins}-${jar}-${this.secretSalt}`;
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = (hash << 5) - hash + str.charCodeAt(i);
      hash |= 0;
    }
    return hash.toString(36);
  }

  init() {
    this.setupWindowResize();
    this.setupEventListeners();
    this.loadLevel(this.state.levelIndex);
    this.saveSecureState();
  }

  setupWindowResize() {
    const resize = () => {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
      this.adjustCrosswordScale();
    };
    window.addEventListener('resize', resize);
    resize();
  }

  setupEventListeners() {
    // Sound
    document.getElementById('btn-sound').addEventListener('click', () => {
      const isMuted = !window.soundFX.toggle();
      const soundBtn = document.getElementById('btn-sound');
      soundBtn.style.opacity = isMuted ? '0.4' : '1';
    });

    // QR Phone Share Modal
    document.getElementById('btn-qr').addEventListener('click', () => this.openModal(this.modalQr));
    document.getElementById('btn-close-qr').addEventListener('click', () => this.closeModal(this.modalQr));
    document.getElementById('btn-copy-url').addEventListener('click', () => {
      const input = document.getElementById('mobile-url-input');
      navigator.clipboard.writeText(input.value);
      this.flashToast("Bağlantı kopyalandı! Ailenize gönderebilirsiniz.");
    });

    // Shop
    document.getElementById('btn-shop').addEventListener('click', () => this.openModal(this.modalShop));
    document.getElementById('btn-close-shop').addEventListener('click', () => this.closeModal(this.modalShop));

    // Bonus Jar
    document.getElementById('btn-bonus-jar').addEventListener('click', () => this.openJarModal());
    document.getElementById('btn-close-jar').addEventListener('click', () => this.closeModal(this.modalJar));
    document.getElementById('btn-claim-jar').addEventListener('click', () => this.claimJar());

    // Powerups
    document.getElementById('btn-shuffle').addEventListener('click', () => this.shuffleWheel());
    document.getElementById('btn-hint').addEventListener('click', () => this.useRandomHint());
    document.getElementById('btn-magic-hint').addEventListener('click', () => this.toggleHammerMode());

    // Victory
    document.getElementById('btn-next-level').addEventListener('click', () => this.nextLevel());
    document.getElementById('btn-share').addEventListener('click', () => this.shareScore());

    // Pointer Drag on Letter Turntable
    this.letterWheel.addEventListener('pointerdown', (e) => this.onPointerDown(e));
    window.addEventListener('pointermove', (e) => this.onPointerMove(e));
    window.addEventListener('pointerup', () => this.onPointerUp());
    window.addEventListener('pointercancel', () => this.onPointerUp());
  }

  getCurrentLevel() {
    return WOW_LEVELS[this.state.levelIndex % WOW_LEVELS.length];
  }

  loadLevel(index) {
    this.state.levelIndex = index;
    this.saveSecureState();

    const level = this.getCurrentLevel();
    this.levelDisplay.textContent = level.level;
    this.locationBadge.textContent = level.location;
    document.body.className = `theme-${level.bgTheme || 'cappadocia'}`;

    this.solvedWords.clear();
    this.bonusWordsFound.clear();
    this.cellMap.clear();
    this.closeModal(this.modalVictory);
    this.setHammerMode(false);

    // 1. Grid Bounding Box
    let maxR = 0, maxC = 0;
    level.words.forEach(w => {
      const endR = w.dir === 'V' ? w.row + w.word.length - 1 : w.row;
      const endC = w.dir === 'H' ? w.col + w.word.length - 1 : w.col;
      if (endR > maxR) maxR = endR;
      if (endC > maxC) maxC = endC;
    });

    const rows = maxR + 1;
    const cols = maxC + 1;

    // Responsive cell calculation (Compact & Centered)
    const availableW = Math.min(window.innerWidth - 32, 380);
    const availableH = Math.min(window.innerHeight * 0.38, 300);
    const cellSize = Math.min(48, Math.floor(Math.min(availableW / (cols + 0.3), availableH / (rows + 0.3))));

    this.boardEl.style.setProperty('--tile-size', `${cellSize}px`);
    this.boardEl.style.gridTemplateColumns = `repeat(${cols}, ${cellSize}px)`;
    this.boardEl.style.gridTemplateRows = `repeat(${rows}, ${cellSize}px)`;
    this.boardEl.innerHTML = '';

    // 2. Map coordinates
    const gridData = {};
    level.words.forEach(wObj => {
      for (let i = 0; i < wObj.word.length; i++) {
        const r = wObj.dir === 'V' ? wObj.row + i : wObj.row;
        const c = wObj.dir === 'H' ? wObj.col + i : wObj.col;
        const key = `${r},${c}`;
        if (!gridData[key]) {
          gridData[key] = { char: wObj.word[i], wordIds: [wObj.id] };
        } else {
          gridData[key].wordIds.push(wObj.id);
        }
      }
    });

    // 3. Render 2D Matrix
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const key = `${r},${c}`;
        const cell = document.createElement('div');
        cell.className = 'cw-cell';
        cell.dataset.r = r;
        cell.dataset.c = c;

        if (gridData[key]) {
          cell.classList.add('slot');
          cell.dataset.char = gridData[key].char;
          cell.addEventListener('click', () => this.onCellClick(r, c));

          this.cellMap.set(key, {
            el: cell,
            char: gridData[key].char,
            wordIds: gridData[key].wordIds,
            revealed: false
          });
        } else {
          cell.classList.add('empty');
        }

        this.boardEl.appendChild(cell);
      }
    }

    // 4. Render Letter Nodes
    this.renderWheel(level.wheelLetters);
  }

  adjustCrosswordScale() {
    const level = this.getCurrentLevel();
    if (!level) return;
    let maxR = 0, maxC = 0;
    level.words.forEach(w => {
      const endR = w.dir === 'V' ? w.row + w.word.length - 1 : w.row;
      const endC = w.dir === 'H' ? w.col + w.word.length - 1 : w.col;
      if (endR > maxR) maxR = endR;
      if (endC > maxC) maxC = endC;
    });
    const rows = maxR + 1;
    const cols = maxC + 1;
    const availableW = Math.min(window.innerWidth - 32, 380);
    const availableH = Math.min(window.innerHeight * 0.38, 300);
    const cellSize = Math.min(48, Math.floor(Math.min(availableW / (cols + 0.3), availableH / (rows + 0.3))));
    this.boardEl.style.setProperty('--tile-size', `${cellSize}px`);
    this.boardEl.style.gridTemplateColumns = `repeat(${cols}, ${cellSize}px)`;
    this.boardEl.style.gridTemplateRows = `repeat(${rows}, ${cellSize}px)`;
  }

  renderWheel(letters) {
    this.letterWheel.innerHTML = '';
    this.wheelSvg.innerHTML = '';
    const radius = 78;
    const center = 118;
    const total = letters.length;

    letters.forEach((char, i) => {
      const angle = (i * (360 / total) - 90) * (Math.PI / 180);
      const x = center + radius * Math.cos(angle);
      const y = center + radius * Math.sin(angle);

      const node = document.createElement('div');
      node.className = 'letter-node';
      node.textContent = char;
      node.dataset.char = char;
      node.style.left = `${x}px`;
      node.style.top = `${y}px`;

      this.letterWheel.appendChild(node);
    });
  }

  shuffleWheel() {
    const level = this.getCurrentLevel();
    const shuffled = [...level.wheelLetters].sort(() => Math.random() - 0.5);
    window.soundFX.playLetterSelect(2);
    this.renderWheel(shuffled);
  }

  // POINTER & TOUCH HANDLING
  onPointerDown(e) {
    const node = this.getNodeUnderPointer(e.clientX, e.clientY);
    if (node) {
      this.isDragging = true;
      this.selectedNodes = [node];
      this.currentWord = node.dataset.char;
      node.classList.add('selected');

      window.soundFX.playLetterSelect(0);
      if (navigator.vibrate) navigator.vibrate(12);

      this.updatePreview();
      this.updateWheelLines(e.clientX, e.clientY);
    }
  }

  onPointerMove(e) {
    if (!this.isDragging) return;

    const node = this.getNodeUnderPointer(e.clientX, e.clientY);
    if (node && !this.selectedNodes.includes(node)) {
      this.selectedNodes.push(node);
      this.currentWord += node.dataset.char;
      node.classList.add('selected');

      window.soundFX.playLetterSelect(this.selectedNodes.length - 1);
      if (navigator.vibrate) navigator.vibrate(12);

      this.updatePreview();
    }

    this.updateWheelLines(e.clientX, e.clientY);
  }

  onPointerUp() {
    if (!this.isDragging) return;
    this.isDragging = false;

    this.validateWord(this.currentWord);

    this.selectedNodes.forEach(node => node.classList.remove('selected'));
    this.selectedNodes = [];
    this.currentWord = "";
    this.wheelSvg.innerHTML = '';
    this.wordPreview.classList.remove('active');
    this.wordPreview.textContent = "";
  }

  getNodeUnderPointer(clientX, clientY) {
    const nodes = this.letterWheel.querySelectorAll('.letter-node');
    for (let node of nodes) {
      const rect = node.getBoundingClientRect();
      const radius = rect.width / 2;
      const centerX = rect.left + radius;
      const centerY = rect.top + radius;
      if (Math.hypot(clientX - centerX, clientY - centerY) <= radius + 8) {
        return node;
      }
    }
    return null;
  }

  updateWheelLines(pointerX, pointerY) {
    this.wheelSvg.innerHTML = '';
    if (this.selectedNodes.length === 0) return;

    const wheelRect = this.letterWheel.getBoundingClientRect();

    for (let i = 0; i < this.selectedNodes.length - 1; i++) {
      const fromRect = this.selectedNodes[i].getBoundingClientRect();
      const toRect = this.selectedNodes[i + 1].getBoundingClientRect();

      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', fromRect.left + fromRect.width / 2 - wheelRect.left);
      line.setAttribute('y1', fromRect.top + fromRect.height / 2 - wheelRect.top);
      line.setAttribute('x2', toRect.left + toRect.width / 2 - wheelRect.left);
      line.setAttribute('y2', toRect.top + toRect.height / 2 - wheelRect.top);
      this.wheelSvg.appendChild(line);
    }

    if (this.isDragging && pointerX !== undefined && pointerY !== undefined) {
      const lastRect = this.selectedNodes[this.selectedNodes.length - 1].getBoundingClientRect();
      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', lastRect.left + lastRect.width / 2 - wheelRect.left);
      line.setAttribute('y1', lastRect.top + lastRect.height / 2 - wheelRect.top);
      line.setAttribute('x2', pointerX - wheelRect.left);
      line.setAttribute('y2', pointerY - wheelRect.top);
      this.wheelSvg.appendChild(line);
    }
  }

  updatePreview() {
    if (this.currentWord.length > 0) {
      this.wordPreview.textContent = this.currentWord;
      this.wordPreview.classList.add('active');
    } else {
      this.wordPreview.classList.remove('active');
    }
  }

  // TDK KELİME KONTROLÜ
  validateWord(word) {
    const level = this.getCurrentLevel();
    const matchedWordObj = level.words.find(w => w.word === word);

    if (matchedWordObj) {
      if (this.solvedWords.has(matchedWordObj.id)) {
        this.flashToast("Bu kelimeyi zaten buldun!");
        window.soundFX.playInvalid();
        return;
      }

      this.solvedWords.add(matchedWordObj.id);
      this.revealWordOnCrossword(matchedWordObj);
      window.soundFX.playWordSuccess();

      if (this.solvedWords.size === level.words.length) {
        setTimeout(() => this.triggerVictory(), 500);
      }
    } else if (level.bonusWords && level.bonusWords.includes(word)) {
      if (this.bonusWordsFound.has(word)) {
        this.flashToast("Bu bonus kelimeyi zaten kavanoza koydun!");
      } else {
        this.bonusWordsFound.add(word);
        this.addBonusToJar(word);
      }
    } else {
      if (word.length >= 2) window.soundFX.playInvalid();
    }
  }

  revealWordOnCrossword(wordObj) {
    for (let i = 0; i < wordObj.word.length; i++) {
      const r = wordObj.dir === 'V' ? wordObj.row + i : wordObj.row;
      const c = wordObj.dir === 'H' ? wordObj.col + i : wordObj.col;
      const key = `${r},${c}`;
      const cellData = this.cellMap.get(key);

      if (cellData) {
        setTimeout(() => {
          cellData.revealed = true;
          cellData.el.textContent = cellData.char;
          cellData.el.classList.add('revealed');
        }, i * 65);
      }
    }
  }

  // BONUS JAR
  addBonusToJar(word) {
    window.soundFX.playJarPop();
    this.state.jarCount = Math.min(5, this.state.jarCount + 1);
    this.saveSecureState();

    this.flashToast(`🏺 "${word}" Kavanoza Girdi! (${this.state.jarCount}/5)`);

    if (this.state.jarCount >= 5) {
      setTimeout(() => this.openJarModal(), 400);
    }
  }

  openJarModal() {
    const claimBtn = document.getElementById('btn-claim-jar');
    claimBtn.disabled = this.state.jarCount < 5;
    this.openModal(this.modalJar);
  }

  claimJar() {
    if (this.state.jarCount >= 5) {
      this.state.jarCount = 0;
      this.state.coins += 30;
      this.saveSecureState();
      window.soundFX.playCoinCollect();
      this.closeModal(this.modalJar);
      this.flashToast("🏺 Kavanoz açıldı: +30 Altın Kazandın! 🪙");
    }
  }

  // HINTS & HAMMER
  useRandomHint() {
    const cost = 25;
    if (this.state.coins < cost) {
      this.openModal(this.modalShop);
      this.flashToast("Yetersiz Altın! Mağazadan altın alabilirsin.");
      return;
    }

    const unrevealed = [];
    this.cellMap.forEach((val) => {
      if (!val.revealed) unrevealed.push(val);
    });

    if (unrevealed.length === 0) {
      this.flashToast("Açılacak harf kalmadı!");
      return;
    }

    const chosen = unrevealed[Math.floor(Math.random() * unrevealed.length)];
    this.revealSingleCell(chosen);

    this.state.coins -= cost;
    this.saveSecureState();
    window.soundFX.playCoinCollect();
  }

  toggleHammerMode() {
    const cost = 50;
    if (this.state.coins < cost && !this.isHammerMode) {
      this.openModal(this.modalShop);
      this.flashToast("Sihirli Çekiç için 50 Altın gerekli!");
      return;
    }
    this.setHammerMode(!this.isHammerMode);
  }

  setHammerMode(active) {
    this.isHammerMode = active;
    const btn = document.getElementById('btn-magic-hint');
    btn.classList.toggle('active-hammer', active);

    this.cellMap.forEach(cell => {
      if (!cell.revealed) {
        cell.el.classList.toggle('hammer-target', active);
      }
    });

    if (active) {
      this.flashToast("🔨 İstediğin bir kareye tıkla!");
    }
  }

  onCellClick(r, c) {
    if (!this.isHammerMode) return;

    const key = `${r},${c}`;
    const cell = this.cellMap.get(key);
    if (cell && !cell.revealed) {
      window.soundFX.playHammer();
      this.state.coins -= 50;
      this.saveSecureState();
      this.revealSingleCell(cell);
      this.setHammerMode(false);
    }
  }

  revealSingleCell(cellData) {
    cellData.revealed = true;
    cellData.el.textContent = cellData.char;
    cellData.el.classList.add('revealed');
    cellData.el.classList.remove('hammer-target');

    const level = this.getCurrentLevel();
    level.words.forEach(wObj => {
      if (!this.solvedWords.has(wObj.id)) {
        let allRevealed = true;
        for (let i = 0; i < wObj.word.length; i++) {
          const r = wObj.dir === 'V' ? wObj.row + i : wObj.row;
          const c = wObj.dir === 'H' ? wObj.col + i : wObj.col;
          const data = this.cellMap.get(`${r},${c}`);
          if (!data || !data.revealed) {
            allRevealed = false;
            break;
          }
        }
        if (allRevealed) {
          this.solvedWords.add(wObj.id);
        }
      }
    });

    if (this.solvedWords.size === level.words.length) {
      setTimeout(() => this.triggerVictory(), 500);
    }
  }

  fakePurchase(name, price, coins = 0) {
    if (coins > 0) this.state.coins += coins;
    else this.state.noAds = true;
    this.saveSecureState();
    window.soundFX.playCoinCollect();
    this.flashToast(`${name} başarıyla satın alındı!`);
    this.closeModal(this.modalShop);
  }

  triggerVictory() {
    window.soundFX.playLevelComplete();
    this.startConfetti();
    this.state.coins += 30;
    this.saveSecureState();

    const level = this.getCurrentLevel();
    document.getElementById('victory-title').textContent = `${level.location} - Bölüm ${level.level}`;
    this.openModal(this.modalVictory);
  }

  nextLevel() {
    this.stopConfetti();
    this.loadLevel(this.state.levelIndex + 1);
  }

  shareScore() {
    const lvl = this.getCurrentLevel();
    const text = `🏆 Kelime Harikaları'nda ${lvl.location} (Bölüm ${lvl.level}/100) çengel bulmacasını bitirdim! Hadi sen de dene: http://10.35.240.87:8080`;
    if (navigator.share) {
      navigator.share({ title: 'Kelime Harikaları', text });
    } else {
      navigator.clipboard.writeText(text);
      this.flashToast("Meydan okuma panoya kopyalandı!");
    }
  }

  openModal(el) {
    el.classList.remove('hidden');
  }

  closeModal(el) {
    el.classList.add('hidden');
  }

  flashToast(msg) {
    let toast = document.getElementById('ka-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'ka-toast';
      toast.style.cssText = `
        position: fixed;
        top: 24px;
        left: 50%;
        transform: translateX(-50%);
        background: #0f172a;
        color: #fff;
        padding: 10px 22px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 13px;
        z-index: 9999;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.2);
      `;
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.style.display = 'block';

    clearTimeout(this.toastTimeout);
    this.toastTimeout = setTimeout(() => {
      toast.style.display = 'none';
    }, 2400);
  }

  startConfetti() {
    this.confettiParticles = [];
    const colors = ['#f59e0b', '#fbbf24', '#10b981', '#3b82f6', '#ffffff'];
    for (let i = 0; i < 85; i++) {
      this.confettiParticles.push({
        x: this.canvas.width / 2,
        y: this.canvas.height / 2,
        vx: (Math.random() - 0.5) * 12,
        vy: (Math.random() - 0.7) * 14,
        size: Math.random() * 8 + 4,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: Math.random() * 360,
        rSpeed: (Math.random() - 0.5) * 10,
        gravity: 0.28
      });
    }

    const render = () => {
      if (this.confettiParticles.length === 0) return;
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

      this.confettiParticles.forEach((p, idx) => {
        p.vy += p.gravity;
        p.x += p.vx;
        p.y += p.vy;
        p.rotation += p.rSpeed;

        this.ctx.save();
        this.ctx.translate(p.x, p.y);
        this.ctx.rotate((p.rotation * Math.PI) / 180);
        this.ctx.fillStyle = p.color;
        this.ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
        this.ctx.restore();

        if (p.y > this.canvas.height + 20) {
          this.confettiParticles.splice(idx, 1);
        }
      });

      this.confettiAnimId = requestAnimationFrame(render);
    };

    render();
  }

  stopConfetti() {
    if (this.confettiAnimId) cancelAnimationFrame(this.confettiAnimId);
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.confettiParticles = [];
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.game = new WoWGame();
});

// Kelime Harikaları - 100 Doğrulanmış TDK Seviyeli Kelime Oyunu Motoru
class WoWGame {
  constructor() {
    this.storageKey = 'kelime_harikalari_save_v1';
    this.secretSalt = 'kelime_harikalari_tdk_100';

    this.state = this.loadSecureState();
    this.currentWord = "";
    this.selectedNodes = [];
    this.isDragging = false;

    // Game Board State
    this.solvedWords = new Set();
    this.bonusWordsFound = new Set();

    // Screens
    this.screenHome = document.getElementById('screen-home');
    this.screenGame = document.getElementById('screen-game');

    // Home Elements
    this.homeLoc = document.getElementById('home-current-loc');
    this.homeLvl = document.getElementById('home-current-lvl');
    this.homeCoins = document.getElementById('home-coins');

    // Game Elements
    this.boardEl = document.getElementById('word-board');
    this.letterWheel = document.getElementById('letter-wheel');
    this.wheelSvg = document.getElementById('wheel-lines');
    this.wordPreview = document.getElementById('current-word-preview');
    this.levelDisplay = document.getElementById('level-display');
    this.locationBadge = document.getElementById('location-badge');
    this.coinCount = document.getElementById('coin-count');

    // Modals
    this.modalVictory = document.getElementById('modal-victory');
    this.modalShop = document.getElementById('modal-shop');
    this.modalMap = document.getElementById('modal-map');
    this.regionsGrid = document.getElementById('regions-grid');

    // Confetti Canvas
    this.canvas = document.getElementById('confetti-canvas');
    this.ctx = this.canvas.getContext('2d');
    this.confettiParticles = [];

    this.init();
  }

  loadSecureState() {
    const raw = localStorage.getItem(this.storageKey);
    const defaultState = {
      levelIndex: 0,
      coins: 100,
      noAds: false
    };

    if (!raw) return defaultState;

    try {
      const data = JSON.parse(raw);
      const computedHash = this.computeHash(data.levelIndex, data.coins);
      if (data.checksum !== computedHash) return defaultState;
      return {
        levelIndex: Math.max(0, data.levelIndex || 0),
        coins: Math.max(0, data.coins || 100),
        noAds: !!data.noAds
      };
    } catch (e) {
      return defaultState;
    }
  }

  saveSecureState() {
    const checksum = this.computeHash(this.state.levelIndex, this.state.coins);
    localStorage.setItem(this.storageKey, JSON.stringify({
      ...this.state,
      checksum
    }));
    if (this.coinCount) this.coinCount.textContent = this.state.coins;
    if (this.homeCoins) this.homeCoins.textContent = this.state.coins;

    const currentLvl = this.getCurrentLevel();
    if (currentLvl) {
      if (this.homeLoc) this.homeLoc.textContent = currentLvl.location.split(' - ')[0];
      if (this.homeLvl) this.homeLvl.textContent = `Bölüm ${currentLvl.level} / 100`;
    }
  }

  computeHash(lvl, coins) {
    const str = `${lvl}-${coins}-${this.secretSalt}`;
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
    this.renderRegionsMap();
    this.saveSecureState();
  }

  setupWindowResize() {
    const resize = () => {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
      this.adjustBoardScale();
    };
    window.addEventListener('resize', resize);
    resize();
  }

  setupEventListeners() {
    // Screen Navigation
    document.getElementById('btn-home-play').addEventListener('click', () => {
      this.showScreen('game');
      this.loadLevel(this.state.levelIndex);
    });

    document.getElementById('btn-back-home').addEventListener('click', () => {
      this.showScreen('home');
      this.saveSecureState();
    });

    // Level Map Modal
    document.getElementById('btn-home-map').addEventListener('click', () => this.openModal(this.modalMap));
    document.getElementById('btn-level-pill').addEventListener('click', () => this.openModal(this.modalMap));
    document.getElementById('btn-close-map').addEventListener('click', () => this.closeModal(this.modalMap));

    // Sound Toggle
    document.getElementById('btn-sound').addEventListener('click', (e) => {
      const isMuted = !window.soundFX.toggle();
      e.target.textContent = isMuted ? '🔇' : '🔊';
      e.target.style.opacity = isMuted ? '0.5' : '1';
    });

    // Shop
    document.getElementById('btn-shop').addEventListener('click', () => this.openModal(this.modalShop));
    document.getElementById('btn-close-shop').addEventListener('click', () => this.closeModal(this.modalShop));

    // Controls
    document.getElementById('btn-shuffle').addEventListener('click', () => this.shuffleWheel());
    document.getElementById('btn-hint').addEventListener('click', () => this.useRandomHint());

    // Victory
    document.getElementById('btn-next-level').addEventListener('click', () => this.nextLevel());
    document.getElementById('btn-share').addEventListener('click', () => this.shareScore());

    // Letter Wheel Gestures (Mouse & Touch)
    this.letterWheel.addEventListener('pointerdown', (e) => this.onPointerDown(e));
    window.addEventListener('pointermove', (e) => this.onPointerMove(e));
    window.addEventListener('pointerup', () => this.onPointerUp());
    window.addEventListener('pointercancel', () => this.onPointerUp());
  }

  showScreen(name) {
    if (name === 'game') {
      this.screenHome.classList.add('hidden');
      this.screenGame.classList.remove('hidden');
    } else {
      this.screenGame.classList.add('hidden');
      this.screenHome.classList.remove('hidden');
    }
  }

  getCurrentLevel() {
    return WOW_LEVELS[this.state.levelIndex % WOW_LEVELS.length];
  }

  renderRegionsMap() {
    const regions = [
      { name: "Kapadokya - Peri Bacaları", startLvl: 1 },
      { name: "Pamukkale - Travertenler", startLvl: 11 },
      { name: "Galata Kulesi - İstanbul", startLvl: 21 },
      { name: "Nemrut Dağı - Gün Doğumu", startLvl: 31 },
      { name: "Efes Antik Kenti - İzmir", startLvl: 41 },
      { name: "Göbeklitepe - Şanlıurfa", startLvl: 51 },
      { name: "Ölüdeniz - Fethiye", startLvl: 61 },
      { name: "Sümela Manastırı - Trabzon", startLvl: 71 },
      { name: "Safranbolu Evleri - Karabük", startLvl: 81 },
      { name: "Akdamar Adası - Van Gölü", startLvl: 91 },
    ];

    this.regionsGrid.innerHTML = '';
    regions.forEach((reg) => {
      const btn = document.createElement('div');
      btn.className = 'region-item-btn';
      if (this.state.levelIndex >= reg.startLvl - 1 && this.state.levelIndex < reg.startLvl + 9) {
        btn.classList.add('active');
      }

      btn.innerHTML = `
        <div class="region-item-left">
          <span class="region-item-name">${reg.name}</span>
          <span class="region-item-range">Bölüm ${reg.startLvl} - ${reg.startLvl + 9}</span>
        </div>
        <span class="region-item-status">Oyna ➔</span>
      `;

      btn.addEventListener('click', () => {
        this.closeModal(this.modalMap);
        this.showScreen('game');
        this.loadLevel(reg.startLvl - 1);
      });

      this.regionsGrid.appendChild(btn);
    });
  }

  loadLevel(index) {
    this.state.levelIndex = index;
    this.saveSecureState();

    const level = this.getCurrentLevel();
    this.levelDisplay.textContent = level.level;
    this.locationBadge.textContent = level.location.split(' - ')[0].toUpperCase();
    document.body.className = `theme-${level.bgTheme || 'cappadocia'}`;

    this.solvedWords.clear();
    this.bonusWordsFound.clear();
    this.closeModal(this.modalVictory);

    this.adjustBoardScale();
    this.boardEl.innerHTML = '';

    // Render target word rows
    level.targetWords.forEach(word => {
      const row = document.createElement('div');
      row.className = 'word-row';
      row.dataset.word = word;

      for (let i = 0; i < word.length; i++) {
        const slot = document.createElement('div');
        slot.className = 'letter-slot';
        slot.dataset.char = word[i];
        row.appendChild(slot);
      }

      this.boardEl.appendChild(row);
    });

    this.renderWheel(level.wheelLetters);
    this.renderRegionsMap();
  }

  adjustBoardScale() {
    const level = this.getCurrentLevel();
    if (!level || !this.boardEl) return;

    const maxLen = Math.max(...level.targetWords.map(w => w.length));
    const availW = Math.min(window.innerWidth - 32, 380);
    const slotSize = Math.min(46, Math.floor((availW - (maxLen - 1) * 6) / maxLen));
    const fontSize = Math.max(16, Math.floor(slotSize * 0.54));

    this.boardEl.style.setProperty('--slot-size', `${slotSize}px`);
    this.boardEl.style.setProperty('--slot-font-size', `${fontSize}px`);
  }

  renderWheel(letters) {
    this.letterWheel.innerHTML = '';
    this.wheelSvg.innerHTML = '';
    const total = letters.length;

    let radius = 76;
    let nodeSize = 54;
    let fontSize = 26;

    if (total === 6) {
      radius = 78;
      nodeSize = 48;
      fontSize = 23;
    } else if (total === 7) {
      radius = 80;
      nodeSize = 44;
      fontSize = 21;
    } else if (total >= 8) {
      radius = 82;
      nodeSize = 38;
      fontSize = 18;
    }

    this.letterWheel.style.setProperty('--node-size', `${nodeSize}px`);
    this.letterWheel.style.setProperty('--node-font-size', `${fontSize}px`);

    const center = 115; // center of 230x230 turntable

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

  onPointerDown(e) {
    const node = this.getNodeUnderPointer(e.clientX, e.clientY);
    if (node) {
      this.isDragging = true;
      this.selectedNodes = [node];
      this.currentWord = node.dataset.char;
      node.classList.add('selected');

      window.soundFX.playLetterSelect(0);
      if (navigator.vibrate) navigator.vibrate(10);

      this.updatePreview();
      this.updateWheelLines(e.clientX, e.clientY);
    }
  }

  onPointerMove(e) {
    if (!this.isDragging) return;

    const node = this.getNodeUnderPointer(e.clientX, e.clientY);
    if (node) {
      // Backtrack support: sliding finger back to previous letter unselects the last letter
      if (this.selectedNodes.length >= 2 && node === this.selectedNodes[this.selectedNodes.length - 2]) {
        const popped = this.selectedNodes.pop();
        popped.classList.remove('selected');
        this.currentWord = this.selectedNodes.map(n => n.dataset.char).join('');
        window.soundFX.playLetterSelect(this.selectedNodes.length - 1);
        if (navigator.vibrate) navigator.vibrate(8);
        this.updatePreview();
      } else if (!this.selectedNodes.includes(node)) {
        this.selectedNodes.push(node);
        this.currentWord += node.dataset.char;
        node.classList.add('selected');

        window.soundFX.playLetterSelect(this.selectedNodes.length - 1);
        if (navigator.vibrate) navigator.vibrate(10);
        this.updatePreview();
      }
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
      if (Math.hypot(clientX - centerX, clientY - centerY) <= radius + 10) {
        return node;
      }
    }
    return null;
  }

  updateWheelLines(pointerX, pointerY) {
    this.wheelSvg.innerHTML = '';
    if (this.selectedNodes.length === 0) return;

    const wheelRect = this.letterWheel.getBoundingClientRect();

    // Connecting lines between letter nodes (rendered UNDER letter nodes)
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

    // Trailing line to touch/mouse pointer
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

  validateWord(word) {
    if (!word || word.length < 2) return;
    const level = this.getCurrentLevel();

    if (level.targetWords.includes(word)) {
      if (this.solvedWords.has(word)) {
        this.flashToast("Bu kelimeyi zaten buldun!");
        window.soundFX.playInvalid();
        return;
      }

      this.solvedWords.add(word);
      this.revealWordOnBoard(word);
      window.soundFX.playWordSuccess();

      if (this.solvedWords.size === level.targetWords.length) {
        setTimeout(() => this.triggerVictory(), 600);
      }
    } else if (level.bonusWords && level.bonusWords.includes(word)) {
      if (this.bonusWordsFound.has(word)) {
        this.flashToast("Bonus kelimeyi zaten aldın!");
      } else {
        this.bonusWordsFound.add(word);
        this.state.coins += 5;
        this.saveSecureState();
        window.soundFX.playCoinCollect();
        this.flashToast(`Bonus Kelime: ${word}! (+5 🪙)`);
      }
    } else {
      window.soundFX.playInvalid();
      this.wordPreview.classList.add('shake');
      setTimeout(() => this.wordPreview.classList.remove('shake'), 400);
    }
  }

  revealWordOnBoard(word) {
    const row = this.boardEl.querySelector(`[data-word="${word}"]`);
    if (!row) return;

    const slots = row.querySelectorAll('.letter-slot');
    slots.forEach((slot, i) => {
      setTimeout(() => {
        slot.textContent = slot.dataset.char;
        slot.classList.add('revealed');
      }, i * 65);
    });
  }

  useRandomHint() {
    const cost = 25;
    if (this.state.coins < cost) {
      this.openModal(this.modalShop);
      this.flashToast("Yetersiz Altın!");
      return;
    }

    const unrevealedSlots = Array.from(this.boardEl.querySelectorAll('.letter-slot:not(.revealed)'));
    if (unrevealedSlots.length === 0) {
      this.flashToast("Açılacak harf kalmadı!");
      return;
    }

    const chosenSlot = unrevealedSlots[Math.floor(Math.random() * unrevealedSlots.length)];
    chosenSlot.textContent = chosenSlot.dataset.char;
    chosenSlot.classList.add('revealed');
    chosenSlot.classList.add('hinted');

    this.state.coins -= cost;
    this.saveSecureState();
    window.soundFX.playCoinCollect();

    // Check if whole row is now revealed
    const row = chosenSlot.closest('.word-row');
    if (row) {
      const rowWord = row.dataset.word;
      const allRevealed = Array.from(row.querySelectorAll('.letter-slot')).every(s => s.classList.contains('revealed'));
      if (allRevealed && !this.solvedWords.has(rowWord)) {
        this.solvedWords.add(rowWord);
      }
    }

    const level = this.getCurrentLevel();
    if (this.solvedWords.size === level.targetWords.length) {
      setTimeout(() => this.triggerVictory(), 600);
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
    document.getElementById('victory-title').textContent = `Bölüm ${level.level} Tamamlandı!`;
    this.openModal(this.modalVictory);
  }

  nextLevel() {
    this.stopConfetti();
    this.loadLevel((this.state.levelIndex + 1) % WOW_LEVELS.length);
  }

  shareScore() {
    const lvl = this.getCurrentLevel();
    const text = `🏆 Kelime Harikaları'nda ${lvl.location} (Bölüm ${lvl.level}/100) tamamladım! Sen de hemen oyna: https://umutcandemircan.github.io/kelime-harikalari/`;
    if (navigator.share) {
      navigator.share({ title: 'Kelime Harikaları', text }).catch(() => {});
    } else {
      navigator.clipboard.writeText(text);
      this.flashToast("Meydan okuma linki kopyalandı!");
    }
  }

  openModal(el) { el.classList.remove('hidden'); }
  closeModal(el) { el.classList.add('hidden'); }

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
        padding: 9px 20px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 13px;
        z-index: 9999;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.2);
        pointer-events: none;
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
    for (let i = 0; i < 80; i++) {
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

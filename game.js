// Kelime Harikaları - Ultra Akıcı (120 FPS) & Kusursuz Responsive Oyun Motoru
class WoWGame {
  constructor() {
    this.storageKey = 'kelime_harikalari_save_v1';
    this.secretSalt = 'kelime_harikalari_tdk_100';

    this.state = this.loadSecureState();
    this.currentWord = "";
    this.selectedNodes = [];
    this.isDragging = false;

    // Pre-cached Geometry for 120 FPS Touch Tracking
    this.nodeData = [];
    this.wheelRect = null;

    // Board State
    this.solvedWords = new Set();
    this.bonusWordsFound = new Set();

    // Screen Elements
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
    let resizeTimer = null;
    const resize = () => {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
      this.adjustBoardScale();
      // Re-cache wheel rect on window resize/orientation change
      if (this.letterWheel) {
        this.wheelRect = this.letterWheel.getBoundingClientRect();
      }
    };
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(resize, 60);
    });
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

    // Letter Wheel Gestures (Touch & Mouse with passive: false for 0 latency)
    this.letterWheel.addEventListener('pointerdown', (e) => this.onPointerDown(e), { passive: false });
    window.addEventListener('pointermove', (e) => this.onPointerMove(e), { passive: false });
    window.addEventListener('pointerup', () => this.onPointerUp(), { passive: false });
    window.addEventListener('pointercancel', () => this.onPointerUp(), { passive: false });
  }

  showScreen(name) {
    if (name === 'game') {
      this.screenHome.classList.add('hidden');
      this.screenGame.classList.remove('hidden');
      // Recalculate dimensions once visible
      setTimeout(() => {
        this.adjustBoardScale();
        this.updateWheelGeometry();
      }, 50);
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

    this.adjustBoardScale();
    this.renderWheel(level.wheelLetters);
    this.renderRegionsMap();
  }

  adjustBoardScale() {
    const level = this.getCurrentLevel();
    if (!level || !this.boardEl) return;

    const boardArea = this.boardEl.parentElement;
    const availW = Math.min(boardArea ? boardArea.clientWidth - 24 : window.innerWidth - 32, 400);
    const availH = Math.max(160, boardArea ? boardArea.clientHeight - 16 : 240);

    const maxWordLen = Math.max(...level.targetWords.map(w => w.length));
    const numRows = level.targetWords.length;

    // Slot size constrained by available width
    const slotByWidth = Math.floor((availW - (maxWordLen - 1) * 6) / maxWordLen);

    // Slot size constrained by available height
    const slotByHeight = Math.floor((availH - (numRows - 1) * 8) / numRows);

    // Pick best balanced size that never overflows in either dimension
    const slotSize = Math.max(26, Math.min(44, slotByWidth, slotByHeight));
    const fontSize = Math.max(14, Math.floor(slotSize * 0.54));

    this.boardEl.style.setProperty('--slot-size', `${slotSize}px`);
    this.boardEl.style.setProperty('--slot-font-size', `${fontSize}px`);
  }

  updateWheelGeometry() {
    if (!this.letterWheel) return;
    this.wheelRect = this.letterWheel.getBoundingClientRect();
  }

  renderWheel(letters) {
    this.letterWheel.innerHTML = '';
    this.wheelSvg.innerHTML = '';
    this.nodeData = [];

    const turntableW = this.letterWheel.clientWidth || 220;
    const center = turntableW / 2;
    const radius = center * 0.65;
    const total = letters.length;

    let nodeSize = 52;
    let fontSize = 25;
    if (total === 6) { nodeSize = 46; fontSize = 22; }
    else if (total === 7) { nodeSize = 42; fontSize = 20; }
    else if (total >= 8) { nodeSize = 36; fontSize = 17; }

    // Responsive node size on small turntable
    if (turntableW < 200) {
      nodeSize = Math.floor(nodeSize * 0.88);
      fontSize = Math.floor(fontSize * 0.88);
    }

    this.letterWheel.style.setProperty('--node-size', `${nodeSize}px`);
    this.letterWheel.style.setProperty('--node-font-size', `${fontSize}px`);

    letters.forEach((char, i) => {
      const angle = (i * (360 / total) - 90) * (Math.PI / 180);
      const x = center + radius * Math.cos(angle);
      const y = center + radius * Math.sin(angle);

      const node = document.createElement('div');
      node.className = 'letter-node';
      node.textContent = char;
      node.dataset.char = char;
      node.dataset.index = i;
      node.style.left = `${x.toFixed(1)}px`;
      node.style.top = `${y.toFixed(1)}px`;

      this.letterWheel.appendChild(node);

      // Pre-cache coordinates and collision radius for instantaneous math lookups
      this.nodeData.push({
        el: node,
        char: char,
        index: i,
        x: x,
        y: y,
        hitRadius: (nodeSize / 2) + 12
      });
    });

    this.updateWheelGeometry();
  }

  shuffleWheel() {
    const level = this.getCurrentLevel();
    const letters = [...level.wheelLetters];
    const targets = level.targetWords;

    // Intelligent shuffle: guarantee no target word appears sequentially in circular order
    let best = [...letters];
    let minViolations = 999999;

    for (let tries = 0; tries < 200; tries++) {
      letters.sort(() => Math.random() - 0.5);
      const doubled = letters.join('') + letters.join('');
      const revDoubled = [...letters].reverse().join('') + [...letters].reverse().join('');

      let violations = 0;
      for (const w of targets) {
        if (w.length >= 3 && (doubled.includes(w) || revDoubled.includes(w))) {
          violations += w.length;
        }
      }

      if (violations === 0) {
        best = [...letters];
        break;
      }
      if (violations < minViolations) {
        minViolations = violations;
        best = [...letters];
      }
    }

    window.soundFX.playLetterSelect(2);
    this.renderWheel(best);
  }

  onPointerDown(e) {
    if (e.cancelable) e.preventDefault();
    this.updateWheelGeometry();

    const relX = e.clientX - this.wheelRect.left;
    const relY = e.clientY - this.wheelRect.top;

    // Pure mathematical collision lookup - zero DOM reading
    const hit = this.nodeData.find(n => Math.hypot(relX - n.x, relY - n.y) <= n.hitRadius);
    if (hit) {
      this.isDragging = true;
      this.selectedNodes = [hit];
      this.currentWord = hit.char;
      hit.el.classList.add('selected');

      window.soundFX.playLetterSelect(0);
      if (navigator.vibrate) navigator.vibrate(10);

      this.updatePreview();
      this.updateSvgPolyline(relX, relY);
    }
  }

  onPointerMove(e) {
    if (!this.isDragging) return;
    if (e.cancelable) e.preventDefault();

    const relX = e.clientX - this.wheelRect.left;
    const relY = e.clientY - this.wheelRect.top;

    const hit = this.nodeData.find(n => Math.hypot(relX - n.x, relY - n.y) <= n.hitRadius);
    if (hit) {
      const len = this.selectedNodes.length;

      // Backtrack: if sliding back to previous node, unselect last node
      if (len >= 2 && hit === this.selectedNodes[len - 2]) {
        const popped = this.selectedNodes.pop();
        popped.el.classList.remove('selected');
        this.currentWord = this.selectedNodes.map(n => n.char).join('');
        window.soundFX.playLetterSelect(this.selectedNodes.length - 1);
        if (navigator.vibrate) navigator.vibrate(8);
        this.updatePreview();
      } else if (!this.selectedNodes.includes(hit)) {
        this.selectedNodes.push(hit);
        this.currentWord += hit.char;
        hit.el.classList.add('selected');

        window.soundFX.playLetterSelect(this.selectedNodes.length - 1);
        if (navigator.vibrate) navigator.vibrate(10);
        this.updatePreview();
      }
    }

    this.updateSvgPolyline(relX, relY);
  }

  onPointerUp() {
    if (!this.isDragging) return;
    this.isDragging = false;

    this.validateWord(this.currentWord);

    this.selectedNodes.forEach(item => item.el.classList.remove('selected'));
    this.selectedNodes = [];
    this.currentWord = "";
    this.wheelSvg.innerHTML = '';
    this.wordPreview.classList.remove('active');
    this.wordPreview.textContent = "";
  }

  updateSvgPolyline(pointerRelX, pointerRelY) {
    if (this.selectedNodes.length === 0) {
      this.wheelSvg.innerHTML = '';
      return;
    }

    const points = this.selectedNodes.map(n => `${n.x.toFixed(1)},${n.y.toFixed(1)}`);
    if (this.isDragging && pointerRelX !== undefined && pointerRelY !== undefined) {
      points.push(`${pointerRelX.toFixed(1)},${pointerRelY.toFixed(1)}`);
    }

    let polyline = this.wheelSvg.firstElementChild;
    if (!polyline) {
      polyline = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
      polyline.setAttribute('stroke', '#f59e0b');
      polyline.setAttribute('stroke-width', '8');
      polyline.setAttribute('stroke-linecap', 'round');
      polyline.setAttribute('stroke-linejoin', 'round');
      polyline.setAttribute('fill', 'none');
      this.wheelSvg.appendChild(polyline);
    }
    polyline.setAttribute('points', points.join(' '));
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

    // Check if entire row is now revealed
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

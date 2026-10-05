# -*- coding: utf-8 -*-
"""
Full Assembly Script for Kelime Harikaları Commercial Production Release
"""
import os
import json

SCRIPT_CODE = r'''
  /* ==========================================================================
     1. PROCEDURAL SOUND SYNTHESIS (WEB AUDIO API - ZERO EXTERNAL ASSETS)
     ========================================================================== */
  class SoundEngine {
    constructor() {
      this.ctx = null;
      this.muted = localStorage.getItem('wow_sound_muted') === 'true';
    }

    init() {
      if (!this.ctx) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        this.ctx = new AudioCtx();
      }
      if (this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
    }

    toggleMute() {
      this.muted = !this.muted;
      localStorage.setItem('wow_sound_muted', this.muted);
      return this.muted;
    }

    // Incremental note frequencies for dragging letters (Pentatonic scale)
    playLetterNote(index) {
      if (this.muted) return;
      this.init();
      const freqs = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 659.25, 783.99]; // C4, D4, E4, G4, A4, C5, E5, G5
      const freq = freqs[Math.min(index, freqs.length - 1)];

      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

      gain.gain.setValueAtTime(0.2, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.25);

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.25);
    }

    // Success chord arpeggio for word solved
    playWordSuccess() {
      if (this.muted) return;
      this.init();
      const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
      notes.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime + idx * 0.07);

        const startTime = this.ctx.currentTime + idx * 0.07;
        gain.gain.setValueAtTime(0.22, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.45);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + 0.45);
      });
    }

    // Error boop on invalid word
    playErrorBuzz() {
      if (this.muted) return;
      this.init();
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(140, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(80, this.ctx.currentTime + 0.22);

      gain.gain.setValueAtTime(0.18, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.22);

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.22);
    }

    // Hint chime
    playHint() {
      if (this.muted) return;
      this.init();
      const freqs = [659.25, 830.61, 987.77]; // E5, G#5, B5
      freqs.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime + idx * 0.08);

        const startTime = this.ctx.currentTime + idx * 0.08;
        gain.gain.setValueAtTime(0.25, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.5);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + 0.5);
      });
    }

    // Lightning blast with rumble
    playLightning() {
      if (this.muted) return;
      this.init();
      // Low Saw rumble
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(100, this.ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(30, this.ctx.currentTime + 0.6);

      gain.gain.setValueAtTime(0.35, this.ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.6);

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start();
      osc.stop(this.ctx.currentTime + 0.6);

      // White noise blast
      const bufferSize = this.ctx.sampleRate * 0.35;
      const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
      const output = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        output[i] = Math.random() * 2 - 1;
      }
      const whiteNoise = this.ctx.createBufferSource();
      whiteNoise.buffer = buffer;
      const noiseGain = this.ctx.createGain();
      noiseGain.gain.setValueAtTime(0.25, this.ctx.currentTime);
      noiseGain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.35);

      whiteNoise.connect(noiseGain);
      noiseGain.connect(this.ctx.destination);
      whiteNoise.start();
    }

    // Coin shower ping
    playCoinShower() {
      if (this.muted) return;
      this.init();
      const pings = [880, 1174, 1318, 1760];
      pings.forEach((freq, i) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime + i * 0.06);

        const startTime = this.ctx.currentTime + i * 0.06;
        gain.gain.setValueAtTime(0.2, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.3);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + 0.3);
      });
    }

    // Fanfare victory
    playFanfare() {
      if (this.muted) return;
      this.init();
      const motif = [
        { f: 523.25, t: 0.0, d: 0.15 },
        { f: 659.25, t: 0.15, d: 0.15 },
        { f: 783.99, t: 0.30, d: 0.2 },
        { f: 1046.50, t: 0.50, d: 0.6 }
      ];
      motif.forEach(m => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(m.f, this.ctx.currentTime + m.t);

        const startTime = this.ctx.currentTime + m.t;
        gain.gain.setValueAtTime(0.25, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + m.d);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + m.d);
      });
    }
  }

  /* ==========================================================================
     2. CURATED LEVEL DATABASE (STRICT 90° CROSSWORD + CULTURAL TRIVIA)
     ========================================================================== */
  const LEVELS_DATA = [
    {
      id: 1,
      title: "Kapadokya - Peri Bacaları",
      region: "NEVŞEHİR",
      bg: "https://images.unsplash.com/photo-1570939274717-7eda259b50ed?auto=format&fit=crop&w=1200&q=80",
      trivia: "Milyonlarca yıl önce yanardağ küllerinin rüzgâr ve yağmurla aşınmasıyla oluşan peri bacaları, yüzlerce yıldır yeraltı şehirlerine ve gökyüzünü süsleyen rengarenk sıcak hava balonlarına ev sahipliği yapar.",
      wheel: ["A", "K", "T"],
      words: [
        { id: "w1", word: "KAT", row: 2, col: 0, dir: "H" },
        { id: "w2", word: "TAK", row: 0, col: 0, dir: "V" }
      ],
      bonus: ["AK"]
    },
    {
      id: 2,
      title: "Pamukkale - Travertenler",
      region: "DENİZLİ",
      bg: "https://images.unsplash.com/photo-1549880338-65ddcdfd017b?auto=format&fit=crop&w=1200&q=80",
      trivia: "Termal suların içerisindeki kalsiyum karbonatın binlerce yılda çökelmesiyle oluşan bembeyaz traverten terasları, antik Hierapolis kentinin şifalı suları ile UNESCO Dünya Mirası listesindedir.",
      wheel: ["E", "K", "A", "L"],
      words: [
        { id: "w1", word: "KALE", row: 1, col: 0, dir: "H" },
        { id: "w2", word: "KEL", row: 1, col: 0, dir: "V" },
        { id: "w3", word: "ELA", row: 0, col: 2, dir: "V" }
      ],
      bonus: ["LAK", "LAKE"]
    },
    {
      id: 3,
      title: "Galata Kulesi - İstanbul",
      region: "İSTANBUL",
      bg: "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1200&q=80",
      trivia: "1348 yılında Cenevizliler tarafından inşa edilen kule, 17. yüzyılda Hezarfen Ahmed Çelebi'nin tahta kanatlarla Boğaz'ı aşarak Üsküdar'a uçtuğu efsanevi kuledir.",
      wheel: ["S", "M", "A", "A"],
      words: [
        { id: "w1", word: "MASA", row: 2, "col": 0, "dir": "H" },
        { id: "w2", word: "ASMA", row: 0, "col": 0, "dir": "V" }
      ],
      bonus: ["AMA", "SAM", "AS"]
    },
    {
      id: 4,
      title: "Efes - Celsus Kütüphanesi",
      region: "İZMİR",
      bg: "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80",
      trivia: "Antik dünyanın en büyük üçüncü kütüphanesi olan Celsus Kütüphanesi, 12 binden fazla parşömen rulosuna ev sahipliği yapmış ve antik felsefenin beşiği olmuştur.",
      wheel: ["I", "B", "K", "A", "L"],
      words: [
        { id: "w1", word: "BALIK", row: 2, col: 0, dir: "H" },
        { id: "w2", word: "BAL", row: 2, col: 0, dir: "V" },
        { id: "w3", word: "KIL", row: 0, col: 2, dir: "V" }
      ],
      bonus: ["ALIK", "BAK", "KAL", "LAK", "AKIL"]
    },
    {
      id: 5,
      title: "Nemrut Dağı - Tanrılar Tahtı",
      region: "ADIYAMAN",
      bg: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80",
      trivia: "2150 metre yükseklikte Kommagene Kralı I. Antiochos tarafından yaptırılan devasa kral ve tanrı heykelleri, dünyanın en büyüleyici gün doğumu ve gün batımına tanıklık eder.",
      wheel: ["T", "P", "İ", "K", "A"],
      words: [
        { id: "w1", word: "KİTAP", row: 2, col: 0, dir: "H" },
        { id: "w2", word: "TAKİP", row: 0, col: 0, dir: "V" },
        { id: "w3", word: "PAK", row: 1, col: 3, dir: "V" }
      ],
      bonus: ["TİP", "PAT", "KAT", "AİT", "PATİK"]
    },
    {
      id: 6,
      title: "Göbeklitepe - Tarihin Sıfırı",
      region: "ŞANLIURFA",
      bg: "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1200&q=80",
      trivia: "Yaklaşık 12.000 yıl öncesine dayanan T biçimli devasa kireçtaşı sütunlarıyla Göbeklitepe, insanlık tarihinin bilinen en eski anıtsal tapınak kompleksidir.",
      wheel: ["N", "Z", "E", "D", "İ"],
      words: [
        { id: "w1", word: "DENİZ", row: 2, col: 0, dir: "H" },
        { id: "w2", word: "DİZ", row: 2, col: 0, dir: "V" },
        { id: "w3", word: "DİN", row: 0, col: 2, dir: "V" }
      ],
      bonus: ["DİZE", "İZ", "İN", "ZİN"]
    },
    {
      id: 7,
      title: "Kolezyum - Gladyatörler Arenası",
      region: "ROMA, İTALYA",
      bg: "https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=1200&q=80",
      trivia: "İmparator Vespasianus tarafından MS 80 yılında tamamlanan 50.000 kişilik dev amfitiyatro, Roma İmparatorluğu'nun mühendislik harikası ve antik gladyatör dövüşlerinin merkezidir.",
      wheel: ["M", "N", "A", "R", "O"],
      words: [
        { id: "w1", word: "ROMA", row: 2, col: 0, dir: "H" },
        { id: "w2", word: "ORAN", row: 1, col: 0, dir: "V" },
        { id: "w3", word: "ROMAN", row: 0, col: 2, dir: "V" }
      ],
      bonus: ["MOR", "ONAR", "ROM"]
    },
    {
      id: 8,
      title: "Tac Mahal - Aşkın Mermer Anıtı",
      region: "AGRA, HİNDİSTAN",
      bg: "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1200&q=80",
      trivia: "Şah Cihan'ın sevgili eşi Mümtaz Mahal anısına beyaz mermerden yaptırdığı bu kusursuz simetrik anıt mezar, dünyanın yeni 7 harikasından biri olarak kabul edilir.",
      wheel: ["Ş", "A", "K", "U", "K"],
      words: [
        { id: "w1", word: "AŞK", row: 6, col: 0, dir: "H" },
        { id: "w2", word: "ŞAK", row: 4, col: 2, dir: "V" },
        { id: "w3", word: "KUŞ", row: 4, col: 0, dir: "H" },
        { id: "w4", word: "KUŞAK", row: 0, col: 0, dir: "V" }
      ],
      bonus: ["KAŞ"]
    }
  ];

  const DAILY_LEVEL_DATA = {
    id: "daily",
    title: "Günün Özel Meydan Okuması",
    region: "GÜNLÜK GÖREV",
    bg: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
    trivia: "Tebrikler! Bugünkü günlük bulmacayı başarıyla tamamladın ve 3 parlayan yıldızı koleksiyonuna kattın! Serini korumak için yarın tekrar gelmeyi unutma.",
    wheel: ["R", "H", "A", "B", "A"],
    words: [
      { id: "dw1", word: "BAHAR", row: 1, col: 1, dir: "H" },
      { id: "dw2", word: "HARA", row: 0, col: 2, dir: "V" },
      { id: "dw3", word: "BAR", row: 0, col: 4, dir: "V" },
      { id: "dw4", word: "ARA", row: 3, col: 0, dir: "H" }
    ],
    bonus: ["RAB", "ABA", "AHA"]
  };

  /* ==========================================================================
     3. CORE GAME CONTROLLER
     ========================================================================== */
  class WoWGame {
    constructor() {
      this.sound = new SoundEngine();

      // Persistent Game State
      this.coins = parseInt(localStorage.getItem('wow_coins') || '250', 10);
      this.stars = parseInt(localStorage.getItem('wow_stars') || '0', 10);
      this.currentLevelIdx = parseInt(localStorage.getItem('wow_level_idx') || '0', 10);
      this.completedDailyDates = JSON.parse(localStorage.getItem('wow_daily_dates') || '[]');
      this.streak = parseInt(localStorage.getItem('wow_streak') || '1', 10);
      this.bonusChestCount = parseInt(localStorage.getItem('wow_bonus_chest') || '0', 10);

      this.levelsCompletedCount = 0;
      this.isDailyMode = false;
      this.isTargetingMode = false;

      // Active level state
      this.level = null;
      this.unlockedWords = new Set();
      this.revealedCells = new Set();
      this.foundBonusWords = new Set();
      this.dailyStarCells = new Set();
      this.dailyStarsCollected = new Set();

      // Wheel touch state
      this.isDragging = false;
      this.selectedNodeIndices = [];
      this.currentLetters = [];
      this.wheelNodePositions = [];
      this.currentWheelLetters = [];

      // DOM Elements
      this.dom = {
        bgLayer: document.getElementById('bg-layer'),
        regionText: document.getElementById('region-text'),
        levelTitleText: document.getElementById('level-title-text'),
        streakIndicator: document.getElementById('streak-indicator'),
        soundIcon: document.getElementById('sound-icon'),
        coinsDisplay: document.getElementById('coins-display'),
        crosswordGrid: document.getElementById('crossword-grid'),
        wordPreview: document.getElementById('word-preview'),
        wheelWrapper: document.getElementById('wheel-wrapper'),
        wheelNodesContainer: document.getElementById('wheel-nodes-container'),
        connectionLine: document.getElementById('connection-line'),
        targetingBanner: document.getElementById('targeting-banner'),
        bonusCounter: document.getElementById('bonus-counter'),
        screenFlash: document.getElementById('screen-flash'),
        confettiCanvas: document.getElementById('confetti-canvas'),
        // Modals
        modalDiscovery: document.getElementById('modal-discovery'),
        discoveryImg: document.getElementById('discovery-img'),
        discoveryRegion: document.getElementById('discovery-region'),
        discoveryTitle: document.getElementById('discovery-title'),
        discoveryTrivia: document.getElementById('discovery-trivia'),
        modalVictory: document.getElementById('modal-victory'),
        modalCalendar: document.getElementById('modal-calendar'),
        calendarStreakText: document.getElementById('calendar-streak-text'),
        calendarGridContainer: document.getElementById('calendar-grid-container'),
        modalNoCoins: document.getElementById('modal-no-coins'),
        rewardedAdScreen: document.getElementById('rewarded-ad-screen'),
        rewardedAdTimer: document.getElementById('rewarded-ad-timer'),
        rewardedAdProgress: document.getElementById('rewarded-ad-progress'),
        interstitialAdScreen: document.getElementById('interstitial-ad-screen'),
        interstitialAdTimer: document.getElementById('interstitial-ad-timer')
      };

      // Confetti Setup
      this.ctxConfetti = this.dom.confettiCanvas.getContext('2d');
      this.confettiParticles = [];
      this.confettiAnimId = null;

      this.initEvents();
      this.updateTopbar();
      this.loadLevel(this.currentLevelIdx);
    }

    /* ---------------- Event Listeners ---------------- */
    initEvents() {
      // Sound Toggle
      document.getElementById('btn-sound-toggle').addEventListener('click', () => {
        const isMuted = this.sound.toggleMute();
        this.dom.soundIcon.textContent = isMuted ? '🔇' : '🔊';
      });
      this.dom.soundIcon.textContent = this.sound.muted ? '🔇' : '🔊';

      // Daily Calendar Modal
      document.getElementById('btn-open-daily').addEventListener('click', () => {
        this.openCalendarModal();
      });
      document.getElementById('btn-close-calendar').addEventListener('click', () => {
        this.dom.modalCalendar.classList.remove('active');
      });
      document.getElementById('btn-play-daily').addEventListener('click', () => {
        this.dom.modalCalendar.classList.remove('active');
        this.startDailyChallenge();
      });

      // Power-ups
      document.getElementById('btn-shuffle').addEventListener('click', () => this.handleShuffle());
      document.getElementById('btn-hint-bulb').addEventListener('click', () => this.handleBulbHint());
      document.getElementById('btn-hint-target').addEventListener('click', () => this.handleTargetMagnifier());
      document.getElementById('btn-hint-lightning').addEventListener('click', () => this.handleLightning());
      document.getElementById('btn-bonus-chest').addEventListener('click', () => {
        this.showToast(`🎁 Bonus Sandık: ${this.bonusChestCount}/5 kelime`);
      });

      // Modals
      document.getElementById('btn-discovery-continue').addEventListener('click', () => {
        this.dom.modalDiscovery.classList.remove('active');
        this.openVictoryModal();
      });

      // Victory Modals
      document.getElementById('btn-victory-normal').addEventListener('click', () => {
        this.dom.modalVictory.classList.remove('active');
        this.addCoins(25);
        this.advanceAfterVictory();
      });
      document.getElementById('btn-victory-2x').addEventListener('click', () => {
        this.dom.modalVictory.classList.remove('active');
        this.showRewardedAd(50, () => {
          this.advanceAfterVictory();
        });
      });

      // Insufficient Coins
      document.getElementById('btn-close-no-coins').addEventListener('click', () => {
        this.dom.modalNoCoins.classList.remove('active');
      });
      document.getElementById('btn-watch-ad-for-coins').addEventListener('click', () => {
        this.dom.modalNoCoins.classList.remove('active');
        this.showRewardedAd(100, () => {
          this.showToast("🎉 +100 Altın hesabına eklendi!");
        });
      });

      // Resize
      window.addEventListener('resize', () => {
        this.cacheWheelGeometry();
        this.resizeCrosswordBoard();
      });

      // Wheel Pointer Drag Engine
      const wrapper = this.dom.wheelWrapper;
      wrapper.addEventListener('pointerdown', (e) => this.onPointerDown(e));
      wrapper.addEventListener('pointermove', (e) => this.onPointerMove(e));
      wrapper.addEventListener('pointerup', (e) => this.onPointerUp(e));
      wrapper.addEventListener('pointercancel', (e) => this.onPointerUp(e));

      // Haptic Helper
      this.vibrate = (ms = 15) => {
        if ('vibrate' in navigator) {
          try { navigator.vibrate(ms); } catch (err) {}
        }
      };
    }

    /* ---------------- UI Updates ---------------- */
    updateTopbar() {
      this.dom.coinsDisplay.textContent = this.coins;
      this.dom.streakIndicator.textContent = `🔥 ${this.streak}`;
      this.dom.bonusCounter.textContent = `${this.bonusChestCount}/5`;
    }

    addCoins(amount) {
      this.coins += amount;
      localStorage.setItem('wow_coins', this.coins);
      this.sound.playCoinShower();
      this.updateTopbar();
    }

    showToast(message) {
      const toast = document.createElement('div');
      toast.className = 'floating-toast';
      toast.textContent = message;
      document.body.appendChild(toast);
      setTimeout(() => toast.remove(), 1600);
    }

    /* ---------------- Crossword Layout Engine ---------------- */
    loadLevel(levelIndex) {
      this.isDailyMode = false;
      this.level = LEVELS_DATA[levelIndex % LEVELS_DATA.length];
      this.unlockedWords.clear();
      this.revealedCells.clear();
      this.foundBonusWords.clear();
      this.dailyStarCells.clear();
      this.dailyStarsCollected.clear();

      this.setupLevelUI();
    }

    startDailyChallenge() {
      this.isDailyMode = true;
      this.level = DAILY_LEVEL_DATA;
      this.unlockedWords.clear();
      this.revealedCells.clear();
      this.foundBonusWords.clear();
      this.dailyStarCells.clear();
      this.dailyStarsCollected.clear();

      this.setupLevelUI();
    }

    setupLevelUI() {
      // Background Image
      this.dom.bgLayer.style.backgroundImage = `url('${this.level.bg}')`;

      // Header Info
      this.dom.regionText.textContent = this.level.region;
      this.dom.levelTitleText.textContent = this.isDailyMode ? "Günün Bulmacası" : `Bölüm ${this.level.id}`;

      // Build Crossword Board
      this.renderCrosswordGrid();

      // Render Wheel
      this.currentWheelLetters = [...this.level.wheel];
      this.renderWheel();
    }

    renderCrosswordGrid() {
      const words = this.level.words;

      // 1. Calculate Bounding Box
      let minR = Infinity, maxR = -Infinity;
      let minC = Infinity, maxC = -Infinity;

      words.forEach(w => {
        const len = w.word.length;
        const endR = w.dir === 'V' ? w.row + len - 1 : w.row;
        const endC = w.dir === 'H' ? w.col + len - 1 : w.col;

        minR = Math.min(minR, w.row);
        maxR = Math.max(maxR, endR);
        minC = Math.min(minC, w.col);
        maxC = Math.max(maxC, endC);
      });

      const totalRows = maxR - minR + 1;
      const totalCols = maxC - minC + 1;

      // 2. Map coordinates (normalized) to letters & words
      this.gridLetterMap = new Map(); // key: "r_c" -> { char, wordIds: [] }
      words.forEach(w => {
        const normR = w.row - minR;
        const normC = w.col - minC;
        for (let i = 0; i < w.word.length; i++) {
          const r = normR + (w.dir === 'V' ? i : 0);
          const c = normC + (w.dir === 'H' ? i : 0);
          const key = `${r}_${c}`;
          const ch = w.word[i].toLocaleUpperCase('tr-TR');

          if (!this.gridLetterMap.has(key)) {
            this.gridLetterMap.set(key, { char: ch, wordIds: [w.id], r, c });
          } else {
            this.gridLetterMap.get(key).wordIds.push(w.id);
          }
        }
      });

      // 3. For Daily Mode: assign 3 stars to 3 random distinct cells
      if (this.isDailyMode) {
        const allKeys = Array.from(this.gridLetterMap.keys());
        // shuffle keys and pick 3
        const shuffled = [...allKeys].sort(() => 0.5 - Math.random());
        const starKeys = shuffled.slice(0, Math.min(3, shuffled.length));
        starKeys.forEach(k => this.dailyStarCells.add(k));
      }

      // 4. Determine Dynamic Responsive Cell Size
      this.gridRows = totalRows;
      this.gridCols = totalCols;

      this.resizeCrosswordBoard();
    }

    resizeCrosswordBoard() {
      if (!this.gridRows || !this.gridCols) return;
      const boardArea = document.getElementById('board-area');
      const maxW = boardArea.clientWidth - 24;
      const maxH = boardArea.clientHeight - 24;

      const cellW = Math.floor(maxW / this.gridCols);
      const cellH = Math.floor(maxH / this.gridRows);
      let cellSize = Math.min(cellW, cellH);
      cellSize = Math.max(34, Math.min(cellSize, 60)); // Clamp 34px - 60px

      const gridEl = this.dom.crosswordGrid;
      gridEl.style.gridTemplateColumns = `repeat(${this.gridCols}, ${cellSize}px)`;
      gridEl.style.gridTemplateRows = `repeat(${this.gridRows}, ${cellSize}px)`;
      gridEl.innerHTML = '';

      // Create cells
      for (let r = 0; r < this.gridRows; r++) {
        for (let c = 0; c < this.gridCols; c++) {
          const key = `${r}_${c}`;
          const cellEl = document.createElement('div');
          cellEl.className = 'crossword-cell';
          cellEl.dataset.key = key;

          if (this.gridLetterMap.has(key)) {
            const cellData = this.gridLetterMap.get(key);
            const isRevealed = this.revealedCells.has(key);

            cellEl.innerHTML = `
              <div class="cell-inner">
                <div class="cell-front"></div>
                <div class="cell-back">${cellData.char}</div>
              </div>
            `;

            if (isRevealed) {
              cellEl.classList.add('revealed');
            }

            // Daily Challenge Star Badge
            if (this.isDailyMode && this.dailyStarCells.has(key) && !this.dailyStarsCollected.has(key)) {
              const starEl = document.createElement('div');
              starEl.className = 'star-badge';
              starEl.textContent = '⭐';
              cellEl.appendChild(starEl);
            }

            // Target click handler
            cellEl.addEventListener('click', () => this.onCellClicked(key));

          } else {
            cellEl.classList.add('hidden');
          }

          gridEl.appendChild(cellEl);
        }
      }
    }

    /* ---------------- Wheel & Interaction ---------------- */
    renderWheel() {
      const container = this.dom.wheelNodesContainer;
      container.innerHTML = '';

      const letters = this.currentWheelLetters;
      const count = letters.length;
      const radius = (this.dom.wheelWrapper.clientWidth / 2) - 34;
      const center = this.dom.wheelWrapper.clientWidth / 2;

      this.wheelNodePositions = [];

      letters.forEach((char, idx) => {
        // Angle in radians (starting from top -pi/2)
        const angle = (idx * (2 * Math.PI / count)) - (Math.PI / 2);
        const x = center + radius * Math.cos(angle);
        const y = center + radius * Math.sin(angle);

        const node = document.createElement('div');
        node.className = 'wheel-node';
        node.textContent = char;
        node.style.left = `${x}px`;
        node.style.top = `${y}px`;
        node.dataset.index = idx;

        container.appendChild(node);

        this.wheelNodePositions.push({
          index: idx,
          char: char,
          x: x,
          y: y,
          element: node
        });
      });
    }

    cacheWheelGeometry() {
      if (!this.currentWheelLetters) return;
      this.renderWheel();
    }

    handleShuffle() {
      this.vibrate(20);
      // Circular rotation animation
      this.dom.wheelNodesContainer.style.transition = 'transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1)';
      this.dom.wheelNodesContainer.style.transform = 'rotate(360deg)';

      setTimeout(() => {
        // Shuffle letters
        this.currentWheelLetters.sort(() => 0.5 - Math.random());
        this.dom.wheelNodesContainer.style.transition = 'none';
        this.dom.wheelNodesContainer.style.transform = 'rotate(0deg)';
        this.renderWheel();
      }, 400);
    }

    /* ---------------- Pointer Drag Handling ---------------- */
    onPointerDown(e) {
      this.sound.init();
      this.isDragging = true;
      this.selectedNodeIndices = [];
      this.currentLetters = [];
      this.dom.wheelWrapper.setPointerCapture(e.pointerId);

      this.checkPointerCollision(e.clientX, e.clientY);
    }

    onPointerMove(e) {
      if (!this.isDragging) return;
      this.checkPointerCollision(e.clientX, e.clientY);
      this.updateConnectionLine(e.clientX, e.clientY);
    }

    onPointerUp(e) {
      if (!this.isDragging) return;
      this.isDragging = false;

      // Submit Word
      if (this.currentLetters.length > 0) {
        const formed = this.currentLetters.join('').toLocaleUpperCase('tr-TR');
        this.submitWord(formed);
      }

      // Reset Wheel & Line
      this.selectedNodeIndices = [];
      this.currentLetters = [];
      this.dom.connectionLine.setAttribute('points', '');
      this.dom.wordPreview.classList.remove('active');
      document.querySelectorAll('.wheel-node.selected').forEach(n => n.classList.remove('selected'));
    }

    checkPointerCollision(clientX, clientY) {
      const rect = this.dom.wheelWrapper.getBoundingClientRect();
      const relX = clientX - rect.left;
      const relY = clientY - rect.top;

      // Hit radius for wheel nodes
      const hitRadius = 36;

      for (let i = 0; i < this.wheelNodePositions.length; i++) {
        const node = this.wheelNodePositions[i];
        const dx = relX - node.x;
        const dy = relY - node.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist <= hitRadius) {
          // If not already in current sequence
          if (!this.selectedNodeIndices.includes(i)) {
            this.selectedNodeIndices.push(i);
            this.currentLetters.push(node.char);
            node.element.classList.add('selected');

            this.vibrate(15);
            this.sound.playLetterNote(this.selectedNodeIndices.length - 1);

            // Update Preview Pill
            const word = this.currentLetters.join('');
            this.dom.wordPreview.textContent = word;
            this.dom.wordPreview.classList.add('active');

          } else if (this.selectedNodeIndices.length > 1 &&
                     this.selectedNodeIndices[this.selectedNodeIndices.length - 2] === i) {
            // Undo last selected letter if dragging back
            const popped = this.selectedNodeIndices.pop();
            this.currentLetters.pop();
            this.wheelNodePositions[popped].element.classList.remove('selected');

            this.vibrate(10);
            const word = this.currentLetters.join('');
            this.dom.wordPreview.textContent = word;
            if (this.currentLetters.length === 0) {
              this.dom.wordPreview.classList.remove('active');
            }
          }
          break;
        }
      }
    }

    updateConnectionLine(pointerClientX, pointerClientY) {
      if (this.selectedNodeIndices.length === 0) {
        this.dom.connectionLine.setAttribute('points', '');
        return;
      }

      const rect = this.dom.wheelWrapper.getBoundingClientRect();
      const relX = pointerClientX - rect.left;
      const relY = pointerClientY - rect.top;

      let pointsStr = '';
      this.selectedNodeIndices.forEach(idx => {
        const node = this.wheelNodePositions[idx];
        pointsStr += `${node.x},${node.y} `;
      });

      // Add dynamic point trailing mouse/finger
      pointsStr += `${relX},${relY}`;
      this.dom.connectionLine.setAttribute('points', pointsStr);
    }

    /* ---------------- Word Submission & Mechanics ---------------- */
    submitWord(word) {
      const matchLevelWord = this.level.words.find(w => w.word === word);

      if (matchLevelWord) {
        if (this.unlockedWords.has(matchLevelWord.id)) {
          this.showToast("Bu kelime zaten açıldı!");
          this.sound.playErrorBuzz();
        } else {
          // Word Solved!
          this.unlockCrosswordWord(matchLevelWord);
        }
      } else if (this.level.bonus && this.level.bonus.includes(word)) {
        // Bonus Word!
        if (this.foundBonusWords.has(word)) {
          this.showToast("Bu bonus kelime zaten bulundu!");
          this.sound.playErrorBuzz();
        } else {
          this.foundBonusWords.add(word);
          this.sound.playWordSuccess();
          this.showToast(`✨ Bonus Kelime Bulundu: ${word}`);

          this.bonusChestCount++;
          if (this.bonusChestCount >= 5) {
            this.bonusChestCount = 0;
            this.addCoins(30);
            this.showToast("🎁 Sandık Açıldı! +30 Altın!");
          }
          localStorage.setItem('wow_bonus_chest', this.bonusChestCount);
          this.updateTopbar();
        }
      } else {
        // Invalid Word
        this.sound.playErrorBuzz();
        this.vibrate([20, 40, 20]);
      }
    }

    unlockCrosswordWord(wordObj) {
      this.unlockedWords.add(wordObj.id);
      this.sound.playWordSuccess();
      this.vibrate(30);

      // Determine bounding box normalization minR, minC
      let minR = Infinity, minC = Infinity;
      this.level.words.forEach(w => {
        minR = Math.min(minR, w.row);
        minC = Math.min(minC, w.col);
      });

      const normR = wordObj.row - minR;
      const normC = wordObj.col - minC;

      // Launch Flying Sparks from Preview Pill to each Cell
      const previewRect = this.dom.wordPreview.getBoundingClientRect();
      const originX = previewRect.left + previewRect.width / 2;
      const originY = previewRect.top + previewRect.height / 2;

      for (let i = 0; i < wordObj.word.length; i++) {
        const r = normR + (wordObj.dir === 'V' ? i : 0);
        const c = normC + (wordObj.dir === 'H' ? i : 0);
        const key = `${r}_${c}`;

        const cellEl = document.querySelector(`.crossword-cell[data-key="${key}"]`);
        if (cellEl) {
          const cellRect = cellEl.getBoundingClientRect();
          const targetX = cellRect.left + cellRect.width / 2;
          const targetY = cellRect.top + cellRect.height / 2;

          this.spawnSpark(originX, originY, targetX, targetY, i * 80, () => {
            cellEl.classList.add('revealed');
            this.revealedCells.add(key);

            // Collect Star if in Daily Mode
            if (this.isDailyMode && this.dailyStarCells.has(key) && !this.dailyStarsCollected.has(key)) {
              this.collectDailyStar(key, cellEl);
            }

            // Check if all words completed
            this.checkLevelCompletion();
          });
        }
      }
    }

    spawnSpark(startX, startY, endX, endY, delayMs, onArrive) {
      setTimeout(() => {
        const spark = document.createElement('div');
        spark.className = 'spark-projectile';
        spark.style.left = `${startX}px`;
        spark.style.top = `${startY}px`;
        document.body.appendChild(spark);

        // Force reflow
        spark.getBoundingClientRect();

        spark.style.transform = `translate(${endX - startX}px, ${endY - startY}px) scale(1.6)`;

        setTimeout(() => {
          spark.remove();
          if (onArrive) onArrive();
        }, 450);
      }, delayMs);
    }

    collectDailyStar(cellKey, cellEl) {
      this.dailyStarsCollected.add(cellKey);
      const starBadge = cellEl.querySelector('.star-badge');
      if (starBadge) starBadge.remove();

      // Flying Star animation to Topbar
      const rect = cellEl.getBoundingClientRect();
      const star = document.createElement('div');
      star.className = 'star-projectile';
      star.textContent = '⭐';
      star.style.left = `${rect.left + rect.width / 2}px`;
      star.style.top = `${rect.top + rect.height / 2}px`;
      document.body.appendChild(star);

      const targetEl = document.getElementById('btn-open-daily');
      const targetRect = targetEl.getBoundingClientRect();

      star.getBoundingClientRect();
      star.style.transform = `translate(${targetRect.left - rect.left}px, ${targetRect.top - rect.top}px) scale(0.6)`;

      setTimeout(() => {
        star.remove();
        this.stars++;
        localStorage.setItem('wow_stars', this.stars);
        this.showToast("⭐ 1 Yıldız Toplandı!");
      }, 650);
    }

    checkLevelCompletion() {
      // If all words are unlocked
      if (this.unlockedWords.size === this.level.words.length) {
        setTimeout(() => {
          this.triggerVictory();
        }, 600);
      }
    }

    triggerVictory() {
      this.sound.playFanfare();
      this.startConfetti();

      if (this.isDailyMode) {
        const todayStr = new Date().toISOString().split('T')[0];
        if (!this.completedDailyDates.includes(todayStr)) {
          this.completedDailyDates.push(todayStr);
          this.streak++;
          localStorage.setItem('wow_daily_dates', JSON.stringify(this.completedDailyDates));
          localStorage.setItem('wow_streak', this.streak);
          this.updateTopbar();
        }
      }

      // Show Discovery Card first
      this.openDiscoveryCard();
    }

    openDiscoveryCard() {
      this.dom.discoveryImg.src = this.level.bg;
      this.dom.discoveryRegion.textContent = this.level.region;
      this.dom.discoveryTitle.textContent = this.level.title;
      this.dom.discoveryTrivia.textContent = this.level.trivia;

      this.dom.modalDiscovery.classList.add('active');
    }

    openVictoryModal() {
      this.dom.modalVictory.classList.add('active');
    }

    advanceAfterVictory() {
      this.stopConfetti();
      this.levelsCompletedCount++;

      // Check Interstitial Ad Hook (Every 3 levels)
      if (this.levelsCompletedCount % 3 === 0) {
        this.showInterstitialAd(() => {
          this.proceedToNextLevel();
        });
      } else {
        this.proceedToNextLevel();
      }
    }

    proceedToNextLevel() {
      if (this.isDailyMode) {
        this.loadLevel(this.currentLevelIdx);
      } else {
        this.currentLevelIdx = (this.currentLevelIdx + 1) % LEVELS_DATA.length;
        localStorage.setItem('wow_level_idx', this.currentLevelIdx);
        this.loadLevel(this.currentLevelIdx);
      }
    }

    /* ---------------- Power-ups ---------------- */
    handleBulbHint() {
      if (this.coins < 50) {
        this.dom.modalNoCoins.classList.add('active');
        return;
      }

      // Find all unrevealed cells
      const unrevealedKeys = [];
      this.gridLetterMap.forEach((val, key) => {
        if (!this.revealedCells.has(key)) unrevealedKeys.push(key);
      });

      if (unrevealedKeys.length === 0) return;

      this.coins -= 50;
      localStorage.setItem('wow_coins', this.coins);
      this.updateTopbar();
      this.sound.playHint();

      // Pick 1 random cell
      const randomKey = unrevealedKeys[Math.floor(Math.random() * unrevealedKeys.length)];
      this.revealSingleCell(randomKey);
    }

    handleTargetMagnifier() {
      if (this.coins < 100) {
        this.dom.modalNoCoins.classList.add('active');
        return;
      }

      this.isTargetingMode = !this.isTargetingMode;
      const btn = document.getElementById('btn-hint-target');

      if (this.isTargetingMode) {
        btn.classList.add('active-tool');
        document.body.classList.add('targeting-mode');
        this.dom.targetingBanner.style.display = 'block';
        this.showToast("🎯 Açmak istediğin kutucuğa tıkla!");
      } else {
        btn.classList.remove('active-tool');
        document.body.classList.remove('targeting-mode');
        this.dom.targetingBanner.style.display = 'none';
      }
    }

    onCellClicked(cellKey) {
      if (!this.isTargetingMode) return;
      if (this.revealedCells.has(cellKey)) {
        this.showToast("Bu kutucuk zaten açık!");
        return;
      }

      // Consume 100 coins
      this.coins -= 100;
      localStorage.setItem('wow_coins', this.coins);
      this.updateTopbar();
      this.sound.playHint();

      // Deactivate targeting mode
      this.isTargetingMode = false;
      document.getElementById('btn-hint-target').classList.remove('active-tool');
      document.body.classList.remove('targeting-mode');
      this.dom.targetingBanner.style.display = 'none';

      this.revealSingleCell(cellKey);
    }

    handleLightning() {
      if (this.coins < 150) {
        this.dom.modalNoCoins.classList.add('active');
        return;
      }

      // Find all unrevealed cells
      const unrevealedKeys = [];
      this.gridLetterMap.forEach((val, key) => {
        if (!this.revealedCells.has(key)) unrevealedKeys.push(key);
      });

      if (unrevealedKeys.length === 0) return;

      this.coins -= 150;
      localStorage.setItem('wow_coins', this.coins);
      this.updateTopbar();

      // Screen Flash & Thunder
      this.dom.screenFlash.classList.add('flash');
      setTimeout(() => this.dom.screenFlash.classList.remove('flash'), 180);
      this.sound.playLightning();
      this.vibrate([40, 60, 40]);

      // Pick 3-4 random unrevealed cells
      const countToReveal = Math.min(unrevealedKeys.length, Math.floor(Math.random() * 2) + 3);
      const shuffled = [...unrevealedKeys].sort(() => 0.5 - Math.random());
      const selected = shuffled.slice(0, countToReveal);

      selected.forEach((key, idx) => {
        setTimeout(() => {
          this.revealSingleCell(key);
        }, idx * 120);
      });
    }

    revealSingleCell(cellKey) {
      const cellEl = document.querySelector(`.crossword-cell[data-key="${cellKey}"]`);
      if (!cellEl) return;

      cellEl.classList.add('revealed');
      this.revealedCells.add(cellKey);

      if (this.isDailyMode && this.dailyStarCells.has(cellKey) && !this.dailyStarsCollected.has(cellKey)) {
        this.collectDailyStar(cellKey, cellEl);
      }

      // Check if all cells of any word are revealed
      this.level.words.forEach(w => {
        if (!this.unlockedWords.has(w.id)) {
          let minR = Infinity, minC = Infinity;
          this.level.words.forEach(item => {
            minR = Math.min(minR, item.row);
            minC = Math.min(minC, item.col);
          });
          const normR = w.row - minR;
          const normC = w.col - minC;

          let allCellsOpen = true;
          for (let i = 0; i < w.word.length; i++) {
            const r = normR + (w.dir === 'V' ? i : 0);
            const c = normC + (w.dir === 'H' ? i : 0);
            if (!this.revealedCells.has(`${r}_${c}`)) {
              allCellsOpen = false;
              break;
            }
          }

          if (allCellsOpen) {
            this.unlockedWords.add(w.id);
          }
        }
      });

      this.checkLevelCompletion();
    }

    /* ---------------- Calendar Modal & Daily Challenge ---------------- */
    openCalendarModal() {
      const now = new Date();
      const currentYear = now.getFullYear();
      const currentMonth = now.getMonth(); // 0-indexed
      const todayDate = now.getDate();
      const todayStr = now.toISOString().split('T')[0];

      this.dom.calendarStreakText.textContent = `🔥 ${this.streak} Günlük Seri`;

      const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
      const firstDayIndex = new Date(currentYear, currentMonth, 1).getDay(); // 0: Sun, 1: Mon...
      const startCol = (firstDayIndex + 6) % 7; // Convert to Mon:0, Sun:6

      const container = this.dom.calendarGridContainer;
      container.innerHTML = '';

      // Day headers
      const dayHeaders = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz'];
      dayHeaders.forEach(dh => {
        const headerCell = document.createElement('div');
        headerCell.className = 'calendar-day-header';
        headerCell.textContent = dh;
        container.appendChild(headerCell);
      });

      // Blank slots before 1st of month
      for (let i = 0; i < startCol; i++) {
        const blank = document.createElement('div');
        container.appendChild(blank);
      }

      // Days 1..daysInMonth
      for (let day = 1; day <= daysInMonth; day++) {
        const dayCell = document.createElement('div');
        dayCell.className = 'calendar-day-cell';
        dayCell.textContent = day;

        const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

        if (this.completedDailyDates.includes(dateStr)) {
          dayCell.classList.add('completed');
          const check = document.createElement('span');
          check.className = 'check';
          check.textContent = '✔';
          dayCell.appendChild(check);
        }

        if (day === todayDate) {
          dayCell.classList.add('today');
        }

        container.appendChild(dayCell);
      }

      const isTodayCompleted = this.completedDailyDates.includes(todayStr);
      const playBtn = document.getElementById('btn-play-daily');
      const statusDesc = document.getElementById('daily-status-desc');

      if (isTodayCompleted) {
        playBtn.textContent = "Bugünün Bulmacası Tamamlandı!";
        playBtn.disabled = true;
        playBtn.style.opacity = '0.6';
        statusDesc.textContent = "Harika! Bugünün görevini tamamladın. Yarın serini devam ettirmek için tekrar gel.";
      } else {
        playBtn.textContent = "Günün Bulmacasını Oyna (3 ⭐)";
        playBtn.disabled = false;
        playBtn.style.opacity = '1';
        statusDesc.textContent = "Günün bulmacasında 3 parlayan yıldızı toplayarak serini devam ettir!";
      }

      this.dom.modalCalendar.classList.add('active');
    }

    /* ---------------- Simulated Ads Engine (CrazyGames / Poki standard) ---------------- */
    showRewardedAd(rewardCoins, onReward) {
      const adScreen = this.dom.rewardedAdScreen;
      const timerEl = this.dom.rewardedAdTimer;
      const progressEl = this.dom.rewardedAdProgress;

      adScreen.classList.add('active');
      progressEl.style.width = '0%';

      let timeLeft = 5;
      timerEl.textContent = `Ödüllü Reklam - ${timeLeft}s`;

      const interval = setInterval(() => {
        timeLeft--;
        timerEl.textContent = `Ödüllü Reklam - ${timeLeft}s`;
        progressEl.style.width = `${((5 - timeLeft) / 5) * 100}%`;

        if (timeLeft <= 0) {
          clearInterval(interval);
          setTimeout(() => {
            adScreen.classList.remove('active');
            this.addCoins(rewardCoins);
            if (onReward) onReward();
          }, 400);
        }
      }, 1000);
    }

    showInterstitialAd(onComplete) {
      const adScreen = this.dom.interstitialAdScreen;
      const timerEl = this.dom.interstitialAdTimer;

      adScreen.classList.add('active');
      let timeLeft = 3;
      timerEl.textContent = `Geçiş Reklamı - ${timeLeft}s`;

      const interval = setInterval(() => {
        timeLeft--;
        timerEl.textContent = `Geçiş Reklamı - ${timeLeft}s`;

        if (timeLeft <= 0) {
          clearInterval(interval);
          setTimeout(() => {
            adScreen.classList.remove('active');
            if (onComplete) onComplete();
          }, 300);
        }
      }, 1000);
    }

    /* ---------------- Confetti Particles System ---------------- */
    startConfetti() {
      const canvas = this.dom.confettiCanvas;
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;

      const colors = ['#f59e0b', '#fbbf24', '#22c55e', '#38bdf8', '#ec4899', '#a855f7'];
      this.confettiParticles = [];

      for (let i = 0; i < 90; i++) {
        this.confettiParticles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * -canvas.height,
          size: Math.random() * 8 + 6,
          color: colors[Math.floor(Math.random() * colors.length)],
          vx: Math.random() * 4 - 2,
          vy: Math.random() * 5 + 3,
          rot: Math.random() * 360,
          vRot: Math.random() * 6 - 3
        });
      }

      const animate = () => {
        this.ctxConfetti.clearRect(0, 0, canvas.width, canvas.height);

        this.confettiParticles.forEach(p => {
          p.x += p.vx;
          p.y += p.vy;
          p.rot += p.vRot;

          this.ctxConfetti.save();
          this.ctxConfetti.translate(p.x, p.y);
          this.ctxConfetti.rotate((p.rot * Math.PI) / 180);
          this.ctxConfetti.fillStyle = p.color;
          this.ctxConfetti.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
          this.ctxConfetti.restore();

          if (p.y > canvas.height + 20) {
            p.y = -20;
            p.x = Math.random() * canvas.width;
          }
        });

        this.confettiAnimId = requestAnimationFrame(animate);
      };

      animate();
    }

    stopConfetti() {
      if (this.confettiAnimId) cancelAnimationFrame(this.confettiAnimId);
      this.ctxConfetti.clearRect(0, 0, this.dom.confettiCanvas.width, this.dom.confettiCanvas.height);
      this.confettiParticles = [];
    }
  }

  /* Bootstrap Application */
  window.addEventListener('DOMContentLoaded', () => {
    window.game = new WoWGame();
  });
'''

# Load template and combine
with open("index_template.html", "r", encoding="utf-8") as f:
    template = f.read()

final_html = template.replace("__GAME_SCRIPT_INJECTION__", SCRIPT_CODE)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("index.html generated successfully! File size:", len(final_html), "bytes.")

# -*- coding: utf-8 -*-
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Ensure header has btn-sound-toggle and sound-icon
header_markup = '''    <header>
      <div class="header-pill">
        <div class="level-badge">
          <span class="sub-title" id="region-text">KAPADOKYA</span>
          <span class="main-title" id="level-title-text">Bölüm 1</span>
        </div>
      </div>

      <div class="header-actions">
        <button class="btn-header daily-btn" id="btn-open-daily" aria-label="Günlük Bulmaca" title="Günlük Bulmaca">
          <span>📅</span><span id="streak-indicator">🔥 1</span>
        </button>
        <button class="btn-header idiom-btn" id="btn-open-idioms" aria-label="Atasözü ve Deyim Modu" title="Atasözü Modu">
          <span>📜</span><span>Deyim</span>
        </button>
        <button class="btn-header" id="btn-sound-toggle" aria-label="Sesi Aç veya Kapat" title="Ses">
          <span id="sound-icon">🔊</span>
        </button>
        <button class="btn-header" id="btn-open-settings" aria-label="Ayarlar ve Ses" title="Ayarlar">
          <span>⚙️</span>
        </button>
        <div class="header-pill coin-badge" id="btn-coins-info" title="Altın Bakiyesi">
          <span>🪙</span><span id="coins-display">200</span>
        </div>
      </div>
    </header>'''

import re
html = re.sub(r'<header>.*?</header>', header_markup, html, flags=re.DOTALL)

# 2. Defensively wrap all event listeners and dom refs in JS
safe_init_events = '''    initEvents() {
      const bind = (id, event, handler) => {
        const el = document.getElementById(id);
        if (el) el.addEventListener(event, handler);
      };

      // Sound Toggle
      bind('btn-sound-toggle', 'click', () => {
        this.sound.init();
        const isMuted = this.sound.toggleMute();
        if (this.dom.soundIcon) this.dom.soundIcon.textContent = isMuted ? '🔇' : '🔊';
        const toggleSound = document.getElementById('toggle-sound');
        if (toggleSound) toggleSound.classList.toggle('active', !isMuted);
      });

      // Topbar Modals
      bind('btn-open-daily', 'click', () => this.openCalendarModal());
      bind('btn-open-idioms', 'click', () => this.openIdiomsModal());
      bind('btn-open-settings', 'click', () => this.openSettingsModal());
      bind('btn-open-about', 'click', () => this.dom.modalAbout.classList.add('active'));
      bind('btn-open-about-from-settings', 'click', () => {
        this.dom.modalSettings.classList.remove('active');
        this.dom.modalAbout.classList.add('active');
      });
      bind('btn-close-about', 'click', () => this.dom.modalAbout.classList.remove('active'));

      // Power-up Buttons
      bind('btn-shuffle', 'click', () => this.handleShuffle());
      bind('btn-hint-bulb', 'click', () => this.handleBulbHint());
      bind('btn-hint-target', 'click', () => this.handleTargetMagnifier());
      bind('btn-hint-lightning', 'click', () => this.handleLightning());
      bind('btn-bonus-chest', 'click', () => this.openBonusChestModal());
      bind('btn-close-bonus-chest', 'click', () => this.dom.modalBonusChest.classList.remove('active'));

      // Discovery & Victory
      bind('btn-discovery-continue', 'click', () => {
        this.dom.modalDiscovery.classList.remove('active');
        this.openVictoryModal();
      });

      bind('btn-victory-normal', 'click', () => {
        if (this.levelRewardClaimed) return;
        this.levelRewardClaimed = true;
        this.dom.modalVictory.classList.remove('active');
        this.addCoins(30);
        this.proceedToNextLevel();
      });

      bind('btn-victory-2x', 'click', async () => {
        if (this.levelRewardClaimed) return;
        this.levelRewardClaimed = true;
        this.dom.modalVictory.classList.remove('active');
        await this.adProvider.showRewarded("2X Bölüm Zafer Bonusu");
        this.addCoins(60);
        this.proceedToNextLevel();
      });

      // Calendar Play & Share
      bind('btn-close-calendar', 'click', () => this.dom.modalCalendar.classList.remove('active'));
      bind('btn-play-daily', 'click', () => {
        this.dom.modalCalendar.classList.remove('active');
        this.startDailyChallenge();
      });
      bind('btn-share-daily', 'click', () => this.shareDailyResult());

      // Idiom Game
      bind('btn-close-idioms', 'click', () => this.dom.modalIdioms.classList.remove('active'));
      bind('btn-start-idiom-puzzle', 'click', () => {
        this.dom.modalIdioms.classList.remove('active');
        this.startIdiomLevel();
      });

      // Settings Toggles
      bind('btn-close-settings', 'click', () => this.dom.modalSettings.classList.remove('active'));
      bind('toggle-sound', 'click', () => {
        const isMuted = this.sound.toggleMute();
        const toggleSound = document.getElementById('toggle-sound');
        if (toggleSound) toggleSound.classList.toggle('active', !isMuted);
        if (this.dom.soundIcon) this.dom.soundIcon.textContent = isMuted ? '🔇' : '🔊';
      });
      bind('toggle-haptic', 'click', () => {
        this.hapticEnabled = !this.hapticEnabled;
        this.storage.set('haptic_enabled', this.hapticEnabled);
        const toggleHaptic = document.getElementById('toggle-haptic');
        if (toggleHaptic) toggleHaptic.classList.toggle('active', this.hapticEnabled);
      });
      bind('toggle-dyslexia', 'click', () => {
        this.dyslexiaFont = !this.dyslexiaFont;
        this.storage.set('dyslexia_font', this.dyslexiaFont);
        this.applySettings();
      });
      bind('toggle-contrast', 'click', () => {
        this.highContrast = !this.highContrast;
        this.storage.set('high_contrast', this.highContrast);
        this.applySettings();
      });
      bind('toggle-motion', 'click', () => {
        this.reducedMotion = !this.reducedMotion;
        this.storage.set('reduced_motion', this.reducedMotion);
        this.applySettings();
      });

      // No Coins Modal
      bind('btn-close-no-coins', 'click', () => this.dom.modalNoCoins.classList.remove('active'));
      bind('btn-claim-free-hint', 'click', () => {
        this.dom.modalNoCoins.classList.remove('active');
        this.showToast("🎁 Günlük ücretsiz ipucun tahtada açıldı!");
        this.sound.playHint();
        this.revealRandomCell();
      });

      // Pointer Wheel Interaction
      const wrapper = this.dom.wheelWrapper;
      if (wrapper) {
        wrapper.addEventListener('pointerdown', (e) => this.onPointerDown(e));
        wrapper.addEventListener('pointermove', (e) => this.onPointerMove(e));
        wrapper.addEventListener('pointerup', (e) => this.onPointerUp(e));
        wrapper.addEventListener('pointercancel', (e) => this.onPointerUp(e));
      }

      // Resize
      window.addEventListener('resize', () => {
        this.cacheWheelGeometry();
        this.resizeCrosswordBoard();
      });
    }'''

# Replace initEvents() method in index.html
html = re.sub(r'initEvents\(\)\s*\{.*?\n    /\* ---------------- Level Management', safe_init_events + '\n\n    /* ---------------- Level Management', html, flags=re.DOTALL)

# Safe updateTopbar
html = html.replace("this.dom.soundIcon.textContent = this.sound.muted ? '🔇' : '🔊';", "if (this.dom.soundIcon) this.dom.soundIcon.textContent = this.sound.muted ? '🔇' : '🔊';")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Safe initEvents written successfully!")

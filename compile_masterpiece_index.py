# -*- coding: utf-8 -*-
"""
Compile Masterpiece Index for Kelime Harikaları
"""
import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('credits.json', 'r', encoding='utf-8') as f:
    credits_data = json.load(f)

with open('levels_100.json', 'r', encoding='utf-8') as f:
    levels_data = json.load(f)

with open('tdk_dict.json', 'r', encoding='utf-8') as f:
    tdk_dict = json.load(f)

print(f"Data ready: {len(credits_data)} credits, {len(levels_data)} levels, {len(tdk_dict)} dict words.")

# 1. Update CREDITS_DATA and LEVELS_DATA and inject TDK_DICTIONARY
credits_json_str = json.dumps(credits_data, ensure_ascii=False)
levels_json_str = json.dumps(levels_data, ensure_ascii=False)
tdk_json_str = json.dumps(tdk_dict, ensure_ascii=False)

html = re.sub(
    r'const CREDITS_DATA\s*=\s*\[.*?\];',
    f'const CREDITS_DATA = {credits_json_str};',
    html,
    count=1
)

html = re.sub(
    r'const LEVELS_DATA\s*=\s*\[.*?\];',
    f'const LEVELS_DATA = {levels_json_str};\n  const TDK_DICTIONARY = {tdk_json_str};',
    html,
    count=1
)

# 2. Update #bg-layer CSS to ensure 100% full-screen fit on all devices
bg_css_old = r'#bg-layer\s*\{[^}]+\}'
bg_css_new = '''#bg-layer {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      height: 100dvh;
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
      filter: brightness(0.65) saturate(1.25);
      transition: background-image 0.7s cubic-bezier(0.4, 0, 0.2, 1);
      z-index: 0;
    }'''
html = re.sub(bg_css_old, bg_css_new, html, count=1)

# 3. Add #modal-meaning to HTML modals section if not present
if 'id="modal-meaning"' not in html:
    meaning_modal_html = '''
  <!-- 8. TDK Word Meaning Modal -->
  <div class="modal-overlay" id="modal-meaning" role="dialog" aria-modal="true">
    <div class="modal-card" style="max-width: 350px; padding: 20px;">
      <div style="font-size: 32px; margin-bottom: 4px;">📖</div>
      <h2 id="meaning-word-title" style="font-size: 22px; font-weight: 900; margin-bottom: 2px; color: #fef08a; letter-spacing: 1px;">KELİME</h2>
      <span id="meaning-word-type" style="font-size: 11px; font-weight: 800; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.6px;">TDK GÜNCEL SÖZLÜK</span>
      <div id="meaning-word-desc" style="font-size: 13.5px; line-height: 1.5; color: #e2e8f0; margin: 14px 0; text-align: left; background: rgba(15, 23, 42, 0.7); padding: 14px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.12);">
        Kelime açıklaması...
      </div>
      <button class="btn-secondary" id="btn-close-meaning" style="margin-top: 6px;">Kapat</button>
    </div>
  </div>
'''
    html = html.replace('<!-- Modals -->', '<!-- Modals -->' + meaning_modal_html)

# 4. Enhance SoundManager with gentle level chime & warm milestone fanfare
old_sound_methods = r'playFanfare\(\)\s*\{[^}]+(\}[^}]+){1,2}\}'
new_sound_methods = '''playLevelChime() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      // Soft, warm, soothing 3-note harmonic arpeggio (C5 -> E5 -> G5)
      const notes = [523.25, 659.25, 783.99];
      notes.forEach((freq, idx) => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        const t = this.ctx.currentTime + idx * 0.09;
        osc.frequency.setValueAtTime(freq, t);
        gain.gain.setValueAtTime(0.12, t);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.38);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(t);
        osc.stop(t + 0.38);
      });
    }

    playMilestoneFanfare() {
      if (this.muted) return;
      this.init();
      if (!this.ctx) return;
      // Rich celebratory chord for 5-level milestones
      const motif = [
        { f: 523.25, t: 0.0, d: 0.2 },
        { f: 659.25, t: 0.12, d: 0.22 },
        { f: 783.99, t: 0.24, d: 0.26 },
        { f: 1046.50, t: 0.40, d: 0.6 }
      ];
      motif.forEach(m => {
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        const startTime = this.ctx.currentTime + m.t;
        osc.frequency.setValueAtTime(m.f, startTime);
        gain.gain.setValueAtTime(0.18, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + m.d);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(startTime);
        osc.stop(startTime + m.d);
      });
    }'''

# Replace playFanfare with the new sound methods
html = re.sub(r'playFanfare\(\)\s*\{[\s\S]*?^\s*\}', new_sound_methods, html, flags=re.MULTILINE)

# 5. Update triggerVictory logic:
# Levels 1, 2, 3, 4: gentle chime + toast + auto-advance
# Level 5, 10, 15...: milestone fanfare + confetti + discovery card!
new_victory_logic = '''triggerVictory() {
      // Daily streak management
      if (this.isDailyMode) {
        const todayStr = Turkish.getIstanbulDateString();
        const yesterdayStr = Turkish.getYesterdayIstanbulString();

        if (!this.completedDailyDates.includes(todayStr)) {
          if (this.completedDailyDates.includes(yesterdayStr)) {
            this.streak++;
          } else {
            this.streak = 1;
          }
          this.completedDailyDates.push(todayStr);
          this.storage.set('daily_dates', this.completedDailyDates);
          this.storage.set('streak', this.streak);
          this.updateTopbar();
        }
        this.sound.playMilestoneFanfare();
        this.startConfetti();
        this.openVictoryModal();
        return;
      }

      if (this.isIdiomMode) {
        this.sound.playLevelChime();
        this.addCoins(25);
        this.showToast("🎉 Tebrikler! Atasözü Tamamlandı (+25 🪙)");
        setTimeout(() => this.openNextIdiom(), 1200);
        return;
      }

      // REGULAR GAMEPLAY MODE:
      const levelNumber = this.levelIdx + 1;
      const isMilestone = (levelNumber % 5 === 0);

      if (isMilestone) {
        // Milestone reached! (Level 5, 10, 15, 20...)
        this.sound.playMilestoneFanfare();
        this.startConfetti();

        // Calculate Stars
        let starCount = 3;
        let evalText = "Harika! Sıfır ipucu ile kusursuz tamamladın.";
        if (this.levelHintsUsed > 1 || this.levelErrorCount > 4) {
          starCount = 1;
          evalText = "Zorlu bir mücadeleydi, tebrikler!";
        } else if (this.levelHintsUsed > 0 || this.levelErrorCount > 1) {
          starCount = 2;
          evalText = "Çok iyi performans!";
        }
        if (this.dom.victoryStarsDisplay) {
          this.dom.victoryStarsDisplay.textContent = '⭐'.repeat(starCount) + '☆'.repeat(3 - starCount);
        }

        const credit = CREDITS_DATA.find(c => c.id === this.currentLevel.region_id) || CREDITS_DATA[0];
        this.openDiscoveryCard(credit);
      } else {
        // Ordinary level: Seamless, pleasant, addictive auto-progression!
        this.sound.playLevelChime();
        this.addCoins(25);
        this.showToast(`🎉 Bölüm ${levelNumber} Tamamlandı! (+25 🪙)`);
        
        // Brief tile sparkle
        document.querySelectorAll('.crossword-cell.revealed .cell-back').forEach(el => {
          el.style.boxShadow = '0 0 16px rgba(251, 191, 36, 0.9)';
          setTimeout(() => {
            el.style.boxShadow = '';
          }, 800);
        });

        setTimeout(() => {
          this.advanceToNextLevel();
        }, 1100);
      }
    }'''

html = re.sub(
    r'triggerVictory\(\)\s*\{[\s\S]*?openVictoryModal\(\);\s*\}',
    new_victory_logic,
    html
)

# 6. Add onCellClicked TDK Meaning interaction & showWordMeaningModal method
old_cell_clicked = r'onCellClicked\(cellKey\)\s*\{[\s\S]*?this\.isTargetingMode\s*=\s*false;'
new_cell_clicked = '''onCellClicked(cellKey) {
      if (!this.isTargetingMode) {
        // Non-targeting click: If cell is revealed, show authentic TDK word meaning!
        if (this.revealedCellKeys.has(cellKey)) {
          const cellData = this.gridLetterMap.get(cellKey);
          if (cellData && cellData.words && cellData.words.length > 0) {
            const unlockedWord = cellData.words.find(w => this.unlockedWordIds.has(w.id)) || cellData.words[0];
            if (unlockedWord) {
              this.showWordMeaningModal(unlockedWord.word);
            }
          }
        }
        return;
      }
      if (this.revealedCellKeys.has(cellKey)) {
        this.showToast("Bu kutucuk zaten açık!");
        return;
      }

      this.coins -= 90;
      this.storage.set('coins', this.coins);
      this.updateTopbar();
      this.sound.playHint();
      this.levelHintsUsed++;

      this.isTargetingMode = false;'''

html = re.sub(old_cell_clicked, new_cell_clicked, html)

# Add showWordMeaningModal method to class
meaning_methods = '''
    showWordMeaningModal(rawWord) {
      const word = Turkish.toUpper(rawWord);
      const dictEntry = (typeof TDK_DICTIONARY !== 'undefined' && TDK_DICTIONARY[word]) ? TDK_DICTIONARY[word] : {
        type: "TDK GÜNCEL SÖZLÜK",
        meaning: `"${word}" sözcüğü: Türk Dil Kurumu standartlarına uygun, Türkçe kökenli veya dilimize yerleşmiş geçerli sözcük.`
      };

      const modal = document.getElementById('modal-meaning');
      if (!modal) return;
      document.getElementById('meaning-word-title').textContent = word;
      document.getElementById('meaning-word-type').textContent = dictEntry.type || "TDK GÜNCEL SÖZLÜK";
      document.getElementById('meaning-word-desc').textContent = dictEntry.meaning;
      modal.classList.add('active');
    }
'''

if 'showWordMeaningModal(' not in html:
    html = html.replace('advanceToNextLevel() {', meaning_methods + '\n    advanceToNextLevel() {')

# Bind close meaning modal button
if 'btn-close-meaning' not in html:
    bind_meaning_code = '''
      const btnCloseMeaning = document.getElementById('btn-close-meaning');
      const modalMeaning = document.getElementById('modal-meaning');
      if (btnCloseMeaning && modalMeaning) {
        btnCloseMeaning.addEventListener('click', () => modalMeaning.classList.remove('active'));
        modalMeaning.addEventListener('click', (e) => {
          if (e.target === modalMeaning) modalMeaning.classList.remove('active');
        });
      }
'''
    html = html.replace('this.dom.btnCloseSettings.addEventListener', bind_meaning_code + '\n      this.dom.btnCloseSettings.addEventListener')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Masterpiece compilation finished successfully!")

# -*- coding: utf-8 -*-
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Complete Header with all IDs so nothing is null
complete_header = '''    <header>
      <div class="header-pill level-pill">
        <div class="level-badge">
          <span class="sub-title" id="region-text">KAPADOKYA</span>
          <span class="main-title" id="level-title-text">Bölüm 1</span>
        </div>
      </div>

      <div class="header-actions">
        <button class="btn-header daily-btn" id="btn-open-daily" aria-label="Günlük Bulmaca" title="Günlük Bulmaca">
          <span>📅</span><span id="streak-indicator">🔥1</span>
        </button>
        <button class="btn-header idiom-btn" id="btn-open-idioms" aria-label="Atasözü ve Deyim Modu" title="Atasözü Modu">
          <span>📜</span>
        </button>
        <button class="btn-header" id="btn-sound-toggle" aria-label="Sesi Aç veya Kapat" title="Ses">
          <span id="sound-icon">🔊</span>
        </button>
        <button class="btn-header" id="btn-open-settings" aria-label="Ayarlar" title="Ayarlar">
          <span>⚙️</span>
        </button>
        <button class="btn-header" id="btn-open-about" aria-label="Hakkında" title="Hakkında">
          <span>ℹ️</span>
        </button>
        <div class="header-pill coin-badge" id="btn-coins-info" title="Altın Bakiyesi">
          <span>🪙</span><span id="coins-display">200</span>
        </div>
      </div>
    </header>'''

html = re.sub(r'<header>.*?</header>', complete_header, html, flags=re.DOTALL)

# 2. Add safe event binding in JS: wrap every addEventListener with `if (el)`
html = html.replace("document.getElementById('btn-sound-toggle').addEventListener", "const btnSound = document.getElementById('btn-sound-toggle'); if (btnSound) btnSound.addEventListener")
html = html.replace("document.getElementById('btn-open-about').addEventListener", "const btnAbout = document.getElementById('btn-open-about'); if (btnAbout) btnAbout.addEventListener")

# 3. Compact CSS
css_fix = '''
    /* Header Responsive Layout */
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      height: 42px;
      gap: 3px;
      flex-shrink: 0;
    }
    .level-pill {
      flex: 0 0 auto;
      padding: 3px 8px !important;
    }
    .level-badge .sub-title {
      font-size: 8.5px !important;
    }
    .level-badge .main-title {
      font-size: 11.5px !important;
      max-width: 70px !important;
    }
    .header-actions {
      display: flex;
      align-items: center;
      gap: 3px;
      flex-shrink: 0;
    }
    .btn-header {
      min-width: 28px !important;
      height: 28px !important;
      padding: 2px 5px !important;
      font-size: 10.5px !important;
      border-radius: 999px !important;
    }
    .coin-badge {
      padding: 3px 7px !important;
      font-size: 11px !important;
    }

    /* Powerups Toolbar Compact */
    #powerups-toolbar {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      max-width: 310px;
      margin: 0 auto 4px auto;
      padding: 0;
      gap: 8px;
    }
    .btn-powerup, .bonus-chest-btn {
      flex: 0 0 44px !important;
      width: 44px !important;
      min-width: 44px !important;
      max-width: 44px !important;
      height: 44px !important;
      border-radius: 12px !important;
      padding: 1px !important;
      box-sizing: border-box !important;
    }
'''

# Replace header and toolbar css
html = re.sub(r'/\* Header Styles \*/.*?/\* Wheel Container \*/', css_fix + '\n    /* Wheel Container */', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Applied fix_all_elements successfully!")

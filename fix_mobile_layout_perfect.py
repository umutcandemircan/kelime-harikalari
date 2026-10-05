# -*- coding: utf-8 -*-
"""
Perfect Mobile-First Layout Cleaner for Kelime Harikaları
Ensures 100% visible elements on 360x800 and all screens.
"""
import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Clean Header Structure
new_header = '''    <header>
      <div class="header-pill level-pill">
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
        <div class="header-pill coin-badge" id="btn-coins-info" title="Altın Bakiyesi">
          <span>🪙</span><span id="coins-display">200</span>
        </div>
        <button class="btn-header" id="btn-open-settings" aria-label="Ayarlar ve Ses" title="Ayarlar">
          <span>⚙️</span>
        </button>
      </div>
    </header>'''

# Replace whatever <header>...</header> is currently in index.html
html = re.sub(r'<header>.*?</header>', new_header, html, flags=re.DOTALL)

# 2. Clean Power-ups CSS: Replace all toolbar & button styles with single consolidated block
toolbar_css = '''
    /* Consolidated Powerups Toolbar */
    #powerups-toolbar {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      max-width: 330px;
      margin: 0 auto 4px auto;
      padding: 0;
      gap: 7px;
    }

    .btn-powerup, .bonus-chest-btn {
      flex: 0 0 46px !important;
      width: 46px !important;
      max-width: 46px !important;
      height: 46px !important;
      border-radius: 12px !important;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: #fff;
      border: 1.5px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
      padding: 2px !important;
      transition: transform 0.15s, border-color 0.2s;
    }
    .btn-powerup:active, .bonus-chest-btn:active {
      transform: scale(0.92);
    }
    .btn-powerup {
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.96));
    }
    .bonus-chest-btn {
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.4), rgba(126, 34, 206, 0.7));
      border-color: rgba(216, 180, 254, 0.5) !important;
    }
    .btn-powerup .icon, .bonus-chest-btn .icon {
      font-size: 16px;
      line-height: 1;
    }
    .btn-powerup .cost, .bonus-chest-btn .counter {
      font-size: 8.5px;
      font-weight: 800;
      color: #fef08a;
      margin-top: 1px;
      display: flex;
      align-items: center;
      gap: 1px;
    }
    .bonus-chest-btn .counter {
      color: #f3e8ff;
    }
    .btn-powerup.active-tool {
      border-color: #38bdf8 !important;
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.8) !important;
      background: rgba(14, 165, 233, 0.35) !important;
    }
'''

# Remove duplicate toolbar CSS
html = re.sub(r'#powerups-toolbar\s*\{[^}]+\}', '', html)
html = re.sub(r'\.btn-powerup\s*\{[^}]+\}', '', html)
html = re.sub(r'\.bonus-chest-btn\s*\{[^}]+\}', '', html)

# Insert clean toolbar CSS before /* Wheel Container */
html = html.replace('/* Wheel Container */', toolbar_css + '\n    /* Wheel Container */')

# 3. Clean Header CSS
header_css = '''
    /* Header Styles */
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 46px;
      gap: 6px;
      flex-shrink: 0;
      width: 100%;
    }
    .level-pill {
      flex: 0 0 auto;
      max-width: 110px;
    }
    .header-actions {
      display: flex;
      align-items: center;
      gap: 5px;
      flex-shrink: 0;
    }
    .btn-header {
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 3px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 999px;
      padding: 4px 8px;
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      height: 32px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.25);
      transition: transform 0.15s;
    }
    .btn-header:active {
      transform: scale(0.92);
    }
    .btn-header.daily-btn {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.35), rgba(217, 119, 6, 0.55));
      border-color: rgba(245, 158, 11, 0.7);
      color: #fef08a;
    }
    .btn-header.idiom-btn {
      background: linear-gradient(135deg, rgba(168, 85, 247, 0.35), rgba(126, 34, 206, 0.55));
      border-color: rgba(168, 85, 247, 0.7);
      color: #f3e8ff;
    }
'''

html = re.sub(r'header\s*\{[^}]+\}', '', html)
html = re.sub(r'\.header-actions\s*\{[^}]+\}', '', html)
html = re.sub(r'\.btn-header\s*\{[^}]+\}', '', html)

# Insert clean header CSS before .header-pill
html = html.replace('.header-pill {', header_css + '\n    .header-pill {')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Applied perfect mobile layout!")

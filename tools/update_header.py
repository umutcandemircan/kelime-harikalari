# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Header Markup for perfect responsive fit
old_header_markup = '''    <header>
      <div class="header-pill">
        <div class="level-badge">
          <span class="sub-title" id="region-text">KAPADOKYA</span>
          <span class="main-title" id="level-title-text">Bölüm 1</span>
        </div>
      </div>

      <div class="header-actions">
        <!-- Daily Challenge Button -->
        <button class="btn-header daily-btn" id="btn-open-daily" aria-label="Günlük Bulmaca">
          <span>📅</span><span class="btn-text-label"> Günlük </span><span id="streak-indicator">🔥 1</span>
        </button>

        <!-- Proverbs Mode Button -->
        <button class="btn-header idiom-btn" id="btn-open-idioms" aria-label="Atasözü ve Deyim Modu">
          <span>📜</span><span class="btn-text-label"> Deyim</span>
        </button>

        <!-- Settings Button -->
        <button class="btn-header" id="btn-open-settings" aria-label="Ayarlar">
          <span>⚙️</span>
        </button>

        <!-- About Button -->
        <button class="btn-header" id="btn-open-about" aria-label="Hakkında ve Kaynaklar">
          <span>ℹ️</span>
        </button>

        <!-- Sound Toggle -->
        <button class="btn-header" id="btn-sound-toggle" aria-label="Sesi Aç veya Kapat">
          <span id="sound-icon">🔊</span>
        </button>

        <!-- Coins Badge -->
        <div class="header-pill coin-badge" id="btn-coins-info" title="Altın Bakiyesi">
          <span>🪙</span> <span id="coins-display">200</span>
        </div>
      </div>
    </header>'''

new_header_markup = '''    <header>
      <div class="header-pill" style="flex-shrink:0;">
        <div class="level-badge">
          <span class="sub-title" id="region-text">KAPADOKYA</span>
          <span class="main-title" id="level-title-text">Bölüm 1</span>
        </div>
      </div>

      <div class="header-actions">
        <button class="btn-header daily-btn" id="btn-open-daily" aria-label="Günlük Bulmaca" title="Günlük Bulmaca">
          <span>📅</span><span id="streak-indicator">🔥1</span>
        </button>
        <button class="btn-header idiom-btn" id="btn-open-idioms" aria-label="Atasözü ve Deyim" title="Atasözü Modu">
          <span>📜</span>
        </button>
        <button class="btn-header" id="btn-open-settings" aria-label="Ayarlar" title="Ayarlar">
          <span>⚙️</span>
        </button>
        <button class="btn-header" id="btn-open-about" aria-label="Hakkında" title="Hakkında">
          <span>ℹ️</span>
        </button>
        <button class="btn-header" id="btn-sound-toggle" aria-label="Sesi Aç veya Kapat" title="Ses">
          <span id="sound-icon">🔊</span>
        </button>
        <div class="header-pill coin-badge" id="btn-coins-info" title="Altın Bakiyesi">
          <span>🪙</span><span id="coins-display">200</span>
        </div>
      </div>
    </header>'''

if old_header_markup in html:
    html = html.replace(old_header_markup, new_header_markup)
else:
    print("WARNING: Header markup not found exactly as string, checking regex...")

# Also update CSS for powerups-toolbar
old_css_search = '''    #powerups-toolbar {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      max-width: 350px;
      margin: 0 auto 4px auto;
      padding: 0 4px;
      gap: 8px;
    }'''

new_css_toolbar = '''    #powerups-toolbar {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      max-width: 340px;
      margin: 0 auto 4px auto;
      padding: 0 4px;
      gap: 8px;
    }

    .btn-powerup, .bonus-chest-btn {
      flex: 0 0 48px !important;
      width: 48px !important;
      max-width: 48px !important;
      height: 48px !important;
      border-radius: 14px !important;
      padding: 2px !important;
    }'''

if old_css_search in html:
    html = html.replace(old_css_search, new_css_toolbar)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Header & powerups markup updated.')

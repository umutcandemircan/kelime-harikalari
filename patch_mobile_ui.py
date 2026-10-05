# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix toolbar flex-grow and sizing
old_btn = '''    .btn-powerup, .bonus-chest-btn {
      width: 48px !important;
      min-width: 44px !important;
      max-width: 50px !important;
      height: 46px !important;
      padding: 2px !important;
    }'''

new_btn = '''    .btn-powerup, .bonus-chest-btn {
      flex: 0 0 46px !important;
      width: 46px !important;
      min-width: 42px !important;
      height: 46px !important;
      padding: 2px !important;
    }'''

if old_btn in html:
    html = html.replace(old_btn, new_btn)

header_fix = '''
    @media (max-width: 420px) {
      .btn-header .btn-text-label { display: none !important; }
      .btn-header { padding: 4px 6px !important; min-width: 32px !important; font-size: 11px !important; }
      .level-badge .main-title { max-width: 72px !important; font-size: 11px !important; }
      .header-pill { padding: 4px 6px !important; font-size: 11px !important; }
    }
'''

if '/* Crossword Board Area */' in html and '@media (max-width: 420px)' not in html:
    html = html.replace('/* Crossword Board Area */', header_fix + '\n    /* Crossword Board Area */')

# In HTML: wrap text in span.btn-text-label
html = html.replace('<span>📅</span> Günlük <span id="streak-indicator">', '<span>📅</span><span class="btn-text-label"> Günlük </span><span id="streak-indicator">')
html = html.replace('<span>📜</span> Deyim', '<span>📜</span><span class="btn-text-label"> Deyim</span>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Patched mobile UI successfully.')

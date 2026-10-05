import subprocess, os, sys

base = r"C:\Users\umutc\.gemini\antigravity\scratch\kelime-avcisi"
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
html = open(os.path.join(base, 'index.html'), encoding='utf-8').read()

def variant(name, screen, extra=''):
    h = html.replace("this.switchScreen('MENU');", f"this.switchScreen('{screen}');{extra}", 1)
    open(os.path.join(base, name), 'w', encoding='utf-8').write(h)

variant('shot_menu.html', 'MENU')
variant('shot_map.html', 'MAP_VIEW')
variant('shot_game.html', 'GAMEPLAY')

for page in ['shot_menu', 'shot_map', 'shot_game']:
    for (w, h, tag) in [(360, 800, 'm'), (1280, 800, 'd')]:
        wrap = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>*{{margin:0;padding:0}}
html,body{{width:{w}px;height:{h}px;overflow:hidden;background:#000}}iframe{{width:{w}px;height:{h}px;border:0}}</style></head>
<body><iframe src="{page}.html"></iframe></body></html>'''
        wp = os.path.join(base, f'wrap_{page}_{tag}.html')
        open(wp, 'w', encoding='utf-8').write(wrap)
        out = os.path.join(base, f'ss_{page}_{tag}.png')
        win = f'{max(w, 600)},{h}'
        subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        f'--window-size={win}', '--virtual-time-budget=6000',
                        f'--screenshot={out}', 'file:///' + wp.replace(os.sep, '/')],
                       capture_output=True, timeout=60)
        print('ok', out)

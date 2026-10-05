import subprocess
import time
import os

base_dir = r"C:\Users\umutc\.gemini\antigravity\scratch\kelime-avcisi"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def make_shot_file(screen_name, filename):
    with open(os.path.join(base_dir, 'index.html'), 'r', encoding='utf-8') as f:
        html = f.read()

    inject = f'''
<script>
window.addEventListener('load', () => {{
    setTimeout(() => {{
        if (window.game) {{
            window.game.switchScreen('{screen_name}');
        }}
    }}, 200);
}});
</script>
'''
    html_mod = html.replace('</body>', inject + '\n</body>')
    with open(os.path.join(base_dir, filename), 'w', encoding='utf-8') as f:
        f.write(html_mod)

make_shot_file('MENU', 'shot_menu.html')
make_shot_file('MAP_VIEW', 'shot_map.html')
make_shot_file('GAMEPLAY', 'shot_game.html')

screens = [
    ('shot_menu.html', 'screen_menu_mobile.png', 'screen_menu_desktop.png'),
    ('shot_map.html', 'screen_map_mobile.png', 'screen_map_desktop.png'),
    ('shot_game.html', 'screen_game_mobile.png', 'screen_game_desktop.png'),
]

for src, mob_out, dsk_out in screens:
    # Mobile 360x800
    subprocess.run([
        chrome_path,
        '--headless=new',
        '--disable-gpu',
        '--window-size=360,800',
        f'--screenshot={os.path.join(base_dir, mob_out)}',
        f'file:///{os.path.join(base_dir, src).replace(os.sep, "/")}'
    ])
    # Desktop 1280x800
    subprocess.run([
        chrome_path,
        '--headless=new',
        '--disable-gpu',
        '--window-size=1280,800',
        f'--screenshot={os.path.join(base_dir, dsk_out)}',
        f'file:///{os.path.join(base_dir, src).replace(os.sep, "/")}'
    ])

print("All screenshots generated!")

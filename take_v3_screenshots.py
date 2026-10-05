import subprocess
import os

base_dir = r"C:\Users\umutc\.gemini\antigravity\scratch\kelime-avcisi"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

with open(os.path.join(base_dir, 'index.html'), 'r', encoding='utf-8') as f:
    base_html = f.read()

# Menu (default)
with open(os.path.join(base_dir, 'shot_menu.html'), 'w', encoding='utf-8') as f:
    f.write(base_html)

# Map
map_html = base_html.replace("this.switchScreen('MENU');", "this.switchScreen('MAP_VIEW');")
with open(os.path.join(base_dir, 'shot_map.html'), 'w', encoding='utf-8') as f:
    f.write(map_html)

# Game
game_html = base_html.replace("this.switchScreen('MENU');", "this.switchScreen('GAMEPLAY');")
with open(os.path.join(base_dir, 'shot_game.html'), 'w', encoding='utf-8') as f:
    f.write(game_html)

screens = [
    ('shot_menu.html', 'screen_menu_v3_mobile.png', 'screen_menu_v3_desktop.png'),
    ('shot_map.html', 'screen_map_v3_mobile.png', 'screen_map_v3_desktop.png'),
    ('shot_game.html', 'screen_game_v3_mobile.png', 'screen_game_v3_desktop.png'),
]

for src, mob_out, dsk_out in screens:
    src_path = os.path.join(base_dir, src)
    # Mobile
    subprocess.run([
        chrome_path,
        '--headless=new',
        '--disable-gpu',
        '--window-size=360,800',
        f'--screenshot={os.path.join(base_dir, mob_out)}',
        f'file:///{src_path.replace(os.sep, "/")}'
    ])
    # Desktop
    subprocess.run([
        chrome_path,
        '--headless=new',
        '--disable-gpu',
        '--window-size=1280,800',
        f'--screenshot={os.path.join(base_dir, dsk_out)}',
        f'file:///{src_path.replace(os.sep, "/")}'
    ])

print("Screenshots taken successfully!")

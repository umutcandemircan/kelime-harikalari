import re
import json

# 1. Purge from HTML
html_path = 'src/template.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the entire div with class wax-seal
html = re.sub(r'<div class="wax-seal"[\s\S]*?</div>', '', html)
html = re.sub(r'<div class="stars-row"[\s\S]*?</div>', '', html)
html = html.replace('★', '')
html = html.replace('id="post-stars"', '')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Purge from CSS
css_path = 'src/css/main.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(r'\.wax-seal\s*\{[\s\S]*?\}\n?', '', css)
css = re.sub(r'\.wax-seal\s+span\s*\{[\s\S]*?\}\n?', '', css)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Fix image URL
target_url = 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=800&q=80'
def patch_file(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        for city in data:
            if city.get('plate') == 34:
                for lvl in city.get('levels', []):
                    if 'Ayasofya' in lvl.get('landmark', ''):
                        lvl['bg'] = target_url
                    if 'Ayasofya' in lvl.get('postcard', {}).get('landmark', ''):
                        lvl['postcard']['bg'] = target_url
    elif isinstance(data, dict):
        keys = list(data.keys())
        for k in keys:
            if 'Ayasofya' in k:
                data[k] = target_url
            
    with open(file_path, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

patch_file('src/data/unified_cities.json')
patch_file('src/data/resolved_landmark_photos.json')

print("Purge complete")

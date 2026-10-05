import os
import json
import glob

def build():
    print("Building Sözcük Seferî V1 (Production)...")
    
    # 1. Read the template
    with open('src/template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # 2. Read and inject CSS
    css_files = glob.glob('src/css/*.css')
    css_content = ""
    for css_file in css_files:
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content += f.read() + "\n"
    
    template = template.replace('{{ INJECT_CSS }}', css_content)

    # 3. Read Data and build JS context
    with open('src/data/unified_cities.json', 'r', encoding='utf-8') as f:
        unified_cities = f.read()
    with open('src/data/tdk_dict.json', 'r', encoding='utf-8') as f:
        tdk_dict = f.read()
    with open('src/data/idioms.json', 'r', encoding='utf-8') as f:
        idioms = f.read()
    
    # We will prepend this dataset block to the JS
    js_data = f"""
// --- AUTO-GENERATED DATASETS ---
const CITIES = {unified_cities};
const TDK_DICT_FULL = {tdk_dict};
const IDIOMS = {idioms};
"""

    # 4. Read JS Modules in order
    js_order = [
        'src/js/core/utils.js',
        'src/js/core/SaveManager.js',
        'src/js/core/AudioEngine.js',
        'src/js/game/MapEngine.js',
        'src/js/game/GameEngine.js',
        'src/js/game/IdiomEngine.js',
        'src/js/App.js'
    ]
    
    js_content = js_data
    for js_file in js_order:
        if os.path.exists(js_file):
            with open(js_file, 'r', encoding='utf-8') as f:
                js_content += f"\n// --- {os.path.basename(js_file)} ---\n"
                js_content += f.read() + "\n"
        else:
            print(f"Warning: Missing JS module {js_file}")

    template = template.replace('{{ INJECT_JS }}', js_content)

    # 5. Build SVG Map Paths
    with open('src/data/turkey_svg_map.json', 'r', encoding='utf-8') as f:
        map_data = json.load(f)
    
    svg_paths = ""
    for p in map_data:
        svg_paths += f'<path d="{p["d"]}" id="p{p["plate"]}" class="province-path" data-plate="{p["plate"]}" data-name="{p["name"]}"></path>\n'
    
    template = template.replace('{{ INJECT_MAP_PATHS }}', svg_paths)

    # 6. Write final output
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"Build complete! Size: {os.path.getsize('index.html')} bytes")

if __name__ == '__main__':
    build()

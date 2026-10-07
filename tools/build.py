import os
import json
import glob
import re
import sys
import subprocess
from collections import Counter

sys.path.append('tests')
sys.path.append('tools')
from validate_strict_crossword import validate_crossword

sys.stdout.reconfigure(encoding='utf-8')

def build():
    print("=== SÖZCÜK SEFERÎ PRODUCTION BUILD PIPELINE ===")
    
    # 1. Read and validate template
    print("[1/6] Reading and validating src/template.html...")
    with open('src/template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    corruptions = [
        'Açpp', 'Seçfer', 'AçNAç', 'Açudio', 'AçLTIN', 'DEVAçM', 'KAçPAçT',
        'TAçMAçM', 'VAçZGE', 'BULMAçCAç', 'Menüü', 'Seçttings', 'Açntik',
        'Açd', 'Açfter', 'Seçvgi', 'Açç', 'Seçç', 'Sandığıığı', 'KAçRTPOSTAçLI',
        'CAçRD', 'MODAçL', 'JAçVAçSCRIPT'
    ]
    found_corrupt = [c for c in corruptions if c in template]
    if found_corrupt:
        print(f"FATAL: Template contains corrupted strings: {found_corrupt}")
        sys.exit(1)

    # 2. Read and inject CSS
    print("[2/6] Bundling CSS...")
    css_files = glob.glob('src/css/*.css')
    css_content = ""
    for css_file in sorted(css_files):
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content += f"/* --- {os.path.basename(css_file)} --- */\n" + f.read() + "\n"
    
    template = template.replace('{{ INJECT_CSS }}', css_content)

    # 3. Read Data and execute strict dataset audit
    print("[3/6] Auditing and bundling datasets...")
    with open('src/data/unified_cities.json', 'r', encoding='utf-8') as f:
        unified_cities_data = json.load(f)
    with open('src/data/tdk_dict.json', 'r', encoding='utf-8') as f:
        tdk_dict_data = json.load(f)
    with open('src/data/idioms.json', 'r', encoding='utf-8') as f:
        idioms_data = json.load(f)
    with open('src/data/world_cities.json', 'r', encoding='utf-8') as f:
        world_cities_data = json.load(f)
        
    tdk_set = set(tdk_dict_data)
    
    # Strict validation check
    total_levels = 0
    errors = []
    for c in unified_cities_data:
        for lidx, lvl in enumerate(c.get('levels', [])):
            total_levels += 1
            words = lvl.get('words', [])
            wheel = lvl.get('wheel', [])
            letters = lvl.get('letters', [])
            if not wheel or not letters:
                errors.append(f"{c['name']} L{lidx}: Missing wheel or letters")
            ok, reason = validate_crossword(words)
            if not ok:
                errors.append(f"{c['name']} L{lidx}: {reason}")
            w_cnt = Counter(letters)
            for w in words:
                for ch, req in Counter(w['word']).items():
                    if w_cnt[ch] < req:
                        errors.append(f"{c['name']} L{lidx}: Word '{w['word']}' unsolvable with {letters}")
                if w['word'] not in tdk_set:
                    errors.append(f"{c['name']} L{lidx}: Word '{w['word']}' not in TDK dictionary")
                    
    if errors:
        print(f"FATAL: Dataset failed strict validation! {len(errors)} errors found:")
        for e in errors[:10]:
            print(f"  - {e}")
        sys.exit(1)
        
    print(f"  -> All {total_levels} levels passed strict crossword geometry, solvability, and TDK membership!")

    # Compact JSON injection to save space and load fast
    cities_json_str = json.dumps(unified_cities_data, ensure_ascii=False)
    tdk_json_str = json.dumps(tdk_dict_data, ensure_ascii=False)
    idioms_json_str = json.dumps(idioms_data, ensure_ascii=False)
    world_cities_str = json.dumps(world_cities_data, ensure_ascii=False)

    js_data = f"""
// --- AUTO-GENERATED EMBEDDED DATASETS ---
const CITIES = {cities_json_str};
const TDK_DICT_FULL = {tdk_json_str};
const IDIOMS = {idioms_json_str};
const WORLD_CITIES = {world_cities_str};
if (typeof window !== 'undefined') {{
    window.CITIES = CITIES;
    window.TDK_DICT_FULL = TDK_DICT_FULL;
    window.IDIOMS = IDIOMS;
    window.WORLD_CITIES = WORLD_CITIES;
}}
"""

    # 4. Read JS Modules in order
    print("[4/6] Concatenating ES6 modular runtime...")
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
        if not os.path.exists(js_file):
            print(f"FATAL: Required JS module missing: {js_file}")
            sys.exit(1)
        with open(js_file, 'r', encoding='utf-8') as f:
            js_content += f"\n// --- MODULE: {os.path.basename(js_file)} ---\n"
            js_content += f.read() + "\n"

    template = template.replace('{{ INJECT_JS }}', js_content)

    # 5. Build SVG Map Paths
    print("[5/6] Generating SVG 81-province map layers...")
    with open('src/data/turkey_svg_map.json', 'r', encoding='utf-8') as f:
        map_data = json.load(f)
    
    svg_paths = ""
    for p in map_data:
        svg_paths += f'<path d="{p["d"]}" id="p{p["plate"]}" class="province-path" data-plate="{p["plate"]}" data-name="{p["name"]}"></path>\n'
    
    template = template.replace('{{ INJECT_MAP_PATHS }}', svg_paths)

    # 6. Safety Syntax Verification & Write
    print("[6/6] Verifying output integrity and writing index.html...")
    
    # Check that required IDs and elements are present
    required_ids = [
        'screen-hub', 'screen-map', 'screen-game', 'screen-idiom',
        'wheel-assembly', 'crossword-board', 'map-city-card',
        'modal-postcard', 'modal-daily', 'modal-settings', 'modal-insufficient-gold'
    ]
    for rid in required_ids:
        if f'id="{rid}"' not in template:
            print(f"FATAL: Missing critical element id in output: {rid}")
            sys.exit(1)
            
    # Verify no unresolved template placeholders
    unresolved = re.findall(r'\{\{\s*[A-Z_]+\s*\}\}', template)
    if unresolved:
        print(f"FATAL: Unresolved template placeholders detected: {unresolved}")
        sys.exit(1)
        
    # Write to temporary file first for safe verification
    temp_output = 'index.build.tmp.html'
    with open(temp_output, 'w', encoding='utf-8', newline='\n') as f:
        f.write(template)

    # Syntax test using node
    script_start = template.find('<script>') + len('<script>')
    script_end = template.rfind('</script>')
    raw_js = template[script_start:script_end]
    
    with open('temp_check.js', 'w', encoding='utf-8') as f:
        f.write(raw_js)
        
    try:
        subprocess.check_output(['node', '--check', 'temp_check.js'], stderr=subprocess.STDOUT)
        os.remove('temp_check.js')
    except subprocess.CalledProcessError as e:
        print(f"FATAL: JavaScript syntax error in built output:\n{e.output.decode('utf-8', errors='replace')}")
        if os.path.exists('temp_check.js'): os.remove('temp_check.js')
        if os.path.exists(temp_output): os.remove(temp_output)
        sys.exit(1)

    # Move verified temp file to index.html
    if os.path.exists('index.html'):
        os.replace(temp_output, 'index.html')
    else:
        os.rename(temp_output, 'index.html')

    out_size = os.path.getsize('index.html')
    print(f"\nBUILD SUCCESSFUL! index.html verified & written: {out_size} bytes ({out_size / 1024:.1f} KB)")

if __name__ == '__main__':
    build()

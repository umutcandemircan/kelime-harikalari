# -*- coding: utf-8 -*-
"""
Automated Comprehensive Audit for Kelime Harikaları (Phase 1)
"""
import json
import re
from collections import Counter

def run_audit():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    report = {}

    # 1. Dosya yapısı ve bağımlılıklar
    external_scripts = re.findall(r'<script\s+src=[\'"]([^\'"]+)[\'"]', html)
    external_styles = re.findall(r'<link\s+[^>]*href=[\'"]([^\'"]+)[\'"]', html)
    google_fonts = [s for s in external_styles if 'fonts.googleapis' in s]
    report['external_scripts'] = external_scripts
    report['google_fonts'] = google_fonts
    report['file_size_kb'] = len(html.encode('utf-8')) / 1024

    # Extract JS
    js_match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
    js = js_match.group(1) if js_match else ''

    # 2. LocalStorage and State
    ls_gets = re.findall(r'localStorage\.getItem\([\'"]([^\'"]+)[\'"]\)', js)
    ls_sets = re.findall(r'localStorage\.setItem\([\'"]([^\'"]+)[\'"]', js)
    has_try_catch_ls = 'try {' in js and 'localStorage' in js
    has_versioning = 'version' in js.lower() or 'migration' in js.lower()
    report['ls_keys'] = list(set(ls_gets + ls_sets))
    report['ls_try_catch'] = has_try_catch_ls
    report['ls_versioning'] = has_versioning

    # 3. Level Data & Solvability
    # Extract LEVELS_DATA and DAILY_LEVEL_DATA
    levels_match = re.search(r'const LEVELS_DATA\s*=\s*(\[.*?\]);\s*const DAILY_LEVEL_DATA', js, re.DOTALL)
    daily_match = re.search(r'const DAILY_LEVEL_DATA\s*=\s*(\{.*?\});\s*/\*', js, re.DOTALL)
    
    levels_solvability = []
    turkish_alpha = set("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ")
    non_turkish_chars = set()

    if levels_match and daily_match:
        try:
            levels = json.loads(levels_match.group(1))
            daily = json.loads(daily_match.group(1))
            all_levels = levels + [daily]
            
            for lvl in all_levels:
                lvl_id = lvl.get('id', 'daily')
                wheel = lvl.get('wheel', [])
                wheel_counter = Counter([ch.upper() for ch in wheel])
                
                # Check characters against Turkish alphabet
                for ch in wheel:
                    if ch.upper() not in turkish_alpha:
                        non_turkish_chars.add(ch)

                words_status = []
                words = lvl.get('words', [])
                bonus = lvl.get('bonus', [])

                for w in words:
                    word_str = w['word'].upper()
                    w_counter = Counter(word_str)
                    can_spell = True
                    for c, count in w_counter.items():
                        if wheel_counter[c] < count:
                            can_spell = False
                            break
                    words_status.append({'word': word_str, 'solvable': can_spell})

                for b in bonus:
                    b_str = b.upper()
                    b_counter = Counter(b_str)
                    can_spell = True
                    for c, count in b_counter.items():
                        if wheel_counter[c] < count:
                            can_spell = False
                            break
                    words_status.append({'word': b_str, 'is_bonus': True, 'solvable': can_spell})

                all_solvable = all(item['solvable'] for item in words_status)
                levels_solvability.append({
                    'id': lvl_id,
                    'title': lvl.get('title'),
                    'all_solvable': all_solvable,
                    'word_count': len(words),
                    'bonus_count': len(bonus),
                    'issues': [item for item in words_status if not item['solvable']]
                })
        except Exception as e:
            report['level_parse_error'] = str(e)

    report['levels_solvability'] = levels_solvability
    report['non_turkish_chars'] = list(non_turkish_chars)

    # 4. Turkish Locale Checks
    report['has_toLocaleUpperCase_tr'] = ".toLocaleUpperCase('tr-TR')" in js or '.toLocaleUpperCase("tr-TR")' in js
    report['has_toLocaleLowerCase_tr'] = ".toLocaleLowerCase('tr-TR')" in js or '.toLocaleLowerCase("tr-TR")' in js
    raw_to_upper = re.findall(r'\.toUpperCase\(\)', js)
    raw_to_lower = re.findall(r'\.toLowerCase\(\)', js)
    report['raw_toUpperCase_count'] = len(raw_to_upper)
    report['raw_toLowerCase_count'] = len(raw_to_lower)

    # 5. Pointer Events & Gestures
    report['has_pointerdown'] = 'pointerdown' in js
    report['has_pointermove'] = 'pointermove' in js
    report['has_pointerup'] = 'pointerup' in js
    report['has_setPointerCapture'] = 'setPointerCapture' in js
    report['viewport_user_scalable_no'] = 'user-scalable=no' in html
    report['viewport_max_scale'] = 'maximum-scale=1.0' in html

    # 6. Daily Challenge & Timezone
    report['uses_iso_split_date'] = "toISOString().split('T')[0]" in js
    report['has_timezone_istanbul'] = "Europe/Istanbul" in js
    report['is_daily_seeded'] = "seed" in js.lower() or "Math.sin" in js

    # 7. Ads & Placeholders
    report['has_words_of_wonders_phrase'] = "Words of Wonders" in html
    report['placeholder_texts'] = [
        t for t in ["Tarihi Yapı", "Eser hakkında kültürel bilgi burada yer alacak.", "BÖLGE"] if t in html
    ]
    report['has_ad_provider'] = "AdProvider" in js or "showRewarded" in js

    # 8. Unsplash Background Inspection
    bg_urls = re.findall(r'https://images\.unsplash\.com/[^\s\'"]+', js)
    report['bg_images_count'] = len(bg_urls)
    report['bg_urls'] = bg_urls

    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    run_audit()

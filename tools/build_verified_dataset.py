import json
import sys
import random
from collections import Counter

sys.path.append('tests')
sys.path.append('tools')
from validate_strict_crossword import validate_crossword
from find_strict_crosswords import find_strict_crossword

sys.stdout.reconfigure(encoding='utf-8')

def build_verified_dataset():
    print("=== BUILDING VERIFIED PRODUCTION DATASET FOR 81 PROVINCES ===")
    
    # 1. Load dependencies
    with open('src/data/turkey_svg_map.json', 'r', encoding='utf-8') as f:
        turkey_map = json.load(f)
        
    with open('src/data/cities_data.json', 'r', encoding='utf-8') as f:
        showcase_cities = json.load(f)
        
    with open('src/data/levels_100.json', 'r', encoding='utf-8') as f:
        levels_100 = json.load(f)
        
    with open('src/data/tdk_dict.json', 'r', encoding='utf-8') as f:
        tdk_dict = json.load(f)
        
    tdk_set = set(tdk_dict)
    
    # 2. Build showcase city lookup
    showcase_by_plate = {c['plate']: c for c in showcase_cities}
    
    # 3. Journey order across Turkey
    journey_order = [
        35, 45, 9, 48, 20, 7, 15, 32, 42, 70, 33, 1, 80, 31, 27, 79, 63, 2, 44, 23, 62, 24, 29, 61, 53, 8, 75, 36, 76, 65, 30, 73, 56, 72, 21, 47, 46, 58, 60, 52, 28, 55, 5, 19, 18, 37, 74, 78, 67, 81, 14, 26, 43, 64, 10, 17, 22, 39, 59, 34, 41, 54, 11, 16, 77, 6, 71, 40, 50, 68, 51, 66, 49, 13, 12, 69, 3, 4, 25, 38, 57
    ]
    for i in range(1, 82):
        if i not in journey_order:
            journey_order.append(i)
            
    # Pool of pre-verified level layouts from levels_100
    pool_levels = []
    for lvl in levels_100:
        pool_levels.append({
            "words": lvl["words"],
            "wheel": list(lvl["wheel"]),
            "letters": list(lvl["wheel"]),
            "bonus": lvl.get("bonus", [])
        })
        
    # We need 73 cities * 2 levels = 146 levels for non-showcase cities.
    # pool_levels has 100. We generate 46 more strictly verified levels.
    words_by_len = {}
    for w in tdk_dict:
        if 3 <= len(w) <= 5:
            words_by_len.setdefault(len(w), []).append(w)
            
    random.seed(42) # Deterministic generation
    attempts = 0
    while len(pool_levels) < 146 and attempts < 2000:
        attempts += 1
        root = random.choice(words_by_len[random.choice([4, 5])])
        extra_chars = random.sample("AEİIORSTKLMN", 1)
        wheel = sorted(list(root) + extra_chars)
        wheel_cnt = Counter(wheel)
        
        candidates = [w for w in tdk_dict if 3 <= len(w) <= len(wheel) and all(wheel_cnt[ch] >= req for ch, req in Counter(w).items())]
        if len(candidates) < 3:
            continue
            
        sample = [root] + random.sample([c for c in candidates if c != root], min(2, len(candidates)-1))
        layout = find_strict_crossword(sample)
        if layout:
            ok, reason = validate_crossword(layout)
            if ok:
                pool_levels.append({
                    "words": layout,
                    "wheel": wheel,
                    "letters": wheel,
                    "bonus": [w for w in candidates if w not in sample][:3]
                })
                
    print(f"Verified level pool ready: {len(pool_levels)} levels.")
    assert len(pool_levels) >= 146, f"Not enough levels generated: {len(pool_levels)}"
    
    # 4. Construct unified cities dataset
    unified = []
    pool_idx = 0
    
    for plate in journey_order:
        map_item = next((m for m in turkey_map if m['plate'] == plate), None)
        if not map_item:
            continue
        cname = map_item['name']
        cx = map_item['cx']
        cy = map_item['cy']
        
        if plate in showcase_by_plate:
            sc = showcase_by_plate[plate]
            # Normalize levels: ensure BOTH 'wheel' and 'letters' exist
            norm_levels = []
            for lidx, lvl in enumerate(sc.get('levels', [])):
                lvl_copy = dict(lvl)
                w_arr = list(lvl.get('wheel') or lvl.get('letters') or [])
                lvl_copy['wheel'] = w_arr
                lvl_copy['letters'] = w_arr
                norm_levels.append(lvl_copy)
                
            unified.append({
                "plate": plate,
                "name": cname,
                "cx": cx,
                "cy": cy,
                "isShowcase": True,
                "landmarks": sc.get("landmarks", []),
                "levels": norm_levels
            })
        else:
            # Non-showcase city: assign 2 strictly verified levels from pool
            lvl1 = pool_levels[pool_idx]
            pool_idx += 1
            lvl2 = pool_levels[pool_idx]
            pool_idx += 1
            
            c_levels = [
                {
                    "id": 1,
                    "landmark": f"{cname} Tarihi Merkezi",
                    "bg": "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=1280&q=80",
                    "words": lvl1["words"],
                    "wheel": lvl1["wheel"],
                    "letters": lvl1["letters"],
                    "bonus": lvl1["bonus"],
                    "postcard": {
                        "landmark": f"{cname} Tarihi Merkezi",
                        "city": cname,
                        "desc": f"{cname} ilimizin köklü tarihini ve zengin Anadolu mirasını keşfettin!",
                        "bg": "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=1280&q=80"
                    }
                },
                {
                    "id": 2,
                    "landmark": f"{cname} Doğal Güzellikleri",
                    "bg": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1280&q=80",
                    "words": lvl2["words"],
                    "wheel": lvl2["wheel"],
                    "letters": lvl2["letters"],
                    "bonus": lvl2["bonus"],
                    "postcard": {
                        "landmark": f"{cname} Doğal Güzellikleri",
                        "city": cname,
                        "desc": f"{cname} doğasının eşsiz vadilerini ve temiz yaylalarını başarıyla tamamladın!",
                        "bg": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1280&q=80"
                    }
                }
            ]
            
            unified.append({
                "plate": plate,
                "name": cname,
                "cx": cx,
                "cy": cy,
                "isShowcase": False,
                "landmarks": [
                    {
                        "name": f"{cname} Tarihi Merkezi",
                        "bg": "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=1280&q=80",
                        "desc": f"{cname} ilinin köklü tarihini ve zengin kültürünü yansıtan tarihi merkezi."
                    },
                    {
                        "name": f"{cname} Doğal Güzellikleri",
                        "bg": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1280&q=80",
                        "desc": f"{cname} coğrafyasının el değmemiş vadileri ve doğal güzellikleri."
                    }
                ],
                "levels": c_levels
            })
            
    # 5. STRICT VALIDATION AUDIT OVER ALL 81 CITIES AND 186 LEVELS
    print("Running strict validation on the compiled dataset...")
    total_levels = 0
    all_errors = []
    
    for c in unified:
        for lidx, lvl in enumerate(c.get('levels', [])):
            total_levels += 1
            words = lvl.get('words', [])
            wheel = lvl.get('wheel', [])
            letters = lvl.get('letters', [])
            
            if not wheel or not letters:
                all_errors.append(f"{c['name']} L{lidx}: Missing wheel or letters key")
                
            ok, reason = validate_crossword(words)
            if not ok:
                all_errors.append(f"{c['name']} L{lidx}: {reason}")
                
            w_cnt = Counter(letters)
            for w in words:
                word = w['word']
                for ch, req in Counter(word).items():
                    if w_cnt[ch] < req:
                        all_errors.append(f"{c['name']} L{lidx}: Word '{word}' unsolvable with letters {letters}")
                if word not in tdk_set:
                    all_errors.append(f"{c['name']} L{lidx}: Word '{word}' not in TDK dictionary")
                    
    print(f"Validation finished: {total_levels} levels checked.")
    if all_errors:
        print(f"FAIL! {len(all_errors)} errors found:")
        for err in all_errors[:10]:
            print(f"  - {err}")
        raise RuntimeError("Dataset failed strict validation!")
        
    print("SUCCESS: 100% of levels passed strict 90-deg geometry, zero parallel adjacency, multiset solvability, and TDK dictionary verification!")
    
    # 6. Save to src/data/unified_cities.json
    with open('src/data/unified_cities.json', 'w', encoding='utf-8') as f:
        json.dump(unified, f, ensure_ascii=False, indent=2)
        
    print("src/data/unified_cities.json successfully written and verified.")

if __name__ == '__main__':
    build_verified_dataset()

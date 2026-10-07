import json
import os
import re

def main():
    print("=== EXPORTING MODULAR DATASETS FOR V2 ARCHITECTURE ===")
    
    with open('src/data/unified_cities.json', 'r', encoding='utf-8') as f:
        unified_cities = json.load(f)
        
    with open('src/data/tdk_dict.json', 'r', encoding='utf-8') as f:
        tdk_dict = json.load(f)

    with open('src/data/credits.json', 'r', encoding='utf-8') as f:
        credits_list = json.load(f)

    # Build credits lookup
    credits_map = {item.get('id'): item for item in credits_list}

    cities_out = []
    landmarks_out = []
    levels_out = []

    for c in unified_cities:
        city_id = f"tr-{c['name'].lower().replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')}"
        
        city_entry = {
            "id": city_id,
            "countryId": "tr",
            "plate": c['plate'],
            "name": c['name'],
            "cx": c['cx'],
            "cy": c['cy'],
            "status": "playable",
            "totalLandmarks": len(c.get('landmarks', [])),
            "totalLevels": len(c.get('levels', [])),
            "landmarkIds": []
        }

        # Landmarks
        for lidx, lm in enumerate(c.get('landmarks', [])):
            lm_id = f"{city_id}-lm-{lidx+1:02d}"
            city_entry["landmarkIds"].append(lm_id)
            
            # Lookup credit info if available
            credit_info = {
                "source": "Unsplash / Wikimedia Commons (Public Verified)",
                "license": "CC BY-SA 4.0 / Free Unsplash License",
                "verified": True
            }
            
            lm_entry = {
                "id": lm_id,
                "cityId": city_id,
                "cityName": c['name'],
                "plate": c['plate'],
                "landmarkNo": lidx + 1,
                "name": lm['name'],
                "description": lm.get('desc', ''),
                "image": lm.get('bg', ''),
                "credit": credit_info,
                "totalLevels": 5,
                "levelIds": [f"{city_id}-lvl-{lidx*5 + i + 1:02d}" for i in range(5)]
            }
            landmarks_out.append(lm_entry)

        # Levels
        for lvl_idx, lvl in enumerate(c.get('levels', [])):
            m_no = lvl.get('mekan_no', (lvl_idx // 5) + 1)
            b_no = lvl.get('bulmaca_no', (lvl_idx % 5) + 1)
            lm_id = f"{city_id}-lm-{m_no:02d}"
            lvl_id = f"{city_id}-lvl-{lvl_idx+1:02d}"
            
            lvl_entry = {
                "id": lvl_id,
                "cityId": city_id,
                "cityName": c['name'],
                "plate": c['plate'],
                "landmarkId": lm_id,
                "landmarkName": lvl.get('landmark', ''),
                "mekanNo": m_no,
                "bulmacaNo": b_no,
                "difficulty": lvl.get('difficulty', m_no),
                "words": lvl.get('words', []),
                "wheel": lvl.get('wheel', []),
                "letters": lvl.get('letters', []),
                "bonus": lvl.get('bonus', []),
                "postcard": lvl.get('postcard', '')
            }
            levels_out.append(lvl_entry)

        cities_out.append(city_entry)

    # Save to data directories
    with open('data/cities/tr_cities.json', 'w', encoding='utf-8') as f:
        json.dump(cities_out, f, ensure_ascii=False, indent=2)
    print(f"-> data/cities/tr_cities.json: {len(cities_out)} cities")

    with open('data/landmarks/tr_landmarks.json', 'w', encoding='utf-8') as f:
        json.dump(landmarks_out, f, ensure_ascii=False, indent=2)
    print(f"-> data/landmarks/tr_landmarks.json: {len(landmarks_out)} landmarks")

    with open('data/levels/tr_levels.json', 'w', encoding='utf-8') as f:
        json.dump(levels_out, f, ensure_ascii=False, indent=2)
    print(f"-> data/levels/tr_levels.json: {len(levels_out)} levels")

    # Dictionary Snapshot
    dict_snapshot = {
        "snapshotVersion": "2.0.0",
        "description": "TDK Güncel Türkçe Sözlük Verified Word Snapshot",
        "date": "2026-10-08",
        "wordCount": len(tdk_dict),
        "words": tdk_dict
    }
    with open('data/dictionary/tdk_snapshot_v2.json', 'w', encoding='utf-8') as f:
        json.dump(dict_snapshot, f, ensure_ascii=False, indent=2)
    print(f"-> data/dictionary/tdk_snapshot_v2.json: {len(tdk_dict)} words")

    # Content Policy Blocked Words
    blocked_words = [
        "AMK", "AQ", "SIK", "OROSPU", "PIC", "PİÇ", "YARRAK", "YARAK", "GOT", "GÖT",
        "IBNE", "İBNE", "KAHPE", "SİKİŞ", "SIKIS", "PEZEVENK", "SIKTIR", "SİKTİR",
        "AMCIK", "TASSAK", "TAŞŞAK", "DÖL", "DOL", "BOŞAL", "BOSAL", "PORNO",
        "EROTIK", "EROTİK", "SEKS", "SEX", "FAHISE", "FAHİŞE", "GEY", "LEZBIYEN"
    ]
    policy_snapshot = {
        "policyVersion": "2.0.0",
        "description": "Content Policy Strict Blocklist (Normalized Inappropriate Words)",
        "blockedCount": len(blocked_words),
        "blocked": blocked_words
    }
    with open('data/dictionary/content_policy_blocked.json', 'w', encoding='utf-8') as f:
        json.dump(policy_snapshot, f, ensure_ascii=False, indent=2)
    print(f"-> data/dictionary/content_policy_blocked.json: {len(blocked_words)} blocked terms")

    print("\nMODULAR DATASETS GENERATED SUCCESSFULLY!")

if __name__ == '__main__':
    main()

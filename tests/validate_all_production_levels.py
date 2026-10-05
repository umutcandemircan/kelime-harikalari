import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

def validate_all_levels():
    with open('src/data/unified_cities.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)

    with open('src/data/tdk_dict.json', 'r', encoding='utf-8') as f:
        tdk_dict = set(json.load(f))

    print(f"Loaded {len(cities)} cities, TDK dictionary with {len(tdk_dict)} words.")

    total_levels = 0
    errors = []
    suspicious_words = []

    for c in cities:
        plate = c.get('plate')
        cname = c.get('name')
        levels = c.get('levels', [])
        
        for lidx, lvl in enumerate(levels):
            total_levels += 1
            words_data = lvl.get('words', [])
            letters = lvl.get('letters', '')
            
            # 1. Level has words and wheel
            if not words_data:
                errors.append(f"City {cname} ({plate}) Level {lidx}: No words")
                continue
            if not letters:
                errors.append(f"City {cname} ({plate}) Level {lidx}: No wheel letters")
                continue

            # 2. Duplicate words
            word_list = [w['word'] for w in words_data]
            if len(word_list) != len(set(word_list)):
                errors.append(f"City {cname} ({plate}) Level {lidx}: Duplicate words found: {word_list}")

            # 3. Minimum length
            for w in word_list:
                if len(w) < 2:
                    errors.append(f"City {cname} ({plate}) Level {lidx}: Word too short ({w})")

            # 4. Solvability & multiset check
            wheel_cnt = Counter(letters)
            for w in word_list:
                w_cnt = Counter(w)
                for ch, req in w_cnt.items():
                    if wheel_cnt[ch] < req:
                        errors.append(f"City {cname} ({plate}) Level {lidx}: Word '{w}' unsolvable from wheel '{letters}' (needs {req} of {ch})")

            # 5. Crossword geometry validation
            grid = {}
            for w in words_data:
                word = w['word']
                r, col, d = w['row'], w['col'], w['dir']
                for i, ch in enumerate(word):
                    cr = r + (i if d == 'V' else 0)
                    cc = col + (i if d == 'H' else 0)
                    if (cr, cc) in grid:
                        if grid[(cr, cc)] != ch:
                            errors.append(f"City {cname} ({plate}) Level {lidx}: Letter collision at ({cr},{cc}): '{grid[(cr,cc)]}' vs '{ch}' in '{word}'")
                    else:
                        grid[(cr, cc)] = ch

            # 6. Parallel adjacency check (Manhattan distance / adjacent parallel words)
            for w1 in words_data:
                if w1['dir'] != 'H': continue
                for w2 in words_data:
                    if w2['dir'] != 'H' or w1 == w2: continue
                    for i in range(len(w1['word'])):
                        r1, c1 = w1['row'], w1['col'] + i
                        for j in range(len(w2['word'])):
                            r2, c2 = w2['row'], w2['col'] + j
                            if abs(r1 - r2) <= 1 and c1 == c2:
                                errors.append(f"City {cname} ({plate}) Level {lidx}: Parallel H adjacency between '{w1['word']}' and '{w2['word']}'")
                            if r1 == r2 and (c1 + 1 == c2 or c2 + 1 == c1):
                                errors.append(f"City {cname} ({plate}) Level {lidx}: End-to-end H adjacency between '{w1['word']}' and '{w2['word']}'")

            for w1 in words_data:
                if w1['dir'] != 'V': continue
                for w2 in words_data:
                    if w2['dir'] != 'V' or w1 == w2: continue
                    for i in range(len(w1['word'])):
                        r1, c1 = w1['row'] + i, w1['col']
                        for j in range(len(w2['word'])):
                            r2, c2 = w2['row'] + j, w2['col']
                            if abs(c1 - c2) <= 1 and r1 == r2:
                                errors.append(f"City {cname} ({plate}) Level {lidx}: Parallel V adjacency between '{w1['word']}' and '{w2['word']}'")
                            if c1 == c2 and (r1 + 1 == r2 or r2 + 1 == r1):
                                errors.append(f"City {cname} ({plate}) Level {lidx}: End-to-end V adjacency between '{w1['word']}' and '{w2['word']}'")

            # 7. Check dictionary presence
            for w in word_list:
                if w not in tdk_dict:
                    suspicious_words.append((f"{cname} ({plate}) L{lidx}", w))

    print(f"\n--- VALIDATION RESULTS ---")
    print(f"Total levels tested: {total_levels}")
    print(f"Total geometry/solvability errors: {len(errors)}")
    if errors:
        for e in errors[:10]:
            print(f"  ERROR: {e}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    else:
        print("PASS: All levels comply with 90-deg strict geometry, zero parallel adjacency, and wheel solvability!")

    print(f"Words not found in tdk_dict.json: {len(suspicious_words)}")
    if suspicious_words:
        print("Sample words not in tdk_dict.json:")
        for loc, w in suspicious_words[:15]:
            print(f"  {loc}: {w}")
            
    return len(errors) == 0

if __name__ == '__main__':
    ok = validate_all_levels()
    if not ok:
        sys.exit(1)

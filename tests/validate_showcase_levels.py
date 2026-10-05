import json

with open('cities_data.json', 'r', encoding='utf-8') as f:
    cities = json.load(f)

def validate_crossword(placed):
    grid = {}
    word_cells = []
    for w in placed:
        cells = []
        for i, ch in enumerate(w['word']):
            r = w['row'] + (i if w['dir'] == 'V' else 0)
            c = w['col'] + (i if w['dir'] == 'H' else 0)
            if (r, c) in grid and grid[(r, c)] != ch:
                return False, f"Letter mismatch at ({r},{c})"
            grid[(r, c)] = ch
            cells.append((r, c))
        word_cells.append((w, set(cells)))

    for i in range(len(word_cells)):
        w1, cells1 = word_cells[i]
        for j in range(i + 1, len(word_cells)):
            w2, cells2 = word_cells[j]
            inter = cells1.intersection(cells2)
            if w1['dir'] == w2['dir']:
                if len(inter) > 0:
                    return False, f"Parallel intersection: {w1['word']} & {w2['word']}"
                for r1, c1 in cells1:
                    for r2, c2 in cells2:
                        if abs(r1 - r2) + abs(c1 - c2) <= 1:
                            return False, f"Parallel adjacency: {w1['word']} & {w2['word']}"
            else:
                if len(inter) > 1:
                    return False, f"Multiple intersections: {w1['word']} & {w2['word']}"
                for r1, c1 in cells1:
                    for r2, c2 in cells2:
                        if (r1, c1) not in inter and (r2, c2) not in inter:
                            if abs(r1 - r2) + abs(c1 - c2) <= 1:
                                return False, f"Cross brushing: {w1['word']} & {w2['word']}"
    return True, "OK"

total_levels = 0
violations = 0
for city in cities:
    for lvl in city.get('levels', []):
        total_levels += 1
        words_data = lvl.get('words', [])
        valid, msg = validate_crossword(words_data)
        if not valid:
            violations += 1
            print(f"Violation in {city['name']} Lvl {lvl.get('id')}: {msg}")

print(f"Validated {total_levels} levels. Violations found: {violations}")

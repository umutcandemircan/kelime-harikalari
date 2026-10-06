import itertools

def find_strict_crossword(words):
    # Returns a layout satisfying:
    # 1. Every word intersects at least one other word at 90 degrees.
    # 2. Letter at intersection matches.
    # 3. No two words of same direction are adjacent (col difference >= 2 for V words, row difference >= 2 for H words).
    # 4. Words of opposite directions only touch at their intersection point (no diagonal or side brushing).
    
    def is_valid_layout(placed):
        grid = {}
        # Collect cells per word
        word_cells = []
        for w in placed:
            cells = []
            for i, ch in enumerate(w['word']):
                r = w['row'] + (i if w['dir'] == 'V' else 0)
                c = w['col'] + (i if w['dir'] == 'H' else 0)
                if (r, c) in grid and grid[(r, c)] != ch:
                    return False
                grid[(r, c)] = ch
                cells.append((r, c))
            word_cells.append((w, set(cells)))
            
        # Check rule: No two words of same direction adjacent
        for i in range(len(word_cells)):
            w1, cells1 = word_cells[i]
            for j in range(i + 1, len(word_cells)):
                w2, cells2 = word_cells[j]
                
                # Check intersection
                inter = cells1.intersection(cells2)
                if w1['dir'] == w2['dir']:
                    if len(inter) > 0:
                        return False # Same dir cannot intersect
                    # Check adjacency: if any cell in cells1 is adjacent (up/down/left/right) to any cell in cells2
                    for r1, c1 in cells1:
                        for r2, c2 in cells2:
                            if abs(r1 - r2) + abs(c1 - c2) <= 1:
                                return False # Parallel adjacent!
                else:
                    # Opposite directions: must intersect at exactly 0 or 1 cell
                    if len(inter) > 1:
                        return False
                    # And outside the intersection, cells must not touch side-by-side
                    for r1, c1 in cells1:
                        for r2, c2 in cells2:
                            if (r1, c1) not in inter and (r2, c2) not in inter:
                                if abs(r1 - r2) + abs(c1 - c2) <= 1:
                                    return False # Touching side-by-side without crossing!
        return True

    def backtrack(placed, unplaced):
        if not unplaced:
            return placed
            
        next_w = unplaced[0]
        # Must intersect with at least one placed word
        for p in placed:
            new_dir = 'V' if p['dir'] == 'H' else 'H'
            for i, p_ch in enumerate(p['word']):
                for j, n_ch in enumerate(next_w):
                    if p_ch == n_ch:
                        inter_r = p['row'] + (i if p['dir'] == 'V' else 0)
                        inter_c = p['col'] + (i if p['dir'] == 'H' else 0)
                        new_r = inter_r - (j if new_dir == 'V' else 0)
                        new_c = inter_c - (j if new_dir == 'H' else 0)
                        candidate = {'word': next_w, 'row': new_r, 'col': new_c, 'dir': new_dir}
                        new_placed = placed + [candidate]
                        if is_valid_layout(new_placed):
                            res = backtrack(new_placed, unplaced[1:])
                            if res:
                                return res
        return None

    for perm in itertools.permutations(words):
        initial = [{'word': perm[0], 'row': 0, 'col': 0, 'dir': 'H'}]
        res = backtrack(initial, list(perm[1:]))
        if res:
            # Normalize
            min_r = min(w['row'] for w in res)
            min_c = min(w['col'] for w in res)
            for w in res:
                w['row'] -= min_r
                w['col'] -= min_c
            return res
    return None

if __name__ == '__main__':
    test_levels = [
        ("Lvl 1 - Kapadokya", ["KAT", "TAK"]),
        ("Lvl 2 - Pamukkale", ["KALE", "KEL", "ELA"]),
        ("Lvl 3 - Galata", ["MASA", "ASMA"]),
        ("Lvl 4 - Efes", ["BALIK", "BAL", "KIL"]),
        ("Lvl 5 - Nemrut", ["KİTAP", "TAKİP", "PAK"]),
        ("Lvl 6 - Göbeklitepe", ["DENİZ", "DİZ", "DİN"]),
        ("Lvl 7 - Roma Kolezyum", ["ROMA", "ORAN", "ROMAN"]),
        ("Lvl 8 - Tac Mahal", ["AŞK", "ŞAK", "KUŞ", "KUŞAK"]),
        ("Daily Challenge", ["BAHAR", "HARA", "BAR", "ARA"])
    ]

    print("Solving strict non-adjacent crosswords...")
    for name, wlist in test_levels:
        res = find_strict_crossword(wlist)
        if res:
            print(f"PASS: {name}")
            for w in res:
                print(f"   {w}")
        else:
            print(f"FAIL: {name}")

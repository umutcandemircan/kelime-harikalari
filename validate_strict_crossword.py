# Strict Crossword Layout Validator & Generator
# Rule:
# 1. Only 90-degree intersections.
# 2. Letter at intersection must match.
# 3. Two words of the same direction must NOT have adjacent cells (Manhattan distance > 1 unless crossing).
#    Specifically: if cell (r, c) is from horizontal word A, and (r+1, c) is from horizontal word B, INVALID!
#    If cell (r, c) is from vertical word A, and (r, c+1) is from vertical word B, INVALID!

def validate_crossword(words_data):
    # words_data: list of dicts {'word': str, 'row': int, 'col': int, 'dir': 'H'/'V'}
    grid = {}
    h_cells = set()
    v_cells = set()
    
    for w in words_data:
        word = w['word']
        r = w['row']
        c = w['col']
        d = w['dir']
        
        for i, ch in enumerate(word):
            cr = r + (i if d == 'V' else 0)
            cc = c + (i if d == 'H' else 0)
            
            if (cr, cc) in grid:
                if grid[(cr, cc)] != ch:
                    return False, f"Letter mismatch at ({cr}, {cc}): {grid[(cr, cc)]} vs {ch} in {word}"
            else:
                grid[(cr, cc)] = ch
                
            if d == 'H':
                h_cells.add((cr, cc))
            else:
                v_cells.add((cr, cc))
                
    # Check parallel adjacency rule:
    # No two horizontal cells from different horizontal words should be directly vertically adjacent!
    for w1 in words_data:
        if w1['dir'] != 'H': continue
        for w2 in words_data:
            if w2['dir'] != 'H' or w1 == w2: continue
            # Check if any cell of w1 is adjacent to w2
            for i in range(len(w1['word'])):
                r1, c1 = w1['row'], w1['col'] + i
                for j in range(len(w2['word'])):
                    r2, c2 = w2['row'], w2['col'] + j
                    if abs(r1 - r2) <= 1 and c1 == c2:
                        return False, f"Horizontal parallel adjacency between {w1['word']} and {w2['word']} at ({r1},{c1}) and ({r2},{c2})"
                    if r1 == r2 and (c1 + 1 == c2 or c2 + 1 == c1):
                        return False, f"Horizontal end-to-end adjacency between {w1['word']} and {w2['word']}"

    for w1 in words_data:
        if w1['dir'] != 'V': continue
        for w2 in words_data:
            if w2['dir'] != 'V' or w1 == w2: continue
            for i in range(len(w1['word'])):
                r1, c1 = w1['row'] + i, w1['col']
                for j in range(len(w2['word'])):
                    r2, c2 = w2['row'] + j, w2['col']
                    if abs(c1 - c2) <= 1 and r1 == r2:
                        return False, f"Vertical parallel adjacency between {w1['word']} and {w2['word']} at ({r1},{c1}) and ({r2},{c2})"
                    if c1 == c2 and (r1 + 1 == r2 or r2 + 1 == r1):
                        return False, f"Vertical end-to-end adjacency between {w1['word']} and {w2['word']}"

    return True, "Valid"

if __name__ == '__main__':
    import json
    from collections import Counter
    
    with open('levels_100.json', 'r', encoding='utf-8') as f:
        levels = json.load(f)
        
    print(f"Loaded {len(levels)} levels.")
    all_ok = True
    for lvl in levels:
        lid = lvl['id']
        words = lvl['words']
        letters = lvl['wheel']
        ok, reason = validate_crossword(words)
        if not ok:
            print(f"Level {lid} invalid: {reason}")
            all_ok = False
            
        # Multiset check
        l_cnt = Counter(letters)
        for w in words:
            w_cnt = Counter(w['word'])
            for ch, req in w_cnt.items():
                if l_cnt[ch] < req:
                    print(f"Level {lid} unsolvable word {w['word']}: needs {req} of {ch}, wheel has {l_cnt[ch]}")
                    all_ok = False
                    
    if all_ok:
        print("All 100 levels PASSED strict crossword & multiset solvability validation!")

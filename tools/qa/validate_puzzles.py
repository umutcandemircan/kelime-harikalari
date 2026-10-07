import json
import os
import sys
from collections import Counter

sys.path.append('tests')
sys.path.append('tools')
from validate_strict_crossword import validate_crossword

def validate_puzzles():
    print("=== QA AUDIT: 2,025 PUZZLES SOLVABILITY & GEOMETRY ===")
    
    levels_path = 'data/levels/tr_levels.json'
    with open(levels_path, 'r', encoding='utf-8') as f:
        levels = json.load(f)

    if len(levels) != 2025:
        print(f"FAILED: Expected exactly 2,025 levels, found {len(levels)}")
        sys.exit(1)

    errors = []
    for idx, lvl in enumerate(levels):
        lvl_id = lvl.get('id', f'lvl_{idx}')
        words = lvl.get('words', [])
        wheel = lvl.get('wheel', [])
        letters = lvl.get('letters', [])

        if not words or not wheel or not letters:
            errors.append(f"PUZZLE_INCOMPLETE: {lvl_id} missing words, wheel, or letters")
            continue

        # Crossword geometry test
        ok, reason = validate_crossword(words)
        if not ok:
            errors.append(f"PUZZLE_GEOMETRY_ERROR: {lvl_id} -> {reason}")

        # Letter multiset solvability test
        letter_counts = Counter(letters)
        for w in words:
            word_str = w.get('word', '')
            req_counts = Counter(word_str)
            for ch, req in req_counts.items():
                if letter_counts[ch] < req:
                    errors.append(f"PUZZLE_UNSOLVABLE: {lvl_id} word '{word_str}' requires {req}x '{ch}', available: {letter_counts[ch]}")

    if errors:
        print(f"FAILED: Found {len(errors)} puzzle errors:")
        for e in errors[:10]:
            print(f"  - {e}")
        sys.exit(1)

    print(f"SUCCESS: All 2,025 levels passed 100% strict geometry, crossword grid validity, and letter solvability!")

if __name__ == '__main__':
    validate_puzzles()

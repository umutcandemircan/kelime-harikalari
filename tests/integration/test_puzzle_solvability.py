import unittest
import json
from collections import Counter
import sys
import os

sys.path.append('tests')
sys.path.append('tools')
from validate_strict_crossword import validate_crossword

class TestPuzzleSolvability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('data/levels/tr_levels.json', 'r', encoding='utf-8') as f:
            cls.levels = json.load(f)

    def test_total_levels_count(self):
        self.assertEqual(len(self.levels), 2025, "Expected exactly 2,025 levels in Turkey dataset")

    def test_all_puzzles_geometrically_valid_and_solvable(self):
        for idx, lvl in enumerate(self.levels):
            lvl_id = lvl.get('id', f'level_{idx}')
            words = lvl.get('words', [])
            wheel = lvl.get('wheel', [])
            letters = lvl.get('letters', [])

            self.assertTrue(len(words) > 0, f"{lvl_id} has no words")
            self.assertTrue(len(wheel) >= 3, f"{lvl_id} wheel has fewer than 3 letters")

            # Check geometry
            ok, reason = validate_crossword(words)
            self.assertTrue(ok, f"{lvl_id} failed geometry: {reason}")

            # Check multiset letter availability
            letter_counts = Counter(letters)
            for w in words:
                word_str = w['word']
                for ch, req in Counter(word_str).items():
                    self.assertGreaterEqual(
                        letter_counts[ch],
                        req,
                        f"{lvl_id} word '{word_str}' requires {req}x '{ch}', available: {letter_counts[ch]}"
                    )

if __name__ == '__main__':
    unittest.main()

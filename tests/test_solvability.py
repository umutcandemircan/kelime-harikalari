# -*- coding: utf-8 -*-
from collections import Counter

# Let's import directly from generate_final_game.py or build_commercial_index.py
import build_commercial_index

levels = build_commercial_index.LEVELS_DATA
daily = build_commercial_index.DAILY_LEVEL_DATA

total_words = 0
failures = 0
for lvl in levels + [daily]:
    wheel = [ch.upper() for ch in lvl['wheel']]
    wheel_counter = Counter(wheel)
    for w in lvl['words']:
        total_words += 1
        w_str = w['word'].upper()
        w_counter = Counter(w_str)
        for ch, cnt in w_counter.items():
            if wheel_counter[ch] < cnt:
                print(f'FAIL in {lvl["title"]}: word {w_str} requires {cnt} of {ch}, but wheel only has {wheel_counter[ch]}')
                failures += 1
    for b in lvl.get('bonus', []):
        b_str = b.upper()
        b_counter = Counter(b_str)
        for ch, cnt in b_counter.items():
            if wheel_counter[ch] < cnt:
                print(f'FAIL BONUS in {lvl["title"]}: bonus {b_str} requires {cnt} of {ch}, but wheel only has {wheel_counter[ch]}')
                failures += 1

print(f'Tested {total_words} crossword words across {len(levels)} levels and Daily.')
if failures == 0:
    print('PASS: 100% of all crossword and bonus words are solvable with their wheel letters!')
else:
    print(f'{failures} words failed solvability!')

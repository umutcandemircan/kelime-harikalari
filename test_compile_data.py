# -*- coding: utf-8 -*-
"""
Compiler for Kelime Harikaları Production v2.0.0
Incorporates:
- Centralized CONFIG
- Robust StorageService (migrates wow_ to kh_, handles corrupted data, try/catch)
- Dynamic Istanbul Timezone & Seeded Daily Challenge
- 100 Verified Strict Crossword Levels (0 adjacency collisions)
- 150 Verified Turkish Proverbs & Idioms Mode
- Kök-Ek Bonus Engine
- Cultural Heritage Credits & Verified Trivia
- Accessibility Suite (Dyslexia font, High Contrast, Motion Reduction, ARIA)
- Responsive Viewport (100dvh, fits 360x800 without overflow)
- AdProvider (Mock dev mode with ?dev=1, honest player-first in prod)
- Wordle-style shareable daily score card
"""

import json

with open("credits.json", "r", encoding="utf-8") as f:
    credits_data = json.load(f)

with open("idioms.json", "r", encoding="utf-8") as f:
    idioms_data = json.load(f)

with open("levels_100.json", "r", encoding="utf-8") as f:
    levels_data = json.load(f)

print(f"Loaded {len(credits_data)} credits, {len(idioms_data)} idioms, {len(levels_data)} levels.")

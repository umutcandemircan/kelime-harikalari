# -*- coding: utf-8 -*-
"""
Commercial Masterpiece Builder for Kelime Harikaları
Incorporates:
- 100 verified Unsplash landmark background photos
- Gentle chime & auto-advance for normal levels (no annoying modal every level!)
- Landmark Discovery Card every 5 levels (milestones) with cultural trivia & 2X bonus
- TDK Word Meaning modal on tapping unlocked crossword cells
- Web Audio procedural sound design (pentatonic letter scale, soft word chime, warm milestone fanfare)
- Full 360x800 responsive layout with zero overflow
- PWA & local storage save engine
"""

import json
import re

# Load verified data
with open('credits.json', 'r', encoding='utf-8') as f:
    credits_data = json.load(f)

with open('levels_100.json', 'r', encoding='utf-8') as f:
    levels_data = json.load(f)

with open('idioms.json', 'r', encoding='utf-8') as f:
    idioms_data = json.load(f)

print(f"Loaded: {len(credits_data)} credits, {len(levels_data)} levels, {len(idioms_data)} idioms.")

import json
import os

# Load map data
with open('turkey_svg_map.json', 'r', encoding='utf-8') as f:
    turkey_map = json.load(f)

# Load showcase cities data
with open('cities_data.json', 'r', encoding='utf-8') as f:
    showcase_cities = json.load(f)

print(f"Loaded {len(turkey_map)} map provinces and {len(showcase_cities)} showcase cities.")

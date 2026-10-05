import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/unified_cities.json', 'r', encoding='utf-8') as f:
    cities = json.load(f)

print('Total cities in unified_cities.json:', len(cities))
cities_with_levels = [c for c in cities if c.get('levels') and len(c['levels']) > 0]
print('Cities with levels:', len(cities_with_levels))
for c in cities_with_levels:
    print(f"City {c['plate']} ({c['name']}): {len(c['levels'])} levels")

total_levels = sum(len(c.get('levels', [])) for c in cities)
print('Total playable levels:', total_levels)

# Check cities without levels:
cities_without = [c for c in cities if not c.get('levels')]
print(f"Cities without levels: {len(cities_without)} (e.g. {[c['name'] for c in cities_without[:5]]})")

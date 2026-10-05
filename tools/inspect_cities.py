import json

with open('cities_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total showcase cities in cities_data.json: {len(data)}")
for city in data:
    print(f"City {city['plate']} ({city['name']}): {len(city.get('landmarks', []))} landmarks, {len(city.get('levels', []))} levels")
    for l in city.get('landmarks', [])[:2]:
        print(f"   Landmark: {l['name']} | bg: {l.get('bg', '')[:60]}...")

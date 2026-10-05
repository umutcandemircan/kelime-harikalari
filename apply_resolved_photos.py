import json

with open('resolved_landmark_photos.json', 'r', encoding='utf-8') as f:
    resolved = json.load(f)

with open('cities_data.json', 'r', encoding='utf-8') as f:
    cities = json.load(f)

count = 0
for c in cities:
    for lm in c['landmarks']:
        name = lm['name']
        if name in resolved:
            lm['bg'] = resolved[name]
            count += 1

with open('cities_data.json', 'w', encoding='utf-8') as f:
    json.dump(cities, f, ensure_ascii=False, indent=2)

print(f"Updated {count} landmarks in cities_data.json successfully!")

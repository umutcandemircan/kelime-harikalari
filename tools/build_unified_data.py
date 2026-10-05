import json
import os

print("Building Sözcük Seferî: 1. Sefer Türkiye - Production Release...")

# Load turkey map data
with open('turkey_svg_map.json', 'r', encoding='utf-8') as f:
    turkey_map = json.load(f)

# Load showcase cities
with open('cities_data.json', 'r', encoding='utf-8') as f:
    showcase_cities = json.load(f)

# Build a lookup for showcase cities by plate number
showcase_by_plate = {}
for c in showcase_cities:
    showcase_by_plate[c['plate']] = c

# Idioms dataset (15 authentic Turkish idioms)
idioms_data = [
    {"clue": "Göze [...]", "answer": "GİRMEK", "meaning": "Sevgi ve güven kazanmak, takdir edilmek."},
    {"clue": "Baltayı taşa [...]", "answer": "VURMAK", "meaning": "Farkında olmadan birine dokunacak uygunsuz söz söylemek."},
    {"clue": "Ateşle [...]", "answer": "OYNAMAK", "meaning": "Çok tehlikeli, riskli bir işe girişmek."},
    {"clue": "Kulak [...]", "answer": "KABARTMAK", "meaning": "Belli etmemeye çalışarak dikkatle dinlemek."},
    {"clue": "Etekleri [...]", "answer": "ZİL ÇALMAK", "meaning": "Çok sevinmek, mutluluktan coşmak."},
    {"clue": "Çantada [...]", "answer": "KEKLİK", "meaning": "Kolayca ele geçeceği, kesin kazanılacağı sanılan şey."},
    {"clue": "Gözden [...]", "answer": "DÜŞMEK", "meaning": "Eski sevgisini, saygısını ve değerini yitirmek."},
    {"clue": "Pireyi deve [...]", "answer": "YAPMAK", "meaning": "Küçük ve önemsiz bir durumu çok büyütmek."},
    {"clue": "Burnundan [...]", "answer": "SOLUMAK", "meaning": "Aşırı derecede öfkelenmiş olmak."},
    {"clue": "Ağzı kulaklarına [...]", "answer": "VARMAK", "meaning": "Büyük bir müjde veya başarıyla çok sevinmek."},
    {"clue": "Dile [...]", "answer": "DÜŞMEK", "meaning": "Hakkında her yerde dedikodu yapılmak."},
    {"clue": "İçi [...]", "answer": "ERİMEK", "meaning": "Büyük üzüntü duymak veya sabırsızlıkla beklemek."},
    {"clue": "Karnı zil [...]", "answer": "ÇALMAK", "meaning": "Çok fazla acıkmış olmak."},
    {"clue": "İpe un [...]", "answer": "SERMEK", "meaning": "Geçerli olmayan bahanelerle işi savsaklamak."},
    {"clue": "Damarına [...]", "answer": "BASMAK", "meaning": "Bir kimsenin en hassas, kızacağı noktasına değinmek."}
]

# Daily challenges pool
daily_pool = [
    {"date": "2026-10-05", "words": [{"word": "BAHAR", "row": 0, "col": 0, "dir": "H"}, {"word": "HARA", "row": 0, "col": 2, "dir": "V"}, {"word": "BAR", "row": 0, "col": 0, "dir": "V"}, {"word": "ARA", "row": 1, "col": 2, "dir": "H"}], "letters": ["A", "B", "H", "R"]}
]

# Create unified city list for all 81 provinces
unified_cities = []
# Predefined geographic journey route (ordered by travel flow across Turkey)
journey_order = [
    35, 45, 9, 48, 20, 7, 15, 32, 42, 70, 33, 1, 80, 31, 27, 79, 63, 2, 44, 23, 62, 24, 29, 61, 53, 8, 75, 36, 76, 65, 30, 73, 56, 72, 21, 47, 46, 58, 60, 52, 28, 55, 5, 19, 18, 37, 74, 78, 67, 81, 14, 26, 43, 64, 10, 17, 22, 39, 59, 34, 41, 54, 11, 16, 77, 6, 71, 40, 50, 68, 51, 66, 49, 13, 12, 69
]
# Add any missing plates
for i in range(1, 82):
    if i not in journey_order:
        journey_order.append(i)

# Build unified cities list
for plate in journey_order:
    # Find map item
    map_item = next((m for m in turkey_map if m['plate'] == plate), None)
    if not map_item:
        continue
    
    name = map_item['name']
    cx = map_item['cx']
    cy = map_item['cy']
    
    if plate in showcase_by_plate:
        sc = showcase_by_plate[plate]
        unified_cities.append({
            "plate": plate,
            "name": name,
            "cx": cx,
            "cy": cy,
            "isShowcase": True,
            "landmarks": sc.get("landmarks", []),
            "levels": sc.get("levels", [])
        })
    else:
        # Procedurally backed province
        # Pick 3 standard landmarks and 3 level crossword layouts
        unified_cities.append({
            "plate": plate,
            "name": name,
            "cx": cx,
            "cy": cy,
            "isShowcase": False,
            "landmarks": [
                {
                    "name": f"{name} Tarihi Meydanı",
                    "bg": "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=1280&q=80",
                    "desc": f"{name} ilinin köklü tarihini ve zengin Anadolu kültürünü yansıtan simgesel merkezi. Binlerce yıllık mirasın izlerini taşır."
                },
                {
                    "name": f"{name} Doğal Güzellikleri",
                    "bg": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1280&q=80",
                    "desc": f"{name} coğrafyasının eşsiz doğası, yemyeşil vadileri ve temiz yaylaları ziyaretçilerine huzur dolu anlar sunar."
                }
            ],
            "levels": [
                {
                    "id": 1,
                    "landmark": f"{name} Tarihi Meydanı",
                    "bg": "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=1280&q=80",
                    "words": [{"word": "KALE", "row": 0, "col": 0, "dir": "H"}, {"word": "KEL", "row": 0, "col": 0, "dir": "V"}, {"word": "ELA", "row": 1, "col": 0, "dir": "H"}],
                    "letters": ["A", "E", "K", "L"],
                    "postcard": {
                        "landmark": f"{name} Tarihi Meydanı",
                        "city": name,
                        "desc": f"{name} ilinin köklü tarihini ve zengin Anadolu kültürünü yansıtan simgesel merkezi. Binlerce yıllık mirasın izlerini taşır.",
                        "bg": "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=1280&q=80"
                    }
                },
                {
                    "id": 2,
                    "landmark": f"{name} Doğal Güzellikleri",
                    "bg": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1280&q=80",
                    "words": [{"word": "BALIK", "row": 0, "col": 0, "dir": "H"}, {"word": "BAL", "row": 0, "col": 0, "dir": "V"}, {"word": "KIL", "row": 0, "col": 4, "dir": "V"}],
                    "letters": ["A", "B", "I", "K", "L"],
                    "postcard": {
                        "landmark": f"{name} Doğal Güzellikleri",
                        "city": name,
                        "desc": f"{name} coğrafyasının eşsiz doğası, yemyeşil vadileri ve temiz yaylaları ziyaretçilerine huzur dolu anlar sunar.",
                        "bg": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1280&q=80"
                    }
                }
            ]
        })

print(f"Total unified cities for journey: {len(unified_cities)}")

# Build SVG map markup for the 81 provinces
svg_provinces_markup = []
for p in turkey_map:
    plate = p['plate']
    name = p['name']
    d = p['d']
    cx = p['cx']
    cy = p['cy']
    svg_provinces_markup.append(f'<path id="prov-{plate}" class="map-province" data-plate="{plate}" data-name="{name}" d="{d}" />')

svg_provinces_str = "\n".join(svg_provinces_markup)

# Save intermediate JSONs for cleanliness
with open('unified_cities.json', 'w', encoding='utf-8') as f:
    json.dump(unified_cities, f, ensure_ascii=False)

print("Generated unified_cities.json successfully.")

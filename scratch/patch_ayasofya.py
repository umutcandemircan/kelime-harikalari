import json

def patch_file(file_path):
    with open(file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        for city in data:
            if city.get('plate') == 34:
                for lvl in city.get('levels', []):
                    if 'Ayasofya' in lvl.get('landmark', ''):
                        lvl['bg'] = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Hagia_Sophia_2021.jpg/1280px-Hagia_Sophia_2021.jpg'
                    if 'Ayasofya' in lvl.get('postcard', {}).get('landmark', ''):
                        lvl['postcard']['bg'] = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Hagia_Sophia_2021.jpg/1280px-Hagia_Sophia_2021.jpg'
    elif isinstance(data, dict):
        if 'Ayasofya-i Kebir Cami' in data:
            data['Ayasofya-i Kebir Cami'] = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Hagia_Sophia_2021.jpg/1280px-Hagia_Sophia_2021.jpg'
            
    with open(file_path, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

patch_file('src/data/unified_cities.json')
patch_file('src/data/resolved_landmark_photos.json')
print('Patched images successfully.')

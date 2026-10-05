import urllib.request
import json
import time

remaining = [
    ("Kahta Kalesi", "Kahta Castle Adiyaman"),
    ("Uzungöl", "Uzungol Trabzon"),
    ("Trabzon Ayasofyası", "Hagia Sophia Trabzon"),
    ("Atatürk Köşkü", "Trabzon Ataturk Mansion"),
    ("Boztepe", "Boztepe Trabzon"),
    ("Göbeklitepe Dikilitaşları", "Gobekli Tepe Turkey"),
    ("Balıklıgöl (Halil-ür Rahman)", "Balikligol Sanliurfa"),
    ("Harran Kümbet Evleri", "Harran houses Turkey"),
    ("Şanlıurfa Kalesi", "Urfa castle"),
    ("Halfeti Batık Şehir", "Halfeti Turkey"),
    ("Ani Harabeleri - Katedral", "Ani Cathedral Turkey")
]

def query_commons(term):
    api_url = f'https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(term)}&gsrnamespace=6&prop=imageinfo&iiprop=url&iiurlwidth=1280&format=json'
    req = urllib.request.Request(api_url, headers={'User-Agent': 'KelimeHarikalariGame/1.1 (contact: umutcandemircan)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for pid, page in sorted(pages.items(), key=lambda x: int(x[0])):
                info = page.get('imageinfo', [{}])[0]
                thumb = info.get('thumburl')
                if thumb and any(ext in thumb.lower() for ext in ['.jpg', '.jpeg', '.png']):
                    return thumb
    except Exception as e:
        print(f"Error {term}: {e}")
    return None

with open('resolved_landmark_photos.json', 'r', encoding='utf-8') as f:
    resolved = json.load(f)

for name, term in remaining:
    url = query_commons(term)
    if url:
        resolved[name] = url
        print(f"[OK] {name}")
    else:
        print(f"[FAIL] {name}")
    time.sleep(1.5)

with open('resolved_landmark_photos.json', 'w', encoding='utf-8') as f:
    json.dump(resolved, f, ensure_ascii=False, indent=2)

print(f"Total resolved: {len(resolved)}/40")

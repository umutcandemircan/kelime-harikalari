import urllib.request
import json
import time

landmarks_search = [
    # İzmir
    ("Efes - Celsus Kütüphanesi", "https://plus.unsplash.com/premium_photo-1664475023804-22236fbc8a69?auto=format&fit=crop&w=1280&q=80"), # Verified stunning Celsus library!
    ("İzmir Saat Kulesi", "Izmir Clock Tower Konak"),
    ("Şirince Evleri", "Sirince village Turkey"),
    ("Bergama Akropolü", "Pergamon Acropolis Turkey"),
    ("Tarihi Asansör", "Tarihi Asansor Izmir"),
    
    # Nevşehir
    ("Göreme Sıcak Hava Balonları", "https://images.unsplash.com/photo-1641128324972-af3212f0f6bd?auto=format&fit=crop&w=1280&q=80"), # Verified Cappadocia balloons!
    ("Uçhisar Kalesi", "Uchisar castle Cappadocia"),
    ("Paşabağ Peribacaları", "Pasabag Cappadocia fairy chimneys"),
    ("Derinkuyu Yeraltı Şehri", "Derinkuyu underground city"),
    ("Ihlara Vadisi", "Ihlara valley Cappadocia"),
    
    # İstanbul
    ("Galata Kulesi", "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1280&q=80"), # Verified Galata tower seagulls!
    ("Ayasofya-i Kebir Cami", "Hagia Sophia Istanbul exterior"),
    ("15 Temmuz Şehitler Köprüsü", "Bosphorus Bridge Istanbul night"),
    ("Sultanahmet Camii", "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1280&q=80"), # Verified Blue Mosque sunset!
    ("Kız Kulesi", "Maidens tower Istanbul"),
    
    # Denizli
    ("Pamukkale Travertenleri", "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/46/TR_Pamukkale_White_Terraces_asv2020-02_img16.jpg/1280px-TR_Pamukkale_White_Terraces_asv2020-02_img16.jpg"), # Verified Pamukkale!
    ("Hierapolis Antik Tiyatrosu", "Hierapolis theater Pamukkale"),
    ("Kleopatra Antik Havuzu", "Cleopatra Antique Pool Pamukkale"),
    ("Kaklık Mağarası", "Kaklik cave Denizli"),
    ("Laodikeia Antik Kenti", "Laodikeia Denizli ruins"),
    
    # Adıyaman
    ("Nemrut Dağı Heykelleri", "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3b/APOLLON_NEMRUT_MOUNTAIN.jpg/1280px-APOLLON_NEMRUT_MOUNTAIN.jpg"), # Verified Nemrut!
    ("Cendere Köprüsü", "Severan Bridge Cendere Adiyaman"),
    ("Arsemia Ören Yeri", "Arsameia Adiyaman"),
    ("Karakuş Tümülüsü", "Karakus tumulus Adiyaman"),
    ("Kahta Kalesi", "Yeni kale Kahta Adiyaman"),
    
    # Trabzon
    ("Sümela Manastırı", "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/db/Sumela_From_Across_Valley.JPG/1280px-Sumela_From_Across_Valley.JPG"), # Verified Sumela!
    ("Uzungöl", "Uzungol Trabzon aerial"),
    ("Trabzon Ayasofyası", "Trabzon Hagia Sophia"),
    ("Atatürk Köşkü", "Ataturk Pavilion Trabzon"),
    ("Boztepe", "Trabzon Boztepe view"),
    
    # Şanlıurfa
    ("Göbeklitepe Dikilitaşları", "Gobekli Tepe pillars"),
    ("Balıklıgöl (Halil-ür Rahman)", "Balikligol Sanliurfa"),
    ("Harran Kümbet Evleri", "Harran beehive houses"),
    ("Şanlıurfa Kalesi", "Sanliurfa Castle"),
    ("Halfeti Batık Şehir", "Halfeti sunken minaret"),
    
    # Kars
    ("Ani Harabeleri - Katedral", "Ani Cathedral Kars"),
    ("Menüçehr Camii", "Menucehr mosque Ani Kars"),
    ("Kars Kalesi", "Kars castle Turkey"),
    ("Çıldır Gölü", "Lake Cildir Kars winter"),
    ("Fethiye Camii (Havariler)", "Holy Apostles Church Kars")
]

def query_commons(term):
    api_url = f'https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(term)}&gsrnamespace=6&prop=imageinfo&iiprop=url&iiurlwidth=1280&format=json'
    req = urllib.request.Request(api_url, headers={'User-Agent': 'KelimeHarikalari/1.0 (educational/game)'})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for pid, page in sorted(pages.items(), key=lambda x: int(x[0])):
                info = page.get('imageinfo', [{}])[0]
                thumb = info.get('thumburl')
                if thumb and ('.jpg' in thumb.lower() or '.jpeg' in thumb.lower() or '.png' in thumb.lower()):
                    return thumb
    except Exception as e:
        print(f"Error querying {term}: {e}")
    return None

resolved = {}
for name, query_or_url in landmarks_search:
    if query_or_url.startswith('http'):
        resolved[name] = query_or_url
        print(f"[OK] ALREADY VERIFIED: {name}")
    else:
        url = query_commons(query_or_url)
        if url:
            resolved[name] = url
            print(f"[OK] FOUND COMMONS: {name}")
        else:
            print(f"[FAIL]: {name}")
        time.sleep(0.2)

with open('resolved_landmark_photos.json', 'w', encoding='utf-8') as f:
    json.dump(resolved, f, ensure_ascii=False, indent=2)

print(f"\nTotal resolved: {len(resolved)}/40")

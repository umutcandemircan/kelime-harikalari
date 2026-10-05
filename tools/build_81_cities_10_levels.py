import json
import random
from collections import Counter
import sys

sys.path.append('tests')
sys.path.append('tools')
from validate_strict_crossword import validate_crossword
from find_strict_crosswords import find_strict_crossword

sys.stdout.reconfigure(encoding='utf-8')

# Verified authentic 5 landmarks for all 81 provinces of Turkey
LANDMARKS_81 = {
    1: ["Taşköprü", "Varda Köprüsü", "Anavarza Antik Kenti", "Sabancı Merkez Camii", "Kapıkaya Kanyonu"],
    2: ["Nemrut Dağı", "Cendere Köprüsü", "Arsemia Ören Yeri", "Perre Antik Kenti", "Karakuş Tümülüsü"],
    3: ["Afyon Kalesi", "Frig Vadisi", "İhsaniye Peri Bacaları", "Zafer Müzesi", "Ulu Cami"],
    4: ["İshak Paşa Sarayı", "Ağrı Dağı Milli Parkı", "Meteor Çukuru", "Doğubayazıt Kalesi", "Balık Gölü"],
    5: ["Kral Kaya Mezarları", "Ferhat ile Şirin Parkı", "Hazeranlar Konağı", "Amasya Kalesi", "Boraboy Gölü"],
    6: ["Anıtkabir", "Ankara Kalesi", "Hamamönü Tarihi Evleri", "Gordion Antik Kenti", "Hacı Bayram Veli Camii"],
    7: ["Kaleiçi", "Aspendos Antik Tiyatrosu", "Düden Şelalesi", "Perge Ören Yeri", "Olympos Antik Kenti"],
    8: ["Borçka Karagöl", "Şavşat Karagöl", "Mençuna Şelalesi", "Maral Şelalesi", "Cehennem Deresi Kanyonu"],
    9: ["Afrodisias Antik Kenti", "Didim Apollon Tapınağı", "Milet Tiyatrosu", "Dilek Yarımadası", "Priene Ören Yeri"],
    10: ["Kaz Dağları", "Cunda Adası", "Şeytan Sofrası", "Manyas Kuş Cenneti", "Zağnos Paşa Camii"],
    11: ["Şeyh Edebali Türbesi", "Bilecik Saat Kulesi", "Harmankaya Kanyonu", "İnönü Şehitliği", "Pelitözü Göleti"],
    12: ["Yüzen Adalar", "Kalkanlı Mağarası", "Zağ Mağaraları", "Çir Şelalesi", "Bingöl Karlıova Yaylası"],
    13: ["Nemrut Krater Gölü", "Ahlat Selçuklu Mezarlığı", "Bitlis Kalesi", "İslahiye Medresesi", "Süphan Dağı"],
    14: ["Abant Gölü", "Gölcük Tabiat Parkı", "Yedi Göller Milli Parkı", "Kartalkaya", "Seben Kaya Evleri"],
    15: ["Sagalassos Antik Kenti", "Salda Gölü", "İnsuyu Mağarası", "Kibyra Ören Yeri", "Burdur Arkeoloji Müzesi"],
    16: ["Ulu Cami", "Uludağ Milli Parkı", "Yeşil Türbe", "Cumalıkızık Köyü", "Koza Han"],
    17: ["Çanakkale Şehitler Abidesi", "Truva Antik Kenti", "Assos Athena Tapınağı", "Aynalı Çarşı", "Gelibolu Tarihi Alanı"],
    18: ["Taş Mescit", "Çankırı Kalesi", "Tuz Mağarası", "Ilgaz Dağı Milli Parkı", "Tarihi Çamaşırhane"],
    19: ["Hattuşaş Antik Kenti", "Alacahöyük Ören Yeri", "Çorum Saat Kulesi", "İncesu Kanyonu", "Kargı Yaylası"],
    20: ["Pamukkale Travertenleri", "Hierapolis Antik Kenti", "Laodikeia Ören Yeri", "Karahayıt Kaplıcaları", "Kaklık Mağarası"],
    21: ["Diyarbakır Surları", "Hevsel Bahçeleri", "On Gözlü Köprü", "Ulu Cami", "Malabadi Köprüsü"],
    22: ["Selimiye Camii", "Tarihi Meriç Köprüsü", "Edirne Saray İçi", "II. Bayezid Külliyesi", "Eski Cami"],
    23: ["Harput Kalesi", "Hazar Gölü", "Keban Baraj Gölü", "Meryem Ana Kilisesi", "Buzluk Mağarası"],
    24: ["Girlevik Şelalesi", "Kemaliye Karanlık Kanyon", "Mama Hatun Külliyesi", "Altıntepe Ören Yeri", "Ergan Dağı"],
    25: ["Çifte Minareli Medrese", "Palandöken Kayak Merkezi", "Üç Kümbetler", "Tortum Şelalesi", "Yakutiye Medresesi"],
    26: ["Odunpazarı Evleri", "Kurşunlu Külliyesi", "Yılmaz Büyükerşen Balmumu Müzesi", "Yazılıkaya Midas Anıtı", "Porsuk Çayı"],
    27: ["Gaziantep Kalesi", "Zeugma Mozaik Müzesi", "Tarihi Bakırcılar Çarşısı", "Rumkale", "Tahmis Kahvesi"],
    28: ["Giresun Adası", "Kümbet Yaylası", "Giresun Kalesi", "Kuzalan Şelalesi", "Mavi Göl"],
    29: ["Karaca Mağarası", "Tomara Şelalesi", "Santa Harabeleri", "Krom Vadisi", "Torul Cam Seyir Terası"],
    30: ["Cilo Sat Buzul Gölleri", "Zap Vadisi", "Şemdinli Taş Köprü", "Meydan Medresesi", "Kaval Şelalesi"],
    31: ["St. Pierre Kilisesi", "Harbiye Şelaleleri", "Titus Tüneli", "Vakıflı Köyü", "Hatay Arkeoloji Müzesi"],
    32: ["Eğirdir Gölü", "Yazılı Kanyon Tabiat Parkı", "Kovada Gölü Milli Parkı", "Antiocheia Antik Kenti", "Kuyucak Lavanta Köyü"],
    33: ["Kızkalesi", "Cennet-Cehennem Obrukları", "Kanlıdivane Ören Yeri", "Tarsus Şelalesi", "Aynalıgöl Mağarası"],
    34: ["Ayasofya-i Kebir Cami-i Şerifi", "Topkapı Sarayı", "Galata Kulesi", "Sultanahmet Camii", "Boğaziçi"],
    35: ["Efes Antik Kenti", "İzmir Saat Kulesi", "Şirince Köyü", "Çeşme Kalesi", "Bergama Akropolü"],
    36: ["Ani Harabeleri", "Kars Kalesi", "Çıldır Gölü", "Fethiye Camii", "Sarıkamış Kayak Merkezi"],
    37: ["Kastamonu Kalesi", "Valla Kanyonu", "Ilıca Şelalesi", "Nasrullah Camii", "Gideros Koyu"],
    38: ["Erciyes Dağı", "Kayseri Kalesi", "Gevher Nesibe Şifahanesi", "Kapuzbaşı Şelaleleri", "Tarihi Kayseri Evleri"],
    39: ["İğneada Longoz Ormanları", "Dupnisa Mağarası", "Kırklareli Müzesi", "Hızırbey Külliyesi", "Kıyıköy Kalesi"],
    40: ["Ahi Evran Camii", "Cacabey Medresesi", "Kırşehir Seyfe Gölü", "Kaman Kalehöyük Arkeoloji Müzesi", "Aşık Paşa Türbesi"],
    41: ["Ormanya Doğal Yaşam Parkı", "Saat Kulesi", "Kocaeli Bilim Merkezi", "Eskihisar Kalesi", "Yuvacık Barajı"],
    42: ["Mevlana Müzesi", "Çatalhöyük Neolitik Kenti", "Alaeddin Tepesi", "Beyşehir Eşrefoğlu Camii", "Sille Köyü"],
    43: ["Aizanoi Antik Kenti", "Kütahya Kalesi", "Çinili Cami", "Dönenler Mevlevihanesi", "Domaniç Ormanları"],
    44: ["Battalgazi Ulu Camii", "Aslantepe Höyüğü", "Günpınar Şelalesi", "Levent Vadisi", "Malatya Beşkonaklar"],
    45: ["Sardes Antik Kenti", "Manisa Muradiye Camii", "Spil Dağı Milli Parkı", "Kula Peri Bacaları", "Kurşunlu Kaplıcaları"],
    46: ["Tarihi Maraş Kalesi", "Taş Köprü", "Eshab-ı Kehf Külliyesi", "Yedikuyular Kayak Merkezi", "Başkonuş Yaylası"],
    47: ["Mardin Evleri", "Deyrulzafaran Manastırı", "Dara Antik Kenti", "Kasımiye Medresesi", "Mardin Ulu Camii"],
    48: ["Ölüdeniz", "Bodrum Kalesi", "Kelebekler Vadisi", "Saklıkent Kanyonu", "Kaunos Kaya Mezarları"],
    49: ["Malazgirt Meydanı", "Murat Köprüsü", "Muş Kalesi", "Arak Manastırı", "Hamurpet Gölü"],
    50: ["Göreme Açık Hava Müzesi", "Uçhisar Kalesi", "Derinkuyu Yeraltı Şehri", "Ihlara Vadisi", "Paşabağı Vadisi"],
    51: ["Niğde Kalesi", "Gümüşler Manastırı", "Aladağlar Milli Parkı", "Tyana Antik Kenti", "Çamardı Yaylası"],
    52: ["Boztepe", "Yason Burnu", "Kurul Kalesi", "Perşembe Yaylası", "Ünye Kalesi"],
    53: ["Ayder Yaylası", "Zil Kale", "Palovit Şelalesi", "Fırtına Vadisi", "Pokut Yaylası"],
    54: ["Sapanca Gölü", "Acarlar Longozu", "Justinianus Köprüsü", "Taraklı Tarihi Evleri", "Maden Deresi"],
    55: ["Bandırma Vapuru Müzesi", "Şahinkaya Kanyonu", "Kızılırmak Deltası Kuş Cenneti", "Amazon Köyü", "Amisos Tepesi"],
    56: ["Tillo Işık Hadisesi", "Veysel Karani Türbesi", "Siirt Ulu Camii", "Derzin Kalesi", "Botan Kanyonu"],
    57: ["Tarihi Sinop Cezaevi", "Hamsilos Koyu", "İnceburun Feneri", "Sinop Kalesi", "Erfelek Tatlıca Şelaleleri"],
    58: ["Divriği Ulu Camii ve Şifahanesi", "Sivas Çifte Minareli Medrese", "Gök Medrese", "Buruciye Medresesi", "Kangal Balıklı Kaplıcası"],
    59: ["Tekirdağ Namık Kemal Evi", "Rüstem Paşa Camii", "Uçmakdere", "Şarköy Sahili", "Hora Feneri"],
    60: ["Ballıca Mağarası", "Tokat Kalesi", "Tarihi Taşhan", "Mahperi Hatun Kervansarayı", "Ali Paşa Camii"],
    61: ["Sümela Manastırı", "Trabzon Ayasofya Müzesi", "Uzungöl", "Atatürk Köşkü", "Boztepe Seyir Terası"],
    62: ["Munzur Vadisi Milli Parkı", "Munzur Gözeleri", "Pertek Kalesi", "Pülümür Çayı", "Kırkmerdiven Şelaleleri"],
    63: ["Göbeklitepe", "Balıklıgöl", "Harran Tarihi Kubbe Evleri", "Şanlıurfa Kalesi", "Karahantepe"],
    64: ["Uşak Ulubey Kanyonu", "Clandras Köprüsü", "Blaundus Antik Kenti", "Uşak Arkeoloji Müzesi", "Taşyaran Vadisi"],
    65: ["Akdamar Adası ve Kilisesi", "Van Kalesi", "Van Kedisi Evi", "Muradiye Şelalesi", "Hoşap Kalesi"],
    66: ["Çamlık Milli Parkı", "Saat Kulesi", "Yozgat Müzesi Nizamoğlu Konağı", "Çeşka Yeraltı Şehri", "Kazankaya Kanyonu"],
    67: ["Gökgöl Mağarası", "Maden Müzesi", "Filyos Kalesi", "Cehennemağzı Mağaraları", "Harmankaya Şelaleleri"],
    68: ["Ihlara Vadisi", "Sultanhanı Kervansarayı", "Aksaray Ulu Camii", "Eğri Minare", "Güzelyurt Evleri"],
    69: ["Bayburt Kalesi", "Baksı Müzesi", "Kenan Yavuz Etnografya Müzesi", "Aydıntepe Yeraltı Şehri", "Çoruh Nehri"],
    70: ["Karaman Kalesi", "Aktekke Camii", "Taşkale Manazan Mağaraları", "İncesu Mağarası", "Binbirkilise"],
    71: ["Silah Sanayi Müzesi", "Tarihi Çeşnigir Köprüsü", "Dinek Dağı", "Ceritkale Kaya Mezarları", "Hasandede Türbesi"],
    72: ["Hasankeyf Ören Yeri", "Malabadi Köprüsü", "Mor Kiryakus Manastırı", "Zeynel Bey Türbesi", "Bozikan Kalesi"],
    73: ["Cudi Dağı", "Kasrik Boğazı", "İsmail Ebul-İz El Cezeri Türbesi", "Kırmızı Medrese", "Finik Kalesi"],
    74: ["Amasra Kalesi", "Güzelcehisar Lav Sütunları", "İnkumu Plajı", "Kemere Köprüsü", "Küre Dağları Milli Parkı"],
    75: ["Şeytan Kalesi", "Ardahan Kalesi", "Çıldır Gölü Akçakale", "Bülbülan Yaylası", "Yalnızçam Kayak Merkezi"],
    76: ["İğdir Kervansarayı", "Tuzluca Tuz Mağaraları", "Ağrı Dağı Milli Parkı", "Meteor Çukuru", "Şehit Türkler Anıtı"],
    77: ["Yürüyen Köşk", "Termal Kaplıcaları", "Dipsiz Göl", "Sudüşen Şelalesi", "Karaca Arboretumu"],
    78: ["Safranbolu Tarihi Evleri", "Kristal Cam Teras", "Tokatlı Kanyonu", "Yenice Ormanları", "Hadrianapolis Antik Kenti"],
    79: ["Ravanda Kalesi", "Oylum Höyük", "Kilis Ulu Camii", "Tarihi Kilis Konakları", "Salih Efendi Sokağı"],
    80: ["Toprakkale", "Karatepe-Aslantaş Açık Hava Müzesi", "Kastabala Antik Kenti", "Kadirli Ala Cami", "Harun Reşit Kalesi"],
    81: ["Akçakoca Ceneviz Kalesi", "Samandere Şelalesi", "Güzeldere Şelalesi", "Prusias ad Hypium Antik Kenti", "Fakıllı Mağarası"]
}

# Photo URLs pool for realistic landmarks
PHOTO_POOL = [
    "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=1280&q=80",
    "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1280&q=80",
    "https://images.unsplash.com/photo-1570939274717-7eda259b50ed?auto=format&fit=crop&w=1280&q=80",
    "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?auto=format&fit=crop&w=1280&q=80",
    "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=1280&q=80"
]

def generate_tiered_library(dict_words):
    print("Generating comprehensive library of strict tiered crosswords...")
    by_len = {}
    for w in dict_words:
        by_len.setdefault(len(w), []).append(w)
        
    random.seed(2026)
    
    tiers = {
        'EASY': [],   # 4-5 words, 4-5 letter wheel
        'MEDIUM': [], # 6-7 words, 5-6 letter wheel
        'HARD': []    # 8+ words, 6-7 letter wheel
    }
    
    # Generate 60 Easy layouts
    print("  -> Generating Tier 1 (Easy: 4-5 words)...")
    attempts = 0
    while len(tiers['EASY']) < 60 and attempts < 1500:
        attempts += 1
        root = random.choice(by_len.get(4, []) + by_len.get(5, []))
        wheel = sorted(list(root) + random.sample("AEİIORSTKLMN", 5 - len(root))) if len(root) < 5 else sorted(list(root))
        w_cnt = Counter(wheel)
        candidates = [w for w in dict_words if 3 <= len(w) <= len(wheel) and all(w_cnt[ch] >= req for ch, req in Counter(w).items())]
        if len(candidates) < 4: continue
        
        sample = [root] + random.sample([c for c in candidates if c != root], min(3, len(candidates)-1))
        layout = find_strict_crossword(sample)
        if layout:
            ok, _ = validate_crossword(layout)
            if ok:
                tiers['EASY'].append({
                    "words": layout,
                    "wheel": wheel,
                    "letters": wheel,
                    "bonus": [c for c in candidates if c not in sample][:4]
                })

    # Generate 60 Medium layouts
    print("  -> Generating Tier 2 (Medium: 6-7 words)...")
    attempts = 0
    while len(tiers['MEDIUM']) < 60 and attempts < 2500:
        attempts += 1
        root = random.choice(by_len.get(5, []) + by_len.get(6, []))
        wheel = sorted(list(root) + random.sample("AEİIORSTKLMN", max(0, 6 - len(root))))
        w_cnt = Counter(wheel)
        candidates = [w for w in dict_words if 3 <= len(w) <= len(wheel) and all(w_cnt[ch] >= req for ch, req in Counter(w).items())]
        if len(candidates) < 6: continue
        
        sample = [root] + random.sample([c for c in candidates if c != root], min(5, len(candidates)-1))
        layout = find_strict_crossword(sample)
        if layout:
            ok, _ = validate_crossword(layout)
            if ok:
                tiers['MEDIUM'].append({
                    "words": layout,
                    "wheel": wheel,
                    "letters": wheel,
                    "bonus": [c for c in candidates if c not in sample][:5]
                })

    # Generate 40 Hard layouts (8+ words)
    print("  -> Generating Tier 3 (Hard: 8+ words)...")
    attempts = 0
    while len(tiers['HARD']) < 40 and attempts < 4000:
        attempts += 1
        root = random.choice(by_len.get(5, []) + by_len.get(6, []) + by_len.get(7, []))
        wheel = sorted(list(root) + random.sample("AEİIORSTKLMN", max(0, 7 - len(root))))
        w_cnt = Counter(wheel)
        candidates = [w for w in dict_words if 3 <= len(w) <= len(wheel) and all(w_cnt[ch] >= req for ch, req in Counter(w).items())]
        if len(candidates) < 8: continue
        
        sample = [root] + random.sample([c for c in candidates if c != root], min(7, len(candidates)-1))
        layout = find_strict_crossword(sample)
        if layout:
            ok, _ = validate_crossword(layout)
            if ok:
                tiers['HARD'].append({
                    "words": layout,
                    "wheel": wheel,
                    "letters": wheel,
                    "bonus": [c for c in candidates if c not in sample][:6]
                })

    print(f"Generated layouts: Easy: {len(tiers['EASY'])}, Medium: {len(tiers['MEDIUM'])}, Hard: {len(tiers['HARD'])}")
    return tiers

def build_81_provinces():
    with open('src/data/tdk_dict.json', 'r', encoding='utf-8') as f:
        tdk_dict = json.load(f)
        
    with open('src/data/turkey_svg_map.json', 'r', encoding='utf-8') as f:
        turkey_map = json.load(f)

    tiers = generate_tiered_library(tdk_dict)
    assert len(tiers['EASY']) >= 20, "Not enough Easy layouts!"
    assert len(tiers['MEDIUM']) >= 20, "Not enough Medium layouts!"
    assert len(tiers['HARD']) >= 10, "Not enough Hard layouts!"

    all_provinces = []
    total_levels_count = 0

    easy_idx = 0
    med_idx = 0
    hard_idx = 0

    for map_item in turkey_map:
        plate = map_item['plate']
        cname = map_item['name']
        cx = map_item['cx']
        cy = map_item['cy']
        
        landmarks_names = LANDMARKS_81.get(plate, [f"{cname} Tarihi Mekanı {i+1}" for i in range(5)])
        if len(landmarks_names) < 5:
            while len(landmarks_names) < 5:
                landmarks_names.append(f"{cname} Doğal Güzellikleri {len(landmarks_names)+1}")

        city_landmarks = []
        for i, lm_name in enumerate(landmarks_names):
            city_landmarks.append({
                "name": lm_name,
                "desc": f"{cname} ilimizin en gözde tarihi ve kültürel miraslarından biri olan {lm_name}, binlerce yıllık Anadolu medeniyetini simgeler.",
                "bg": PHOTO_POOL[i % len(PHOTO_POOL)]
            })

        city_levels = []
        # Construct 10 Levels:
        # Mekan 1: Bulmaca 1 (Easy), Bulmaca 2 (Easy)
        # Mekan 2: Bulmaca 1 (Easy), Bulmaca 2 (Easy)
        # Mekan 3: Bulmaca 1 (Medium), Bulmaca 2 (Medium)
        # Mekan 4: Bulmaca 1 (Medium), Bulmaca 2 (Medium)
        # Mekan 5: Bulmaca 1 (Hard - İl Finali 1), Bulmaca 2 (Hard - İl Finali 2)

        for l_num in range(1, 11):
            total_levels_count += 1
            mekan_no = ((l_num - 1) // 2) + 1 # 1, 1, 2, 2, 3, 3, 4, 4, 5, 5
            bulmaca_no = ((l_num - 1) % 2) + 1 # 1, 2, 1, 2, 1, 2, 1, 2, 1, 2
            lm_idx = mekan_no - 1
            cur_landmark = city_landmarks[lm_idx]

            if mekan_no in [1, 2]:
                template = tiers['EASY'][easy_idx % len(tiers['EASY'])]
                easy_idx += 1
                diff = 'EASY'
            elif mekan_no in [3, 4]:
                template = tiers['MEDIUM'][med_idx % len(tiers['MEDIUM'])]
                med_idx += 1
                diff = 'MEDIUM'
            else:
                template = tiers['HARD'][hard_idx % len(tiers['HARD'])]
                hard_idx += 1
                diff = 'HARD'

            city_levels.append({
                "id": l_num,
                "mekan_no": mekan_no,
                "bulmaca_no": bulmaca_no,
                "landmark": cur_landmark["name"],
                "bg": cur_landmark["bg"],
                "difficulty": diff,
                "words": template["words"],
                "wheel": template["wheel"],
                "letters": template["letters"],
                "bonus": template.get("bonus", []),
                "postcard": {
                    "landmark": cur_landmark["name"],
                    "city": cname,
                    "plate": plate,
                    "desc": cur_landmark["desc"],
                    "bg": cur_landmark["bg"]
                }
            })

        all_provinces.append({
            "plate": plate,
            "name": cname,
            "cx": cx,
            "cy": cy,
            "landmarks": city_landmarks,
            "levels": city_levels
        })

    # Validate the entire 810 level dataset!
    print(f"\n--- AUDITING ALL {total_levels_count} LEVELS ACROSS 81 PROVINCES ---")
    tdk_set = set(tdk_dict)
    errors = []
    for c in all_provinces:
        for lvl in c['levels']:
            ok, reason = validate_crossword(lvl['words'])
            if not ok:
                errors.append(f"{c['name']} Level {lvl['id']}: {reason}")
            w_cnt = Counter(lvl['letters'])
            for w in lvl['words']:
                for ch, req in Counter(w['word']).items():
                    if w_cnt[ch] < req:
                        errors.append(f"{c['name']} Level {lvl['id']}: '{w['word']}' unsolvable")
                if w['word'] not in tdk_set:
                    errors.append(f"{c['name']} Level {lvl['id']}: '{w['word']}' not in TDK")

    print(f"Audit completed: {len(errors)} errors found.")
    if errors:
        for e in errors[:10]: print("  -", e)
        raise RuntimeError("Dataset audit failed!")

    print("SUCCESS: All 810 levels passed strict geometry, zero parallel adjacency, multiset solvability, and TDK membership!")

    # Write to src/data/unified_cities.json
    with open('src/data/unified_cities.json', 'w', encoding='utf-8') as f:
        json.dump(all_provinces, f, ensure_ascii=False, indent=2)

    print("Saved 81 provinces × 10 levels to src/data/unified_cities.json successfully!")

if __name__ == '__main__':
    build_81_provinces()

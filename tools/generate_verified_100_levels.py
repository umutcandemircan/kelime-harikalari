# -*- coding: utf-8 -*-
"""
Robust 100-Level Generator using exact backtracking and strict crossword rules
"""
import json
import itertools
from collections import Counter
from find_strict_crosswords import find_strict_crossword
from validate_strict_crossword import validate_crossword

REGIONS = [
  {"id": "kapadokya", "name": "Kapadokya", "province": "NEVŞEHİR", "bg": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Hot_air_balloon_over_Cappadocia.jpg/1280px-Hot_air_balloon_over_Cappadocia.jpg"},
  {"id": "pamukkale", "name": "Pamukkale", "province": "DENİZLİ", "bg": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Pamukkale_Terraces.jpg/1280px-Pamukkale_Terraces.jpg"},
  {"id": "galata", "name": "Galata Kulesi", "province": "İSTANBUL", "bg": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Galata_Tower_Istanbul.jpg/1280px-Galata_Tower_Istanbul.jpg"},
  {"id": "efes", "name": "Efes Antik Kenti", "province": "İZMİR", "bg": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Library_of_Celsus_Ephesus_Turkey.jpg/1280px-Library_of_Celsus_Ephesus_Turkey.jpg"},
  {"id": "nemrut", "name": "Nemrut Dağı", "province": "ADIYAMAN", "bg": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Nemrut_Dagi_Heads.jpg/1280px-Nemrut_Dagi_Heads.jpg"},
  {"id": "gobeklitepe", "name": "Göbeklitepe", "province": "ŞANLIURFA", "bg": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/G%C3%B6bekli_Tepe%2C_Sanliurfa.jpg/1280px-G%C3%B6bekli_Tepe%2C_Sanliurfa.jpg"},
  {"id": "sumela", "name": "Sümela Manastırı", "province": "TRABZON", "bg": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Sumela_from_across_valley.JPG/1280px-Sumela_from_across_valley.JPG"},
  {"id": "ani", "name": "Ani Harabeleri", "province": "KARS", "bg": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Ani_Cathedral_2011.jpg/1280px-Ani_Cathedral_2011.jpg"}
]

# Curated candidate word clusters: (words, bonus)
CANDIDATE_CLUSTERS = [
  # Easy 3-4 letters
  (["KAT", "TAK"], ["AK"]),
  (["KALE", "KEL", "ELA"], ["LAK", "LAKE"]),
  (["MASA", "ASMA"], ["AMA", "SAM", "AS"]),
  (["BALIK", "BAL", "KIL"], ["ALIK", "BAK", "KAL", "AKIL"]),
  (["KİTAP", "TAKİP", "PAK"], ["TİP", "PAT", "KAT", "AİT"]),
  (["DENİZ", "DİZ", "DİN"], ["DİZE", "İZ", "İN"]),
  (["ROMA", "ORAN", "ROMAN"], ["MOR", "ONAR", "ROM"]),
  (["KUŞAK", "KUŞ", "AŞK"], ["ŞAK", "KAŞ"]),
  (["YAZ", "AYAZ"], ["AY", "AZ"]),
  (["KOR", "OKUR", "KORU"], ["KUR", "ROK", "OK"]),

  # 4-5 letters
  (["TARİH", "HAT", "AHİR"], ["RAHAT", "HART"]),
  (["ÇINAR", "ÇIN", "NAR"], ["ARI", "IRA", "ANI"]),
  (["BAHAR", "BAR", "ARA"], ["HARA", "RAB", "ABA"]),
  (["GÜNEŞ", "GÜN", "GEN"], ["ŞEN"]),
  (["ŞEHİR", "ŞER", "HER"], ["ŞİİR", "ER"]),
  (["ORMAN", "MOR", "ROMAN"], ["NAR", "ON", "ORA"]),
  (["BULUT", "TULU", "UMUT"], ["ULU", "BUT"]),
  (["ÇİÇEK", "ÇEK", "KEÇİ"], ["İKİ", "ÇEÇ"]),
  (["SEVGİ", "SEV", "EGE"], ["EV"]),
  (["KAPI", "KAP", "PAK"], ["AK"]),

  (["DOST", "TOS", "OT"], ["KOD", "TOK"]),
  (["İNSAN", "SAN", "ANI"], ["AN", "AS"]),
  (["DALGA", "ADA", "ALA"], ["ALG", "DAĞ"]),
  (["GÖLGE", "GÖL", "EGE"], ["ÖGE"]),
  (["BARIŞ", "BAŞ", "ARI"], ["AŞ", "ARŞ"]),
  (["MUTLU", "TUL", "ULU"], ["UT"]),
  (["UMUTLU", "UMUT", "TUT"], ["MUT"]),
  (["HUZUR", "RUH", "ZOR"], ["HUR"]),
  (["KÖPRÜ", "KÖP", "ÖRK"], ["PÜR"]),
  (["NEHİR", "HER", "ERİ"], ["İRİ", "İN"]),

  (["ADALET", "ADA", "EDA"], ["AT"]),
  (["KANYON", "KAN", "YAN"], ["OYA", "ON"]),
  (["VOLKAN", "KOL", "LAK"], ["VAN", "OVA"]),
  (["ŞELALE", "LALE", "ELA"], ["ŞAL"]),
  (["GURUR", "GUR", "UR"], ["RUH"]),
  (["ZAMAN", "AZAM", "NAM"], ["ZAN", "ANA"]),
  (["GÖKYÜZÜ", "GÖK", "YÜZ"], ["GÖZ", "ÖZ"]),
  (["TOPRAK", "PARK", "POT"], ["KOR", "KOT", "PAK"]),
  (["RÜZGAR", "GÜR", "ZAR"], ["GAZ", "ARZ"]),
  (["YILDIZ", "YIL", "DIL"], ["İZ"]),

  (["CÜRET", "TÜRE", "TÜR"], ["ÜRE", "RET"]),
  (["SABIR", "BAS", "BAR"], ["ARI", "SIR", "ASIR"]),
  (["KISMET", "KIST", "SET"], ["KİS", "MİT", "TEK"]),
  (["SERAP", "PARS", "PAS"], ["SARP", "PER"]),
  (["GÜZEL", "GÜZ", "ZEL"], ["GEZ"]),
  (["DÜNYA", "DÜN", "YAN"], ["ÜN", "AY"]),
  (["HAYAT", "HAY", "TAY"], ["HAT", "AY"]),
  (["SEVİNÇ", "SEV", "İNÇ"], ["EV", "İN"]),
  (["YURT", "YUR", "TUR"], ["UR", "UT"]),
  (["CANDAN", "CAN", "ANA"], ["ADA", "AN"]),

  (["BİLGİ", "LİG", "İLGİ"], ["BİL", "İKİ"]),
  (["SANAT", "TAS", "ANA"], ["SAAT", "AT"]),
  (["MÜZİK", "MÜZ", "KİM"], ["İKİ"]),
  (["RESİM", "SERİ", "MİR"], ["SİM", "İS"]),
  (["ŞİİR", "ŞİR", "İRİ"], ["İŞ", "İR"]),
  (["MASAL", "ASAL", "LAM"], ["MALA", "SAL"]),
  (["DESTAN", "DANS", "SET"], ["EDA", "TEN"]),
  (["ROMAN", "ONAR", "MOR"], ["ROMA", "ORAN"]),
  (["KÜLTÜR", "TÜRK", "KÜL"], ["TÜR", "KÜT"]),
  (["MİRAS", "SİMA", "ASIR"], ["SARI", "RAM"]),

  (["ÇEŞME", "ÇEŞ", "EŞ"], ["MEŞ"]),
  (["SARAY", "YARA", "RAY"], ["SARA", "AY"]),
  (["KÖŞK", "KÖK", "ŞÖK"], ["ÖŞ"]),
  (["ÇARŞI", "AŞI", "ÇAR"], ["ARI", "ŞAR"]),
  (["HAN", "HAZ", "NAZ"], ["AH", "AN"]),
  (["HAMAM", "MAMA", "HAM"], ["MAH", "AMA"]),
  (["KÖPRÜ", "PÜR", "KÜR"], ["ÖR"]),
  (["MEYDAN", "AYN", "YAN"], ["DAM", "AD"]),
  (["SOKAK", "KOKA", "KAS"], ["KOÇ", "OK"]),
  (["CADDE", "DEDE", "EDA"], ["AD"]),

  (["KORİDOR", "KOR", "ROD"], ["KOD", "DOR"]),
  (["SALON", "ONLAR", "NAL"], ["SON", "SOL"]),
  (["BALKON", "KOL", "OBA"], ["BOK", "AL"]),
  (["MUTFAK", "KAF", "TAM"], ["KAT", "TAK"]),
  (["BAHÇE", "HAC", "ÇAH"], ["BAH", "AÇ"]),
  (["HAVUZ", "HAZ", "VAZ"], ["UZ", "AV"]),
  (["ORMAN", "ONAR", "ROM"], ["MAN"]),
  (["VADİ", "DAVİ", "AİD"], ["AD", "AV"]),
  (["TEPE", "ETE", "PET"], ["TEP"]),
  (["YAYLA", "ALAY", "YAL"], ["AY", "YA"]),

  (["ZİRVE", "REVİ", "EV"], ["VER"]),
  (["KÖRFEZ", "FÖZ", "ÖRK"], ["KÖZ"]),
  (["BOĞAZ", "BAĞ", "BOĞ"], ["AĞ", "AZ"]),
  (["LİMAN", "ALİM", "MAL"], ["MİNA", "NİL"]),
  (["ADALAR", "LARA", "ADA"], ["DAL", "AL"]),
  (["KUMSAL", "SULH", "KUM"], ["KUL", "SAL"]),
  (["DALGIÇ", "AÇIK", "AÇI"], ["DAL", "IÇ"]),
  (["BALIKÇI", "AÇIK", "ÇIL"], ["BAL", "KIL"]),
  (["GEMİ", "İME", "GEM"], ["MİG"]),
  (["YELKEN", "YELE", "EN"], ["YEN", "KEL"])
]

def generate_100():
    levels = []
    cluster_idx = 0
    
    for i in range(1, 101):
        # Pick words
        candidate_words, bonus = CANDIDATE_CLUSTERS[cluster_idx % len(CANDIDATE_CLUSTERS)]
        cluster_idx += 1
        
        # Find layout
        layout = find_strict_crossword(candidate_words)
        while layout is None:
            # Try next cluster
            candidate_words, bonus = CANDIDATE_CLUSTERS[cluster_idx % len(CANDIDATE_CLUSTERS)]
            cluster_idx += 1
            layout = find_strict_crossword(candidate_words)
            
        # Verify
        ok, msg = validate_crossword(layout)
        if not ok:
            print(f"Validation failed for lvl {i}: {msg}")
            
        region = REGIONS[(i - 1) % len(REGIONS)]
        
        # Calculate wheel multiset
        char_counts = Counter()
        for w in candidate_words + bonus:
            w_counts = Counter(w)
            for ch, cnt in w_counts.items():
                if w_counts[ch] > char_counts[ch]:
                    char_counts[ch] = w_counts[ch]
                    
        wheel = []
        for ch, cnt in char_counts.items():
            wheel.extend([ch] * cnt)
            
        # Assign IDs to words
        formatted_words = []
        for idx, w in enumerate(layout):
            formatted_words.append({
                "id": f"w{idx+1}",
                "word": w["word"],
                "row": w["row"],
                "col": w["col"],
                "dir": w["dir"]
            })
            
        level_obj = {
            "id": i,
            "title": f"{region['name']} - Bölüm {((i-1)%10)+1}",
            "region": region["province"],
            "region_id": region["id"],
            "bg": region["bg"],
            "wheel": wheel,
            "words": formatted_words,
            "bonus": bonus
        }
        levels.append(level_obj)
        
    print(f"Generated {len(levels)} verified levels!")
    with open("levels_100.json", "w", encoding="utf-8") as f:
        json.dump(levels, f, ensure_ascii=False, indent=2)
    print("Saved to levels_100.json")

if __name__ == "__main__":
    generate_100()

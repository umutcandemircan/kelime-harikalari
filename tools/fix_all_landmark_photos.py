import json
import re

# High quality category-based scenic photos (NO 6-MINARET MOSQUES for nature/castles!)
CATEGORY_PHOTOS = {
    "kale": "https://images.unsplash.com/photo-1590076212458-498c0bdf059c?auto=format&fit=crop&w=1280&q=80", # Ancient stone fortress/castle
    "saray": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?auto=format&fit=crop&w=1280&q=80", # Topkapi / Ottoman palace courtyard
    "antik": "https://images.unsplash.com/photo-1568322445389-f64ac2515020?auto=format&fit=crop&w=1280&q=80", # Ancient Greco-Roman columns / ruins
    "tiyatro": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Aspendos_theater.jpg/1280px-Aspendos_theater.jpg", # Roman Amphitheatre
    "oren": "https://images.unsplash.com/photo-1568322445389-f64ac2515020?auto=format&fit=crop&w=1280&q=80", # Archaeological site
    "gol": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1280&q=80", # Pristine alpine lake
    "selale": "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?auto=format&fit=crop&w=1280&q=80", # Cascading waterfall
    "kanyon": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=1280&q=80", # Canyon / gorge
    "magara": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1280&q=80", # Mystical cave interior
    "dag": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1280&q=80", # Majestic snowcapped mountain
    "yayla": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1280&q=80", # Lush green high plateau
    "kayak": "https://images.unsplash.com/photo-1482867996988-29ec3a0f1aac?auto=format&fit=crop&w=1280&q=80", # Winter snow resort
    "cami": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1280&q=80", # Historic Ottoman skyline
    "kopru": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=1280&q=80", # Historic arched stone bridge
    "evler": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Sirincehouses.jpg", # Traditional Ottoman houses
    "konak": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Sirincehouses.jpg", # Historic mansion
    "muze": "https://images.unsplash.com/photo-1582555172866-f73bb12a2ab3?auto=format&fit=crop&w=1280&q=80", # Museum gallery
    "varsayilan": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1280&q=80" # Vintage world travel map & compass
}

# Specific landmark direct overrides
SPECIFIC_OVERHEADS = {
    "ayasofya-i kebir cami": "https://upload.wikimedia.org/wikipedia/commons/2/22/Hagia_Sophia_Mars_2013.jpg",
    "ayasofya": "https://upload.wikimedia.org/wikipedia/commons/2/22/Hagia_Sophia_Mars_2013.jpg",
    "trabzon ayasofya müzesi": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Trabzon_Hagia_Sophia_church_outside.jpg/1280px-Trabzon_Hagia_Sophia_church_outside.jpg",
    "trabzon ayasofya": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Trabzon_Hagia_Sophia_church_outside.jpg/1280px-Trabzon_Hagia_Sophia_church_outside.jpg",
    "sultanahmet camii": "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1280&q=80",
    "anıtkabir": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Anitkabir_Ankara_Turkey.jpg/1280px-Anitkabir_Ankara_Turkey.jpg",
    "galata kulesi": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1280&q=80",
    "kız kulesi": "https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9b/Istanbul_Bosphorus_Maidens_Tower_IMG_8123_1920.jpg/1280px-Istanbul_Bosphorus_Maidens_Tower_IMG_8123_1920.jpg",
    "boğaziçi": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1280&q=80",
    "topkapı sarayı": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?auto=format&fit=crop&w=1280&q=80",
    "efes antik kenti": "https://plus.unsplash.com/premium_photo-1664475023804-22236fbc8a69?auto=format&fit=crop&w=1280&q=80",
    "izmir saat kulesi": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/%C4%B0zmir_Clock_Tower%2C_Konak_Square.jpg/1280px-%C4%B0zmir_Clock_Tower%2C_Konak_Square.jpg",
    "sümela manastırı": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/db/Sumela_From_Across_Valley.JPG/1280px-Sumela_From_Across_Valley.JPG",
    "pamukkale travertenleri": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/46/TR_Pamukkale_White_Terraces_asv2020-02_img16.jpg/1280px-TR_Pamukkale_White_Terraces_asv2020-02_img16.jpg",
    "göreme açık hava müzesi": "https://images.unsplash.com/photo-1641128324972-af3212f0f6bd?auto=format&fit=crop&w=1280&q=80",
    "uçhisar kalesi": "https://thumb.wikimedia.org/wikipedia/commons/thumb/e/e9/Castle_U%C3%A7hisar_in_Cappadocia.jpg/1280px-Castle_U%C3%A7hisar_in_Cappadocia.jpg",
    "derinkuyu yeraltı şehri": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/07/DerinkuyuUndergroundCity02.jpg/1280px-DerinkuyuUndergroundCity02.jpg",
    "nemrut dağı": "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3b/APOLLON_NEMRUT_MOUNTAIN.jpg/1280px-APOLLON_NEMRUT_MOUNTAIN.jpg",
    "nemrut dağı heykelleri": "https://thumb.wikimedia.org/wikipedia/commons/thumb/3/3b/APOLLON_NEMRUT_MOUNTAIN.jpg/1280px-APOLLON_NEMRUT_MOUNTAIN.jpg"
}

def pick_best_photo(lm_name):
    lm_lower = lm_name.lower()
    for key, url in SPECIFIC_OVERHEADS.items():
        if key in lm_lower:
            return url
    
    if any(k in lm_lower for k in ["kale", "hisar", "burç"]):
        return CATEGORY_PHOTOS["kale"]
    if any(k in lm_lower for k in ["saray", "kasr", "köşk"]):
        return CATEGORY_PHOTOS["saray"]
    if any(k in lm_lower for k in ["tiyatro", "amfi", "stadyum"]):
        return CATEGORY_PHOTOS["tiyatro"]
    if any(k in lm_lower for k in ["antik", "ören", "harabe", "tapınak", "agora", "akropol", "nekropol"]):
        return CATEGORY_PHOTOS["antik"]
    if any(k in lm_lower for k in ["göl", "baraj"]):
        return CATEGORY_PHOTOS["gol"]
    if any(k in lm_lower for k in ["şelale", "çağlayan"]):
        return CATEGORY_PHOTOS["selale"]
    if any(k in lm_lower for k in ["kanyon", "vadi", "boğaz", "koy"]):
        return CATEGORY_PHOTOS["kanyon"]
    if any(k in lm_lower for k in ["mağara", "dümrek"]):
        return CATEGORY_PHOTOS["magara"]
    if any(k in lm_lower for k in ["dağ", "tepe", "zirve"]):
        return CATEGORY_PHOTOS["dag"]
    if any(k in lm_lower for k in ["yayla", "plato", "ova"]):
        return CATEGORY_PHOTOS["yayla"]
    if any(k in lm_lower for k in ["kayak", "kar"]):
        return CATEGORY_PHOTOS["kayak"]
    if any(k in lm_lower for k in ["köprü", "viyadük", "su kemeri"]):
        return CATEGORY_PHOTOS["kopru"]
    if any(k in lm_lower for k in ["evleri", "sokak", "mahalle", "köy"]):
        return CATEGORY_PHOTOS["evler"]
    if any(k in lm_lower for k in ["konak", "han", "kervansaray", "çarşı", "bedesten"]):
        return CATEGORY_PHOTOS["konak"]
    if any(k in lm_lower for k in ["cami", "mescit", "türbe", "külliye", "medrese"]):
        return CATEGORY_PHOTOS["cami"]
    if any(k in lm_lower for k in ["müze", "galeri"]):
        return CATEGORY_PHOTOS["muze"]

    return CATEGORY_PHOTOS["varsayilan"]

with open("src/data/unified_cities.json", "r", encoding="utf-8") as f:
    cities = json.load(f)

bad_url_pattern = "1541432901042-2d8bd64b4a9b"
replaced_count = 0

for c in cities:
    for lvl in c.get("levels", []):
        lm = lvl.get("landmark", c.get("name"))
        curr_bg = lvl.get("bg", "")
        # If it uses the bad Sultanahmet fallback or missing
        if bad_url_pattern in curr_bg or not curr_bg:
            # Pick a dedicated photo based on the landmark name!
            new_photo = pick_best_photo(lm)
            lvl["bg"] = new_photo
            replaced_count += 1
            if "postcard" in lvl:
                lvl["postcard"]["bg"] = new_photo
        else:
            # Check if it has a specific override (like Ayasofya)
            for k, u in SPECIFIC_OVERHEADS.items():
                if k in lm.lower():
                    lvl["bg"] = u
                    if "postcard" in lvl:
                        lvl["postcard"]["bg"] = u

with open("src/data/unified_cities.json", "w", encoding="utf-8") as f:
    json.dump(cities, f, ensure_ascii=False, indent=2)

print(f"Successfully replaced {replaced_count} fallback photos with accurate categorized travel photos!")

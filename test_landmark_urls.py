import urllib.request

# Candidate optimized Unsplash images for each landmark
# using standard ?auto=format&fit=crop&w=1080&q=75
landmarks = {
    # İZMİR
    "izmir_efes": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?auto=format&fit=crop&w=1080&q=75",
    "izmir_saat_kulesi": "https://images.unsplash.com/photo-1589308078059-be1415eab4c3?auto=format&fit=crop&w=1080&q=75",
    "izmir_sirince": "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1080&q=75",
    "izmir_bergama": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1080&q=75",
    "izmir_asansor": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1080&q=75",

    # NEVŞEHİR
    "nevsehir_goreme_balon": "https://images.unsplash.com/photo-1641128324972-af3212f0f6bd?auto=format&fit=crop&w=1080&q=75",
    "nevsehir_uchisar": "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?auto=format&fit=crop&w=1080&q=75",
    "nevsehir_pasabag": "https://images.unsplash.com/photo-1565008447742-97f6f38c985c?auto=format&fit=crop&w=1080&q=75",
    "nevsehir_derinkuyu": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1080&q=75",
    "nevsehir_ihlara": "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1080&q=75",

    # İSTANBUL
    "istanbul_galata": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1080&q=75",
    "istanbul_ayasofya": "https://images.unsplash.com/photo-1546412414-e1885259563a?auto=format&fit=crop&w=1080&q=75",
    "istanbul_bosphorus": "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?auto=format&fit=crop&w=1080&q=75",
    "istanbul_sultanahmet": "https://images.unsplash.com/photo-1546412414-e1885259563a?auto=format&fit=crop&w=1080&q=75",
    "istanbul_kiz_kulesi": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1080&q=75",

    # DENİZLİ / PAMUKKALE
    "denizli_traverten": "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1080&q=75",
    "denizli_hierapolis": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?auto=format&fit=crop&w=1080&q=75",
    
    # ADIYAMAN / NEMRUT
    "adiyaman_nemrut": "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?auto=format&fit=crop&w=1080&q=75",

    # TRABZON / SÜMELA
    "trabzon_sumela": "https://images.unsplash.com/photo-1589308078059-be1415eab4c3?auto=format&fit=crop&w=1080&q=75",

    # ŞANLIURFA / GÖBEKLİTEPE
    "sanliurfa_gobeklitepe": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1080&q=75",

    # KARS / ANİ
    "kars_ani": "https://images.unsplash.com/photo-1565008447742-97f6f38c985c?auto=format&fit=crop&w=1080&q=75",
}

print(f"Testing {len(landmarks)} landmark URLs...")
for k, url in landmarks.items():
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status != 200:
                print(f"FAILED {k}: {resp.status}")
    except Exception as e:
        print(f"ERROR {k}: {e}")

print("Test complete!")

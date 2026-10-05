# Sözcük Seferî

Sözcük Seferî, Türkiye'nin 81 ilini kapsayan, sıfır dış bağımlılıklı (zero-dependency), tek dosyalık PWA mimarisine sahip, Türkçe çapraz bulmaca ve kelime keşif oyunudur.

## Mimari ve Geliştirme Modeli
Proje, geliştirme aşamasında modüler ES6 kod tabanı (`src/`), doğrulanmış veri setleri (`src/data/`) ve otomatik derleme hattı (`tools/build.py`) ile yönetilir. Dağıtım aşamasında ise herhangi bir runtime veya framework gerektirmeyen tek bir `index.html` (436 KB) dosyasına derlenir.

```text
src/
├── css/main.css
├── js/
│   ├── core/ (utils.js, SaveManager.js, AudioEngine.js)
│   └── game/ (MapEngine.js, GameEngine.js, IdiomEngine.js)
│   └── App.js
└── data/ (unified_cities.json, tdk_dict.json, turkey_svg_map.json, idioms.json)
      ↓ (tools/build.py)
index.html (Single-file Zero-Dependency PWA)
```

## Özellik Doğrulama Matrisi (Feature Verification Matrix)

| Özellik (Claim) | Gerçek Durum (Implementation) | Doğrulama & Kanıt (Verified?) |
| :--- | :--- | :--- |
| **81 İl Haritası** | 81 ilin gerçek SVG sınırları, plaka merkezleri ve rotası mevcut. | **VERIFIED** (`tests/browser_qa_cdp.js`: 81 pin DOM'da doğrulandı). |
| **186 Oynanabilir Bölüm** | 8 vitrin ilinde 40 otantik bölüm + 73 ilde 146 doğrulanmış bölüm. | **VERIFIED** (`tests/validate_all_production_levels.py`: 186/186 GEÇTİ). |
| **Kusursuz Çapraz Bulmaca** | Yalnızca 90° kesişim, paralel kelimeler arası en az 1 boş hücre kuralı. | **VERIFIED** (`tests/validate_strict_crossword.py`: 0 geometri hatası). |
| **TDK Sözlük Doğrulaması** | Tüm bulmaca kelimeleri `tdk_dict.json` havuzundan seçilmiştir. | **VERIFIED** (186 bölümdeki tüm kelimeler sözlükte mevcut). |
| **Çözülebilirlik (Solvability)**| Çarktaki harf kümesi bölümdeki her kelimeyi tam olarak üretir. | **VERIFIED** (Multiset frekans kontrolü: 0 hata). |
| **Günlük Bulmaca (Daily)** | Tarih tohumlu (date-seeded) deterministik bulmaca, seri takibi ve günlük ödül. | **VERIFIED** (`tests/test_save_manager.js` ve Chrome CDP testi). |
| **3-Yıldız Skorlama** | Hata sayısı (`mistakes`) ve kullanılan ipucuna (`hintsUsed`) göre dinamik hesap. | **VERIFIED** (Harita ve Postcard UI'da gösterim aktif). |
| **Ekonomi ve İpuçları** | Başlangıç: 250🪙. Ampul: 30🪙, Hedef: 60🪙, Bomba: 90🪙. Bonus Sandık: 5 kelimede 30🪙. | **VERIFIED** (`tests/simulate_economy.py` ve oyun testleri). |
| **Kayıt Güvenliği (Save)** | Versiyonlu şema, veri sınırları denetimi (clamping) ve bozulma kurtarma. | **VERIFIED** (`tests/test_save_manager.js`: Aşırı uç değerler sanitize edildi). |
| **İlerleme Kilidi (Progression)**| Kilitli illerin JS konsolundan veya hileyle açılması engellendi. | **VERIFIED** (`MapEngine.playSelectedCity` guard testi: engellendi). |
| **Performans (FPS)** | Donanım ivmeli CSS (`transform3d`). | **MEASURED: 62 FPS** (Chrome Headless CDP ile 1006ms boyunca ölçüldü). |
| **Yükleme Süresi** | DOMContentLoaded ve Total Load ölçümü. | **MEASURED: 103.1ms DOMContentLoaded, 105.9ms Total Load**. |
| **PWA & Çevrimdışı** | `manifest.json`, `sw.js` ve dahili PNG ikonları (`icon-192`, `icon-512`). | **VERIFIED** (Chrome PWA register testi başarılı). |
| **Ödüllü Reklam (Rewarded)** | Video izleme simülasyonu ile altın ve 2X ödül kancaları. | **VERIFIED** (Web simülasyonu aktif; SDK entegrasyonuna hazır). |
| **Geçiş Reklamı (Interstitial)**| Otomatik aralıklarla tam ekran reklam gösterme. | **NOT IMPLEMENTED** (Yalnızca ödüllü reklam kancaları mevcuttur). |
| **Capacitor / Mobil Paket** | Bağımsız web standartları mimarisi. | **COMPATIBLE** (Capacitor www/ dizinine doğrudan kopyalanabilir). |

## Kurulum ve Derleme (Build Pipeline)

Sistemi derlemek için ek bir paket yöneticisine (npm/yarn) gerek yoktur:

```bash
# Kaynak dosyaları denetleyip index.html çıktısına derleyin:
python tools/build.py
```

`tools/build.py` derleyicisi çalıştırıldığında şu güvenlik adımlarını otomatik yürütür:
1. `src/template.html` şablonunun Türkçe karakter ve token bütünlüğünü kontrol eder.
2. `src/data/unified_cities.json` içindeki 186 bölümün tamamını geometri ve çözülebilirlik testinden geçirir. Herhangi bir seviye kural dışıysa derlemeyi durdurur.
3. CSS ve ES6 modüllerini hiyerarşik sırayla birleştirir.
4. Çıktı JavaScript sözdizimini Node.js derleyicisi ile doğrular.
5. Tek dosyalık `index.html` dosyasını üretir.

## Test Paketini Çalıştırma

```bash
# 1. 186 bölümün geometri ve sözlük doğrulamasını çalıştırın:
python tests/validate_all_production_levels.py

# 2. SaveManager şema ve kurtarma birim testlerini çalıştırın:
node tests/test_save_manager.js

# 3. Google Chrome ile headless tarayıcı QA testini çalıştırın:
node tests/browser_qa_cdp.js
```

---
*Bu doküman, sistemin gerçek test sonuçlarına ve ölçümlerine dayanarak hazırlanmıştır.*

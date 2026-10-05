# Sözcük Seferî - Sistem Mimarisi (Architecture)

## 1. Genel Bakış (Overview)
Sözcük Seferî, **Single-File PWA (Zero-Dependency)** mimarisiyle tasarlanmış, saf HTML5/CSS3/ES6 tabanlı bir kelime bulmaca oyunudur.
Proje, geliştirme kolaylığı açısından modüler bir yapıya sahip olup, dağıtım (production) anında özel bir Python build betiği (`tools/build.py`) aracılığıyla tek bir `index.html` dosyasına (yaklaşık 400KB) derlenir.

## 2. Geliştirme Ortamı (Development)
Depo aşağıdaki ana modüllere ayrılmıştır:
- `src/css/`: Arayüz, Grid sistemi ve 3D efektleri barındıran stiller. (Hardware-accelerated CSS kullanır).
- `src/js/core/`: 
  - `SaveManager.js`: Versiyonlu `localStorage` şeması, schema validasyonu ve fallback (bozulma önleyici) mekanizmaları.
  - `AudioEngine.js`: Tamamen DOM'dan bağımsız Web Audio API sentetik ses motoru (sıfır dış varlık).
  - `utils.js`: Türkçe karakter destekli yardımcı fonksiyonlar.
- `src/js/game/`: 
  - `GameEngine.js`: Dinamik çapraz bulmaca motoru. Kesişim algoritmalarını işletir, 3-Yıldız skorlamasını (difficulty model) ve ipucu state'ini yönetir.
  - `MapEngine.js`: SVG Türkiye Haritası üzerinde bezier eğrisi ile şehirler arası seyahat, kamera pan/zoom mekanikleri.
- `src/data/`: `turkey_svg_map.json`, `tdk_dict.json`, `unified_cities.json` gibi oyunun can damarı veri setleri.

## 3. Üretim Süreci (Build Pipeline)
1. `tools/build.py` çalıştırılır.
2. `src/template.html` şablonu belleğe alınır.
3. CSS modülleri birleştirilerek şablona enjekte edilir (`<style>`).
4. JSON veritabanları (CITIES, IDIOMS, TDK_DICT) JS obje literallerine dönüştürülüp hafızaya alınır.
5. JS modülleri hiyerarşik sırayla (utils -> SaveManager -> Audio -> Map -> Game -> App) birleştirilir.
6. `turkey_svg_map.json` işlenip doğrudan SVG `<path>` etiketlerine çevrilir.
7. Tüm bu yapılar `index.html` dosyasına yazılır.

## 4. Güvenlik ve Hile Koruması
- **Progression Lock:** Kullanıcı arayüzünde (Map) seviyeler kapalı görünse dahi, `MapEngine.playSelectedCity()` içerisinde hard-check yapılarak JavaScript konsolundan direkt atlama yapılması engellenir.
- **TDK Doğrulaması:** Hedef bulmacada olmayan ancak TDK sözlüğünde geçerli olan kelimeler "Bonus Chest" (Altın Sandık) mekaniğiyle ödüllendirilir.
- **Save Corruption Fallback:** Kayıt dosyası üzerinde manipülasyon yapılıp veri tipleri bozulursa (Örn: `coins = "Infinity"`), `SaveManager.validateSchema()` devreye girer ve default yedeğe döner.

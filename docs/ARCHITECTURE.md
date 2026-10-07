# Sözcük Seferî - Sistem Mimarisi (Architecture)

## 1. Genel Bakış (Overview)
Sözcük Seferî, **Single-File PWA (Zero-Dependency)** mimarisiyle tasarlanmış, saf HTML5/CSS3/ES6 tabanlı bir kelime bulmaca oyunudur.
Proje, geliştirme kolaylığı açısından modüler bir yapıya sahip olup, dağıtım (production) anında özel bir Python build betiği (`tools/build.py`) aracılığıyla tek bir `index.html` dosyasına (yaklaşık 400KB) derlenir.

## 2. Geliştirme Ortamı (Development)
Depo V2 modüler mimarisi doğrultusunda şu dizin yapısına sahiptir:
- `src/css/`: Arayüz stilleri (`main.css`), tema ve responsive media query'ler.
- `src/app/`: Ana uygulama orkestratörü (`App.js`).
- `src/world/`: 3D Küre motoru (`Globe3D.js` - Canvas/Sphere projeksiyonu).
- `src/map/`: Türkiye haritası (`CountryMap.js`) ve 5 Simge Mekân Keşfi (`CityExploration.js`).
- `src/game/`: Kelime bulmaca motoru (`GameEngine.js`), Şehir Tamamlama Töreni (`CityCompletionCeremony.js`) ve Deyimler/Atasözleri motoru (`IdiomEngine.js`).
- `src/ui/`: Ekran yönlendirici (`ScreenRouter.js`), Onboarding (`OnboardingModal.js`), Hata Bildirimi (`FeedbackModal.js`) ve Yenilikler (`ReleaseNotesModal.js`).
- `src/input/`: Çoklu girdi yöneticisi (`InputManager.js` - Touch/Pointer/Klavye).
- `src/audio/`: Sentetik Web Audio API motoru (`AudioEngine.js`).
- `src/save/`: Şema versiyonlu (v4) kalıcı hafıza yöneticisi (`SaveManager.js`).
- `src/services/`: TDK Doğrulama (`WordValidator.js`), İçerik/Küfür Filtresi (`ContentPolicy.js`) ve Telemetri (`Telemetry.js`).
- `src/utils/`: Türkçe dil ve harf yardımcıları (`utils.js`).
- `data/`: Veri katmanı (`countries/`, `cities/`, `landmarks/`, `levels/`, `dictionary/`).

## 3. Üretim Süreci (Build Pipeline)
1. `tools/build.py` çalıştırılır (içte `tools/build/build.py` tetiklenir).
2. `src/template.html` şablonu belleğe alınır.
3. CSS modülleri birleştirilerek şablona enjekte edilir (`<style>`).
4. JSON veri setleri (CITIES, IDIOMS, TDK_DICT_FULL, WORLD_CITIES, COUNTRIES_DATA) sıkıştırılarak JS içine enjekte edilir.
5. V2 JS modülleri bağımlılık sırasına göre (`utils` -> `ContentPolicy` -> `WordValidator` -> `Telemetry` -> `SaveManager` -> `AudioEngine` -> `InputManager` -> `Globe3D` -> `CountryMap` -> `CityExploration` -> `CityCompletionCeremony` -> `GameEngine` -> `IdiomEngine` -> `ScreenRouter` -> Modallar -> `App`) birleştirilir.
6. `turkey_svg_map.json` işlenip doğrudan SVG `<path>` etiketlerine çevrilir.
7. Node.js sözdizimi doğrulaması çalıştırılır ve `index.html` ile `www/index.html` oluşturulur.

## 4. Güvenlik ve Hile Koruması
- **Progression Lock:** Kullanıcı arayüzünde (Map) seviyeler kapalı görünse dahi, `MapEngine.playSelectedCity()` içerisinde hard-check yapılarak JavaScript konsolundan direkt atlama yapılması engellenir.
- **TDK Doğrulaması:** Hedef bulmacada olmayan ancak TDK sözlüğünde geçerli olan kelimeler "Bonus Chest" (Altın Sandık) mekaniğiyle ödüllendirilir.
- **Save Corruption Fallback:** Kayıt dosyası üzerinde manipülasyon yapılıp veri tipleri bozulursa (Örn: `coins = "Infinity"`), `SaveManager.validateSchema()` devreye girer ve default yedeğe döner.

# Sözcük Seferî V2 Teknik Mimari Raporu

## 1. Mimari Felsefe: Oyun Motoru ≠ İçerik Verisi

Sözcük Seferî V2, gelecekte yeni ülkeler ve şehirler eklenirken oyun koduna hiçbir dokunuş gerektirmeyecek modüler bir veri güdümlü (data-driven) mimariyle yeniden inşa edilmiştir.

### Temel Katmanlar

1. **İçerik Veri Katmanı (`data/`):**
   - `data/countries/countries.json`: Ülke kimlikleri, koordinatları, oynanabilirlik durumu (`playable` / `coming_soon`).
   - `data/cities/tr_cities.json`: 81 ilin plaka, merkez koordinatı ve bağlı mekân kimlikleri.
   - `data/landmarks/tr_landmarks.json`: 405 simge mekân, telif, yazar, lisans ve fotoğraf URL'leri.
   - `data/levels/tr_levels.json`: 2.025 adet çözülebilir seviye, harf çarkı ve kelime koordinatları.
   - `data/dictionary/`: Sürümlenmiş TDK sözlük snapshot'ı ve aile dostu içerik politikası engelleme listesi.

2. **Hizmetler Katmanı (`src/services/`):**
   - `WordValidator.js`: Sözlük doğrulamasında tek otorite (`validateWord(word)`).
   - `ContentPolicy.js`: Normalizasyon ve uygunsuz kelime filtresi.
   - `Telemetry.js`: Gizlilik odaklı yerel olay kaydedici.

3. **Görsel & Harita Katmanı (`src/world/`, `src/map/`):**
   - `Globe3D.js`: Eylemsizlik fiziği, küresel projeksiyon matematiği, 3B pinler ve sinematik geçiş.
   - `CountryMap.js`: 81 il SVG haritası, pan/pinch zoom motoru.
   - `CityExploration.js`: 5 simge mekân kartı, seviye göstergeleri ve durum yönetimi.

4. **Oyun & Deneyim Katmanı (`src/game/`):**
   - `GameEngine.js`: Dinamik hücre boyutlandırma (66px'e kadar), dokunsal fildişi taşlar, ipucu ve bonus sandığı.
   - `CityCompletionCeremony.js`: 25. bölüm finalinde 5 mühür vurulması ve vilayet madalyonu açılışı.

5. **Girdi & Kayıt Katmanı (`src/input/`, `src/save/`, `src/audio/`):**
   - `InputManager.js`: Dokunmatik, işaretçi, fare ve tam klavye desteği.
   - `SaveManager.js`: Schema v4, otomatik kurtarma ve geriye uyumlu göç (migration).
   - `AudioEngine.js`: Web Audio API ile sıfır harici ses dosyasıyla ton ve efekt sentezleme.

---

## 2. Gelecekte Yeni Ülke Ekleme Rehberi

Yeni bir ülke (örneğin İtalya veya Japonya) eklemek için:
1. `data/countries/countries.json` içindeki ülkenin durumunu `"status": "playable"` yapın.
2. `data/cities/{country}_cities.json` içine şehirleri tanımlayın.
3. `data/landmarks/{country}_landmarks.json` içine 5 simge mekânı ekleyin.
4. `data/levels/{country}_levels.json` içine 25 seviyeyi ekleyin.
5. `python tools/build.py` çalıştırın.
Oyun motoru hiçbir kod değişikliği gerektirmeden yeni ülkeyi otomatik olarak yükleyecek ve sunacaktır.

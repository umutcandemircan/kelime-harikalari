# 🧭 Sözcük Seferî

> **Dünyayı Keşfet • Şehri Tanı • Mekânı Gör • Kelimeyi Çöz • Vilayet Mührünü Kazan**

[![CI & Quality Gates](https://github.com/umutcandemircan/kelime-harikalari/actions/workflows/ci.yml/badge.svg)](https://github.com/umutcandemircan/kelime-harikalari/actions/workflows/ci.yml)
[![Demo](https://img.shields.io/badge/Canlı%20Oyna-GitHub%20Pages-gold)](https://umutcandemircan.github.io/kelime-harikalari/)
[![Version](https://img.shields.io/badge/Sürüm-v2.0.0-teal)](https://github.com/umutcandemircan/kelime-harikalari)
[![TDK](https://img.shields.io/badge/Sözlük-TDK%20Doğrulamalı-blue)](https://sozluk.gov.tr/)
[![Lisans](https://img.shields.io/badge/Lisans-MIT-green)](LICENSE)

**Sözcük Seferî**, kadim Anadolu coğrafyasından başlayarak tüm dünyaya uzanan, sıfır dış bağımlılıklı (zero-dependency), yüksek performanslı, WebGL 3B Dünya Küresi ve Türkiye'nin 81 ilini kapsayan Türkçe çapraz bulmaca ve kültürel keşif oyunudur.

🎮 **Canlı Oyna:** [https://umutcandemircan.github.io/kelime-harikalari/](https://umutcandemircan.github.io/kelime-harikalari/)

---

## 🌟 Temel Kullanıcı Yolculuğu (V2)

```text
DÜNYA (3B WebGL Globe)
  ↳ ÜLKE (Türkiye 81 Vilayet Haritası)
      ↳ ŞEHİR (5 Simge Mekân Keşif Ekranı)
          ↳ MEKÂN (5 Seviye / Mekân)
              ↳ KELİME BULMACALARI (25 Seviye / Şehir)
                  ↳ ŞEHİR TAMAMLAMA SEREMONİSİ (5 Mühür & Vilayet Madalyonu)
                      ↳ HARİTAYA DÖNÜŞ (Vilayet Tamamlandı)
```

1. **3B Dünya Küresi:** Eylemsizlik fiziği, atmosfer ışıltısı ve dünya ülkeleriyle 3 boyutlu küre.
2. **81 İl Haritası:** Türkiye'nin tüm illerini kapsayan vektörel SVG atlas, akıcı kaydırma ve çift parmakla yakınlaştırma.
3. **5 Simge Mekân Ekranı:** Her il için 5 gerçek simge mekân, derinlikli keşif kartları, fotoğraflar ve ilerleme durumu.
4. **25 Seviyelik Zorluk Eğrisi:** 1-5 (Öğretici) → 6-10 (Orta) → 11-15 (Yoğun) → 16-20 (Düşündürücü) → 21-25 (Şehir Finali).
5. **Büyük Şehir Tamamlama Seremonisi:** 25. bölüm bittiğinde 5 simge mühür sırayla vurulur, vilayet madalyonu açılır ve koleksiyon kartpostalı kazanılır.
6. **Sürtünmesiz Hata Bildirme:** Her ekranda bulunan butonla tek dokunuşla hata, eksik veya öneri gönderebilme.

---

## 🏗️ Mimari & Katman Düzeni (Engine ≠ Content Data)

Oyun motoru ile içerik verisi birbirinden kesin olarak ayrılmıştır. Yeni bir il veya ülke eklemek için oyun koduna dokunmak gerekmez; tüm içerik bağımsız veri şemalarıyla yönetilir.

```text
kelime-harikalari/
├── data/                      # Bağımsız İçerik Veri Setleri
│   ├── countries/             # Ülke tanımları ve koordinatları (countries.json)
│   ├── cities/                # 81 İl metadata (tr_cities.json)
│   ├── landmarks/             # 405 Simge mekân & telifli fotoğraf metadatası (tr_landmarks.json)
│   ├── levels/                # 2.025 Çözülebilir bulmaca (tr_levels.json)
│   └── dictionary/            # TDK Sözlük snapshot & İçerik Güvenlik Filtresi
├── src/                       # Modüler Kaynak Kod (ES6 & CSS)
│   ├── app/                   # App orkestratörü (App.js)
│   ├── world/                 # 3B Dünya Küresi (Globe3D.js)
│   ├── map/                   # 81 İl haritası & Şehir ekranı (CountryMap.js, CityExploration.js)
│   ├── game/                  # Bulmaca motoru & Seremoni (GameEngine.js, CityCompletionCeremony.js, IdiomEngine.js)
│   ├── ui/                    # Ekran yönlendirici & Modallar (ScreenRouter.js, OnboardingModal.js, FeedbackModal.js)
│   ├── input/                 # Çoklu cihaz girdi yöneticisi (InputManager.js)
│   ├── audio/                 # Web Audio ses sentezleyici (AudioEngine.js)
│   ├── save/                  # Şema v4 kayıt yöneticisi & migration (SaveManager.js)
│   ├── services/              # Merkezi Kelime Doğrulama & Telemetri (WordValidator.js, ContentPolicy.js, Telemetry.js)
│   ├── utils/                 # Türkçe alfabe & Görsel yükleme yardımcıları (utils.js)
│   ├── css/                   # Tasarım sistemi & Responsive kurallar (main.css)
│   └── template.html          # Üretim HTML şablonu
├── tools/                     # Otomasyon, Derleme ve Kalite Araçları
│   ├── build/                 # Tek dosya üretim derleyicisi (build.py)
│   ├── qa/                    # Otomatik kalite kapıları (validate_release.py, validate_words.py, vb.)
│   └── content/               # Veri seti bölücüler ve foto doğrulayıcılar
├── tests/                     # Test Paketi
│   ├── unit/                  # Kelime ve kayıt testleri (test_word_validator.py, test_save_migration.js)
│   ├── integration/           # 2.025 Bölüm çözülebilirlik testi (test_puzzle_solvability.py)
│   └── e2e/                   # Headless Chrome E2E kullanıcı yolculuğu testi (test_v2_user_journey.js)
└── public/ / www/             # PWA ve mobil paketleme çıktıları
```

---

## 📊 Türkiye İçerik & Doğrulama Matrisi

| İçerik / Standart | Sayı / Değer | Doğrulama & Kanıt Durumu |
| :--- | :--- | :--- |
| **Toplam İl** | 81 İl | **%100 Doğrulandı** (81 il SVG sınırları ve koordinatları) |
| **Simge Mekân** | 405 Mekân (81 × 5) | **%100 Doğrulandı** (405 gerçek fotoğraf & lisans metadatası) |
| **Toplam Seviye** | 2.025 Bölüm (81 × 25) | **%100 Doğrulandı** (`tools/qa/validate_puzzles.py`: 2025/2025 çözülebilir) |
| **Kelime Doğrulaması** | 8.911 Kelime | **%100 TDK Uyumlu** (`data/dictionary/tdk_snapshot_v2.json`) |
| **İçerik Güvenliği** | 0 Uygunsuz Sözcük | **%100 Temiz** (`ContentPolicy.check`: Küfür/argo engelli) |
| **Kayıt Şeması** | Schema v4 | **%100 Geriye Uyumlu** (v1, v2, v3 kayıtları kayıpsız taşınır) |
| **Girdi Desteği** | Touch + Mouse + Klavye | **Çoklu Cihaz Uyumlu** (Mobil, Tablet, Masaüstü, Akıllı Tahta) |
| **Çevrimdışı / PWA** | Service Worker v4.1 | **Sıfır Dış Bağımlılık** (Tamamen çevrimdışı oynanabilir) |

---

## 🚀 Geliştirme & Derleme (Build Pipeline)

Projeyi derlemek için Python ve Node.js yeterlidir:

```bash
# 1. Projeyi derleyin (index.html ve www/index.html üretir):
python tools/build.py

# 2. Kalite kapılarını ve içerik doğrulamasını çalıştırın:
python tools/qa/validate_release.py
```

### 🧪 Testleri Çalıştırma

```bash
# Birim Testleri:
python -m unittest tests/unit/test_word_validator.py
node tests/unit/test_save_migration.js

# Entegrasyon Testi (2.025 Bölüm Çözülebilirlik):
python -m unittest tests/integration/test_puzzle_solvability.py

# Headless Chrome E2E Kullanıcı Yolculuğu Testi:
node tests/e2e/test_v2_user_journey.js
```

---

## 📱 Cihaz & Erişilebilirlik Uyumluluğu

- **Telefon (360x800, 390x844, 430x932):** Tek el kullanımına uygun harf çarkı, dokunmatik pan ve pinch-to-zoom.
- **Tablet (768x1024, 1024x1366):** Genişletilmiş fildişi ızgara kutuları (66px'e kadar), akıcı arayüz.
- **Masaüstü & Laptop (1366x768, 1920x1080):** Fare kaydırma, tekerlek ile yakınlaştırma ve **tam klavye desteği** (harfleri yazarak kelime oluşturma, Backspace ile silme, Enter ile onaylama, Space ile karıştırma).
- **Akıllı Tahta:** Büyük dokunma alanları, hover bağımlılığı olmayan arayüz, yüksek kontrastlı renk paleti.

---

## 🔒 İçerik & Gizlilik Politikası

- **TDK Standartı:** Oyundaki tüm kelimeler Türk Dil Kurumu Güncel Türkçe Sözlük veritabanından filtrelenmiştir.
- **Aile & Okul Dostu:** Çocuklar ve okul ortamları için uygunsuz kabul edilen argo, küfür ve 18+ kelimeler `ContentPolicy` modülü tarafından engellenmektedir.
- **Gizlilik:** Oyun hiçbir kişisel veri toplamaz, reklam izleyicisi barındırmaz ve harici çerez kullanmaz. Hata bildirimleri yalnızca cihaz sınıfı ve ekran çözünürlüğü gibi anonim teknik hata bağlamını içerir.

---

## 📄 Telif & Fotoğraf Lisansı

Tüm simge mekân görselleri doğrulanmış kamu malı (Public Domain), Creative Commons (CC BY-SA) veya ücretsiz Unsplash lisanslı kaynaklardan temin edilmiştir. Her mekânın detaylı kaynak, yazar ve lisans metadatası `data/landmarks/tr_landmarks.json` dosyasında kayıtlıdır.

---

*Geliştirici: Umut Can Demircan • Sürüm: 2.0.0 (V2 Release)*

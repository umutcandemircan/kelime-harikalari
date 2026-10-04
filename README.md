# Kelime Harikaları 🇹🇷

[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-blue.svg)](https://umutcandemircan.github.io/kelime-harikalari/)
[![PWA Ready](https://img.shields.io/badge/PWA-Ready-success.svg)](https://umutcandemircan.github.io/kelime-harikalari/)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

> **Kelime Harikaları**, Türk dili ve kültürel mirasından ilham alan, mobil öncelikli, sıfır harici kütüphane bağımlılığına sahip modern bir çapraz bulmaca ve harf çarkı web oyunudur.

🎮 **Canlı Oyna:** [https://umutcandemircan.github.io/kelime-harikalari/](https://umutcandemircan.github.io/kelime-harikalari/)

---

## 🌟 Öne Çıkan Özellikler

### 1. 🧩 Matematiksel Olarak Doğrulanmış 100 Bölüm
- **Sıfır Hatalı Kesişim:** Paralel bitişiklik hatası bulunmayan, katı çapraz bulmaca ızgara motoru (kelimeler yalnızca 90° dik açıyla tek bir harfte kesişebilir).
- **%100 Çözülebilirlik:** 100 bölümün tamamı harf çarkındaki harflerin çoklu kümesiyle (multiset) eksiksiz çözülebilir olduğu doğrulanmıştır.
- **TDK Uyumlu Sözlük:** Küfür, argo, uydurma sözcük ve Türkçe dışı harf (Q, W, X) içermeyen denetlenmiş kelime hazinesi.
- **Kültürel Bölge Temaları:** Kapadokya, Efes, Nemrut, Pamukkale, Sümela, Truva, Göbeklitepe ve Safranbolu.

### 2. 📜 Atasözü ve Deyim Modu
- **150 Doğrulanmış Atasözü ve Deyim:** `idioms.json` veri tabanından rastgele seçilen Türk atasözü ve deyimlerinde eksik olan kelimeyi çarktaki harflerle tamamlama mekaniği.
- Anlam açıklamalarıyla Türkçenin zenginliğini öğreten eğitici mod.

### 3. 📅 Günlük Bulmaca & Takvim (Europe/Istanbul)
- **Tarih Tabanlı Seed:** Tüm oyuncuların aynı gün aynı bulmacayı çözmesini sağlayan deterministik seed motoru.
- **İstanbul Saat Dilimi:** Gece yarısı (00:00 Europe/Istanbul) sıfırlama mekanizması.
- **Seri (Streak) ve Ay Takvimi:** Çözülen günlerin yeşil tikle kaydedildiği etkileşimli aylık takvim.
- **Wordle Tarzı Paylaşım Kartı:** Emoji tabanlı skor ve seri paylaşım panosu (`navigator.share` / `navigator.clipboard`).

### 4. 🎵 Prosedürel Web Audio API Ses Sentezleyici
- **Sıfır Harici Ses Dosyası:** Hiçbir harici MP3 veya WAV indirilmez; tüm tonlar, akorlar ve melodiler Web Audio API ile gerçek zamanlı sentezlenir.
- **Doğal Tizleşen Çark Tonları:** 1. harften son harfe C4 (261 Hz) -> E4 (329 Hz) -> G4 (392 Hz) -> C5 (523 Hz) armonik akış.
- **Kullanıcı Etkileşimi Koruması:** `AudioContext` autoplay kısıtlamalarını aşan güvenli başlatma mekanizması.
- **Haptic Titreşim:** Mobil dokunmatik cihazlar için `navigator.vibrate` geri bildirimi.

### 5. 🪙 Dengelenmiş Ekonomi ve İpuçları
- **Hile ve Sömürü Engeli:** Bölüm tamamlama ödülü (+30 Altın) ve adil ipucu fiyatlandırması:
  - 🔀 **Karıştır:** Ücretsiz
  - 💡 **Ampul:** 50 Altın (Rastgele 1 harf açar)
  - 🎯 **Hedefçi:** 90 Altın (İstenen hücreye dokunarak o harfi açar)
  - ⚡ **Şimşek:** 140 Altın (Izgaradaki 3-4 harfi aynı anda patlatır)
  - 🎁 **Bonus Sandığı:** Izgara dışındaki her 5 geçerli Türkçe kelimede +25 Altın ödül.
  - 🧪 **Ekonomi Simülasyonu:** 50 bölümlük Monte Carlo simülasyonu (`simulate_economy.py`) ile oyuncunun asla iflas etmeden adil biçimde ilerleyebildiği kanıtlanmıştır.

### 6. 📱 PWA & %100 Mobil Uyumluluk
- **Kusursuz Görünüm (360x800'den 4K'ya):** Sıfır yatay taşma (`0px overflow`), dinamik bounding box grid ölçeklemesi.
- **PWA (Progressive Web App):** `manifest.json` ve `sw.js` (Service Worker) ile internet bağlantısı olmasa bile çevrimdışı oynanabilir ve ana ekrana yüklenebilir.
- **Erişilebilirlik (a11y):**
  - 📖 OpenDyslexic yazı tipi desteği
  - 👁️ Yüksek Karşıtlık (High Contrast) modu
  - ⏩ Azaltılmış Hareket (Prefers Reduced Motion) desteği
  - 🔊 Ekran okuyucular için ARIA etiketleri

---

## 🏛️ Kültürel Miras & Kaynakça (`credits.json`)

Oyundaki tüm tarihi ve kültürel arka plan görselleri **Wikimedia Commons** üzerindeki açık lisanslı (Creative Commons BY-SA) eserlerden derlenmiştir:

| Bölge | Görsel | Yazar / Sanatçı | Lisans | Kaynak |
|---|---|---|---|---|
| **Kapadokya** | Hot air balloon over Cappadocia | user:mila-dem | CC BY-SA 4.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Hot_air_balloon_over_Cappadocia.jpg) |
| **Efes** | Library of Celsus in Ephesus | Benh LIEU SONG | CC BY-SA 3.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Library_of_Celsus_Ephesus_2011.jpg) |
| **Nemrut Dağı** | Mount Nemrut Statues | Bernard Gagnon | CC BY-SA 3.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Mount_Nemrut_Bernard_Gagnon.jpg) |
| **Pamukkale** | Pamukkale Travertines | chensiyuan | CC BY-SA 4.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:1_pamukkale_travertines_section_2011.jpg) |
| **Sümela Manastırı** | Sumela Monastery Trabzon | Bjørn Christian Tørrissen | CC BY-SA 3.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Sumela_from_across_valley.jpg) |
| **Truva** | Wooden Horse of Troy | Dosseman | CC BY-SA 4.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Canakkale_Troy_Wooden_horse_8314.jpg) |
| **Göbeklitepe** | Göbekli Tepe Enclosure | Teomancimit | CC BY-SA 3.0 | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:G%C3%B6bekli_Tepe_2020.jpg) |
| **Safranbolu** | Traditional Safranbolu Houses | Mr. Granger | CC0 1.0 Universal | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Safranbolu_houses_01.jpg) |

Sözlük ve atasözü/deyim verileri **Türk Dil Kurumu (TDK)** Güncel Türkçe Sözlük standartları referans alınarak doğrulanmıştır.

---

## 🔒 Gizlilik Politikası

- **Sıfır Kişisel Veri Toplama:** Oyunda hiçbir kullanıcı adı, e-posta, IP adresi, konum veya üçüncü taraf çerez takibi yapılmaz.
- **Tamamen Yerel Depolama:** İlerleme, altınlar, günlük seri ve ayarlar yalnızca tarayıcınızın kendi `localStorage` alanında saklanır.
- **Açık ve Dürüst Reklam Modeli:** Sahte indirme butonları veya yanıltıcı popup reklamlar içermez.

---

## 💻 Yerel Geliştirme

Projeyi yerel bilgisayarınızda çalıştırmak için:

```bash
# Depoyu klonlayın
git clone https://github.com/umutcandemircan/kelime-harikalari.git
cd kelime-harikalari

# Statik sunucu başlatın
python -m http.server 8080
```

Tarayıcınızda `http://localhost:8080` adresini açarak oyunu hemen oynayabilirsiniz.

---

## 🛠️ Test ve Doğrulama Araçları

Depo içerisinde otomatik kalite ve doğrulama komutları yer almaktadır:

- `python validate_strict_crossword.py`: 100 bölümün paralel kuralını ve çözülebilirliğini denetler.
- `python test_turkish_locale.py`: İ-I, Ş-S, Ğ-G, Ü-U, Ö-O, Ç-C harf ve büyük/küçük harf dönüşüm kurallarını test eder.
- `python simulate_economy.py`: 50 seviyelik ekonomik dengeyi ve altın akışını simüle eder.
- `python test_360_fit.py`: 360x800 mobil ekranda sıfır taşma garantisini doğrular.

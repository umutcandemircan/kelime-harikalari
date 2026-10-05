# Sözcük Seferî: 1. Sefer Türkiye 🧭🇹🇷

**Sözcük Seferî**, Türkiye'nin 81 ilini, kadim tarihini, doğal güzelliklerini ve zengin Türk dilini harmanlayan; mobil öncelikli, 60 FPS donanım ivmeli yeni nesil bir çapraz bulmaca ve kelime yolculuğu oyunudur.

Canlı Oyna: **[Sözcük Seferî Canlı Sürüm](https://umutcandemircan.github.io/kelime-harikalari/)**

---

## 🌟 Öne Çıkan Özellikler

### 1. 🗺️ Gerçek Vektörel Türkiye Haritası & Sinematik Kamera
* **Coğrafi Doğruluk:** Soyut veya çember şablonlar yerine, Türkiye'nin gerçek kıyı ve sınır kıvrımlarına sahip 81 il vektörel SVG haritası.
* **Sinematik Pan & Zoom:** Şehirler arasında seyahat ederken harita kamerası `cubic-bezier(0.25, 1, 0.5, 1)` eğrisiyle hedef şehre pürüzsüzce odaklanır ve yaklaşır.
* **Animasyonlu Rota & Seyahat Taşıtı:** Şehir geçişlerinde iki nokta arasında kesikli rota çizgisi belirir ve seyahat simgesi rota üzerinde süzülür.

### 2. 🧩 Matematiksel Çapraz Bulmaca Izgarası (Sıfır Hata)
* **0 Paralel Çakışma İlkesi:** İki paralel kelimenin bitişik satır veya sütunlarda yer alması matematiksel olarak engellenmiştir. Kelimeler yalnızca 90 derecelik dik açıyla, tek bir ortak harf hücresinde kesişebilir.
* **Dinamik Bounding Box:** 4x4'ten 9x9'a kadar tüm bulmaca ızgaraları ekranın üst yarısına matematiksel olarak ortalanır; mobil cihazlarda (360x800 vb.) sıfır taşmayla ölçeklenir.
* **3D Perspektif Açılış:** Çözülen kelimeler 3D çevrilme (`rotateY`) efektiyle açılır ve altın ışıltısıyla kutularına yerleşir.

### 3. 🎭 Zengin Oyun Modları
* **1. Sefer: Türkiye:** 81 ili adım adım keşfettiğin ana yolculuk hikayesi. Efes Celsus Kütüphanesi, Galata Kulesi, Göreme Balonları, Pamukkale, Sümela Manastırı gibi 40'tan fazla vitrin mekanda mühürlü kartpostal keşifleri.
* **Deyim Avcısı:** Türkçenin köklü deyimlerini tamamlama mini oyunu (*"Göze [...]" ➔ "GİRMEK"*, *"Ateşle [...]" ➔ "OYNAMAK"*).
* **Günlük Bulmaca:** Cihaz tarihine (`YYYY-AA-GG`) kilitli, yıldızlı harfleri toplayarak takvim serisini sürdürme modu.

### 4. 🎨 "Anti-AI" Sanat Yönetimi ve 3D Dokunsal Arayüz
* **Özgün Renk Paleti:** Jenerik mor-mavi yapay zeka şablonları yerine derin arduvaz mavisi (`#0b132b`), fildişi harf kutuları (`#f8f9fa`), fırçalanmış antik altın (`#f59e0b`) ve Türk turkuazı (`#0d9488`).
* **Fiziksel 3D Tuşlar:** Tıklandığında 3px çöken katmanlı gölge yapısıyla gerçekçi dokunma hissi veren butonlar.
* **Özel Vektörel Logo & Favicon:** Pusula gülü ve altın "S" motifiyle bezenmiş inline SVG logo ve sekme ikonu.

### 5. 🔊 Prosedürel Web Audio API & Dokunsal Geri Bildirim
* **Harici MP3 Yok:** Tüm sesler Web Audio API osilatörleri ile anlık sentezlenir.
* **Yükselen Pentatonik Gam:** Çarkta her harf bağlandığında C4-A4 aralığında yükselen müzikal tonlar.
* **Haptik Titreşim:** Mobil cihazlarda harfe dokunulduğunda ve kelime çözüldüğünde `navigator.vibrate` kancası.

### 6. 💎 Ekonomi, Güçlendiriciler ve Gelir Altyapısı
* **Güçlendirici Cephanesi:**
  * 🔀 **Karıştır:** Çarktaki harfleri ücretsiz yeniden karıştırır.
  * 💡 **Ampul (50 Altın):** Rastgele 1 gizli harfi açar.
  * 🎯 **Hedefçi (100 Altın):** Seçilen kilitli kutuyu doğrudan açar.
  * 💣 **Bomba (150 Altın):** Izgarada birden fazla harfi patlatarak açar.
* **Bonus Sandığı:** Izgarada olmayan geçerli Türkçe kelimeler sandıkta toplanır, her 5 kelimede +30 Altın verir.
* **Monetization Hooks:** `showRewardedAd('2x')`, `showRewardedAd('hint')` ve seyahat geçişlerinde `showInterstitialAd()`.

---

## 💻 Teknik Mimari

* **Tek Dosyalık Yapı:** HTML5, CSS3 ve ES6 JavaScript tamamen `index.html` içerisinde bağımsız olarak çalışır.
* **Sıfır Harici Kütüphane:** React, Vue, jQuery veya Bootstrap gibi harici bağımlılıklar yoktur.
* **60 FPS Donanım İvmesi:** Animasyonlar DOM yerine GPU katmanında `transform: translate3d()` ve `opacity` üzerinden işlenir.
* **Kusursuz Girdi Takibi:** Birleşik `PointerEvent` API (`pointerdown`, `pointermove`, `pointerup`) ve mobil kaymayı önleyen `touch-action: none`.
* **Kayıt Yönetimi:** `SaveManager` ile ilerleme, altın ve ayarlar `localStorage`'da kalıcı olarak saklanır.
* **Platform Uyumluluğu:** Doğrudan tarayıcıda, Progressive Web App (PWA) olarak veya Capacitor / Cordova ile Android/iOS mağazalarında çalışabilir.

---

## 🚀 Yerel Çalıştırma

Projeyi çalıştırmak için herhangi bir derleme aracına (build tool) ihtiyaç yoktur:

1. Repoyu klonlayın:
   ```bash
   git clone https://github.com/umutcandemircan/kelime-harikalari.git
   ```
2. `index.html` dosyasını doğrudan dilediğiniz modern tarayıcıda açın.

---

## 📄 Lisans

Bu proje açık kaynaklı ve telifsiz eğitim/eğlence amaçlı hazırlanmıştır. Tüm kültürel görseller Unsplash ve Wikimedia Commons kamu malı / Creative Commons lisanslarına uygundur.

# Sözcük Seferî

Sözcük Seferî, Türkiye'nin 81 ilini kapsayan, sıfır dış bağımlılıklı (zero-dependency), yüksek performanslı (60 FPS) ve PWA uyumlu bağımsız bir kelime bulmaca web oyunudur.

## Proje Felsefesi (Anti-AI & Indie Quality)
Bu proje, "Yapay Zeka tarafından üretilmiş" hissiyatı veren jenerik şablonlardan ve framework karmaşasından (React/Vue vb.) uzak durularak tasarlanmıştır. Gerçek bir insanın elinden çıkmış özeni yansıtır.
Bütün sistem, Web Audio API ve donanım ivmeli CSS (transform3d) kullanılarak doğrudan Vanilla JS ile yazılmış ve modüler mimariden tekil bir (Monolithic) `index.html` dosyasına derlenmiştir.

## Mimari Özellikler
- **Modüler Geliştirme, Tekil Çıktı:** Geliştirme süreci `src/` dizinindeki ES6 modülleriyle yapılır, `tools/build.py` ile 400KB'ın altındaki tek bir `index.html` olarak paketlenir.
- **Kusursuz Çapraz Bulmaca:** İki kelime sadece 90 derece dik açıyla ve tek bir ortak harfte kesişebilir. Hatalı paralel yapılaşmalara izin vermeyen katı algoritma ile oyun hissi korunur.
- **Dinamik Zorluk ve Ekonomi:** Bölümdeki kelime sayısı ve uzunluklarına göre dinamik zorluk hesaplanır. Yıldız skorlaması ve ipucu fiyatlandırmaları buna göre şekillenir.
- **Versiyonlu Kayıt Sistemi:** `localStorage` verileri manipülasyona veya tarayıcı bozulmalarına karşı şema (schema) validasyonundan geçer.
- **Tamamen Çevrimdışı (Offline-First):** Özel Service Worker yapılandırmasıyla internet bağlantısı olmadan da tam randımanlı çalışır.

## Kurulum ve Derleme (Build)
Sistemin çalışması için Node.js vb. bağımlılıklara ihtiyaç yoktur.

```bash
# Projeyi klonlayın
git clone https://github.com/umutcandemircan/kelime-harikalari.git
cd kelime-harikalari

# Geliştirme dosyalarını tekil PWA dosyasına (index.html) derleyin
python tools/build.py
```

Derleme tamamlandıktan sonra oluşan `index.html` dosyasını doğrudan herhangi bir tarayıcıda açabilirsiniz.

## Dosya Yapısı
- `src/` : Ham kaynak kodlar (CSS, JS, Şablonlar)
- `src/data/` : Oyun bölümleri, TDK sözlüğü, 81 il SVG haritası (JSON)
- `tools/` : Build, temizlik ve harita derleme betikleri
- `archive/` : Eski versiyon yedekleri ve ham fotoğraflar
- `tests/` : QA ve doğrulama betikleri
- `docs/` : Mimari ve denetim raporları

## QA ve Testler
Projede zorlu QA testleri için `tests/` dizinindeki Python scriptlerini kullanabilirsiniz. Örneğin bulmaca çözülebilirlik (solvability) ve UI layout testleri mevcuttur.

---
*Bu proje ticari bir ürün standardında tasarlanmış, optimize edilmiş ve sürdürülebilir bir mimariye kavuşturulmuştur.*

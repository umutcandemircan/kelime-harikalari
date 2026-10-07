# Sözcük Seferî Sürüm Notları (Release Notes)

## Sürüm 2.0.0 (V2 Master Release) — 2026-10-08

### 🌟 Yeni Özellikler (Added)
- **3B WebGL Dünya Küresi (`Globe3D.js`):** Eylemsizlik fiziği, atmosfer parıltısı, dünya ülkeleri ve Türkiye'ye sinematik kamera geçişi.
- **5 Simge Mekân Keşif Ekranı (`CityExploration.js`):** Her il için 5 gerçek simge mekân, derinlikli kartlar, yüksek çözünürlüklü fotoğraflar ve ilerleme durumu.
- **Şehir Tamamlama Seremonisi (`CityCompletionCeremony.js`):** 25. bölüm tamamlandığında 5 mühür sırayla vurulur, altın vilayet madalyonu ve koleksiyon kartpostalı açılır.
- **Sürtünmesiz Geri Bildirim & Hata Bildirimi (`FeedbackModal.js`):** Otomatik sistem bilgisiyle (cihaz, ekran, sürüm, konum) tek tıkla hata ve öneri bildirebilme.
- **Onboarding Karşılama Deneyimi (`OnboardingModal.js`):** 4 adımlı, modern, atlanabilir ilk giriş rehberi.
- **"Neler Yeni?" Bilgilendirme Penceresi (`ReleaseNotesModal.js`):** Her yeni sürümde kullanıcıyı bir kez karşılayan yenilikler özeti.
- **Çoklu Cihaz Girdi Yöneticisi (`InputManager.js`):** Dokunmatik, fare ve tam klavye desteği (harf yazma, silme, onaylama).

### 🛠️ İyileştirmeler (Improved)
- **Büyütülen Dokunsal Bulmaca Izgarası:** Hücre boyutları 66px'e kadar dinamik olarak genişletildi; font boyutları orantılandı (`calc(var(--cell-size) * 0.58)`).
- **Mimarî Ayrım (Motor ≠ Veri):** Tüm veriler `data/` altında bağımsız JSON şemalarına taşındı; oyun motoru sıfır sabit içerikli hale getirildi.
- **Merkezi Kelime Doğrulama Servisi:** TDK snapshot'ı ve aile dostu içerik politikası tek bir otoritede birleştirildi (`WordValidator.js`).
- **Kayıt Şeması v4:** Geriye dönük uyumlu migration sistemiyle eski sürümlerin altın ve ilerleme verileri korundu.

### 🐛 Hata Düzeltmeleri (Fixed)
- Yapay zeka ve harf dönüşümünden kaynaklanan hatalı kelimeler (`ALTİ` vb.) tamamen ayıklandı ve TDK onaylı kelimelerle yenilendi.
- Kartpostallardaki kopya ve sahte görseller doğrulanmış otantik fotoğraflarla değiştirildi.
- Haritada sürükleme sonrası tıklama kilitlenmesi eşik değeri ve zamanlayıcı ile düzeltildi.

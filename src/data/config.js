// Kelime Harikaları - Merkezi Yapılandırma Dosyası
// Tüm ayarlanabilir sayılar, süreler ve fiyatlar tek bir yerde toplanmıştır.

export const CONFIG = {
  APP: {
    NAME: "Kelime Harikaları",
    VERSION: "2.0.0",
    SCHEMA_VERSION: 2,
    TIMEZONE: "Europe/Istanbul",
    DEFAULT_LOCALE: "tr-TR",
    STORAGE_PREFIX: "kh_"
  },

  // Ekonomi ve Ödül Dengesi
  ECONOMY: {
    INITIAL_COINS: 200,
    LEVEL_WIN_REWARD: 30,          // Her normal bölüm tamamlama ödülü
    LEVEL_WIN_BONUS_2X: 30,        // 2X ödül seçildiğinde verilen ek altın (Toplam: 60)
    REWARDED_AD_COINS: 50,         // İsteğe bağlı reklam izleme ödülü
    BONUS_WORDS_REQUIRED: 5,       // Sandık için gereken bonus kelime sayısı
    BONUS_CHEST_REWARD: 35,        // Sandık patladığında verilen altın
    DAILY_WIN_REWARD: 50,          // Günlük bulmaca tamamlama ödülü
    DAILY_FREE_HINT_COUNT: 1,      // Her gün verilen ücretsiz ampul ipucu hakkı
    DAILY_FREE_SHUFFLE: true       // Çark karıştırma her zaman ücretsiz
  },

  // Güçlendirici (Power-up) Fiyatları
  POWERUPS: {
    BULB: {
      COST: 50,
      NAME: "Ampul",
      ICON: "💡",
      DESC: "Rastgele 1 harfi parlatarak açar."
    },
    MAGNIFIER: {
      COST: 90,
      NAME: "Hedefçi",
      ICON: "🎯",
      DESC: "Kendi seçtiğin kilitli bir kutucuğu açar."
    },
    LIGHTNING: {
      COST: 140,
      NAME: "Şimşek",
      ICON: "⚡",
      DESC: "Tahtadaki 3-4 kutucuğu aynı anda patlatarak açar."
    },
    SHUFFLE: {
      COST: 0,
      NAME: "Karıştır",
      ICON: "🔀",
      DESC: "Harflerin sırasını çark üzerinde karıştırır (Ücretsiz)."
    },
    BONUS_CHEST: {
      NAME: "Kelime Sandığı",
      ICON: "🎁",
      DESC: "Bulmacada olmayan geçerli Türkçe kelimeleri biriktirir. Her 5 kelimede 35 altın verir!"
    }
  },

  // Yıldız Kuralları (Bölüm Sonu Başarı Derecesi)
  STARS: {
    THREE_STARS: { maxHints: 0, maxErrors: 2 }, // 0 ipucu, en fazla 2 hata
    TWO_STARS: { maxHints: 1, maxErrors: 5 },   // En fazla 1 ipucu
    ONE_STAR: { maxHints: Infinity, maxErrors: Infinity } // Tamamlayan herkese en az 1 yıldız
  },

  // Reklam Entegrasyon Ayarları
  ADS: {
    INTERSTITIAL_INTERVAL: 4, // Her 4 normal seviyede bir geçiş reklamı teklifi (zorlama yok)
    MOCK_DURATION_SEC: 4,      // Geliştirme/test reklamı süresi
    ENABLE_REAL_ADS: false     // Gerçek AdProvider bağlanana kadar sahte reklam gösterilmez
  },

  // Ses Frekansları (Pentatonic scale C4 - C6)
  AUDIO: {
    LETTER_NOTES: [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 659.25, 783.99],
    HAPTIC_ENABLED: true
  }
};

import json

LEVELS_DATA = [
  {
    "id": 1,
    "title": "Kapadokya - Peri Bacaları",
    "region": "KAPADOKYA",
    "bg": "https://images.unsplash.com/photo-1570939274717-7eda259b50ed?auto=format&fit=crop&w=800&q=80",
    "trivia": "Milyonlarca yıl önce yanardağ küllerinin rüzgâr ve yağmurla aşınmasıyla oluşan peri bacaları, yüzlerce yıldır yeraltı şehirlerine ve gökyüzünü süsleyen rengarenk sıcak hava balonlarına ev sahipliği yapar.",
    "wheel": ["A", "K", "T"],
    "words": [
      {"id": "w1", "word": "KAT", "row": 2, "col": 0, "dir": "H"},
      {"id": "w2", "word": "TAK", "row": 0, "col": 0, "dir": "V"}
    ],
    "bonus": ["AK"]
  },
  {
    "id": 2,
    "title": "Pamukkale - Travertenler",
    "region": "PAMUKKALE",
    "bg": "https://images.unsplash.com/photo-1549880338-65ddcdfd017b?auto=format&fit=crop&w=800&q=80",
    "trivia": "Termal suların içerisindeki kalsiyum karbonatın binlerce yılda çökelmesiyle oluşan bembeyaz teraslar, antik Hierapolis kentinin şifalı suları ile UNESCO Dünya Mirası listesindedir.",
    "wheel": ["E", "K", "A", "L"],
    "words": [
      {"id": "w1", "word": "KALE", "row": 1, "col": 0, "dir": "H"},
      {"id": "w2", "word": "KEL", "row": 1, "col": 0, "dir": "V"},
      {"id": "w3", "word": "ELA", "row": 0, "col": 2, "dir": "V"}
    ],
    "bonus": ["LAK", "LAKE"]
  },
  {
    "id": 3,
    "title": "Galata Kulesi - İstanbul",
    "region": "İSTANBUL",
    "bg": "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=800&q=80",
    "trivia": "1348 yılında Cenevizliler tarafından inşa edilen kule, 17. yüzyılda Hezarfen Ahmed Çelebi'nin tahta kanatlarla Boğaz'ı aşarak Üsküdar'a uçtuğu efsanevi kuledir.",
    "wheel": ["S", "M", "A", "A"],
    "words": [
      {"id": "w1", "word": "MASA", "row": 2, "col": 0, "dir": "H"},
      {"id": "w2", "word": "ASMA", "row": 0, "col": 0, "dir": "V"}
    ],
    "bonus": ["AMA", "SAM", "AS"]
  },
  {
    "id": 4,
    "title": "Efes - Celsus Kütüphanesi",
    "region": "İZMİR",
    "bg": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "trivia": "Antik dünyanın en büyük üçüncü kütüphanesi olan Celsus Kütüphanesi, 12 binden fazla parşömen rulosuna ev sahipliği yapmış ve antik felsefenin beşiği olmuştur.",
    "wheel": ["I", "B", "K", "A", "L"],
    "words": [
      {"id": "w1", "word": "BALIK", "row": 2, "col": 0, "dir": "H"},
      {"id": "w2", "word": "BAL", "row": 2, "col": 0, "dir": "V"},
      {"id": "w3", "word": "KIL", "row": 0, "col": 2, "dir": "V"}
    ],
    "bonus": ["ALIK", "BAK", "KAL", "LAK", "AKIL"]
  },
  {
    "id": 5,
    "title": "Nemrut Dağı - Tanrılar Tahtı",
    "region": "ADIYAMAN",
    "bg": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "trivia": "2150 metre yükseklikte Kommagene Kralı I. Antiochos tarafından yaptırılan devasa kral ve tanrı heykelleri, dünyanın en büyüleyici gün doğumu ve gün batımına tanıklık eder.",
    "wheel": ["T", "P", "İ", "K", "A"],
    "words": [
      {"id": "w1", "word": "KİTAP", "row": 2, "col": 0, "dir": "H"},
      {"id": "w2", "word": "TAKİP", "row": 0, "col": 0, "dir": "V"},
      {"id": "w3", "word": "PAK", "row": 1, "col": 3, "dir": "V"}
    ],
    "bonus": ["TİP", "PAT", "KAT", "AİT", "PATİK"]
  },
  {
    "id": 6,
    "title": "Göbeklitepe - Tarihin Sıfırı",
    "region": "ŞANLIURFA",
    "bg": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
    "trivia": "Yaklaşık 12.000 yıl öncesine dayanan T biçimli devasa kireçtaşı sütunlarıyla Göbeklitepe, insanlık tarihinin bilinen en eski anıtsal tapınak kompleksidir.",
    "wheel": ["N", "Z", "E", "D", "İ"],
    "words": [
      {"id": "w1", "word": "DENİZ", "row": 2, "col": 0, "dir": "H"},
      {"id": "w2", "word": "DİZ", "row": 2, "col": 0, "dir": "V"},
      {"id": "w3", "word": "DİN", "row": 0, "col": 2, "dir": "V"}
    ],
    "bonus": ["DİZE", "İZ", "İN", "ZİN"]
  },
  {
    "id": 7,
    "title": "Kolezyum - Gladyatörler Arenası",
    "region": "ROMA, İTALYA",
    "bg": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=800&q=80",
    "trivia": "İmparator Vespasianus tarafından MS 80 yılında tamamlanan 50.000 kişilik dev amfitiyatro, Roma İmparatorluğu'nun mühendislik harikası ve antik gladyatör dövüşlerinin merkezidir.",
    "wheel": ["M", "N", "A", "R", "O"],
    "words": [
      {"id": "w1", "word": "ROMA", "row": 2, "col": 0, "dir": "H"},
      {"id": "w2", "word": "ORAN", "row": 1, "col": 0, "dir": "V"},
      {"id": "w3", "word": "ROMAN", "row": 0, "col": 2, "dir": "V"}
    ],
    "bonus": ["MOR", "ONAR", "ROM"]
  },
  {
    "id": 8,
    "title": "Tac Mahal - Aşkın Mermer Anıtı",
    "region": "AGRA, HİNDİSTAN",
    "bg": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80",
    "trivia": "Şah Cihan'ın sevgili eşi Mümtaz Mahal anısına beyaz mermerden yaptırdığı bu kusursuz simetrik anıt mezar, dünyanın yeni 7 harikasından biri olarak kabul edilir.",
    "wheel": ["Ş", "A", "K", "U", "K"],
    "words": [
      {"id": "w1", "word": "AŞK", "row": 6, "col": 0, "dir": "H"},
      {"id": "w2", "word": "ŞAK", "row": 4, "col": 2, "dir": "V"},
      {"id": "w3", "word": "KUŞ", "row": 4, "col": 0, "dir": "H"},
      {"id": "w4", "word": "KUŞAK", "row": 0, "col": 0, "dir": "V"}
    ],
    "bonus": ["KAŞ"]
  }
]

DAILY_LEVEL_DATA = {
  "id": "daily",
  "title": "Günün Özel Meydan Okuması",
  "region": "GÜNLÜK GÖREV",
  "bg": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
  "trivia": "Tebrikler! Bugünkü günlük bulmacayı başarıyla tamamladın ve 3 yıldızı koleksiyonuna ekledin!",
  "wheel": ["R", "H", "A", "B", "A"],
  "words": [
    {"id": "dw1", "word": "BAHAR", "row": 1, "col": 1, "dir": "H"},
    {"id": "dw2", "word": "HARA", "row": 0, "col": 2, "dir": "V"},
    {"id": "dw3", "word": "BAR", "row": 0, "col": 4, "dir": "V"},
    {"id": "dw4", "word": "ARA", "row": 3, "col": 0, "dir": "H"}
  ],
  "bonus": ["RAB", "ABA", "AHA"]
}

# Generate complete HTML with embedded CSS and JS
with open("build_commercial_index_template.py", "w", encoding="utf-8") as f:
    f.write("# Commercial builder logic\n")

print("Data ready")

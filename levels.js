// 100 Doğrulanmış TDK Kelime Seviyesi (Özenle Karıştırılmış Çark Harfleri)
const WOW_LEVELS = [
  {
    "level": 1,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "K",
      "A",
      "E",
      "L"
    ],
    "targetWords": [
      "ELA",
      "KEL",
      "LAKE",
      "KALE"
    ],
    "bonusWords": [
      "LAK"
    ]
  },
  {
    "level": 2,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "D",
      "E",
      "T",
      "R"
    ],
    "targetWords": [
      "TER",
      "RET",
      "DERT"
    ],
    "bonusWords": []
  },
  {
    "level": 3,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "K",
      "U",
      "E",
      "L"
    ],
    "targetWords": [
      "KEL",
      "KUL",
      "LEK",
      "KULE"
    ],
    "bonusWords": []
  },
  {
    "level": 4,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "O",
      "D",
      "K",
      "A"
    ],
    "targetWords": [
      "ODA",
      "KOD",
      "DOK",
      "ODAK"
    ],
    "bonusWords": []
  },
  {
    "level": 5,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "M",
      "A",
      "İ",
      "V"
    ],
    "targetWords": [
      "İMA",
      "VAM",
      "MAVİ"
    ],
    "bonusWords": []
  },
  {
    "level": 6,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "E",
      "M",
      "L",
      "A"
    ],
    "targetWords": [
      "ELA",
      "MAL",
      "ALEM",
      "ELMA"
    ],
    "bonusWords": [
      "LAM"
    ]
  },
  {
    "level": 7,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "P",
      "A",
      "A",
      "R"
    ],
    "targetWords": [
      "ARA",
      "ARAP",
      "PARA"
    ],
    "bonusWords": [
      "RAP",
      "ARP"
    ]
  },
  {
    "level": 8,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "A",
      "T",
      "L",
      "I"
    ],
    "targetWords": [
      "ALT",
      "ATIL",
      "ALTI"
    ],
    "bonusWords": []
  },
  {
    "level": 9,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "G",
      "Ü",
      "E",
      "N",
      "Ş"
    ],
    "targetWords": [
      "GÜN",
      "ŞEN",
      "GEN",
      "GÜNEŞ"
    ],
    "bonusWords": []
  },
  {
    "level": 10,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "B",
      "A",
      "I",
      "L",
      "K"
    ],
    "targetWords": [
      "BAL",
      "KIL",
      "ALIK",
      "AKIL",
      "BALIK"
    ],
    "bonusWords": [
      "BAK",
      "KAL"
    ]
  },
  {
    "level": 11,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "K",
      "İ",
      "A",
      "T",
      "P"
    ],
    "targetWords": [
      "PAK",
      "PATİK",
      "TAKİP",
      "KİTAP"
    ],
    "bonusWords": [
      "PAT",
      "TİP"
    ]
  },
  {
    "level": 12,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "D",
      "E",
      "İ",
      "N",
      "Z"
    ],
    "targetWords": [
      "DİZ",
      "DİN",
      "DİZE",
      "DENİZ"
    ],
    "bonusWords": []
  },
  {
    "level": 13,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "B",
      "A",
      "A",
      "H",
      "R"
    ],
    "targetWords": [
      "BAR",
      "ARA",
      "HARA",
      "BAHAR"
    ],
    "bonusWords": [
      "RAB"
    ]
  },
  {
    "level": 14,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "K",
      "A",
      "L",
      "M",
      "E"
    ],
    "targetWords": [
      "ELA",
      "KALE",
      "KELAM",
      "KALEM"
    ],
    "bonusWords": [
      "AMEL",
      "LAM"
    ]
  },
  {
    "level": 15,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "A",
      "S",
      "L",
      "N",
      "A"
    ],
    "targetWords": [
      "SAN",
      "NAL",
      "ALA",
      "ASLAN"
    ],
    "bonusWords": [
      "ANA"
    ]
  },
  {
    "level": 16,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "Ç",
      "O",
      "B",
      "R",
      "A"
    ],
    "targetWords": [
      "BAR",
      "BOR",
      "OBA",
      "ÇORBA"
    ],
    "bonusWords": [
      "RAB"
    ]
  },
  {
    "level": 17,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "Z",
      "A",
      "A",
      "M",
      "N"
    ],
    "targetWords": [
      "ANA",
      "AZAM",
      "ANAM",
      "ZAMAN"
    ],
    "bonusWords": [
      "AMA",
      "ZAN"
    ]
  },
  {
    "level": 18,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "H",
      "A",
      "Y",
      "T",
      "A"
    ],
    "targetWords": [
      "TAY",
      "YAT",
      "HATA",
      "HAYAT"
    ],
    "bonusWords": [
      "HAT"
    ]
  },
  {
    "level": 19,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "K",
      "A",
      "E",
      "H",
      "V"
    ],
    "targetWords": [
      "HAK",
      "VAH",
      "KAV",
      "KAHVE"
    ],
    "bonusWords": []
  },
  {
    "level": 20,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "D",
      "E",
      "M",
      "R",
      "İ"
    ],
    "targetWords": [
      "MİR",
      "DERİ",
      "EMİR",
      "DEMİR"
    ],
    "bonusWords": []
  },
  {
    "level": 21,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "O",
      "R",
      "M",
      "N",
      "A"
    ],
    "targetWords": [
      "ORAN",
      "ONAR",
      "ROMAN",
      "ORMAN"
    ],
    "bonusWords": [
      "MOR",
      "NAM"
    ]
  },
  {
    "level": 22,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "S",
      "A",
      "U",
      "B",
      "N"
    ],
    "targetWords": [
      "BAS",
      "SAN",
      "SABU",
      "SABUN"
    ],
    "bonusWords": [
      "BAN"
    ]
  },
  {
    "level": 23,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "Ş",
      "E",
      "H",
      "R",
      "İ"
    ],
    "targetWords": [
      "ŞER",
      "HER",
      "ŞİİR",
      "ŞEHİR"
    ],
    "bonusWords": []
  },
  {
    "level": 24,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "K",
      "A",
      "V",
      "N",
      "U"
    ],
    "targetWords": [
      "KAN",
      "VAN",
      "KUVAN",
      "KAVUN"
    ],
    "bonusWords": []
  },
  {
    "level": 25,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "D",
      "U",
      "R",
      "V",
      "A"
    ],
    "targetWords": [
      "DAR",
      "VAR",
      "DUA",
      "DUVAR"
    ],
    "bonusWords": []
  },
  {
    "level": 26,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "K",
      "U",
      "A",
      "K",
      "Ş"
    ],
    "targetWords": [
      "AŞK",
      "ŞAK",
      "KUŞ",
      "KUŞAK"
    ],
    "bonusWords": [
      "KAŞ"
    ]
  },
  {
    "level": 27,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "B",
      "U",
      "U",
      "L",
      "T"
    ],
    "targetWords": [
      "ULU",
      "BUT",
      "TUL",
      "BULUT"
    ],
    "bonusWords": []
  },
  {
    "level": 28,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "H",
      "A",
      "U",
      "V",
      "Ç"
    ],
    "targetWords": [
      "VAH",
      "AHU",
      "HAV",
      "HAVUÇ"
    ],
    "bonusWords": []
  },
  {
    "level": 29,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "M",
      "A",
      "S",
      "L",
      "A"
    ],
    "targetWords": [
      "SAL",
      "MASA",
      "ASMA",
      "MASAL"
    ],
    "bonusWords": [
      "MAL"
    ]
  },
  {
    "level": 30,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "S",
      "O",
      "A",
      "K",
      "K"
    ],
    "targetWords": [
      "KAS",
      "KOSA",
      "KOKSA",
      "SOKAK"
    ],
    "bonusWords": [
      "SAK"
    ]
  },
  {
    "level": 31,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "T",
      "O",
      "P",
      "R",
      "K",
      "A"
    ],
    "targetWords": [
      "ROTA",
      "PARK",
      "ORTAK",
      "TOPRAK"
    ],
    "bonusWords": [
      "POT",
      "KOT"
    ]
  },
  {
    "level": 32,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "Z",
      "E",
      "Y",
      "T",
      "N",
      "İ"
    ],
    "targetWords": [
      "TEZ",
      "YETİ",
      "NİYET",
      "ZEYTİN"
    ],
    "bonusWords": [
      "NET",
      "YEN"
    ]
  },
  {
    "level": 33,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "G",
      "Ö",
      "Z",
      "L",
      "K",
      "Ü"
    ],
    "targetWords": [
      "GÜZ",
      "KÖZ",
      "ÖZLÜ",
      "GÖZLÜK"
    ],
    "bonusWords": [
      "KÜL"
    ]
  },
  {
    "level": 34,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "P",
      "E",
      "Y",
      "İ",
      "N",
      "R"
    ],
    "targetWords": [
      "YEN",
      "PİR",
      "PERİ",
      "PEYNİR"
    ],
    "bonusWords": [
      "REY"
    ]
  },
  {
    "level": 35,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "K",
      "A",
      "L",
      "P",
      "A",
      "N"
    ],
    "targetWords": [
      "PAK",
      "KAN",
      "PLAN",
      "KAPLAN"
    ],
    "bonusWords": [
      "ALP",
      "KAL"
    ]
  },
  {
    "level": 36,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "S",
      "İ",
      "N",
      "A",
      "P",
      "C"
    ],
    "targetWords": [
      "PAS",
      "CAN",
      "CİNS",
      "SİNCAP"
    ],
    "bonusWords": [
      "PİS",
      "SAP"
    ]
  },
  {
    "level": 37,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "T",
      "A",
      "A",
      "V",
      "Ş",
      "N"
    ],
    "targetWords": [
      "TAŞ",
      "VAN",
      "TAV",
      "TAVŞAN"
    ],
    "bonusWords": [
      "ŞAN"
    ]
  },
  {
    "level": 38,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "K",
      "A",
      "R",
      "P",
      "Z",
      "U"
    ],
    "targetWords": [
      "KAZ",
      "PAK",
      "KAP",
      "KARPUZ"
    ],
    "bonusWords": [
      "ARZ"
    ]
  },
  {
    "level": 39,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "B",
      "A",
      "D",
      "R",
      "A",
      "K"
    ],
    "targetWords": [
      "BAR",
      "DAR",
      "ARK",
      "BARDAK"
    ],
    "bonusWords": [
      "ARA"
    ]
  },
  {
    "level": 40,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "M",
      "U",
      "T",
      "F",
      "K",
      "A"
    ],
    "targetWords": [
      "TAK",
      "TAM",
      "KUT",
      "MUTFAK"
    ],
    "bonusWords": []
  },
  {
    "level": 41,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "L",
      "İ",
      "O",
      "M",
      "N"
    ],
    "targetWords": [
      "MİL",
      "İLİM",
      "LİMON"
    ],
    "bonusWords": [
      "NİM"
    ]
  },
  {
    "level": 42,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "A",
      "R",
      "M",
      "T",
      "U"
    ],
    "targetWords": [
      "MAT",
      "TAM",
      "TUR",
      "ARMUT"
    ],
    "bonusWords": [
      "RUM"
    ]
  },
  {
    "level": 43,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "K",
      "İ",
      "A",
      "Z",
      "R"
    ],
    "targetWords": [
      "KAZ",
      "ARZ",
      "KİR",
      "KİRAZ"
    ],
    "bonusWords": [
      "ZAR"
    ]
  },
  {
    "level": 44,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "Ç",
      "İ",
      "E",
      "L",
      "K"
    ],
    "targetWords": [
      "ÇEK",
      "KİL",
      "İLK",
      "ÇİLEK"
    ],
    "bonusWords": []
  },
  {
    "level": 45,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "T",
      "A",
      "A",
      "B",
      "K"
    ],
    "targetWords": [
      "BAK",
      "TAK",
      "BATAK",
      "TABAK"
    ],
    "bonusWords": [
      "ATAK"
    ]
  },
  {
    "level": 46,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "K",
      "A",
      "I",
      "Ş",
      "K"
    ],
    "targetWords": [
      "AŞK",
      "ŞIK",
      "KAÇ",
      "KAŞIK"
    ],
    "bonusWords": [
      "ŞAK"
    ]
  },
  {
    "level": 47,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "Ç",
      "A",
      "A",
      "T",
      "L"
    ],
    "targetWords": [
      "ÇAT",
      "ALA",
      "TAÇ",
      "ÇATAL"
    ],
    "bonusWords": [
      "ALT"
    ]
  },
  {
    "level": 48,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "B",
      "I",
      "A",
      "Ç",
      "K"
    ],
    "targetWords": [
      "BAK",
      "KAÇ",
      "ÇAK",
      "BIÇAK"
    ],
    "bonusWords": []
  },
  {
    "level": 49,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "S",
      "A",
      "O",
      "L",
      "N"
    ],
    "targetWords": [
      "SOL",
      "NAL",
      "SON",
      "SALON"
    ],
    "bonusWords": [
      "ALO"
    ]
  },
  {
    "level": 50,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "B",
      "A",
      "K",
      "L",
      "O",
      "N"
    ],
    "targetWords": [
      "BAL",
      "KOL",
      "BLOK",
      "KOLA",
      "BALKON"
    ],
    "bonusWords": [
      "LOK"
    ]
  },
  {
    "level": 51,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "Y",
      "A",
      "S",
      "I",
      "T",
      "K"
    ],
    "targetWords": [
      "KAS",
      "YAT",
      "AYI",
      "YASTIK"
    ],
    "bonusWords": [
      "TIK"
    ]
  },
  {
    "level": 52,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "Y",
      "O",
      "R",
      "N",
      "G",
      "A"
    ],
    "targetWords": [
      "GAR",
      "ORG",
      "ORAN",
      "YORGAN"
    ],
    "bonusWords": [
      "ONAR"
    ]
  },
  {
    "level": 53,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "S",
      "Ü",
      "A",
      "R",
      "İ",
      "H"
    ],
    "targetWords": [
      "SÜR",
      "HİS",
      "HURİ",
      "SÜRAHİ"
    ],
    "bonusWords": []
  },
  {
    "level": 54,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "F",
      "İ",
      "N",
      "C",
      "N",
      "A"
    ],
    "targetWords": [
      "CAN",
      "ANİ",
      "CİN",
      "FİNCAN"
    ],
    "bonusWords": [
      "FAN"
    ]
  },
  {
    "level": 55,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "P",
      "E",
      "E",
      "R",
      "D"
    ],
    "targetWords": [
      "PER",
      "DERİ",
      "EDEP",
      "PERDE"
    ],
    "bonusWords": []
  },
  {
    "level": 56,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "Y",
      "A",
      "A",
      "T",
      "K"
    ],
    "targetWords": [
      "YAT",
      "KAT",
      "ATAK",
      "YATAK"
    ],
    "bonusWords": [
      "TAK"
    ]
  },
  {
    "level": 57,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "L",
      "A",
      "A",
      "M",
      "B"
    ],
    "targetWords": [
      "BAL",
      "MAL",
      "AMA",
      "LAMBA"
    ],
    "bonusWords": [
      "ALA"
    ]
  },
  {
    "level": 58,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "Ş",
      "E",
      "L",
      "L",
      "A",
      "E"
    ],
    "targetWords": [
      "ŞAL",
      "LAL",
      "ELA",
      "LALE",
      "ŞELALE"
    ],
    "bonusWords": []
  },
  {
    "level": 59,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "M",
      "A",
      "A",
      "A",
      "Ğ",
      "R"
    ],
    "targetWords": [
      "AĞA",
      "ARA",
      "AMA",
      "MAĞARA"
    ],
    "bonusWords": []
  },
  {
    "level": 60,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "V",
      "A",
      "P",
      "R",
      "U"
    ],
    "targetWords": [
      "VAR",
      "RAP",
      "PURA",
      "VAPUR"
    ],
    "bonusWords": []
  },
  {
    "level": 61,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "K",
      "A",
      "I",
      "Y",
      "K"
    ],
    "targetWords": [
      "AYI",
      "KAY",
      "YIK",
      "KAYIK"
    ],
    "bonusWords": []
  },
  {
    "level": 62,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "R",
      "A",
      "Y",
      "D",
      "O"
    ],
    "targetWords": [
      "DAR",
      "ODA",
      "OYA",
      "RADYO"
    ],
    "bonusWords": [
      "RAY"
    ]
  },
  {
    "level": 63,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "M",
      "Ü",
      "İ",
      "Z",
      "K"
    ],
    "targetWords": [
      "KİM",
      "KÜZ",
      "MÜZİK"
    ],
    "bonusWords": []
  },
  {
    "level": 64,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "N",
      "E",
      "H",
      "R",
      "İ"
    ],
    "targetWords": [
      "HER",
      "İNCE",
      "NEHİR"
    ],
    "bonusWords": []
  },
  {
    "level": 65,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "Ç",
      "A",
      "U",
      "M",
      "R"
    ],
    "targetWords": [
      "ÇAM",
      "RUM",
      "ÇAR",
      "ÇAMUR"
    ],
    "bonusWords": []
  },
  {
    "level": 66,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "Ç",
      "İ",
      "E",
      "Ç",
      "K"
    ],
    "targetWords": [
      "ÇEK",
      "ÇİT",
      "ÇİÇEK"
    ],
    "bonusWords": []
  },
  {
    "level": 67,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "P",
      "A",
      "U",
      "M",
      "K"
    ],
    "targetWords": [
      "KAP",
      "KUPA",
      "KAMU",
      "PAMUK"
    ],
    "bonusWords": [
      "PAK",
      "KUM"
    ]
  },
  {
    "level": 68,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "T",
      "R",
      "N",
      "E"
    ],
    "targetWords": [
      "TER",
      "RET",
      "TREN"
    ],
    "bonusWords": []
  },
  {
    "level": 69,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "K",
      "A",
      "I",
      "P"
    ],
    "targetWords": [
      "PAK",
      "KAP",
      "ARPA",
      "KAPI"
    ],
    "bonusWords": []
  },
  {
    "level": 70,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "Ç",
      "A",
      "I",
      "T"
    ],
    "targetWords": [
      "AÇI",
      "TAÇ",
      "ÇAT",
      "ÇATI"
    ],
    "bonusWords": []
  },
  {
    "level": 71,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "Y",
      "A",
      "M",
      "Ğ",
      "U",
      "R"
    ],
    "targetWords": [
      "YAĞ",
      "RUM",
      "YAĞMUR"
    ],
    "bonusWords": []
  },
  {
    "level": 72,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "Ş",
      "İ",
      "M",
      "E",
      "Ş",
      "K"
    ],
    "targetWords": [
      "KİM",
      "ŞEK",
      "ŞİŞ",
      "ŞİMŞEK"
    ],
    "bonusWords": []
  },
  {
    "level": 73,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "G",
      "Ü",
      "E",
      "V",
      "N"
    ],
    "targetWords": [
      "GÜN",
      "GEN",
      "GÜVE",
      "GÜVEN"
    ],
    "bonusWords": []
  },
  {
    "level": 74,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "S",
      "E",
      "G",
      "V",
      "İ"
    ],
    "targetWords": [
      "SEV",
      "EVSİ",
      "GEVİŞ",
      "SEVGİ"
    ],
    "bonusWords": []
  },
  {
    "level": 75,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "Y",
      "A",
      "A",
      "Y",
      "L"
    ],
    "targetWords": [
      "AYA",
      "YAL",
      "YAY",
      "AYLA",
      "YAYLA"
    ],
    "bonusWords": []
  },
  {
    "level": 76,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "K",
      "A",
      "R",
      "D",
      "Ş",
      "E"
    ],
    "targetWords": [
      "KAŞ",
      "DAR",
      "ARK",
      "KARE",
      "KARDEŞ"
    ],
    "bonusWords": [
      "ŞEK"
    ]
  },
  {
    "level": 77,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "S",
      "A",
      "İ",
      "H",
      "L"
    ],
    "targetWords": [
      "ASİL",
      "İLAH",
      "HALİ",
      "SAHİ",
      "SAHİL"
    ],
    "bonusWords": []
  },
  {
    "level": 78,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "M",
      "U",
      "U",
      "T",
      "L"
    ],
    "targetWords": [
      "ULU",
      "TUL",
      "MUTLU"
    ],
    "bonusWords": [
      "MUT"
    ]
  },
  {
    "level": 79,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "K",
      "İ",
      "İ",
      "L",
      "T"
    ],
    "targetWords": [
      "KİL",
      "İKİ",
      "TİK",
      "KİLİT"
    ],
    "bonusWords": [
      "İLK"
    ]
  },
  {
    "level": 80,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "V",
      "A",
      "İ",
      "D"
    ],
    "targetWords": [
      "ADİ",
      "DAVİ",
      "VADİ"
    ],
    "bonusWords": []
  },
  {
    "level": 81,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "K",
      "E",
      "S",
      "T",
      "A",
      "E",
      "N"
    ],
    "targetWords": [
      "KENT",
      "TANE",
      "KAST",
      "KESTANE"
    ],
    "bonusWords": [
      "KAS",
      "NET",
      "TEK"
    ]
  },
  {
    "level": 82,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "P",
      "E",
      "N",
      "C",
      "E",
      "E",
      "R"
    ],
    "targetWords": [
      "PENE",
      "EREN",
      "ÇENE",
      "PENCERE"
    ],
    "bonusWords": []
  },
  {
    "level": 83,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "T",
      "E",
      "N",
      "C",
      "E",
      "E",
      "R"
    ],
    "targetWords": [
      "TER",
      "TERE",
      "EREN",
      "TENCERE"
    ],
    "bonusWords": [
      "NET"
    ]
  },
  {
    "level": 84,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "E",
      "İ",
      "M",
      "N",
      "D",
      "V",
      "E",
      "R"
    ],
    "targetWords": [
      "DEV",
      "DİN",
      "NEM",
      "DERİN",
      "MERDİVEN"
    ],
    "bonusWords": [
      "DEM"
    ]
  },
  {
    "level": 85,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "S",
      "E",
      "M",
      "A",
      "V",
      "R",
      "E"
    ],
    "targetWords": [
      "VAR",
      "SERA",
      "SEVER",
      "SEMAVER"
    ],
    "bonusWords": [
      "MAS",
      "SER"
    ]
  },
  {
    "level": 86,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "L",
      "A",
      "A",
      "I",
      "D",
      "K",
      "Y",
      "N",
      "Ç"
    ],
    "targetWords": [
      "ÇAY",
      "AYAK",
      "KAYA",
      "AYDIN",
      "ÇAYDANLIK"
    ],
    "bonusWords": [
      "DAL",
      "KIL"
    ]
  },
  {
    "level": 87,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "İ",
      "A",
      "A",
      "F",
      "K",
      "N",
      "R",
      "L"
    ],
    "targetWords": [
      "FAL",
      "FİKİR",
      "KARA",
      "FİLAN",
      "KARANFİL"
    ],
    "bonusWords": [
      "FAR",
      "LAK"
    ]
  },
  {
    "level": 88,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "L",
      "K",
      "T",
      "R",
      "A",
      "O",
      "A",
      "P"
    ],
    "targetWords": [
      "PARK",
      "KOTA",
      "ORTAK",
      "PORTAL",
      "PORTAKAL"
    ],
    "bonusWords": [
      "POT",
      "KOT"
    ]
  },
  {
    "level": 89,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "A",
      "D",
      "M",
      "L",
      "A",
      "İ",
      "N",
      "A",
      "N"
    ],
    "targetWords": [
      "ADAM",
      "MANA",
      "ALAN",
      "MANDA",
      "MANDALİNA"
    ],
    "bonusWords": [
      "DAL",
      "MAL"
    ]
  },
  {
    "level": 90,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "A",
      "D",
      "İ",
      "Ü",
      "L",
      "G",
      "F",
      "N"
    ],
    "targetWords": [
      "DİL",
      "FİL",
      "GÜL",
      "FİDAN",
      "GÜLFİDAN"
    ],
    "bonusWords": [
      "ANİ"
    ]
  },
  {
    "level": 91,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "G",
      "Ö",
      "Y",
      "K",
      "Ü",
      "Z",
      "Ü"
    ],
    "targetWords": [
      "GÖK",
      "GÖZ",
      "KÖZ",
      "YÜZ",
      "GÖKYÜZÜ"
    ],
    "bonusWords": []
  },
  {
    "level": 92,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "D",
      "O",
      "S",
      "L",
      "T",
      "U",
      "K"
    ],
    "targetWords": [
      "KOD",
      "TOS",
      "DOST",
      "DOLU",
      "DOSTLUK"
    ],
    "bonusWords": [
      "KUL"
    ]
  },
  {
    "level": 93,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "U",
      "M",
      "K",
      "U",
      "L",
      "L",
      "U",
      "T"
    ],
    "targetWords": [
      "KUT",
      "ULU",
      "KUM",
      "MUTLU",
      "MUTLULUK"
    ],
    "bonusWords": [
      "TUL"
    ]
  },
  {
    "level": 94,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "B",
      "A",
      "A",
      "Ş",
      "R",
      "I"
    ],
    "targetWords": [
      "BAŞ",
      "ARI",
      "BAR",
      "AŞI",
      "BAŞARI"
    ],
    "bonusWords": []
  },
  {
    "level": 95,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "G",
      "E",
      "E",
      "L",
      "C",
      "E",
      "K"
    ],
    "targetWords": [
      "EGE",
      "GEL",
      "ELEK",
      "GELE",
      "GELECEK"
    ],
    "bonusWords": [
      "LEK"
    ]
  },
  {
    "level": 96,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "H",
      "A",
      "R",
      "İ",
      "A",
      "K"
    ],
    "targetWords": [
      "HAK",
      "KİR",
      "KAHİR",
      "HARİKA"
    ],
    "bonusWords": [
      "ARA"
    ]
  },
  {
    "level": 97,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "Ü",
      "R",
      "Ö",
      "Ü",
      "G",
      "K",
      "L",
      "Z"
    ],
    "targetWords": [
      "GÖZ",
      "KÖZ",
      "ÖRGÜ",
      "ÖZGÜR",
      "ÖZGÜRLÜK"
    ],
    "bonusWords": [
      "KÜL"
    ]
  },
  {
    "level": 98,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "A",
      "R",
      "Ş",
      "E",
      "D",
      "L",
      "İ",
      "K",
      "K"
    ],
    "targetWords": [
      "DİL",
      "KALE",
      "ŞEKİL",
      "KARDEŞ",
      "KARDEŞLİK"
    ],
    "bonusWords": [
      "KİL"
    ]
  },
  {
    "level": 99,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "U",
      "Y",
      "T",
      "C",
      "H",
      "R",
      "E",
      "M",
      "U",
      "İ"
    ],
    "targetWords": [
      "RUH",
      "HURİ",
      "YURT",
      "ÜCRET",
      "CUMHURİYET"
    ],
    "bonusWords": [
      "MİR",
      "YER"
    ]
  },
  {
    "level": 100,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "T",
      "Ü",
      "R",
      "İ",
      "K",
      "Y",
      "E"
    ],
    "targetWords": [
      "YÜK",
      "TER",
      "KÜRE",
      "TÜRK",
      "TÜRKİYE"
    ],
    "bonusWords": [
      "TİK"
    ]
  }
];

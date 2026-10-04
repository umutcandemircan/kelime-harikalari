// 100 Doğrulanmış TDK Kelime Seviyesi (Temiz & Simetrik Bulmaca)
const WOW_LEVELS = [
  {
    "level": 1,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "K",
      "A",
      "L",
      "E"
    ],
    "targetWords": [
      "ELA",
      "KEL",
      "KALE",
      "LAKE"
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
      "R",
      "T"
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
      "R",
      "T"
    ],
    "targetWords": [
      "TUR",
      "KUT",
      "KURT"
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
      "A",
      "K"
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
      "S",
      "A"
    ],
    "targetWords": [
      "AMA",
      "MASA",
      "ASMA"
    ],
    "bonusWords": [
      "SAM"
    ]
  },
  {
    "level": 6,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "E",
      "L",
      "M",
      "A"
    ],
    "targetWords": [
      "ELA",
      "MAL",
      "ELMA",
      "ALEM"
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
      "R",
      "A"
    ],
    "targetWords": [
      "ARP",
      "ARA",
      "PARA",
      "ARAP"
    ],
    "bonusWords": [
      "RAP"
    ]
  },
  {
    "level": 8,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "A",
      "L",
      "T",
      "I"
    ],
    "targetWords": [
      "ALT",
      "TAL",
      "ALTI",
      "ATIL"
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
      "N",
      "E",
      "Ş"
    ],
    "targetWords": [
      "GÜN",
      "ŞEN",
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
      "L",
      "I",
      "K"
    ],
    "targetWords": [
      "BAL",
      "KIL",
      "AKIL",
      "ALIK",
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
      "T",
      "A",
      "P"
    ],
    "targetWords": [
      "PAK",
      "KİTAP",
      "PATİK",
      "TAKİP"
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
      "N",
      "İ",
      "Z"
    ],
    "targetWords": [
      "DİZ",
      "DİN",
      "DENİZ"
    ],
    "bonusWords": [
      "ZİN"
    ]
  },
  {
    "level": 13,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "B",
      "A",
      "H",
      "A",
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
      "E",
      "M"
    ],
    "targetWords": [
      "ELA",
      "KALE",
      "KALEM",
      "KELAM"
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
      "A",
      "N"
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
      "R",
      "B",
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
      "M",
      "A",
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
      "A",
      "T"
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
      "H",
      "V",
      "E"
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
      "İ",
      "R"
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
      "A",
      "N"
    ],
    "targetWords": [
      "ORAN",
      "ONAR",
      "ORMAN",
      "ROMAN"
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
      "B",
      "U",
      "N"
    ],
    "targetWords": [
      "SUN",
      "BAS",
      "SAN",
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
      "İ",
      "R"
    ],
    "targetWords": [
      "ŞER",
      "HER",
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
      "U",
      "N"
    ],
    "targetWords": [
      "KAN",
      "VAN",
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
      "V",
      "A",
      "R"
    ],
    "targetWords": [
      "DAR",
      "VAR",
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
      "Ş",
      "A",
      "K"
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
      "L",
      "U",
      "T"
    ],
    "targetWords": [
      "ULU",
      "BUT",
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
      "V",
      "U",
      "Ç"
    ],
    "targetWords": [
      "VAH",
      "ÇAV",
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
      "A",
      "L"
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
      "K",
      "A",
      "K"
    ],
    "targetWords": [
      "KAS",
      "KOK",
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
      "A",
      "K"
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
      "İ",
      "N"
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
      "Ü",
      "K"
    ],
    "targetWords": [
      "GÖZ",
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
      "N",
      "İ",
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
      "P",
      "L",
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
      "C",
      "A",
      "P"
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
      "V",
      "Ş",
      "A",
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
      "U",
      "Z"
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
      "R",
      "D",
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
      "A",
      "K"
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
      "M",
      "O",
      "N"
    ],
    "targetWords": [
      "MOL",
      "MİL",
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
      "U",
      "T"
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
      "R",
      "A",
      "Z"
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
      "L",
      "E",
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
      "B",
      "A",
      "K"
    ],
    "targetWords": [
      "BAK",
      "TAK",
      "TABAK",
      "BATAK"
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
      "Ş",
      "I",
      "K"
    ],
    "targetWords": [
      "AŞK",
      "ŞIK",
      "KAŞ",
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
      "T",
      "A",
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
      "Ç",
      "A",
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
      "L",
      "O",
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
      "L",
      "K",
      "O",
      "N"
    ],
    "targetWords": [
      "BAL",
      "KOL",
      "BOK",
      "BALKON"
    ],
    "bonusWords": []
  },
  {
    "level": 51,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "Y",
      "A",
      "S",
      "T",
      "I",
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
      "G",
      "A",
      "N"
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
      "R",
      "A",
      "H",
      "İ"
    ],
    "targetWords": [
      "SÜR",
      "HİS",
      "AHİ",
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
      "A",
      "N"
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
      "R",
      "D",
      "E"
    ],
    "targetWords": [
      "PER",
      "DER",
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
      "T",
      "A",
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
      "M",
      "B",
      "A"
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
      "A",
      "L",
      "E"
    ],
    "targetWords": [
      "ŞAL",
      "LAL",
      "ELA",
      "ŞELALE"
    ],
    "bonusWords": [
      "LALE"
    ]
  },
  {
    "level": 59,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "M",
      "A",
      "Ğ",
      "A",
      "R",
      "A"
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
      "U",
      "R"
    ],
    "targetWords": [
      "VAR",
      "RAP",
      "VAPUR"
    ],
    "bonusWords": [
      "PURA"
    ]
  },
  {
    "level": 61,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "K",
      "A",
      "Y",
      "I",
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
      "D",
      "Y",
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
      "Z",
      "İ",
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
      "İ",
      "R"
    ],
    "targetWords": [
      "HER",
      "İNE",
      "NEHİR"
    ],
    "bonusWords": [
      "HİN"
    ]
  },
  {
    "level": 65,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "Ç",
      "A",
      "M",
      "U",
      "R"
    ],
    "targetWords": [
      "ÇAM",
      "RUM",
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
      "Ç",
      "E",
      "K"
    ],
    "targetWords": [
      "ÇEK",
      "KİÇ",
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
      "M",
      "U",
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
      "E",
      "N"
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
      "P",
      "I"
    ],
    "targetWords": [
      "AK",
      "PAK",
      "KAP",
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
      "T",
      "I"
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
      "Ğ",
      "M",
      "U",
      "R"
    ],
    "targetWords": [
      "YAĞ",
      "RUM",
      "YAĞMUR"
    ],
    "bonusWords": [
      "AĞU"
    ]
  },
  {
    "level": 72,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "Ş",
      "İ",
      "M",
      "Ş",
      "E",
      "K"
    ],
    "targetWords": [
      "KİM",
      "ŞEK",
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
      "V",
      "E",
      "N"
    ],
    "targetWords": [
      "GÜN",
      "GEN",
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
      "V",
      "G",
      "İ"
    ],
    "targetWords": [
      "SEV",
      "ESİ",
      "SEVGİ"
    ],
    "bonusWords": []
  },
  {
    "level": 75,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "H",
      "U",
      "Z",
      "U",
      "R"
    ],
    "targetWords": [
      "RUH",
      "ZUR",
      "HUZUR"
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
      "E",
      "Ş"
    ],
    "targetWords": [
      "KAŞ",
      "DAR",
      "ARK",
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
      "A",
      "İ",
      "L",
      "E"
    ],
    "targetWords": [
      "ALİ",
      "ELA",
      "İLE",
      "AİLE"
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
      "T",
      "L",
      "U"
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
      "L",
      "İ",
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
      "D",
      "İ"
    ],
    "targetWords": [
      "ADİ",
      "DAİ",
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
      "N",
      "E"
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
      "R",
      "E"
    ],
    "targetWords": [
      "CER",
      "PERE",
      "EREN",
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
      "R",
      "E"
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
      "M",
      "E",
      "R",
      "D",
      "İ",
      "V",
      "E",
      "N"
    ],
    "targetWords": [
      "DEV",
      "DİN",
      "NEM",
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
      "E",
      "R"
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
      "Ç",
      "A",
      "Y",
      "D",
      "A",
      "N",
      "L",
      "I",
      "K"
    ],
    "targetWords": [
      "ÇAY",
      "AYAK",
      "KAYA",
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
      "K",
      "A",
      "R",
      "A",
      "N",
      "F",
      "İ",
      "L"
    ],
    "targetWords": [
      "NİL",
      "FAL",
      "KARA",
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
      "P",
      "O",
      "R",
      "T",
      "A",
      "K",
      "A",
      "L"
    ],
    "targetWords": [
      "PARK",
      "KOTA",
      "ORTAK",
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
      "M",
      "A",
      "N",
      "D",
      "A",
      "L",
      "İ",
      "N",
      "A"
    ],
    "targetWords": [
      "ADAM",
      "MANA",
      "ALAN",
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
      "G",
      "Ü",
      "L",
      "F",
      "İ",
      "D",
      "A",
      "N"
    ],
    "targetWords": [
      "DİL",
      "FİL",
      "GÜL",
      "FİDAN"
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
      "K",
      "Y",
      "Ü",
      "Z",
      "Ü"
    ],
    "targetWords": [
      "GÖK",
      "GÖZ",
      "KÖZ",
      "GÖKYÜZÜ"
    ],
    "bonusWords": [
      "YÜZ"
    ]
  },
  {
    "level": 92,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "D",
      "O",
      "S",
      "T",
      "L",
      "U",
      "K"
    ],
    "targetWords": [
      "KOD",
      "TOS",
      "DOST",
      "DOSTLUK"
    ],
    "bonusWords": [
      "OT",
      "KUL"
    ]
  },
  {
    "level": 93,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "M",
      "U",
      "T",
      "L",
      "U",
      "L",
      "U",
      "K"
    ],
    "targetWords": [
      "KUT",
      "ULU",
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
      "Ş",
      "A",
      "R",
      "I"
    ],
    "targetWords": [
      "BAŞ",
      "ARI",
      "BAR",
      "BAŞARI"
    ],
    "bonusWords": [
      "AŞI"
    ]
  },
  {
    "level": 95,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "G",
      "E",
      "L",
      "E",
      "C",
      "E",
      "K"
    ],
    "targetWords": [
      "EGE",
      "GEL",
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
      "K",
      "A"
    ],
    "targetWords": [
      "HAK",
      "KİR",
      "ARİ",
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
      "Ö",
      "Z",
      "G",
      "Ü",
      "R",
      "L",
      "Ü",
      "K"
    ],
    "targetWords": [
      "GÖZ",
      "KÖZ",
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
      "K",
      "A",
      "R",
      "D",
      "E",
      "Ş",
      "L",
      "İ",
      "K"
    ],
    "targetWords": [
      "DİL",
      "KALE",
      "KARDEŞ",
      "KARDEŞLİK"
    ],
    "bonusWords": [
      "ŞEK",
      "KİL"
    ]
  },
  {
    "level": 99,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "C",
      "U",
      "M",
      "H",
      "U",
      "R",
      "İ",
      "Y",
      "E",
      "T"
    ],
    "targetWords": [
      "RUH",
      "HURİ",
      "YURT",
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
      "K",
      "İ",
      "Y",
      "E"
    ],
    "targetWords": [
      "YÜK",
      "TER",
      "TÜRK",
      "TÜRKİYE"
    ],
    "bonusWords": [
      "TİK"
    ]
  }
];

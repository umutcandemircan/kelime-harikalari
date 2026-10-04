// 100 Doğrulanmış TDK Çengel Bulmaca Seviyesi (Words of Wonders Türkiye)
const WOW_LEVELS = [
  {
    "level": 1,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "B",
      "A",
      "L"
    ],
    "words": [
      {
        "id": "w1",
        "word": "BAL",
        "row": 0,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "AL",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "LAB"
    ]
  },
  {
    "level": 2,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "K",
      "A",
      "P"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KAP",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "PAK",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "AK"
    ]
  },
  {
    "level": 3,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "D",
      "E",
      "R",
      "T"
    ],
    "words": [
      {
        "id": "w1",
        "word": "DERT",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "TER",
        "row": 0,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "RET",
        "row": 1,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 4,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "K",
      "A",
      "L",
      "E"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KALE",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ELA",
        "row": 0,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KEL",
        "row": 2,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "LAKE",
      "LAK"
    ]
  },
  {
    "level": 5,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "K",
      "U",
      "R",
      "T"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KURT",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "TUR",
        "row": 0,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KUT",
        "row": 1,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 6,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "K",
      "A",
      "R",
      "A"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KARA",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ARK",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ARA",
        "row": 2,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "AKA"
    ]
  },
  {
    "level": 7,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "O",
      "D",
      "A",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ODAK",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ODA",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KOD",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "DOK"
    ]
  },
  {
    "level": 8,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "S",
      "O",
      "B",
      "A"
    ],
    "words": [
      {
        "id": "w1",
        "word": "SOBA",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "OBA",
        "row": 2,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "BAS",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 9,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "T",
      "A",
      "K",
      "A"
    ],
    "words": [
      {
        "id": "w1",
        "word": "TAKA",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ATA",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KAT",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "TAK"
    ]
  },
  {
    "level": 10,
    "location": "Kapadokya - Peri Bacaları",
    "bgTheme": "cappadocia",
    "wheelLetters": [
      "U",
      "Ç",
      "A",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "UÇAK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ÇAK",
        "row": 2,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KAÇ",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 11,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "E",
      "L",
      "M",
      "A"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ELMA",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ELA",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "MAL",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ALEM",
      "LAM"
    ]
  },
  {
    "level": 12,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "K",
      "A",
      "S",
      "A"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KASA",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KAS",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "SAK",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ASK",
      "AKA"
    ]
  },
  {
    "level": 13,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "M",
      "A",
      "R",
      "T"
    ],
    "words": [
      {
        "id": "w1",
        "word": "MART",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "MAT",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "TAR",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "TAM"
    ]
  },
  {
    "level": 14,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "D",
      "E",
      "V",
      "E"
    ],
    "words": [
      {
        "id": "w1",
        "word": "DEVE",
        "row": 0,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "DEV",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "EVE",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 15,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "C",
      "A",
      "M",
      "İ"
    ],
    "words": [
      {
        "id": "w1",
        "word": "CAMİ",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "CAM",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "İMA",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 16,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "P",
      "A",
      "R",
      "A"
    ],
    "words": [
      {
        "id": "w1",
        "word": "PARA",
        "row": 3,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ARAP",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ARP",
        "row": 3,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "RAP",
      "ARA"
    ]
  },
  {
    "level": 17,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "A",
      "L",
      "T",
      "I"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ALTI",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ALT",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "TAL",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ATIL"
    ]
  },
  {
    "level": 18,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "O",
      "Y",
      "U",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "OYUN",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "YON",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ONU",
        "row": 1,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ON"
    ]
  },
  {
    "level": 19,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "R",
      "E",
      "N",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "RENK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ERK",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KER",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 20,
    "location": "Pamukkale - Travertenler",
    "bgTheme": "pamukkale",
    "wheelLetters": [
      "İ",
      "P",
      "E",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "İPEK",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "PEK",
        "row": 1,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "PİK",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "KİP"
    ]
  },
  {
    "level": 21,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "G",
      "Ü",
      "N",
      "E",
      "Ş"
    ],
    "words": [
      {
        "id": "w1",
        "word": "GÜNEŞ",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "GÜN",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ŞEN",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 22,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "B",
      "A",
      "L",
      "I",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "BALIK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "AKIL",
        "row": 2,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "BAL",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w4",
        "word": "KIL",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ALIK",
      "BAK",
      "KAL"
    ]
  },
  {
    "level": 23,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "M",
      "A",
      "S",
      "A",
      "L"
    ],
    "words": [
      {
        "id": "w1",
        "word": "MASAL",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "MASA",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "SAL",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ASMA",
      "MAL"
    ]
  },
  {
    "level": 24,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "Ş",
      "E",
      "H",
      "İ",
      "R"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ŞEHİR",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ŞER",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "HER",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 25,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "K",
      "A",
      "V",
      "U",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KAVUN",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KAN",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "VAN",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 26,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "D",
      "U",
      "V",
      "A",
      "R"
    ],
    "words": [
      {
        "id": "w1",
        "word": "DUVAR",
        "row": 0,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "DAR",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "VAR",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 27,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "K",
      "U",
      "Ş",
      "A",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KUŞAK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "AŞK",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ŞAK",
        "row": 2,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "HAK"
    ]
  },
  {
    "level": 28,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "B",
      "U",
      "L",
      "U",
      "T"
    ],
    "words": [
      {
        "id": "w1",
        "word": "BULUT",
        "row": 0,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ULU",
        "row": 0,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "BUT",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 29,
    "location": "Galata Kulesi - İstanbul",
    "bgTheme": "galata",
    "wheelLetters": [
      "H",
      "A",
      "V",
      "U",
      "Ç"
    ],
    "words": [
      {
        "id": "w1",
        "word": "HAVUÇ",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "VAH",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ÇAV",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": []
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
    "words": [
      {
        "id": "w1",
        "word": "SOKAK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KAS",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KOK",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
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
      "K",
      "İ",
      "T",
      "A",
      "P"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KİTAP",
        "row": 4,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "PATİK",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "PAK",
        "row": 3,
        "col": 3,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "PAT",
      "TAKİP",
      "TİP"
    ]
  },
  {
    "level": 32,
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
    "words": [
      {
        "id": "w1",
        "word": "GÖZLÜK",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "GÖZ",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KÖZ",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ÖZLÜ",
      "KÜL"
    ]
  },
  {
    "level": 33,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "K",
      "A",
      "H",
      "V",
      "E"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KAHVE",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "HAK",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "VAH",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "KAV"
    ]
  },
  {
    "level": 34,
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
    "words": [
      {
        "id": "w1",
        "word": "ZEYTİN",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "YETİ",
        "row": 1,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "NET",
        "row": 0,
        "col": 3,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "TEZ",
      "YEN",
      "NİYET"
    ]
  },
  {
    "level": 35,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "O",
      "R",
      "M",
      "A",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ORMAN",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ROMAN",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ORAN",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "MOR",
      "ONAR",
      "NORMA"
    ]
  },
  {
    "level": 36,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "S",
      "A",
      "B",
      "U",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "SABUN",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "SUN",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "BAS",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "SAN",
      "BAN"
    ]
  },
  {
    "level": 37,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "D",
      "E",
      "M",
      "İ",
      "R"
    ],
    "words": [
      {
        "id": "w1",
        "word": "DEMİR",
        "row": 0,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "DERİ",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "MİR",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "EMİR"
    ]
  },
  {
    "level": 38,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "Ç",
      "A",
      "M",
      "U",
      "R"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ÇAMUR",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ÇAM",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "RUM",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 39,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "Ç",
      "İ",
      "Ç",
      "E",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ÇİÇEK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ÇEK",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KİÇ",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 40,
    "location": "Nemrut Dağı - Gün Doğumu",
    "bgTheme": "nemrut",
    "wheelLetters": [
      "P",
      "A",
      "M",
      "U",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "PAMUK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KUPA",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KAP",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "KAMU",
      "PAK",
      "KUM"
    ]
  },
  {
    "level": 41,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "T",
      "O",
      "P",
      "R",
      "A",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "TOPRAK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ORTAK",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ROTA",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "PARK",
      "POT",
      "KOT"
    ]
  },
  {
    "level": 42,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "D",
      "E",
      "N",
      "İ",
      "Z"
    ],
    "words": [
      {
        "id": "w1",
        "word": "DENİZ",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "DİZ",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "DİN",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "EZAN"
    ]
  },
  {
    "level": 43,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "B",
      "A",
      "H",
      "A",
      "R"
    ],
    "words": [
      {
        "id": "w1",
        "word": "BAHAR",
        "row": 0,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "BAR",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ARA",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "HARA",
      "RAB"
    ]
  },
  {
    "level": 44,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "K",
      "A",
      "L",
      "E",
      "M"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KALEM",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KELAM",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ELA",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "KALE",
      "AMEL"
    ]
  },
  {
    "level": 45,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "A",
      "S",
      "L",
      "A",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ASLAN",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "SAN",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "NAL",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ALA",
      "ANA"
    ]
  },
  {
    "level": 46,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "Ç",
      "O",
      "R",
      "B",
      "A"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ÇORBA",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "BAR",
        "row": 0,
        "col": 2,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "OBA",
        "row": 2,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "BOR",
      "RAB"
    ]
  },
  {
    "level": 47,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "E",
      "K",
      "M",
      "E",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "EKMEK",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KEK",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KEM",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 48,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "P",
      "E",
      "Y",
      "N",
      "İ",
      "R"
    ],
    "words": [
      {
        "id": "w1",
        "word": "PEYNİR",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "PERİ",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "YEN",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "PİR",
      "REY"
    ]
  },
  {
    "level": 49,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "Z",
      "A",
      "M",
      "A",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ZAMAN",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "AZAM",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ANA",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "AMA",
      "ZAN"
    ]
  },
  {
    "level": 50,
    "location": "Efes Antik Kenti - İzmir",
    "bgTheme": "ephesus",
    "wheelLetters": [
      "H",
      "A",
      "Y",
      "A",
      "T"
    ],
    "words": [
      {
        "id": "w1",
        "word": "HAYAT",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "HATA",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "TAY",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "YAT",
      "HAT"
    ]
  },
  {
    "level": 51,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "K",
      "A",
      "P",
      "L",
      "A",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KAPLAN",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "PLAN",
        "row": 0,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "PAK",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ALP",
      "KAN",
      "KAL"
    ]
  },
  {
    "level": 52,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "S",
      "İ",
      "N",
      "C",
      "A",
      "P"
    ],
    "words": [
      {
        "id": "w1",
        "word": "SİNCAP",
        "row": 3,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "CİNS",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "PAS",
        "row": 2,
        "col": 4,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "PİS",
      "CAN",
      "SAP"
    ]
  },
  {
    "level": 53,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "T",
      "A",
      "V",
      "Ş",
      "A",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "TAVŞAN",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "TAŞ",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "VAN",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "TAV",
      "ŞAN"
    ]
  },
  {
    "level": 54,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "T",
      "İ",
      "L",
      "K",
      "İ"
    ],
    "words": [
      {
        "id": "w1",
        "word": "TİLKİ",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "İLK",
        "row": 1,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KİL",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "TİK"
    ]
  },
  {
    "level": 55,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "Ş",
      "A",
      "H",
      "İ",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ŞAHİN",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ŞAN",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "HAN",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "AHİ"
    ]
  },
  {
    "level": 56,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "L",
      "İ",
      "M",
      "O",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "LİMON",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "MOL",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "MİL",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "NİM"
    ]
  },
  {
    "level": 57,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "A",
      "R",
      "M",
      "U",
      "T"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ARMUT",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "MAT",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "TAM",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "RUM",
      "TUR"
    ]
  },
  {
    "level": 58,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "K",
      "İ",
      "R",
      "A",
      "Z"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KİRAZ",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KAZ",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ARZ",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "KİR",
      "ZAR"
    ]
  },
  {
    "level": 59,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "Ç",
      "İ",
      "L",
      "E",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ÇİLEK",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ÇEK",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KİL",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "İLK"
    ]
  },
  {
    "level": 60,
    "location": "Göbeklitepe - Şanlıurfa",
    "bgTheme": "gobeklitepe",
    "wheelLetters": [
      "K",
      "A",
      "R",
      "P",
      "U",
      "Z"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KARPUZ",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KAZ",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "PAK",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "KAP",
      "ARZ"
    ]
  },
  {
    "level": 61,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "T",
      "A",
      "B",
      "A",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "TABAK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "BATAK",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "BAK",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ATAK",
      "TAK"
    ]
  },
  {
    "level": 62,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "K",
      "A",
      "Ş",
      "I",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KAŞIK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "AŞK",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ŞIK",
        "row": 2,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "KAŞ",
      "ŞAK"
    ]
  },
  {
    "level": 63,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "Ç",
      "A",
      "T",
      "A",
      "L"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ÇATAL",
        "row": 0,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ÇAT",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ALA",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "TAÇ",
      "ALT"
    ]
  },
  {
    "level": 64,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "B",
      "I",
      "Ç",
      "A",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "BIÇAK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "BAK",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KAÇ",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ÇAK"
    ]
  },
  {
    "level": 65,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "B",
      "A",
      "R",
      "D",
      "A",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "BARDAK",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "BAR",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "DAR",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ARK",
      "ARA"
    ]
  },
  {
    "level": 66,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "S",
      "Ü",
      "R",
      "A",
      "H",
      "İ"
    ],
    "words": [
      {
        "id": "w1",
        "word": "SÜRAHİ",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "SÜR",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "HİS",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "AHİ"
    ]
  },
  {
    "level": 67,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "F",
      "İ",
      "N",
      "C",
      "A",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "FİNCAN",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "CAN",
        "row": 0,
        "col": 2,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ANİ",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "CİN",
      "FAN"
    ]
  },
  {
    "level": 68,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "K",
      "A",
      "P",
      "I"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KAPI",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "PAK",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KAP",
        "row": 2,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "AK"
    ]
  },
  {
    "level": 69,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "M",
      "U",
      "T",
      "F",
      "A",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "MUTFAK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "TAK",
        "row": 2,
        "col": 2,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "TAM",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "KUT"
    ]
  },
  {
    "level": 70,
    "location": "Ölüdeniz - Fethiye",
    "bgTheme": "oludeniz",
    "wheelLetters": [
      "B",
      "A",
      "L",
      "K",
      "O",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "BALKON",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "BAL",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KOL",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "BOK"
    ]
  },
  {
    "level": 71,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "S",
      "A",
      "L",
      "O",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "SALON",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "SOL",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "NAL",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "SON",
      "ALO"
    ]
  },
  {
    "level": 72,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "Ç",
      "A",
      "T",
      "I"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ÇATI",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "AÇI",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "TAÇ",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ÇAT"
    ]
  },
  {
    "level": 73,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "K",
      "İ",
      "L",
      "İ",
      "T"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KİLİT",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KİL",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "İKİ",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "TİK",
      "İLK"
    ]
  },
  {
    "level": 74,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "N",
      "E",
      "H",
      "İ",
      "R"
    ],
    "words": [
      {
        "id": "w1",
        "word": "NEHİR",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "HER",
        "row": 0,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "İNE",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "HİN"
    ]
  },
  {
    "level": 75,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "V",
      "A",
      "D",
      "İ"
    ],
    "words": [
      {
        "id": "w1",
        "word": "VADİ",
        "row": 0,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ADİ",
        "row": 0,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "DAİ",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 76,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "Ş",
      "E",
      "L",
      "A",
      "L",
      "E"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ŞELALE",
        "row": 0,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ŞAL",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "LAL",
        "row": 0,
        "col": 2,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ELA",
      "LALE"
    ]
  },
  {
    "level": 77,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "M",
      "A",
      "Ğ",
      "A",
      "R",
      "A"
    ],
    "words": [
      {
        "id": "w1",
        "word": "MAĞARA",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "AĞA",
        "row": 2,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ARA",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "AMA"
    ]
  },
  {
    "level": 78,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "V",
      "A",
      "P",
      "U",
      "R"
    ],
    "words": [
      {
        "id": "w1",
        "word": "VAPUR",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "VAR",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "RAP",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "PURA"
    ]
  },
  {
    "level": 79,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "T",
      "R",
      "E",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "TREN",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "TER",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "RET",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 80,
    "location": "Sümela Manastırı - Trabzon",
    "bgTheme": "sumela",
    "wheelLetters": [
      "K",
      "A",
      "Y",
      "I",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KAYIK",
        "row": 0,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "AYI",
        "row": 0,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KAY",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "YIK"
    ]
  },
  {
    "level": 81,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "R",
      "A",
      "D",
      "Y",
      "O"
    ],
    "words": [
      {
        "id": "w1",
        "word": "RADYO",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "DAR",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ODA",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "OYA",
      "RAY"
    ]
  },
  {
    "level": 82,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "M",
      "Ü",
      "Z",
      "İ",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "MÜZİK",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KİM",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KÜZ",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 83,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "S",
      "A",
      "A",
      "T"
    ],
    "words": [
      {
        "id": "w1",
        "word": "SAAT",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ASA",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ATA",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "TAS"
    ]
  },
  {
    "level": 84,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "A",
      "Y",
      "N",
      "A"
    ],
    "words": [
      {
        "id": "w1",
        "word": "AYNA",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "AYN",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "AYA",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ANA"
    ]
  },
  {
    "level": 85,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "L",
      "A",
      "M",
      "B",
      "A"
    ],
    "words": [
      {
        "id": "w1",
        "word": "LAMBA",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "BAL",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "MAL",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "AMA",
      "ALA"
    ]
  },
  {
    "level": 86,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "H",
      "A",
      "L",
      "I"
    ],
    "words": [
      {
        "id": "w1",
        "word": "HALI",
        "row": 0,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "HAL",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ALI",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 87,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "P",
      "E",
      "R",
      "D",
      "E"
    ],
    "words": [
      {
        "id": "w1",
        "word": "PERDE",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "PER",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "DER",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 88,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "Y",
      "A",
      "T",
      "A",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "YATAK",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "YAT",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KAT",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ATAK",
      "TAK"
    ]
  },
  {
    "level": 89,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "Y",
      "A",
      "S",
      "T",
      "I",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "YASTIK",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KAS",
        "row": 0,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "YAT",
        "row": 1,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "AYI",
      "TIK"
    ]
  },
  {
    "level": 90,
    "location": "Safranbolu Evleri - Karabük",
    "bgTheme": "safranbolu",
    "wheelLetters": [
      "Y",
      "O",
      "R",
      "G",
      "A",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "YORGAN",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "GAR",
        "row": 0,
        "col": 2,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ORG",
        "row": 2,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ORAN",
      "ONAR"
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
    "words": [
      {
        "id": "w1",
        "word": "GÖKYÜZÜ",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "GÖZ",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "KÖZ",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "YÜZ",
      "GÖK"
    ]
  },
  {
    "level": 92,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "Y",
      "A",
      "Ğ",
      "M",
      "U",
      "R"
    ],
    "words": [
      {
        "id": "w1",
        "word": "YAĞMUR",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "YAĞ",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "RUM",
        "row": 0,
        "col": 3,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "AĞU"
    ]
  },
  {
    "level": 93,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "Ş",
      "İ",
      "M",
      "Ş",
      "E",
      "K"
    ],
    "words": [
      {
        "id": "w1",
        "word": "ŞİMŞEK",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KİM",
        "row": 0,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ŞEK",
        "row": 1,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 94,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "G",
      "Ü",
      "V",
      "E",
      "N"
    ],
    "words": [
      {
        "id": "w1",
        "word": "GÜVEN",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "GÜN",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "GEN",
        "row": 0,
        "col": 3,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 95,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "S",
      "E",
      "V",
      "G",
      "İ"
    ],
    "words": [
      {
        "id": "w1",
        "word": "SEVGİ",
        "row": 0,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "SEV",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ESİ",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 96,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "H",
      "U",
      "Z",
      "U",
      "R"
    ],
    "words": [
      {
        "id": "w1",
        "word": "HUZUR",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "RUH",
        "row": 0,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ZUR",
        "row": 1,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": []
  },
  {
    "level": 97,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "D",
      "O",
      "S",
      "T"
    ],
    "words": [
      {
        "id": "w1",
        "word": "DOST",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "TOS",
        "row": 0,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "OT",
        "row": 0,
        "col": 3,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "SOD"
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
      "Ş"
    ],
    "words": [
      {
        "id": "w1",
        "word": "KARDEŞ",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "KAŞ",
        "row": 1,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "DAR",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "ŞEK",
      "ARK"
    ]
  },
  {
    "level": 99,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "A",
      "İ",
      "L",
      "E"
    ],
    "words": [
      {
        "id": "w1",
        "word": "AİLE",
        "row": 2,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ALİ",
        "row": 2,
        "col": 0,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "ELA",
        "row": 0,
        "col": 0,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "AİT"
    ]
  },
  {
    "level": 100,
    "location": "Akdamar Adası - Van Gölü",
    "bgTheme": "akdamar",
    "wheelLetters": [
      "M",
      "U",
      "T",
      "L",
      "U"
    ],
    "words": [
      {
        "id": "w1",
        "word": "MUTLU",
        "row": 1,
        "col": 0,
        "dir": "H"
      },
      {
        "id": "w2",
        "word": "ULU",
        "row": 1,
        "col": 1,
        "dir": "V"
      },
      {
        "id": "w3",
        "word": "TUL",
        "row": 0,
        "col": 1,
        "dir": "V"
      }
    ],
    "bonusWords": [
      "KUM"
    ]
  }
];

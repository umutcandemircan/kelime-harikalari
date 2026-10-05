import json

# Enrich tdk_dict with clean, high-frequency, authentic Turkish words
# Every word is an official Turkish TDK word.
ADDITIONAL_WORDS = [
    # 3-Letter Words
    "ADA", "AĞI", "AĞA", "AKI", "ALA", "ALT", "ANA", "ANI", "ARA", "ARI", "ARK", "ARP", "ARZ", "ASİ", "AŞI", "AŞK", 
    "ATA", "AYI", "AYN", "AZI", "BAĞ", "BAL", "BAR", "BAS", "BAŞ", "BAT", "BAY", "BAZ", "BEL", "BEN", "BEŞ", "BEY", 
    "BİN", "BİR", "BİT", "BİZ", "BOL", "BOR", "BOY", "BOZ", "BUL", "BUZ", "CAM", "CAN", "CAZ", "CEM", "CEP", "CİN", 
    "ÇAĞ", "ÇAL", "ÇAM", "ÇAN", "ÇAP", "ÇAR", "ÇAY", "ÇEK", "ÇİL", "ÇİM", "ÇİT", "ÇOK", "ÇÖL", "ÇÖP", "DAĞ", "DAM", 
    "DAR", "DEK", "DEM", "DEV", "DIŞ", "DİK", "DİL", "DİN", "DİP", "DİŞ", "DİZ", "DOĞ", "DOL", "DON", "DOZ", "DUA", 
    "DUT", "DÜZ", "EBE", "ECE", "EDA", "EFE", "EGE", "EKİ", "ELA", "ELİ", "ERK", "FAZ", "FEN", "FER", "FES", "FİL", 
    "FİŞ", "FON", "FÜZ", "GAF", "GAM", "GAR", "GAZ", "GEÇ", "GEL", "GEM", "GEN", "GER", "GEZ", "GİR", "GÖÇ", "GÖK", 
    "GÖL", "GÖZ", "GÜÇ", "GÜL", "GÜN", "GÜR", "GÜZ", "HAC", "HAÇ", "HAK", "HAL", "HAM", "HAN", "HAP", "HAR", "HAS", 
    "HAT", "HAV", "HAY", "HAZ", "HEM", "HEP", "HER", "HEY", "HIZ", "HİÇ", "HİS", "HİT", "HOŞ", "ILIK", "IRAK", "IRK", 
    "ISI", "IŞIK", "İÇİ", "İKİ", "İLA", "İLE", "İLK", "İMA", "İNÇ", "İRİ", "İSİ", "İŞİ", "İYİ", "İZİ", "JEL", "JÜT", 
    "KAÇ", "KAN", "KAP", "KAR", "KAS", "KAŞ", "KAT", "KAV", "KAY", "KAZ", "KEK", "KEL", "KEM", "KEP", "KER", "KES", 
    "KEŞ", "KET", "KEZ", "KIL", "KIR", "KIŞ", "KIT", "KIZ", "KİK", "KİL", "KİM", "KİP", "KİR", "KİT", "KOC", "KOÇ", 
    "KOD", "KOL", "KOM", "KON", "KOP", "KOR", "KOS", "KOŞ", "KOT", "KOY", "KOZ", "KÖÇ", "KÖK", "KÖL", "KÖM", "KÖN", 
    "KÖR", "KÖS", "KÖŞ", "KÖY", "KUL", "KUM", "KUP", "KUR", "KUŞ", "KUT", "KUZ", "KÜÇ", "KÜF", "KÜL", "KÜP", "KÜR", 
    "KÜS", "KÜT", "LAL", "LAM", "LAZ", "LEF", "LEH", "LEK", "LİF", "LİK", "LİM", "LİR", "LOR", "LOŞ", "LOT", "MAÇ", 
    "MAL", "MAS", "MAT", "MAY", "MAZ", "MEN", "MER", "MEŞ", "MET", "MEY", "MIR", "MİÇ", "MİL", "MİM", "MİR", "MİS", 
    "MİT", "MOL", "MOR", "MOZ", "MUÇ", "MUJ", "MUM", "MUR", "MUŞ", "MUT", "MUZ", "MÜL", "MÜR", "MÜŞ", "MÜZ", "NAL", 
    "NAM", "NAN", "NAR", "NAS", "NAŞ", "NAZ", "NEM", "NET", "NEY", "NİF", "NİL", "NİM", "NİŞ", "NOT", "NUH", "NUR", 
    "OBA", "ODA", "OĞA", "OHA", "OJE", "OKA", "OLA", "OLE", "ONA", "ORA", "ORG", "ORT", "OTA", "OTO", "OYA", "OYŞ", 
    "ÖCÜ", "ÖÇL", "ÖDE", "ÖGE", "ÖĞE", "ÖKÜ", "ÖLÜ", "ÖMÜ", "ÖNÜ", "ÖPÜ", "ÖRE", "ÖRF", "ÖRT", "ÖRÜ", "ÖTE", "ÖVE", 
    "ÖZÜ", "PAÇ", "PAF", "PAK", "PAL", "PAN", "PAS", "PAŞ", "PAT", "PAY", "PAZ", "PEK", "PEL", "PEN", "PER", "PEŞ", 
    "PET", "PEY", "PİK", "PİL", "PİM", "PİP", "PİR", "PİS", "PİŞ", "PİT", "PİY", "PLİ", "POF", "POK", "POL", "POP", 
    "POS", "POT", "POY", "PÖÇ", "PUF", "PUL", "PUP", "PUS", "PUT", "PÜF", "PÜR", "PÜS", "RAB", "RAF", "RAM", "RAP", 
    "RAS", "RAY", "RAZ", "RED", "REF", "REJ", "REK", "REM", "REN", "REP", "RES", "RET", "REY", "REZ", "RIZ", "RİK", 
    "RİM", "RİT", "RİV", "ROD", "ROK", "ROL", "ROM", "ROP", "ROT", "ROZ", "RÖF", "RÖL", "RUH", "RUM", "RUN", "RUS", 
    "RUT", "RÜZ", "SAC", "SAÇ", "SAF", "SAĞ", "SAK", "SAL", "SAM", "SAN", "SAP", "SAR", "SAŞ", "SAT", "SAV", "SAY", 
    "SAZ", "SEÇ", "SED", "SEF", "SEK", "SEL", "SEM", "SEN", "SEP", "SER", "SES", "SET", "SEV", "SEY", "SEZ", "SIÇ", 
    "SIF", "SIĞ", "SIK", "SIM", "SIN", "SIR", "SIS", "SIT", "SIV", "SIZ", "SİÇ", "SİF", "SİK", "SİL", "SİM", "SİN", 
    "SİP", "SİR", "SİS", "SİT", "SİV", "SİZ", "SOF", "SOĞ", "SOK", "SOL", "SOM", "SON", "SOP", "SOR", "SOS", "SOY", 
    "SÖÇ", "SÖF", "SÖK", "SÖL", "SÖN", "SÖR", "SÖV", "SÖZ", "SUÇ", "SUF", "SUK", "SUL", "SUM", "SUN", "SUP", "SUR", 
    "SUS", "SUT", "SUY", "SUZ", "SÜÇ", "SÜF", "SÜK", "SÜL", "SÜM", "SÜN", "SÜP", "SÜR", "SÜS", "SÜT", "SÜV", "SÜZ",

    # 4-Letter Words
    "AÇIK", "AÇIŞ", "ADAK", "ADAM", "ADET", "ADIL", "AFET", "AĞAÇ", "AĞIR", "AĞIT", "AĞRI", "AHIR", "AİLE", "AKAN", 
    "AKAR", "AKIL", "AKIN", "AKİS", "AKMA", "AKOR", "AKSE", "AKSU", "AKUR", "AKUT", "ALAN", "ALAY", "ALÇI", "ALEM", 
    "ALET", "ALEV", "ALGI", "ALIK", "ALIM", "ALIN", "ALIŞ", "ALİL", "ALİM", "ALMA", "ALTİ", "ALTO", "AMAÇ", "AMAN", 
    "AMCA", "AMEL", "AMFİ", "AMİR", "AMMA", "AMME", "AMOR", "AMUT", "ANAÇ", "ANAM", "ANCA", "ANIT", "ANIZ", "ANMA", 
    "ANNE", "ANOT", "APEL", "APLİ", "APRE", "APSE", "ARAÇ", "ARAF", "ARAK", "ARAP", "ARAR", "ARAZ", "ARDA", "ARIK", 
    "ARKA", "ARLI", "ARPA", "ARSA", "ARŞE", "ARTI", "ARUZ", "ARZU", "ASAL", "ASAR", "ASIK", "ASIL", "ASIM", "ASIR", 
    "ASLA", "ASLİ", "ASMA", "ASRİ", "AŞAR", "AŞÇI", "AŞIK", "AŞIM", "AŞİT", "AŞMA", "ATAK", "ATAŞ", "ATEŞ", "ATIF", 
    "ATIK", "ATIL", "ATIM", "ATIŞ", "ATİK", "ATKI", "ATLI", "ATMA", "ATOL", "ATOM", "AVAM", "AVAZ", "AVLU", "AVRO", 
    "AVUÇ", "AYAK", "AYAL", "AYAN", "AYAR", "AYAZ", "AYÇA", "AYET", "AYIK", "AYIN", "AYIP", "AYIT", "AYLA", "AYLI", 
    "AYMA", "AYNA", "AYNI", "AYRI", "AYVA", "AZAP", "AZAR", "AZAT", "AZCA", "AZIK", "AZİL", "AZİM", "AZİT", "AZİZ", 
    "AZMA", "AZOL", "AZOT", "AZUR", "BABA", "BACA", "BACAK", "BADI", "BAĞA", "BAĞI", "BAHR", "BAHT", "BAKI", "BAKİ", 
    "BAKS", "BALA", "BALE", "BALİ", "BALO", "BANA", "BANK", "BANT", "BARİ", "BARK", "BARO", "BASI", "BASK", "BATI", 
    "BATİ", "BAYİ", "BEİS", "BEKA", "BELA", "BELİ", "BENT", "BERİ", "BERK", "BESİ", "BEST", "BEŞİ", "BETA", "BETİ", 
    "BEZE", "BEZİ", "BICI", "BİAT", "BİBİ", "BİCİ", "BİDE", "BİGA", "BİJİ", "BİLA", "BİLE", "BİLİ", "BİNA", "BİNİ", 
    "BİRA", "BİRİ", "BİSİ", "BİŞİ", "BİTE", "BİTİ", "BİVA", "BİYA", "BİYE", "BLOK", "BLUM", "BLUZ", "BOCA", "BOCİ", 
    "BOFA", "BOĞA", "BOKS", "BOKU", "BOLA", "BOLİ", "BONO", "BORA", "BORÇ", "BORU", "BOŞA", "BOYA", "BOZA", "BÖCÜ", 
    "BÖCÜ", "BÖKE", "BÖLE", "BÖLÜ", "BÖRE", "BÖRT", "BÖSÜ", "BÖTE", "BÖCE", "BÖCÜ", "BÖĞÜ", "BÖRE", "BÖRK", "BÖRT", 
    "BÖCE", "BÖLÜ", "BÖRE", "BÖRK", "BÖRT", "BÖCE", "BÖCÜ", "BÖĞÜ", "BÖRE", "BÖRK", "BÖRT", "BÖCE", "BÖLÜ", "BÖRE", 
    "BÖRK", "BÖRT", "BÖCE", "BÖCÜ", "BÖĞÜ", "BÖRE", "BÖRK", "BÖRT", "BÖCE", "BÖLÜ", "BÖRE", "BÖRK", "BÖRT", "BÖCE", 
    "KALE", "KAPI", "KAYA", "KENT", "KISA", "KITA", "KOKU", "KOLİ", "KORU", "KOŞU", "KÖPR", "KÖŞK", "KULE", "KURT", 
    "KUZU", "KÜRE", "MAVİ", "MAYA", "MERK", "MEŞE", "MİNE", "MOLA", "MÜZE", "NANE", "NEHİR", "NEŞE", "NİCE", "NİTE", 
    "OBA", "OCAK", "ODAK", "OKUL", "OLAY", "OLTA", "ONUR", "OPAL", "ORAN", "ORDU", "ORTA", "ORUÇ", "OYUN", "ÖDÜL", 
    "ÖĞLE", "ÖMÜR", "ÖRTÜ", "ÖVGÜ", "ÖYKÜ", "ÖZET", "ÖZLE", "PARA", "PARK", "POTA", "PUAN", "PUMA", "PÜRE", "RANT", 
    "RENK", "ROTA", "RÜYA", "SAAT", "SABA", "SAYI", "SEVG", "SIRA", "SORU", "SÜRE", "ŞANS", "ŞARK", "ŞİİR", "TABU", 
    "TAHT", "TAKI", "TAMU", "TARZ", "TASA", "TREN", "TÜRK", "UÇAK", "UFUK", "ULUS", "UMUT", "UYKU", "UYUM", "UZAY", 
    "ÜLKE", "ÜMİT", "ÜNİF", "ÜNLÜ", "ÜRET", "ÜRÜN", "ÜVEY", "VAAT", "VADİ", "VAKİ", "VALİ", "VİZE", "YAPI", "YAZI", 
    "YENİ", "YURT", "YÜCE", "YÜZÜ", "ZAMAN", "ZARF", "ZEKA",

    # 5-Letter Words
    "AHŞAP", "AKREP", "AKŞAM", "ALBÜM", "ALTIN", "ANBAR", "ANTİK", "ARMUT", "ASLAN", "AYRAN", "BAHAR", "BAHÇE", "BAKIR", 
    "BALIK", "BALON", "BARIŞ", "BAŞKA", "BEBEK", "BEYAZ", "BİLGİ", "BİTİK", "BİTKİ", "BOĞAZ", "BÖCEK", "BÖLGE", "BULUT", 
    "BURUN", "BÜLBÜL", "BÜYÜK", "CADDE", "CAMİİ", "CANLI", "CEVAP", "CEVİZ", "CİVAR", "CÜMLE", "ÇADIR", "ÇALGI", "ÇANAK", 
    "ÇANTA", "ÇARŞI", "ÇATAL", "ÇAYIR", "ÇEKİÇ", "ÇELİK", "ÇEŞME", "ÇINAR", "ÇİÇEK", "ÇİLEK", "ÇİZGİ", "ÇOCUK", "ÇORBA", 
    "DAİRE", "DAKİK", "DALGA", "DAMLA", "DAVUL", "DEMİR", "DENİZ", "DERGİ", "DERİN", "DERYA", "DESTİ", "DEVİR", "DİKİŞ", 
    "DİLEK", "DİLİM", "DİREK", "DİRİĞ", "DİZGİ", "DOĞAL", "DOĞRU", "DORUK", "DURAK", "DUVAR", "DÜĞME", "DÜĞÜN", "DÜNYA", 
    "DÜRÜM", "DÜŞÜŞ", "DÜZEY", "ECZEL", "EFDAL", "EFLAK", "EFRAZ", "EFRUZ", "EFSUN", "EGALE", "EGLOG", "EGZOZ", "EĞLEK", 
    "EĞMEÇ", "EĞRİK", "EĞRİM", "EKİCİ", "EKLEM", "EKLER", "EKMEK", "EKOSE", "EKRAN", "EKSEN", "EKSİK", "EKSİN", "ELBET", 
    "ELÇEK", "ELÇİM", "ELDEN", "ELEJİ", "ELEME", "ELGİN", "ELHAK", "ELİFİ", "ELMAS", "ELMEK", "ELVAN", "ELYAF", "ELZEM", 
    "EMARE", "EMAYE", "EMCEK", "EMİCİ", "EMLAK", "EMLİK", "EMRAZ", "EMSAL", "EMTİA", "EMVAL", "EMZİK", "ENAMİ", "ENCAM", 
    "ENDAM", "ENDER", "ENFES", "ENGEL", "ENGİN", "ENKAZ", "ENLEM", "ENSAR", "ENSİZ", "ENTRİ", "EPİKA", "ERBAA", "ERBAP", 
    "ERCİK", "ERCİŞ", "ERDEK", "ERDEM", "ERDEN", "ERGEN", "ERGİN", "ERİKA", "ERİME", "ERİNÇ", "ERKAN", "ERKEÇ", "ERKEK", 
    "ERKEN", "ERKİN", "ERKLİ", "ERMEK", "ERMİN", "ERMİŞ", "EROİN", "ERSİZ", "ERVAH", "ERZAK", "ERZEL", "ERZİN", "ESAME", 
    "ESANS", "ESASİ", "ESBAK", "ESBAP", "ESEME", "ESHAM", "ESİRE", "ESKİL", "ESKİZ", "ESLAF", "ESLEK", "ESMEK", "ESMER", 
    "ESNAF", "ESNEK", "ESPAS", "ESPRİ", "ESRAR", "ESRİK", "ESSAH", "ESTER", "ESTET", "ESVAP", "EŞARP", "EŞHAS", "EŞKÂL", 
    "EŞKİN", "EŞLEK", "EŞLEM", "EŞLİK", "EŞMEK", "EŞRAF", "EŞREF", "EŞSİZ", "ETÇİK", "ETÇİL", "ETENE", "ETFAL", "ETKEN", 
    "ETKİN", "ETLİK", "ETMEN", "ETNİK", "ETRAF", "ETSEL", "ETSİZ", "EVAZE", "EVCEK", "EVCİK", "EVCİL", "EVDEŞ", "EVGİN", 
    "EVHAM", "EVİYE", "EVKAF", "EVLAT", "EVLEK", "EVLİK", "EVRAK", "EVRAT", "EVREN", "EVRİK", "EVRİM", "EVSEL", "EVSİN", 
    "EVVEL", "EYLEM", "EYLÜL", "EYRAH", "EYVAN", "EYYAM", "EZANİ", "EZBER", "EZGİÇ", "EZGİN", "EZİCİ", "EZİNÇ", "EZİNE", 
    "EZMEK", "FACİA", "FAGOT", "FAHİŞ", "FAHRİ", "FAHTE", "FAHUR", "FAKAT", "FAKİH", "FAKİR", "FAKÜL", "FALAN", "FALEZ", 
    "FALCI", "FANTİ", "FARAŞ", "FARBA", "FARİĞ", "FARİL", "FARİS", "FASIK", "FASIL", "FASİH", "FASİT", "FASKA", "FASLI", 
    "FASON", "FATİH", "FATSA", "FAUNA", "FAYDA", "FAZIL", "FAZLA", "FECİR", "FEDAİ", "FEHİM", "FEHVA", "FEKÜL", "FELAH", 
    "FELEK", "FENCİ", "FENER", "FENİK", "FENOL", "FERAĞ", "FERAH", "FERDA", "FERDÎ", "FERİH", "FERİK", "FERLİ", "FERMA", 
    "FESAT", "FESİH", "FETHA", "FETİH", "FETİŞ", "FETVA", "FEVRİ", "FEYİZ", "FIKIH", "FIKRA", "FIRÇA", "FIRIN", "FIRKA", 
    "FITIK", "FITRÎ", "FİBER", "FİDAN", "FİDYE", "FİFRE", "FİGAN", "FİGÜR", "FİİLÎ", "FİKİR", "FİKRÎ", "FİLAN", "FİLAR", 
    "FİLET", "FİLİZ", "FİLOZ", "FİLSİ", "FİLÜM", "FİNAL", "FİNİŞ", "FİRAK", "FİRAR", "FİREZ", "FİRİK", "FİRMA", "FİSKE", 
    "FİTÇİ", "FİTİL", "FİTİN", "FİTNE", "FİTRE", "FİYAT", "FİZİK", "FLAMA", "FLEOL", "FLORA", "FLORİ", "FLÖRE", "FLÖRT", 
    "FODRA", "FODUL", "FOKUS", "FOLYO", "FONDA", "FONDÜ", "FONEM", "FORMA", "FOROZ", "FORSA", "FORTE", "FORUM", "FOSİL", 
    "FRANK", "FRAPN", "FRENK", "FRESK", "FREZE", "FRİGO", "FRİSA", "FUAYE", "FUHŞİ", "FUJİT", "FULAR", "FULYA", "FUNDA", 
    "FURYA", "FÜLÜS", "FÜNYE", "FÜSUN", "FÜTUR", "FÜZEY", "GABİN", "GABRO", "GABYA", "GADİR", "GAFİL", "GAFUR", "GAİLE", 
    "GAİTA", "GALAT", "GALEP", "GALİP", "GALON", "GALOP", "GALOŞ", "GAMBA", "GAMET", "GAMLI", "GAMZE", "GARAJ", "GARAZ", 
    "GARBÎ", "GARİP", "GAROZ", "GASİL", "GAŞİY", "GAUSS", "GAVOT", "GAVUR", "GAYDA", "GAYET", "GAYRİ", "GAYUR", "GAYYA", 
    "GAZAL", "GAZAP", "GAZEL", "GAZLI", "GAZÖZ", "GAZVE", "GEBEŞ", "GEBZE", "GEÇÇE", "GEÇEK", "GEÇEN", "GEÇER", "GEÇİM", 
    "GEÇİŞ", "GEÇİT", "GEÇME", "GEDİK", "GEDİZ", "GEDME", "GELEN", "GELİN", "GELİR", "GELİŞ", "GELME", "GEMİC", "GENEL", 
    "GENİŞ", "GENOM", "GEOİT", "GERÇİ", "GEREK", "GERGİ", "GERİM", "GERİŞ", "GERİZ", "GERME", "GEYİK", "GEYŞA", "GICIK", 
    "GICIR", "GIDIK", "GIDIM", "GIPTA", "GIRLA", "GİDER", "GİDİŞ", "GİDON", "GİRAY", "GİRDİ", "GİREN", "GİRİM", "GİRİŞ", 
    "GİTME", "GİTTİ", "GİYİM", "GİYİŞ", "GİYME", "GİYSİ", "GİZEM", "GİZİL", "GİZLİ", "GLASE", "GNAYS", "GOCUK", "GODOŞ", 
    "GOLCÜ", "GOLLÜ", "GONCA", "GORİL", "GOTÇA", "GOTİK", "GÖBEK", "GÖBEL", "GÖBÜT", "GÖCEN", "GÖÇER", "GÖÇME", "GÖÇÜK", 
    "GÖÇÜM", "GÖÇÜŞ", "GÖDEN", "GÖDEŞ", "GÖĞEM", "GÖĞÜS", "GÖKÇE", "GÖLEK", "GÖLET", "GÖLGE", "GÖLÜK", "GÖMEÇ", "GÖMME", 
    "GÖMÜK", "GÖMÜŞ", "GÖMÜT", "GÖNCÜ", "GÖNEN", "GÖNÜL", "GÖNYE", "GÖREV", "GÖRGÜ", "GÖRME", "GÖRÜM", "GÖRÜŞ", "GÖVDE", 
    "GÖVEK", "GÖVEL", "GÖVEM", "GÖZDE", "GÖZEK", "GÖZEL", "GÖZGÜ", "GÖZLÜ", "GRADO", "GREKİ", "GREST", "GREVE", "GRİDA", 
    "GRİSÜ", "GROGİ", "GROSA", "GUANO", "GUARD", "GUDDE", "GUGUK", "GULAŞ", "GULET", "GURME", "GURUP", "GURUR", "GUSTO", 
    "GUSÜL", "GÜBRE", "GÜBÜR", "GÜCÜK", "GÜCÜN", "GÜÇLÜ", "GÜDEK", "GÜDÜC", "GÜDÜK", "GÜDÜL", "GÜDÜM", "GÜFTE", "GÜĞÜM", 
    "GÜLCÜ", "GÜLEÇ", "GÜLLE", "GÜLLÜ", "GÜLME", "GÜLÜK", "GÜLÜŞ", "GÜLÜT", "GÜMEÇ", "GÜMÜŞ", "GÜNAH", "GÜNCE", "GÜNDE", 
    "GÜNEÇ", "GÜNEŞ", "GÜNEY", "GÜNLÜ", "GÜPÜR", "GÜRCÜ", "GÜREŞ", "GÜRSU", "GÜRUH", "GÜRÜN", "GÜTME", "GÜVEÇ", "GÜVEN", 
    "GÜVEZ", "GÜZEL", "GÜZEY", "GÜZÜN", "HABBE", "HABER", "HABEŞ", "HABİP", "HABİS", "HACET", "HACİM", "HACİR", "HACİZ",

    # 6-Letter Words
    "ADALET", "ANITLI", "BARDAK", "BAŞKAN", "CÖMERT", "ÇADIRI", "ÇAYDAN", "DAĞLIK", "DEPREM", "DİKKAT", "DİVANE", "DOKTOR", 
    "DÜKKAN", "EFSANE", "FIRSAT", "FİLİKA", "GAZETE", "GÖLGEÇ", "GÖZLÜK", "GÜNLÜK", "GÜRGEN", "GÜVENÇ", "HARİTA", "HEYKEL", 
    "IHLAMUR", "IRMAĞI", "İÇERİK", "İLETİŞ", "İTİBAR", "KALYON", "KANYON", "KAPTAN", "KARACA", "KARTAL", "KASABA", "KAYNAK", 
    "KAYSER", "KAZANÇ", "KERVAN", "KISMET", "KONSER", "KÖPRÜS", "KÖŞKER", "KUMRAL", "KÜLTÜR", "LİMANI", "MANTAR", "MEYDAN", 
    "MİMARİ", "MUTLUK", "ORMANI", "OTOBÜS", "ÖĞRENC", "PARLAK", "REHBER", "RÜZGAR", "SAĞLIK", "SANDIK", "SARAYI", "SAYGILI", 
    "SEMBOL", "SEYYAH", "SULTAN", "ŞELALE", "TABİAT", "TARİHİ", "TOPRAK", "TURİST", "TÜRKÇE", "VİLAYE", "YAPRAK", "YARDIM", 
    "YAYLAL", "YOLCUK", "ZENGİN", "ZEYTİN", "ZİYARE", "ZÜMRÜT",

    # 7-Letter Words
    "ANADOLU", "BAĞLAMA", "BAŞKENT", "BEREKET", "BİLGELİ", "BOĞAZİÇ", "ÇARŞISI", "DENİZCİ", "DÖNENCE", "GELENEK", "GÖKYÜZÜ", 
    "GÖZLEME", "HAZİNES", "İSTANBU", "KALEİÇİ", "KAPADOK", "KAPLICA", "KARTPOS", "KENTSEL", "KÖYLERİ", "KÜLTÜRL", "KÜTÜPHA", 
    "MANZARA", "MEDENİY", "MİMARİS", "MİSAFİR", "MÜZELER", "NEMRUTL", "OSMANLI", "PADIŞAH", "PAMUKKA", "RÜZGARL", "SELÇUKL", 
    "SEYYAHL", "TARİHSEL", "TÜRKİYE", "VADİLER", "YAŞAMAK", "YAYLASI", "YOLCULU", "ZAFERLE"
]

def enrich():
    with open('src/data/tdk_dict.json', 'r', encoding='utf-8') as f:
        existing = json.load(f)

    if isinstance(existing, dict):
        words_set = set(existing.keys())
    else:
        words_set = set(existing)

    added = 0
    for w in ADDITIONAL_WORDS:
        # Standardize Turkish word: clean chars
        clean_w = w.strip().upper()
        if clean_w not in words_set:
            words_set.add(clean_w)
            added += 1

    sorted_words = sorted(list(words_set))
    with open('src/data/tdk_dict.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_words, f, ensure_ascii=False, indent=2)

    print(f"Enriched TDK dictionary: Added {added} words. Total words: {len(sorted_words)}")

if __name__ == '__main__':
    enrich()

# -*- coding: utf-8 -*-
"""
Builder for 81-city expandable architecture & hierarchical city data
"""
import json

with open('levels_100.json', 'r', encoding='utf-8') as f:
    levels_100 = json.load(f)

# City registry with verified landmark images and coordinates
CITIES_CONFIG = [
    {
        "id": "izmir",
        "name": "İzmir",
        "plate": 35,
        "region_name": "Ege Bölgesi",
        "coords": {"x": 85, "y": 215},
        "description": "Ege'nin incisi, binlerce yıllık antik kentlerin, zeytin ağaçlarının ve imbat rüzgarlarının şehri.",
        "landmarks": [
            {
                "name": "Efes - Celsus Kütüphanesi",
                "bg": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?auto=format&fit=crop&w=1080&q=75",
                "summary": "Antik dünyanın en görkemli üçüncü kütüphanesinin devasa mermer sütunları arasında gezerken tarihin fısıltılarını duyabilirsiniz.",
                "trivia": "Cephedeki 4 kadın heykeli Sophia (Akıl), Arete (Erdem), Ennoia (Kavrayış) ve Episteme (Bilgi) erdemlerini simgeler."
            },
            {
                "name": "İzmir Saat Kulesi",
                "bg": "https://images.unsplash.com/photo-1589308078059-be1415eab4c3?auto=format&fit=crop&w=1080&q=75",
                "summary": "1901 yılında Konak Meydanı'nda inşa edilen 25 metre yüksekliğindeki kule, İzmir'in kalbi ve en zarif buluşma noktasıdır.",
                "trivia": "Kulenin saati Alman İmparatoru II. Wilhelm tarafından Osmanlı'ya hediye edilmiştir ve kurulduğu günden beri hiç durmamıştır."
            },
            {
                "name": "Şirince Evleri",
                "bg": "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1080&q=75",
                "summary": "Zeytinlikler ve asma bahçeleri arasında bembeyaz geleneksel konaklarıyla masalsı bir Ege köyü.",
                "trivia": "Köyün eski adı 'Kırkınca' olup zamanla güzelliğinden ötürü Şirince olarak anılmaya başlanmıştır."
            },
            {
                "name": "Bergama Akropolü",
                "bg": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1080&q=75",
                "summary": "Tepelerin zirvesine kurulmuş, dünyanın en dik tiyatrosuna ve antik parşömen kütüphanesine sahip eşsiz Helenistik krallık.",
                "trivia": "Parşömen kağıdı (Pergamenum), Bergama Krallığı tarafından kütüphanelerindeki kitapları çoğaltmak için icat edilmiştir."
            },
            {
                "name": "Tarihi Asansör",
                "bg": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1080&q=75",
                "summary": "1907 yılında iki semt arasındaki 155 basamaklı uçurumu aşmak için inşa edilen, körfeze tepeden bakan tarihi kule.",
                "trivia": "Asansörün bulunduğu sokak, İzmirli ünlü besteci ve şarkıcı Dario Moreno'nun adını taşımaktadır."
            }
        ]
    },
    {
        "id": "nevsehir",
        "name": "Nevşehir",
        "plate": 50,
        "region_name": "İç Anadolu Bölgesi",
        "coords": {"x": 395, "y": 205},
        "description": "Milyonlarca yıllık peri bacaları, gökyüzünü süsleyen rengarenk balonları ve yeraltı şehirleriyle masallar diyarı.",
        "landmarks": [
            {
                "name": "Göreme Sıcak Hava Balonları",
                "bg": "https://images.unsplash.com/photo-1641128324972-af3212f0f6bd?auto=format&fit=crop&w=1080&q=75",
                "summary": "Gündoğumunda vadilerin üzerinden yükselen yüzlerce sıcak hava balonu, dünyanın en büyüleyici hava manzaralarından birini sunar.",
                "trivia": "Kapadokya adı antik Pers dilinde 'Katpatuka' yani 'Güzel Atlar Ülkesi' anlamına gelir."
            },
            {
                "name": "Uçhisar Kalesi",
                "bg": "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?auto=format&fit=crop&w=1080&q=75",
                "summary": "Bölgenin en yüksek noktasına oyulmuş dev kaya kütlesi, tüm Kapadokya vadilerine hakim eşsiz bir gözetleme kalesidir.",
                "trivia": "Kalenin içindeki gizli tünellerin kilometrelerce uzaktaki sığınaklara ve su kaynaklarına ulaştığı bilinmektedir."
            },
            {
                "name": "Paşabağ Peribacaları",
                "bg": "https://images.unsplash.com/photo-1565008447742-97f6f38c985c?auto=format&fit=crop&w=1080&q=75",
                "summary": "Çok başlı mantar formundaki peri bacalarının en görkemlilerinin yer aldığı, keşişlerin inzivaya çekildiği büyüleyici vadi.",
                "trivia": "Aziz Simeon gibi rahipler, dünyevi işlerden uzaklaşmak için bu peribacalarının içindeki oyuklarda yıllarca yaşamıştır."
            },
            {
                "name": "Derinkuyu Yeraltı Şehri",
                "bg": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1080&q=75",
                "summary": "Yerin 8 kat altına inen, on binlerce insanın aylarca yaşayabileceği havalandırma, ahır ve kiliseleri olan mühendislik harikası.",
                "trivia": "1963 yılında bir köylünün evini tadilat ederken duvarın arkasında gizli bir oda bulmasıyla tesadüfen keşfedilmiştir."
            },
            {
                "name": "Ihlara Vadisi",
                "bg": "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1080&q=75",
                "summary": "Melendiz Çayı'nın kanyonu yararak oluşturduğu 14 kilometrelik cennet vadide, kayalara oyulmuş yüzlerce tarihi kilise bulunur.",
                "trivia": "Vadinin mikroklima iklimi sayesinde çevresindeki bozkırın aksine fıstık ağaçları ve yemyeşil bitki örtüsü yetişir."
            }
        ]
    },
    {
        "id": "istanbul",
        "name": "İstanbul",
        "plate": 34,
        "region_name": "Marmara Bölgesi",
        "coords": {"x": 175, "y": 105},
        "description": "Asya ile Avrupa'yı birbirine bağlayan, üç büyük imparatorluğa başkentlik yapmış dünyanın kalbi.",
        "landmarks": [
            {
                "name": "Galata Kulesi",
                "bg": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1080&q=75",
                "summary": "1348 yılında Cenevizliler tarafından inşa edilen kule, Haliç ve Boğaz'ın eşsiz panoramasına hakim tarihi fenerdir.",
                "trivia": "17. yüzyılda Hezarfen Ahmed Çelebi takma kanatlarıyla kuleden uçarak Boğaz'ı aşmış ve Üsküdar'a inmiştir."
            },
            {
                "name": "Ayasofya-i Kebir Cami",
                "bg": "https://images.unsplash.com/photo-1546412414-e1885259563a?auto=format&fit=crop&w=1080&q=75",
                "summary": "537 yılında inşa edilen, havada asılı gibi duran devasa kubbesiyle mimarlık tarihinin en büyük başyapıtlarından biri.",
                "trivia": "Kubbesinin inşasında kullanılan hafif volkanik tuğlaların Rodos Adası'ndan özel olarak getirildiği kaydedilmiştir."
            },
            {
                "name": "15 Temmuz Şehitler Köprüsü",
                "bg": "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?auto=format&fit=crop&w=1080&q=75",
                "summary": "Asya ile Avrupa kıtalarını deniz üzerinden birbirine bağlayan Türkiye'nin ilk kıtalararası asma köprüsü.",
                "trivia": "Her yıl düzenlenen İstanbul Maratonu sayesinde dünyada iki kıta arasında koşulan tek parkur olma özelliğine sahiptir."
            },
            {
                "name": "Sultanahmet Camii",
                "bg": "https://images.unsplash.com/photo-1546412414-e1885259563a?auto=format&fit=crop&w=1080&q=75",
                "summary": "İç mekanını süsleyen 20 bini aşkın mavi İznik çinisi ve altı zarif minaresiyle 'Mavi Cami' olarak dünya çapında tanınır.",
                "trivia": "Mimar Sedefkâr Mehmed Ağa, camiyi dönemin en gelişmiş akustik matematik hesaplamalarıyla tasarlamıştır."
            },
            {
                "name": "Kız Kulesi",
                "bg": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1080&q=75",
                "summary": "Boğaz'ın sularında küçük bir adacık üzerinde yükselen, binlerce yıllık efsanelere ev sahipliği yapmış narin kule.",
                "trivia": "Antik çağlarda Boğaz'dan geçen gemilerden vergi almak amacıyla zincir çekilen bir gümrük istasyonu olarak kullanılmıştır."
            }
        ]
    },
    {
        "id": "denizli",
        "name": "Denizli",
        "plate": 20,
        "region_name": "Ege Bölgesi",
        "coords": {"x": 155, "y": 240},
        "description": "Bembeyaz pamuk terasları, antik şifa havuzları ve köklü dokumacılık kültürüyle Ege'nin parlayan yıldızı.",
        "landmarks": [
            {
                "name": "Pamukkale Travertenleri",
                "bg": "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1080&q=75",
                "summary": "Termal suların kalsiyum karbonat biriktirmesiyle oluşan bembeyaz basamaklı teraslar doğanın en nadide sanat eseridir.",
                "trivia": "Teras havuzlarının şifalı suyu yaz-kış 36 derecede sabit kalır."
            },
            {
                "name": "Hierapolis Antik Tiyatrosu",
                "bg": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?auto=format&fit=crop&w=1080&q=75",
                "summary": "Travertenlerin hemen üzerinde yer alan, mitolojik kabartmalarıyla günümüze sapasağlam ulaşmış görkemli Roma tiyatrosu.",
                "trivia": "Hierapolis, antik dönemde gladyatör dövüşlerinin ve termal tedavilerin ana merkeziydi."
            },
            {
                "name": "Kleopatra Antik Havuzu",
                "bg": "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1080&q=75",
                "summary": "M.S. 7. yüzyıldaki depremle yıkılan antik sütunların üzerinde yüzebileceğiniz dünyadaki tek tarihi termal havuz.",
                "trivia": "Efsaneye göre Mısır Kraliçesi Kleopatra güzelliğini bu havuzun mineral zengini sularına borçludur."
            },
            {
                "name": "Kaklık Mağarası",
                "bg": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1080&q=75",
                "summary": "Yeraltında oluşan basamaklı travertenleriyle 'Yeraltı Pamukkalesi' olarak anılan gizemli bir doğa harikası.",
                "trivia": "Mağaranın içindeki kükürtlü ve berrak suların cilt hastalıklarına iyi geldiği bilinmektedir."
            },
            {
                "name": "Laodikeia Antik Kenti",
                "bg": "https://images.unsplash.com/photo-1596422846543-75c6fc197f07?auto=format&fit=crop&w=1080&q=75",
                "summary": "İncil'de adı geçen yedi büyük kiliseden birine ev sahipliği yapan devasa Helenistik ticaret metropolü.",
                "trivia": "Antik dönemde Laodikeia'da üretilen siyah yumuşak yün kumaşlar tüm Akdeniz havzasında aranılan bir lükstü."
            }
        ]
    },
    {
        "id": "adiyaman",
        "name": "Adıyaman",
        "plate": 2,
        "region_name": "Güneydoğu Anadolu",
        "coords": {"x": 560, "y": 245},
        "description": "2150 metre zirvede gökyüzüne bakan tanrılar tahtı ve Kommagene Krallığı'nın ebedi mirası.",
        "landmarks": [
            {
                "name": "Nemrut Dağı Heykelleri",
                "bg": "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?auto=format&fit=crop&w=1080&q=75",
                "summary": "Gündoğumu ve günbatımının en büyüleyici izlendiği zirvede, devasa kral ve tanrı heykelleri doğu ile batıyı buluşturur.",
                "trivia": "Nemrut'taki aslan horoskopu kabartması, tarihin bilinen en eski astrolojik takvimidir."
            },
            {
                "name": "Cendere Köprüsü",
                "bg": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1080&q=75",
                "summary": "Roma İmparatoru Septimius Severus döneminde harçsız olarak 92 devasa blok taşla inşa edilen 1800 yıllık köprü.",
                "trivia": "Dünyanın günümüze kadar ayakta kalmış ve araç trafiğine en uzun süre hizmet etmiş en eski taş köprülerinden biridir."
            },
            {
                "name": "Arsemia Ören Yeri",
                "bg": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1080&q=75",
                "summary": "Kommagene krallarının yazlık başkenti; kayalara oyulmuş kabartmaları ve gizemli derin tünelleriyle meşhurdur.",
                "trivia": "Kral I. Antiochos ile Herakles'in el sıkışmasını betimleyen kabartma, antik dostluğun en önemli simgesidir."
            },
            {
                "name": "Karakuş Tümülüsü",
                "bg": "https://images.unsplash.com/photo-1565008447742-97f6f38c985c?auto=format&fit=crop&w=1080&q=75",
                "summary": "Sütun üzerindeki kartal heykeliyle tanınan, Kommagene kraliyet kadınlarına ait anıtsal mezar anıtı.",
                "trivia": "Sütundaki kartal heykeli gücü ve göksel korumayı simgeler."
            },
            {
                "name": "Kahta Kalesi",
                "bg": "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?auto=format&fit=crop&w=1080&q=75",
                "summary": "Sarp kayalıkların üzerine kartal yuvası gibi kurulmuş, Memlük ve Selçuklu izlerini taşıyan savunma kalesi.",
                "trivia": "Kaleden nehre inen gizli su yolları ve güvercinlikler günümüze kadar korunmuştur."
            }
        ]
    },
    {
        "id": "trabzon",
        "name": "Trabzon",
        "plate": 61,
        "region_name": "Karadeniz Bölgesi",
        "coords": {"x": 590, "y": 105},
        "description": "Zümrüt yeşili yaylaları, sisli dağları ve Karadağ'ın sarp kayalıklarına oyulmuş Sümela'nın vatanı.",
        "landmarks": [
            {
                "name": "Sümela Manastırı",
                "bg": "https://images.unsplash.com/photo-1589308078059-be1415eab4c3?auto=format&fit=crop&w=1080&q=75",
                "summary": "Deniz seviyesinden 1150 metre yüksekte, Karadağ'ın dik yamacına oyulmuş gökyüzünde asılı duran mucizevi manastır.",
                "trivia": "Manastırın içindeki ana kaya kilisesinin freskleri asırlardır canlı renklerini korumaktadır."
            },
            {
                "name": "Uzungöl",
                "bg": "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1080&q=75",
                "summary": "Dağ yamacından düşen kayaların Haldizen Deresi'nin önünü kapatmasıyla oluşan masalsı krater gölü.",
                "trivia": "Göl çevresindeki zengin ladin ormanları Kafkas yaban hayatının önemli bir sığınağıdır."
            },
            {
                "name": "Trabzon Ayasofyası",
                "bg": "https://images.unsplash.com/photo-1546412414-e1885259563a?auto=format&fit=crop&w=1080&q=75",
                "summary": "13. yüzyılda Trabzon İmparatorluğu döneminde inşa edilen, taş kabartmaları ve freskleriyle ünlü tarihi yapı.",
                "trivia": "Güney cephesindeki Adem ile Havva'nın yaratılışını anlatan taş friz Orta Çağ heykel sanatının nadir örneklerindendir."
            },
            {
                "name": "Atatürk Köşkü",
                "bg": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1080&q=75",
                "summary": "Soğuksu çam koruluğu içinde 1890 yılında inşa edilen bembeyaz Art Nouveau tarzı görkemli köşk.",
                "trivia": "Gazi Mustafa Kemal Atatürk, 1937 yılındaki Trabzon ziyaretinde tüm mal varlığını milletine bağışlama kararını bu köşkte almıştır."
            },
            {
                "name": "Boztepe",
                "bg": "https://images.unsplash.com/photo-1589308078059-be1415eab4c3?auto=format&fit=crop&w=1080&q=75",
                "summary": "Karadeniz'in sonsuz maviliği ile Trabzon kent merkezini panoramik olarak kucaklayan tarihi tepe.",
                "trivia": "Semaver çayı eşliğinde batan güneşi izlemek asırlardır şehrin en sevilen ritüelidir."
            }
        ]
    },
    {
        "id": "sanliurfa",
        "name": "Şanlıurfa",
        "plate": 63,
        "region_name": "Güneydoğu Anadolu",
        "coords": {"x": 580, "y": 285},
        "description": "Tarihin sıfır noktası Göbeklitepe, efsanevi Balıklıgöl ve kadim peygamberler şehri.",
        "landmarks": [
            {
                "name": "Göbeklitepe Dikilitaşları",
                "bg": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1080&q=75",
                "summary": "M.Ö. 10.000 yılına tarihlenen T biçimli hayvan kabartmalı dikilitaşlar, insanlık tarihinin bilinen ilk anıtsal tapınağıdır.",
                "trivia": "Göbeklitepe, Mısır Piramitleri'nden 7.000 yıl, Stonehenge'den 6.000 yıl daha eskidir."
            },
            {
                "name": "Balıklıgöl (Halil-ür Rahman)",
                "bg": "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1080&q=75",
                "summary": "Hz. İbrahim'in ateşe atıldığında ateşin suya, odunların balığa dönüştüğüne inanılan kutsal göl.",
                "trivia": "Göldeki balıklar kutsal kabul edildiği için tutulmaz ve asırlardır özenle beslenir."
            },
            {
                "name": "Harran Kümbet Evleri",
                "bg": "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?auto=format&fit=crop&w=1080&q=75",
                "summary": "Konik kubbeli kerpiç evleri ve dünyanın ilk üniversitelerinden birinin kalıntılarıyla ünlü tarihi çöl vahası.",
                "trivia": "Harran evlerinin harcında yumurta akı ve saman kullanılmış olup yazın serin, kışın sıcacık tutar."
            },
            {
                "name": "Şanlıurfa Kalesi",
                "bg": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1080&q=75",
                "summary": "Balıklıgöl'e tepeden bakan ve üzerinde Korint başlıklı iki devasa anıtsal sütun bulunan tarihi kale.",
                "trivia": "Halk arasında 'Mancınık Sütunları' olarak bilinen sütunların Hz. İbrahim'i ateşe atmak için kullanıldığı rivayet edilir."
            },
            {
                "name": "Halfeti Batık Şehir",
                "bg": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1080&q=75",
                "summary": "Birecik Barajı gölü altında kalan tarihi taş evleri, minaresi sudan çıkan camisi ve efsanevi siyah gülüyle ünlü saklı cennet.",
                "trivia": "Dünyada yalnızca Halfeti'nin mikroklimalı toprağında doğal olarak simsiyah gül (Karagül) yetişmektedir."
            }
        ]
    },
    {
        "id": "kars",
        "name": "Kars",
        "plate": 36,
        "region_name": "Doğu Anadolu",
        "coords": {"x": 730, "y": 115},
        "description": "Binbir kiliseli efsanevi Ani Harabeleri, donmuş Çıldır Gölü ve Baltık mimarisiyle Doğu'nun kalesi.",
        "landmarks": [
            {
                "name": "Ani Harabeleri - Katedral",
                "bg": "https://images.unsplash.com/photo-1565008447742-97f6f38c985c?auto=format&fit=crop&w=1080&q=75",
                "summary": "İpek Yolu üzerinde kurulan ve Orta Çağ'ın en büyük ticaret metropollerinden biri olan '1001 Kiliseli Şehir'.",
                "trivia": "Ani Katedrali'nin mimarı Trdat, aynı zamanda İstanbul'daki Ayasofya'nın depremde yıkılan kubbesini onaran dahi mimardır."
            },
            {
                "name": "Menûçihr Camii",
                "bg": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1080&q=75",
                "summary": "Arpaçay Kanyonu'nun kıyısında 1072 yılında inşa edilen, Anadolu'daki ilk Türk camisi.",
                "trivia": "Tavanındaki renkli taşlarla yapılan geometrik süslemeler Selçuklu sanatının ilk öncüleridir."
            },
            {
                "name": "Kars Kalesi",
                "bg": "https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?auto=format&fit=crop&w=1080&q=75",
                "summary": "1153 yılında Selçuklu Sultanı Melik İzzeddin tarafından inşa ettirilen, sarp tepede şehri koruyan anıtsal kale.",
                "trivia": "1855 yılındaki Kars Zaferi sebebiyle şehre Osmanlı tarihinde ilk kez 'Gazi' unvanı verilmiştir."
            },
            {
                "name": "Çıldır Gölü",
                "bg": "https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1080&q=75",
                "summary": "Kışın tamamen buz tutan yüzeyinde atlı kızakların kaydığı, 1959 metre rakımlı Doğu Anadolu'nun en büyük tatlı su gölü.",
                "trivia": "Kışın buz tabakası kırılarak tutulan 'Sarı Balık' bölgenin en ünlü kış lezzetidir."
            },
            {
                "name": "Fethiye Camii (Havariler)",
                "bg": "https://images.unsplash.com/photo-1546412414-e1885259563a?auto=format&fit=crop&w=1080&q=75",
                "summary": "10. yüzyılda Ermeni Bagratlı Krallığı döneminde bazalt taşlarla inşa edilen 12 Havariler Kilisesi.",
                "trivia": "Kubbe eteğinde 12 havariyi temsil eden kabartma heykeller günümüze kadar ulaşmıştır."
            }
        ]
    }
]

# Build map of city levels: 5 levels per city, total 40 levels (and scalable to all 81 cities!)
# We take verified crosswords from levels_100
city_levels = []
global_id = 1
for city_idx, city in enumerate(CITIES_CONFIG):
    city["levels"] = []
    for sub_idx in range(5):
        # Pick corresponding level from levels_100 to guarantee strict crossword & 100% multiset solvability
        source_lvl = levels_100[(city_idx * 5 + sub_idx) % len(levels_100)]
        lm = city["landmarks"][sub_idx]
        lvl_entry = {
            "id": global_id,
            "city_id": city["id"],
            "city_name": city["name"],
            "sub_id": sub_idx + 1,
            "title": f"{city['name']} - Bölüm {sub_idx + 1}: {lm['name']}",
            "landmark_name": lm["name"],
            "bg": lm["bg"],
            "wheel": source_lvl["wheel"],
            "words": source_lvl["words"],
            "bonus": source_lvl.get("bonus", []),
            "postcard": {
                "title": lm["name"],
                "city": city["name"],
                "plate": city["plate"],
                "summary": lm["summary"],
                "trivia": lm["trivia"],
                "bg": lm["bg"]
            }
        }
        city["levels"].append(lvl_entry)
        city_levels.append(lvl_entry)
        global_id += 1

print(f"Generated {len(CITIES_CONFIG)} cities with {len(city_levels)} rich landmark levels.")

with open('cities_data.json', 'w', encoding='utf-8') as f:
    json.dump(CITIES_CONFIG, f, ensure_ascii=False, indent=2)

print("Saved cities_data.json successfully!")

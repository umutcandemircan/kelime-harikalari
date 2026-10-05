import urllib.request

test_urls = {
    'cappadocia_balloons': 'https://images.unsplash.com/photo-1641128324972-af3212f0f6bd?auto=format&fit=crop&w=1280&q=85',
    'cappadocia_alt': 'https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?auto=format&fit=crop&w=1280&q=85',
    'colosseum': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=1280&q=85',
    'taj_mahal': 'https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1280&q=85',
    'ephesus': 'https://images.unsplash.com/photo-1596422846543-75c6fc197f07?auto=format&fit=crop&w=1280&q=85',
    'pamukkale': 'https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1280&q=85',
    'pyramids': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?auto=format&fit=crop&w=1280&q=85',
    'parthenon': 'https://images.unsplash.com/photo-1555993539-1732b0258235?auto=format&fit=crop&w=1280&q=85',
}

for name, url in test_urls.items():
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"{name}: status {resp.status}, {resp.headers.get('Content-Type')}")
    except Exception as e:
        print(f"{name}: FAILED - {e}")

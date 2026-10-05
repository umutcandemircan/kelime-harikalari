import urllib.request

candidate_urls = {
    'kapadokya': 'https://images.unsplash.com/photo-1641128324972-af3212f0f6bd?auto=format&fit=crop&w=1280&q=85',
    'efes': 'https://images.unsplash.com/photo-1596422846543-75c6fc197f07?auto=format&fit=crop&w=1280&q=85',
    'nemrut': 'https://images.unsplash.com/photo-1578328819058-b69f3a3b0f6b?auto=format&fit=crop&w=1280&q=85',
    'pamukkale': 'https://images.unsplash.com/photo-1527838832700-5059252407fa?auto=format&fit=crop&w=1280&q=85',
    'galata': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a1b?auto=format&fit=crop&w=1280&q=85',
    'sumela': 'https://images.unsplash.com/photo-1589308078059-be1415eab4c3?auto=format&fit=crop&w=1280&q=85',
    'gobeklitepe': 'https://images.unsplash.com/photo-1590059390046-538d5db32123?auto=format&fit=crop&w=1280&q=85',
    'ani': 'https://images.unsplash.com/photo-1565008447742-97f6f38c985c?auto=format&fit=crop&w=1280&q=85',
    'colosseum': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=1280&q=85',
    'taj_mahal': 'https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1280&q=85',
}

for name, url in candidate_urls.items():
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            print(f'{name}: status {resp.status}, {resp.headers.get("Content-Type")}')
    except Exception as e:
        print(f'{name}: FAILED {e}')

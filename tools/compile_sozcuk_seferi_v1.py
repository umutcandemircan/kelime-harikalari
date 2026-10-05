import json
import os

print("Compiling Sözcük Seferî v1.0 Production index.html...")

with open('unified_cities.json', 'r', encoding='utf-8') as f:
    unified_cities = json.load(f)

with open('turkey_svg_map.json', 'r', encoding='utf-8') as f:
    turkey_map = json.load(f)

# Idioms dataset
idioms_data = [
    {"clue": "Göze [...]", "answer": "GİRMEK", "meaning": "Sevgi ve güven kazanmak, takdir edilmek."},
    {"clue": "Baltayı taşa [...]", "answer": "VURMAK", "meaning": "Farkında olmadan birine dokunacak uygunsuz söz söylemek."},
    {"clue": "Ateşle [...]", "answer": "OYNAMAK", "meaning": "Çok tehlikeli, riskli bir işe girişmek."},
    {"clue": "Kulak [...]", "answer": "KABARTMAK", "meaning": "Belli etmemeye çalışarak dikkatle dinlemek."},
    {"clue": "Etekleri [...]", "answer": "ZİL ÇALMAK", "meaning": "Çok sevinmek, mutluluktan coşmak."},
    {"clue": "Çantada [...]", "answer": "KEKLİK", "meaning": "Kolayca ele geçeceği, kesin kazanılacağı sanılan şey."},
    {"clue": "Gözden [...]", "answer": "DÜŞMEK", "meaning": "Eski sevgisini, saygısını ve değerini yitirmek."},
    {"clue": "Pireyi deve [...]", "answer": "YAPMAK", "meaning": "Küçük ve önemsiz bir durumu çok büyütmek."},
    {"clue": "Burnundan [...]", "answer": "SOLUMAK", "meaning": "Aşırı derecede öfkelenmiş olmak."},
    {"clue": "Ağzı kulaklarına [...]", "answer": "VARMAK", "meaning": "Büyük bir müjde veya başarıyla çok sevinmek."},
    {"clue": "Dile [...]", "answer": "DÜŞMEK", "meaning": "Hakkında her yerde dedikodu yapılmak."},
    {"clue": "İçi [...]", "answer": "ERİMEK", "meaning": "Büyük üzüntü duymak veya sabırsızlıkla beklemek."},
    {"clue": "Karnı zil [...]", "answer": "ÇALMAK", "meaning": "Çok fazla acıkmış olmak."},
    {"clue": "İpe un [...]", "answer": "SERMEK", "meaning": "Geçerli olmayan bahanelerle işi savsaklamak."},
    {"clue": "Damarına [...]", "answer": "BASMAK", "meaning": "Bir kimsenin en hassas, kızacağı noktasına değinmek."}
]

# Generate SVG paths for all 81 provinces
svg_provinces_markup = []
for p in turkey_map:
    plate = p['plate']
    name = p['name']
    d = p['d']
    svg_provinces_markup.append(f'<path id="prov-{plate}" class="province-path" data-plate="{plate}" data-name="{name}" d="{d}" />')

svg_provinces_str = "\n".join(svg_provinces_markup)

cities_json_str = json.dumps(unified_cities, ensure_ascii=False)
idioms_json_str = json.dumps(idioms_data, ensure_ascii=False)

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="referrer" content="no-referrer">
    <title>Sözcük Seferî: 1. Sefer Türkiye</title>
    <!-- SVG Data-URI Favicon: Compass & Gold 'S' -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='30' fill='%230b132b' stroke='%23f59e0b' stroke-width='3'/%3E%3Cpolygon points='32,8 37,27 56,32 37,37 32,56 27,37 8,32 27,27' fill='%230d9488'/%3E%3Ccircle cx='32' cy='32' r='12' fill='%23f8f9fa'/%3E%3Ctext x='32' y='38' font-size='16' font-weight='900' font-family='sans-serif' fill='%230b132b' text-anchor='middle'%3ES%3C/text%3E%3C/svg%3E">

    <style>
        :root {{
            --bg-slate: #0b132b;
            --bg-slate-card: #142247;
            --bg-slate-panel: rgba(11, 19, 43, 0.92);
            --text-ivory: #f8f9fa;
            --gold-primary: #f59e0b;
            --gold-dark: #d97706;
            --gold-shadow: #b45309;
            --turquoise: #0d9488;
            --turquoise-dark: #0f766e;
            --turquoise-shadow: #042f2c;
            --seal-red: #991b1b;
            --seal-shadow: #7f1d1d;
            --tile-bg: rgba(255, 255, 255, 0.12);
            --tile-border: rgba(255, 255, 255, 0.28);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
            -webkit-user-select: none;
            -webkit-tap-highlight-color: transparent;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }}

        body {{
            background-color: var(--bg-slate);
            color: var(--text-ivory);
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            position: relative;
        }}

        /* 3D TACTILE BUTTONS */
        .btn-3d {{
            background: linear-gradient(180deg, var(--gold-primary) 0%, var(--gold-dark) 100%);
            color: #ffffff;
            border: none;
            border-radius: 14px;
            padding: 14px 28px;
            font-weight: 700;
            font-size: 16px;
            letter-spacing: 0.5px;
            box-shadow: 0 6px 0 var(--gold-shadow), 0 10px 20px rgba(0, 0, 0, 0.45);
            cursor: pointer;
            transition: transform 0.08s ease, box-shadow 0.08s ease;
            will-change: transform;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}

        .btn-3d:active {{
            transform: translate3d(0, 4px, 0);
            box-shadow: 0 2px 0 var(--gold-shadow), 0 4px 8px rgba(0, 0, 0, 0.4);
        }}

        .btn-3d-turquoise {{
            background: linear-gradient(180deg, #14b8a6 0%, var(--turquoise) 100%);
            box-shadow: 0 6px 0 var(--turquoise-shadow), 0 10px 20px rgba(0, 0, 0, 0.45);
        }}
        .btn-3d-turquoise:active {{
            box-shadow: 0 2px 0 var(--turquoise-shadow), 0 4px 8px rgba(0, 0, 0, 0.4);
        }}

        .btn-3d-indigo {{
            background: linear-gradient(180deg, #6366f1 0%, #4f46e5 100%);
            box-shadow: 0 6px 0 #312e81, 0 10px 20px rgba(0, 0, 0, 0.45);
        }}
        .btn-3d-indigo:active {{
            box-shadow: 0 2px 0 #312e81, 0 4px 8px rgba(0, 0, 0, 0.4);
        }}

        .btn-3d-outline {{
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.25);
            color: var(--text-ivory);
            box-shadow: 0 4px 0 rgba(0, 0, 0, 0.5);
            padding: 8px 16px;
            font-size: 14px;
            border-radius: 10px;
        }}
        .btn-3d-outline:active {{
            transform: translate3d(0, 2px, 0);
            box-shadow: 0 2px 0 rgba(0, 0, 0, 0.5);
        }}

        /* SCREEN STATE MACHINE */
        .screen {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            display: none;
            opacity: 0;
            flex-direction: column;
            will-change: opacity, transform;
            transition: opacity 0.3s cubic-bezier(0.2, 0, 0, 1), transform 0.3s cubic-bezier(0.2, 0, 0, 1);
        }}

        .screen.active {{
            display: flex;
            opacity: 1;
            z-index: 10;
        }}

        /* TOP BAR */
        .top-navbar {{
            width: 100%;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 16px;
            background: rgba(11, 19, 43, 0.85);
            backdrop-filter: blur(8px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            z-index: 50;
        }}

        .brand-badge {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 800;
            font-size: 17px;
            letter-spacing: 0.5px;
            color: var(--gold-primary);
        }}

        .brand-logo-svg {{
            width: 32px;
            height: 32px;
            filter: drop-shadow(0 0 6px rgba(245, 158, 11, 0.5));
        }}

        .nav-stats {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .stat-pill {{
            background: rgba(0, 0, 0, 0.45);
            border: 1px solid rgba(245, 158, 11, 0.4);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 700;
            color: var(--gold-primary);
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.5);
        }}

        /* HUB SCREEN */
        #screen-hub {{
            background: radial-gradient(circle at 50% 20%, #1e2d5a 0%, #0b132b 75%);
            justify-content: space-between;
            align-items: center;
            padding: 24px 16px;
            overflow-y: auto;
        }}

        .hub-hero {{
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            margin-top: 10px;
        }}

        .hub-logo-large {{
            width: 90px;
            height: 90px;
            margin-bottom: 12px;
            filter: drop-shadow(0 0 16px rgba(245, 158, 11, 0.6));
            animation: pulse-slow 3s infinite alternate ease-in-out;
        }}

        @keyframes pulse-slow {{
            0% {{ transform: scale(1); }}
            100% {{ transform: scale(1.05); }}
        }}

        .hub-title {{
            font-size: 30px;
            font-weight: 900;
            color: var(--gold-primary);
            letter-spacing: 2px;
            text-transform: uppercase;
            text-shadow: 0 2px 10px rgba(0,0,0,0.6);
        }}

        .hub-subtitle {{
            font-size: 14px;
            font-weight: 600;
            color: #94a3b8;
            letter-spacing: 4px;
            margin-top: 4px;
            text-transform: uppercase;
        }}

        .hub-cards-container {{
            width: 100%;
            max-width: 420px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin: 20px 0;
        }}

        .hub-card {{
            background: var(--bg-slate-card);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 18px;
            padding: 18px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
            transition: transform 0.15s ease, border-color 0.15s ease;
        }}

        .hub-card:active {{
            transform: scale(0.98);
        }}

        .hub-card-primary {{
            border-color: rgba(245, 158, 11, 0.45);
            background: linear-gradient(135deg, rgba(30, 45, 90, 0.9) 0%, rgba(13, 20, 44, 0.95) 100%);
        }}

        .hub-card-icon {{
            font-size: 32px;
            width: 52px;
            height: 52px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-right: 14px;
        }}

        .hub-card-content {{
            flex: 1;
        }}

        .hub-card-title {{
            font-size: 18px;
            font-weight: 800;
            color: var(--text-ivory);
        }}

        .hub-card-desc {{
            font-size: 12px;
            color: #94a3b8;
            margin-top: 3px;
        }}

        .hub-card-badge {{
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 12px;
            background: rgba(245, 158, 11, 0.2);
            color: var(--gold-primary);
            border: 1px solid rgba(245, 158, 11, 0.4);
            margin-left: 8px;
        }}

        /* MAP SCREEN */
        #screen-map {{
            background: #060b18;
            position: relative;
            overflow: hidden;
        }}

        #map-stage-wrapper {{
            width: 100%;
            height: 100%;
            position: relative;
            overflow: hidden;
        }}

        #map-viewport {{
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            transform-origin: 0 0;
            will-change: transform;
            transition: transform 1.2s cubic-bezier(0.25, 1, 0.5, 1);
        }}

        .turkey-svg {{
            width: 1100px;
            height: 500px;
            display: block;
        }}

        .province-path {{
            fill: #13223f;
            stroke: #0d9488;
            stroke-width: 1.1;
            transition: fill 0.2s ease, stroke 0.2s ease;
            cursor: pointer;
        }}

        .province-path:hover, .province-path.hovered {{
            fill: #1d3561;
            stroke: var(--gold-primary);
            stroke-width: 1.8;
        }}

        .province-path.active-city {{
            fill: #223e75;
            stroke: var(--gold-primary);
            stroke-width: 2.4;
            filter: drop-shadow(0 0 10px rgba(245, 158, 11, 0.8));
        }}

        .province-path.completed {{
            fill: #0c333a;
            stroke: #14b8a6;
        }}

        /* MAP NODES & PINS */
        .city-pin-node {{
            cursor: pointer;
            transition: transform 0.2s ease;
        }}

        .city-pin-circle {{
            fill: #0b132b;
            stroke: var(--gold-primary);
            stroke-width: 2;
            transition: r 0.2s ease, fill 0.2s ease;
        }}

        .city-pin-node.current .city-pin-circle {{
            fill: var(--gold-primary);
            stroke: #ffffff;
            stroke-width: 3;
            animation: pulse-pin 1.5s infinite;
        }}

        @keyframes pulse-pin {{
            0% {{ transform: scale(1); filter: drop-shadow(0 0 4px var(--gold-primary)); }}
            50% {{ transform: scale(1.3); filter: drop-shadow(0 0 12px var(--gold-primary)); }}
            100% {{ transform: scale(1); filter: drop-shadow(0 0 4px var(--gold-primary)); }}
        }}

        .city-pin-text {{
            font-size: 8px;
            font-weight: 800;
            fill: var(--text-ivory);
            text-anchor: middle;
            dominant-baseline: central;
            pointer-events: none;
        }}

        .city-label-text {{
            font-size: 10px;
            font-weight: 700;
            fill: var(--text-ivory);
            text-anchor: middle;
            pointer-events: none;
            text-shadow: 0 1px 4px rgba(0,0,0,0.9);
        }}

        /* ROUTE & TRAVEL CARRIER */
        #travel-route {{
            stroke: var(--gold-primary);
            stroke-width: 3;
            stroke-dasharray: 8 6;
            fill: none;
            opacity: 0;
            transition: opacity 0.4s ease;
            filter: drop-shadow(0 0 6px var(--gold-primary));
        }}

        #travel-carrier {{
            opacity: 0;
            will-change: transform;
            filter: drop-shadow(0 0 8px #ffffff);
            pointer-events: none;
        }}

        /* SLIDING CITY BOTTOM CARD */
        .map-city-card {{
            position: absolute;
            bottom: 24px;
            left: 50%;
            transform: translate3d(-50%, 120%, 0);
            width: 92%;
            max-width: 440px;
            background: var(--bg-slate-panel);
            border: 2px solid var(--gold-primary);
            border-radius: 20px;
            padding: 18px 20px;
            backdrop-filter: blur(16px);
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.65);
            display: flex;
            flex-direction: column;
            gap: 12px;
            z-index: 40;
            transition: transform 0.4s cubic-bezier(0.18, 0.89, 0.32, 1.28);
        }}

        .map-city-card.active {{
            transform: translate3d(-50%, 0, 0);
        }}

        .map-city-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .map-city-plate {{
            background: var(--gold-primary);
            color: #0b132b;
            font-size: 14px;
            font-weight: 900;
            padding: 4px 10px;
            border-radius: 8px;
        }}

        .map-city-name {{
            font-size: 20px;
            font-weight: 800;
            color: var(--text-ivory);
            margin-left: 10px;
            flex: 1;
        }}

        /* GAMEPLAY SCREEN */
        #screen-game {{
            background: #080f24;
            justify-content: space-between;
            position: relative;
        }}

        .game-bg-image {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.28;
            filter: blur(2px) brightness(0.7);
            z-index: 1;
            pointer-events: none;
            transition: opacity 0.5s ease;
        }}

        .game-ui-layer {{
            position: relative;
            z-index: 2;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .game-header {{
            width: 100%;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: linear-gradient(180deg, rgba(11, 19, 43, 0.95) 0%, rgba(11, 19, 43, 0) 100%);
        }}

        .game-title-group {{
            text-align: center;
        }}

        .game-city-label {{
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            color: var(--turquoise);
            text-transform: uppercase;
        }}

        .game-landmark-label {{
            font-size: 16px;
            font-weight: 800;
            color: var(--gold-primary);
            max-width: 200px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        /* CROSSWORD GRID CONTAINER */
        .crossword-viewport {{
            flex: 1;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 16px;
            overflow: hidden;
        }}

        .crossword-board {{
            position: relative;
            will-change: transform;
            transform-origin: center center;
            transition: transform 0.25s ease;
        }}

        .grid-cell {{
            position: absolute;
            width: 44px;
            height: 44px;
            background: var(--tile-bg);
            border: 2px solid var(--tile-border);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            font-weight: 800;
            color: transparent;
            backdrop-filter: blur(6px);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
            will-change: transform;
            perspective: 800px;
            transition: background 0.3s ease, border-color 0.3s ease, transform 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28);
        }}

        .grid-cell.solved {{
            background: var(--text-ivory);
            border-color: #ffffff;
            color: var(--bg-slate);
            transform: scale(1.04) rotateY(360deg);
            box-shadow: 0 6px 16px rgba(245, 158, 11, 0.5);
        }}

        .grid-cell.star-cell::after {{
            content: '⭐';
            position: absolute;
            top: -6px;
            right: -6px;
            font-size: 13px;
        }}

        .grid-cell.target-mode {{
            border-color: #ef4444;
            animation: target-pulse 0.8s infinite alternate;
            cursor: pointer;
        }}

        @keyframes target-pulse {{
            0% {{ transform: scale(1); box-shadow: 0 0 6px #ef4444; }}
            100% {{ transform: scale(1.1); box-shadow: 0 0 16px #ef4444; }}
        }}

        /* PREVIEW PILL & WHEEL */
        .bottom-action-area {{
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-bottom: 24px;
        }}

        .word-preview-pill {{
            background: rgba(13, 148, 136, 0.95);
            color: #ffffff;
            padding: 8px 24px;
            border-radius: 24px;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: 3px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
            opacity: 0;
            transform: translate3d(0, 10px, 0);
            transition: opacity 0.15s ease, transform 0.15s ease, background 0.25s ease;
            margin-bottom: 14px;
            pointer-events: none;
            min-height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .word-preview-pill.active {{
            opacity: 1;
            transform: translate3d(0, 0, 0);
        }}

        .wheel-assembly {{
            position: relative;
            width: 270px;
            height: 270px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(20, 34, 71, 0.85) 0%, rgba(11, 19, 43, 0.95) 100%);
            border: 3px solid rgba(245, 158, 11, 0.35);
            box-shadow: inset 0 0 24px rgba(0, 0, 0, 0.6), 0 12px 32px rgba(0, 0, 0, 0.55);
            display: flex;
            align-items: center;
            justify-content: center;
            touch-action: none;
        }}

        .wheel-svg-layer {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }}

        .letter-node {{
            position: absolute;
            width: 52px;
            height: 52px;
            border-radius: 50%;
            background: var(--text-ivory);
            color: var(--bg-slate);
            font-size: 24px;
            font-weight: 900;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.45);
            cursor: pointer;
            transform: translate(-50%, -50%);
            transition: transform 0.12s cubic-bezier(0.18, 0.89, 0.32, 1.28), background 0.12s ease;
            user-select: none;
        }}

        .letter-node.selected {{
            background: var(--gold-primary);
            color: #ffffff;
            transform: translate(-50%, -50%) scale(1.22);
            box-shadow: 0 8px 20px rgba(245, 158, 11, 0.6);
        }}

        /* POWER-UPS DOCK */
        .powerups-dock {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 14px;
            margin-top: 18px;
            width: 100%;
            max-width: 380px;
        }}

        .powerup-btn {{
            width: 54px;
            height: 54px;
            border-radius: 16px;
            background: var(--bg-slate-card);
            border: 2px solid var(--turquoise);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
            transition: transform 0.08s ease;
        }}

        .powerup-btn:active {{
            transform: scale(0.92);
        }}

        .powerup-icon {{
            font-size: 20px;
        }}

        .powerup-price {{
            font-size: 10px;
            font-weight: 800;
            color: var(--gold-primary);
            margin-top: 1px;
        }}

        /* DEYİM AVCISI SCREEN */
        #screen-idiom {{
            background: radial-gradient(circle at 50% 30%, #2e1065 0%, #0b132b 85%);
            justify-content: space-between;
        }}

        .idiom-banner {{
            font-size: 14px;
            color: #c084fc;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }}

        .idiom-clue-box {{
            font-size: 28px;
            font-weight: 900;
            color: var(--gold-primary);
            text-shadow: 0 2px 12px rgba(0,0,0,0.6);
            margin-bottom: 24px;
            text-align: center;
            padding: 0 20px;
        }}

        .idiom-board {{
            display: flex;
            gap: 8px;
            justify-content: center;
            margin-bottom: 30px;
        }}

        /* MODALS */
        .modal-backdrop {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(4, 8, 20, 0.88);
            backdrop-filter: blur(10px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 100;
            opacity: 0;
            transition: opacity 0.25s ease;
            padding: 20px;
        }}

        .modal-backdrop.active {{
            display: flex;
            opacity: 1;
        }}

        .modal-dialog {{
            background: var(--bg-slate-card);
            border: 2px solid var(--gold-primary);
            border-radius: 24px;
            padding: 24px;
            max-width: 380px;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
            transform: scale(0.9);
            transition: transform 0.25s cubic-bezier(0.18, 0.89, 0.32, 1.28);
        }}

        .modal-backdrop.active .modal-dialog {{
            transform: scale(1);
        }}

        /* DISCOVERY POSTCARD */
        .postcard-photo-frame {{
            width: 100%;
            height: 180px;
            border-radius: 16px;
            position: relative;
            overflow: hidden;
            margin: 14px 0;
            border: 2px solid rgba(255, 255, 255, 0.2);
            box-shadow: inset 0 0 16px rgba(0,0,0,0.5);
        }}

        .postcard-img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .wax-seal {{
            position: absolute;
            bottom: 12px;
            right: 12px;
            width: 58px;
            height: 58px;
            border-radius: 50%;
            background: radial-gradient(circle, var(--seal-red) 60%, var(--seal-shadow) 100%);
            border: 3px dashed rgba(255, 255, 255, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            font-size: 8px;
            font-weight: 900;
            text-transform: uppercase;
            text-align: center;
            transform: rotate(-14deg);
            box-shadow: 0 4px 10px rgba(0,0,0,0.6);
            line-height: 1.1;
        }}

        .postcard-story {{
            font-size: 13px;
            color: #cbd5e1;
            line-height: 1.5;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>

    <!-- SCREEN 1: HUB / ANA MENÜ -->
    <div id="screen-hub" class="screen active">
        <div class="top-navbar" style="background: transparent; border: none;">
            <div class="brand-badge">
                <svg class="brand-logo-svg" viewBox="0 0 64 64">
                    <circle cx="32" cy="32" r="30" fill="#0b132b" stroke="#f59e0b" stroke-width="3"/>
                    <polygon points="32,8 37,27 56,32 37,37 32,56 27,37 8,32 27,27" fill="#0d9488"/>
                    <circle cx="32" cy="32" r="12" fill="#f8f9fa"/>
                    <text x="32" y="38" font-size="16" font-weight="900" font-family="sans-serif" fill="#0b132b" text-anchor="middle">S</text>
                </svg>
                <span>SÖZCÜK SEFERÎ</span>
            </div>
            <div class="nav-stats">
                <div class="stat-pill">🪙 <span id="hub-coins">250</span></div>
                <button class="btn-3d-outline" onclick="App.showSettings()">⚙️</button>
            </div>
        </div>

        <div class="hub-hero">
            <svg class="hub-logo-large" viewBox="0 0 64 64">
                <circle cx="32" cy="32" r="30" fill="#142247" stroke="#f59e0b" stroke-width="3"/>
                <polygon points="32,6 38,26 58,32 38,38 32,58 26,38 6,32 26,26" fill="#0d9488"/>
                <circle cx="32" cy="32" r="13" fill="#f8f9fa"/>
                <text x="32" y="39" font-size="18" font-weight="900" font-family="sans-serif" fill="#0b132b" text-anchor="middle">S</text>
            </svg>
            <div class="hub-title">SÖZCÜK SEFERÎ</div>
            <div class="hub-subtitle">1. SEFER: TÜRKİYE</div>
        </div>

        <div class="hub-cards-container">
            <!-- CARD 1: ANA SEFER -->
            <div class="hub-card hub-card-primary" onclick="App.goToScreen('screen-map')">
                <div class="hub-card-icon">🧭</div>
                <div class="hub-card-content">
                    <div style="display:flex; align-items:center;">
                        <span class="hub-card-title">1. Sefer: Türkiye</span>
                        <span class="hub-card-badge" id="hub-progress-badge">İl 35/81</span>
                    </div>
                    <div class="hub-card-desc">81 ili keşfet, simge mekanların sırlarını çöz.</div>
                </div>
                <div style="font-size:22px; color:var(--gold-primary);">➔</div>
            </div>

            <!-- CARD 2: DEYİM AVCISI -->
            <div class="hub-card" onclick="App.goToScreen('screen-idiom')">
                <div class="hub-card-icon">🎭</div>
                <div class="hub-card-content">
                    <div class="hub-card-title">Deyim Avcısı</div>
                    <div class="hub-card-desc">Türkçenin saklı deyimlerini tamamla, altın kazan.</div>
                </div>
                <div style="font-size:22px; color:#a855f7;">➔</div>
            </div>

            <!-- CARD 3: GÜNLÜK BULMACA -->
            <div class="hub-card" onclick="App.showDailyModal()">
                <div class="hub-card-icon">📅</div>
                <div class="hub-card-content">
                    <div class="hub-card-title">Günlük Bulmaca</div>
                    <div class="hub-card-desc">Yıldızlı harfleri topla, takvim serini koru.</div>
                </div>
                <div style="font-size:22px; color:#14b8a6;">➔</div>
            </div>
        </div>

        <div style="font-size: 11px; color: #64748b; letter-spacing: 1px;">Sözcük Seferî v1.0 • Türkiye Turu</div>
    </div>

    <!-- SCREEN 2: INTERAKTİF 81 İL HARİTASI -->
    <div id="screen-map" class="screen">
        <div class="top-navbar">
            <button class="btn-3d-outline" onclick="App.goToScreen('screen-hub')">⬅ Menü</button>
            <div class="game-city-label" style="font-size:14px; color:var(--gold-primary);">TÜRKİYE YOLCULUK HARİTASI</div>
            <div class="stat-pill">🪙 <span id="map-coins">250</span></div>
        </div>

        <div id="map-stage-wrapper">
            <div id="map-viewport">
                <svg class="turkey-svg" viewBox="0 0 1100 500" id="turkey-map-svg">
                    <!-- Province Boundaries -->
                    <g id="provinces-layer">
                        {svg_provinces_str}
                    </g>
                    <!-- Animated Travel Route -->
                    <path id="travel-route" d="" />
                    <!-- Gliding Travel Icon (Airplane/Compass) -->
                    <g id="travel-carrier">
                        <circle cx="0" cy="0" r="10" fill="#f59e0b" stroke="#ffffff" stroke-width="2"/>
                        <polygon points="0,-8 6,6 0,2 -6,6" fill="#0b132b"/>
                    </g>
                    <!-- City Node Pins -->
                    <g id="city-pins-layer"></g>
                </svg>
            </div>
        </div>

        <!-- SLIDING CITY CARD -->
        <div class="map-city-card" id="map-city-card">
            <div class="map-city-header">
                <div class="map-city-plate" id="card-city-plate">35</div>
                <div class="map-city-name" id="card-city-name">İzmir</div>
                <button class="btn-3d-outline" onclick="MapEngine.closeCard()">✕</button>
            </div>
            <div style="font-size:13px; color:#94a3b8;" id="card-city-desc">Ege'nin incisi, Efes Celsus ve Saat Kulesi'nin büyüleyici diyarı.</div>
            <div style="display:flex; gap:10px;">
                <button class="btn-3d" style="flex:1;" onclick="MapEngine.playSelectedCity()">KEŞFE BAŞLA ➔</button>
            </div>
        </div>
    </div>

    <!-- SCREEN 3: GAMEPLAY (CROSSWORD & WHEEL) -->
    <div id="screen-game" class="screen">
        <img src="" id="game-bg-img" class="game-bg-image" alt="Landmark Background" />
        <div class="game-ui-layer">
            <div class="game-header">
                <button class="btn-3d-outline" onclick="App.goToScreen('screen-map')">🗺️ Harita</button>
                <div class="game-title-group">
                    <div class="game-city-label" id="game-city-label">İZMİR (35)</div>
                    <div class="game-landmark-label" id="game-landmark-label">Efes - Celsus Kütüphanesi</div>
                </div>
                <div class="stat-pill">🪙 <span id="game-coins">250</span></div>
            </div>

            <!-- CROSSWORD GRID -->
            <div class="crossword-viewport" id="crossword-viewport">
                <div class="crossword-board" id="crossword-board"></div>
            </div>

            <!-- BOTTOM AREA -->
            <div class="bottom-action-area">
                <div class="word-preview-pill" id="word-preview-pill"></div>

                <div class="wheel-assembly" id="wheel-assembly">
                    <svg class="wheel-svg-layer" id="wheel-svg-layer">
                        <polyline id="wheel-drag-line" fill="none" stroke="#f59e0b" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                    <div id="wheel-letters-container"></div>
                </div>

                <!-- POWERUPS -->
                <div class="powerups-dock">
                    <div class="powerup-btn" onclick="GameEngine.shuffleLetters()" title="Harfleri Karıştır">
                        <span class="powerup-icon">🔀</span>
                        <span class="powerup-price">Bedava</span>
                    </div>
                    <div class="powerup-btn" onclick="GameEngine.useBulb()" title="Rastgele Harf Aç">
                        <span class="powerup-icon">💡</span>
                        <span class="powerup-price">50</span>
                    </div>
                    <div class="powerup-btn" onclick="GameEngine.useTarget()" title="Hedef Harfi Seç">
                        <span class="powerup-icon">🎯</span>
                        <span class="powerup-price">100</span>
                    </div>
                    <div class="powerup-btn" onclick="GameEngine.useBomb()" title="Bomba Patlat">
                        <span class="powerup-icon">💣</span>
                        <span class="powerup-price">150</span>
                    </div>
                    <div class="powerup-btn" style="border-color:#a855f7;" title="Bonus Kelime Sandığı">
                        <span class="powerup-icon">📦</span>
                        <span class="powerup-price" id="bonus-chest-text">0/5</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- SCREEN 4: DEYİM AVCISI -->
    <div id="screen-idiom" class="screen">
        <div class="top-navbar">
            <button class="btn-3d-outline" onclick="App.goToScreen('screen-hub')">⬅ Menü</button>
            <div class="game-city-label" style="color:#c084fc;">DEYİM AVCISI</div>
            <div class="stat-pill">🪙 <span id="idiom-coins">250</span></div>
        </div>

        <div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:16px;">
            <div class="idiom-banner">Eksik Deyim Kelimesini Tamamla</div>
            <div class="idiom-clue-box" id="idiom-clue-box">Göze [...]</div>
            <div class="idiom-board" id="idiom-board"></div>
            <div style="font-size:13px; color:#cbd5e1; max-width:320px; text-align:center;" id="idiom-meaning-box">Sevgi ve güven kazanmak, takdir edilmek.</div>
        </div>

        <div class="bottom-action-area">
            <div class="word-preview-pill" id="idiom-preview-pill" style="background:#6366f1;"></div>
            <div class="wheel-assembly" id="idiom-wheel-assembly" style="border-color:#818cf8;">
                <svg class="wheel-svg-layer">
                    <polyline id="idiom-drag-line" fill="none" stroke="#818cf8" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <div id="idiom-letters-container"></div>
            </div>
        </div>
    </div>

    <!-- MODAL 1: KEŞİF KARTPOSTALI (POSTCARD WIN MODAL) -->
    <div class="modal-backdrop" id="modal-postcard">
        <div class="modal-dialog">
            <div style="font-size:12px; font-weight:800; color:var(--turquoise); letter-spacing:2px;">MÜHÜRLÜ KEŞİF KARTPOSTALI</div>
            <div style="font-size:20px; font-weight:900; color:var(--gold-primary); margin-top:4px;" id="post-landmark-title">Efes - Celsus Kütüphanesi</div>
            
            <div class="postcard-photo-frame">
                <img src="" id="post-photo-img" class="postcard-img" alt="Landmark" />
                <div class="wax-seal">
                    <span>SÖZCÜK<br>SEFERÎ<br>★</span>
                </div>
            </div>

            <div class="postcard-story" id="post-story-text">
                Efes Antik Kenti'nin kalbinde yer alan Celsus Kütüphanesi, dönemin en büyük bilgi hazinelerinden biri olarak kabul edilir.
            </div>

            <div style="display:flex; gap:10px; width:100%;">
                <button class="btn-3d btn-3d-turquoise" style="flex:1; padding:12px;" onclick="App.claim2xReward()">🎥 2X ALTIN</button>
                <button class="btn-3d" style="flex:1; padding:12px;" onclick="App.continueAfterWin()">DEVAM ET ➔</button>
            </div>
        </div>
    </div>

    <!-- MODAL 2: GÜNLÜK BULMACA TAKVİMİ -->
    <div class="modal-backdrop" id="modal-daily">
        <div class="modal-dialog">
            <div style="font-size:24px; font-weight:900; color:var(--gold-primary);">📅 GÜNLÜK BULMACA</div>
            <div style="font-size:13px; color:#94a3b8; margin: 8px 0 16px;">Bugünün tarihi: <strong id="daily-date-str" style="color:var(--text-ivory);">2026-10-05</strong></div>
            
            <div style="display:flex; justify-content:center; gap:8px; margin-bottom:20px;">
                <div style="width:34px; height:34px; background:var(--gold-primary); border-radius:50%; display:flex; align-items:center; justify-content:center; color:#0b132b; font-weight:900;">✓</div>
                <div style="width:34px; height:34px; background:var(--gold-primary); border-radius:50%; display:flex; align-items:center; justify-content:center; color:#0b132b; font-weight:900;">✓</div>
                <div style="width:34px; height:34px; background:var(--gold-primary); border-radius:50%; display:flex; align-items:center; justify-content:center; color:#0b132b; font-weight:900;">✓</div>
                <div style="width:34px; height:34px; background:rgba(255,255,255,0.1); border-radius:50%; display:flex; align-items:center; justify-content:center;">⭐</div>
                <div style="width:34px; height:34px; background:rgba(255,255,255,0.1); border-radius:50%; display:flex; align-items:center; justify-content:center;">⭐</div>
            </div>

            <p style="font-size:13px; color:#cbd5e1; margin-bottom:20px;">Özel yıldızlı kelimeleri çözerek takvim serini artır ve ekstra altın kazan!</p>

            <button class="btn-3d btn-3d-turquoise" style="width:100%;" onclick="App.startDailyChallenge()">GÜNÜN BULMACASINI OYNA</button>
            <button class="btn-3d-outline" style="width:100%; margin-top:10px;" onclick="App.hideModal('modal-daily')">KAPAT</button>
        </div>
    </div>

    <!-- MODAL 3: YETERSİZ ALTIN & REKLAM İP дву -->
    <div class="modal-backdrop" id="modal-insufficient-gold">
        <div class="modal-dialog">
            <div style="font-size:36px; margin-bottom:8px;">🪙</div>
            <div style="font-size:20px; font-weight:900; color:var(--gold-primary);">Yetersiz Altın!</div>
            <p style="font-size:13px; color:#cbd5e1; margin:10px 0 20px;">Bu ipucunu kullanmak için yeterli altının yok. Kısa bir sponsorlu video izleyerek anında +100 Altın kazanabilirsin.</p>
            <button class="btn-3d" style="width:100%;" onclick="App.watchAdForGold()">🎥 VİDEO İZLE (+100 ALTIN)</button>
            <button class="btn-3d-outline" style="width:100%; margin-top:10px;" onclick="App.hideModal('modal-insufficient-gold')">VAZGEÇ</button>
        </div>
    </div>

    <!-- MODAL 4: AYARLAR -->
    <div class="modal-backdrop" id="modal-settings">
        <div class="modal-dialog">
            <div style="font-size:20px; font-weight:900; color:var(--gold-primary); margin-bottom:16px;">OYUN AYARLARI</div>
            
            <div style="width:100%; display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                <span>🔊 Ses Efektleri</span>
                <input type="checkbox" id="setting-sound" checked onchange="AudioEngine.toggleSound(this.checked)" style="transform:scale(1.4);" />
            </div>
            <div style="width:100%; display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
                <span>📳 Haptik Titreşim</span>
                <input type="checkbox" id="setting-vibrate" checked onchange="SaveManager.setHaptic(this.checked)" style="transform:scale(1.4);" />
            </div>

            <button class="btn-3d" style="width:100%;" onclick="App.hideModal('modal-settings')">TAMAM</button>
        </div>
    </div>

    <!-- JAVASCRIPT MOTORU -->
    <script>
        // TÜRKÇE KARAKTER DÖNÜŞÜM YARDIMCISI
        const trUpper = (s) => s ? s.replace(/i/g, 'İ').replace(/ı/g, 'I').toLocaleUpperCase('tr-TR') : '';
        const trLower = (s) => s ? s.replace(/İ/g, 'i').replace(/I/g, 'ı').toLocaleLowerCase('tr-TR') : '';

        // DATASETS
        const CITIES = {cities_json_str};
        const IDIOMS = {idioms_json_str};

        // 1. SAVE MANAGER (LOCALSTORAGE)
        const SaveManager = {{
            KEY: 'sozcukSeferi_v1_save',
            data: {{
                coins: 250,
                currentCityIdx: 0,
                unlockedCityIdx: 0,
                currentSubLevel: 0,
                completedProvinces: [],
                bonusChest: 0,
                soundEnabled: true,
                hapticEnabled: true,
                dailyStreak: 0,
                lastDaily: null
            }},
            load() {{
                try {{
                    const s = localStorage.getItem(this.KEY);
                    if (s) this.data = {{ ...this.data, ...JSON.parse(s) }};
                }} catch (e) {{ console.error(e); }}
            }},
            save() {{
                try {{ localStorage.setItem(this.KEY, JSON.stringify(this.data)); }} catch (e) {{}}
            }},
            addCoins(amount) {{
                this.data.coins += amount;
                this.save();
                App.updateUI();
            }},
            spendCoins(amount) {{
                if (this.data.coins >= amount) {{
                    this.data.coins -= amount;
                    this.save();
                    App.updateUI();
                    return true;
                }}
                App.showModal('modal-insufficient-gold');
                return false;
            }},
            setHaptic(val) {{
                this.data.hapticEnabled = val;
                this.save();
            }}
        }};

        // 2. PROCEDURAL WEB AUDIO SYNTHESIZER
        const AudioEngine = {{
            ctx: null,
            enabled: true,
            init() {{
                if (!this.ctx) {{
                    const AudioCtx = window.AudioContext || window.webkitAudioContext;
                    if (AudioCtx) this.ctx = new AudioCtx();
                }}
            }},
            toggleSound(val) {{
                this.enabled = val;
                SaveManager.data.soundEnabled = val;
                SaveManager.save();
            }},
            playTone(freq, type='sine', duration=0.2, vol=0.2) {{
                if (!this.enabled) return;
                this.init();
                if (!this.ctx) return;
                try {{
                    const osc = this.ctx.createOscillator();
                    const gain = this.ctx.createGain();
                    osc.type = type;
                    osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
                    gain.gain.setValueAtTime(vol, this.ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
                    osc.connect(gain);
                    gain.connect(this.ctx.destination);
                    osc.start();
                    osc.stop(this.ctx.currentTime + duration);
                }} catch (e) {{}}
            }},
            playLetter(idx) {{
                const scale = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25];
                this.playTone(scale[idx % scale.length], 'sine', 0.18, 0.22);
                if (SaveManager.data.hapticEnabled && navigator.vibrate) navigator.vibrate(12);
            }},
            playWordCorrect() {{
                // Chime chord
                [523.25, 659.25, 783.99].forEach((f, i) => {{
                    setTimeout(() => this.playTone(f, 'triangle', 0.35, 0.25), i * 60);
                }});
                if (SaveManager.data.hapticEnabled && navigator.vibrate) navigator.vibrate([25, 40, 30]);
            }},
            playWrong() {{
                this.playTone(140, 'sawtooth', 0.28, 0.25);
                if (SaveManager.data.hapticEnabled && navigator.vibrate) navigator.vibrate(80);
            }},
            playVictory() {{
                const notes = [523.25, 659.25, 783.99, 1046.50];
                notes.forEach((f, i) => {{
                    setTimeout(() => this.playTone(f, 'sine', 0.4, 0.25), i * 140);
                }});
            }}
        }};

        // 3. INTERACTIVE 81-PROVINCE MAP ENGINE
        const MapEngine = {{
            selectedCityIdx: 0,
            init() {{
                this.renderPins();
                this.highlightProvinces();
                this.bindEvents();
            }},
            renderPins() {{
                const pinsLayer = document.getElementById('city-pins-layer');
                let html = '';
                CITIES.forEach((c, idx) => {{
                    const isUnlocked = idx <= SaveManager.data.unlockedCityIdx;
                    const isCurrent = idx === SaveManager.data.currentCityIdx;
                    const r = isCurrent ? 10 : (isUnlocked ? 7 : 4);
                    
                    html += `<g class="city-pin-node ${{isCurrent ? 'current' : ''}}" data-idx="${{idx}}" onclick="MapEngine.selectCity(${{idx}})" transform="translate(${{c.cx}}, ${{c.cy}})">
                        <circle class="city-pin-circle" r="${{r}}" />
                        <text class="city-pin-text" y="0">${{c.plate < 10 ? '0' + c.plate : c.plate}}</text>
                        ${{isUnlocked ? `<text class="city-label-text" y="-12">${{c.name}}</text>` : ''}}
                    </g>`;
                }});
                pinsLayer.innerHTML = html;
            }},
            highlightProvinces() {{
                document.querySelectorAll('.province-path').forEach(el => {{
                    const plate = parseInt(el.dataset.plate);
                    const cityIdx = CITIES.findIndex(c => c.plate === plate);
                    el.classList.remove('active-city', 'completed');
                    if (cityIdx === SaveManager.data.currentCityIdx) {{
                        el.classList.add('active-city');
                    }} else if (cityIdx < SaveManager.data.unlockedCityIdx) {{
                        el.classList.add('completed');
                    }}
                }});
            }},
            bindEvents() {{
                document.querySelectorAll('.province-path').forEach(el => {{
                    el.addEventListener('click', (e) => {{
                        const plate = parseInt(el.dataset.plate);
                        const cityIdx = CITIES.findIndex(c => c.plate === plate);
                        if (cityIdx !== -1) MapEngine.selectCity(cityIdx);
                    }});
                }});
            }},
            selectCity(idx) {{
                this.selectedCityIdx = idx;
                const city = CITIES[idx];
                
                // Show sliding card
                document.getElementById('card-city-plate').innerText = city.plate < 10 ? '0' + city.plate : city.plate;
                document.getElementById('card-city-name').innerText = city.name;
                const landmarkCount = city.landmarks ? city.landmarks.length : 1;
                document.getElementById('card-city-desc').innerText = `${{city.name}} ilinde keşfedilecek ${{landmarkCount}} simgesel mekan bulunuyor.`;
                document.getElementById('map-city-card').classList.add('active');

                // Animate Route & Pan/Zoom Camera
                this.panCameraTo(city.cx, city.cy, 2.2);
            }},
            panCameraTo(cx, cy, scale) {{
                const viewport = document.getElementById('map-viewport');
                const stage = document.getElementById('map-stage-wrapper');
                const vpW = stage.clientWidth;
                const vpH = stage.clientHeight;
                
                const tx = (vpW / 2) - (cx * scale);
                const ty = (vpH / 2) - (cy * scale);
                viewport.style.transform = `translate3d(${{tx}}px, ${{ty}}px, 0) scale(${{scale}})`;
            }},
            closeCard() {{
                document.getElementById('map-city-card').classList.remove('active');
            }},
            playSelectedCity() {{
                SaveManager.data.currentCityIdx = this.selectedCityIdx;
                SaveManager.data.currentSubLevel = 0;
                SaveManager.save();
                this.closeCard();
                App.goToScreen('screen-game');
            }},
            animateTravel(fromIdx, toIdx, callback) {{
                const fromCity = CITIES[fromIdx];
                const toCity = CITIES[toIdx];
                const route = document.getElementById('travel-route');
                const carrier = document.getElementById('travel-carrier');

                // Draw quadratic bezier curved route
                const midX = (fromCity.cx + toCity.cx) / 2;
                const midY = Math.min(fromCity.cy, toCity.cy) - 30;
                const d = `M ${{fromCity.cx}} ${{fromCity.cy}} Q ${{midX}} ${{midY}} ${{toCity.cx}} ${{toCity.cy}}`;
                route.setAttribute('d', d);
                route.style.opacity = '1';
                carrier.style.opacity = '1';

                // Glide carrier along route over 1.2s
                const totalLen = route.getTotalLength();
                let start = null;
                const duration = 1200;

                function step(ts) {{
                    if (!start) start = ts;
                    const elapsed = ts - start;
                    const progress = Math.min(elapsed / duration, 1);
                    // EaseInOut
                    const ease = progress < 0.5 ? 2 * progress * progress : -1 + (4 - 2 * progress) * progress;
                    const pt = route.getPointAtLength(ease * totalLen);
                    carrier.setAttribute('transform', `translate(${{pt.x}}, ${{pt.y}})`);

                    if (progress < 1) {{
                        requestAnimationFrame(step);
                    }} else {{
                        setTimeout(() => {{
                            route.style.opacity = '0';
                            carrier.style.opacity = '0';
                            if (callback) callback();
                        }}, 200);
                    }}
                }}
                requestAnimationFrame(step);
            }}
        }};

        // 4. CROSSWORD & GAMEPLAY ENGINE
        const GameEngine = {{
            city: null,
            level: null,
            gridCells: [],
            words: [],
            foundWords: new Set(),
            letters: [],
            selectedIndices: [],
            isDragging: false,
            targetModeActive: false,

            loadLevel() {{
                const cityIdx = SaveManager.data.currentCityIdx;
                const subIdx = SaveManager.data.currentSubLevel;
                this.city = CITIES[cityIdx];
                this.level = this.city.levels[subIdx % this.city.levels.length];
                
                document.getElementById('game-city-label').innerText = `${{trUpper(this.city.name)}} (${{this.city.plate < 10 ? '0' + this.city.plate : this.city.plate}})`;
                document.getElementById('game-landmark-label').innerText = this.level.landmark || this.city.name;
                document.getElementById('game-bg-img').src = this.level.bg || '';

                this.foundWords.clear();
                this.words = this.level.words;
                this.letters = [...this.level.letters];
                
                this.buildCrossword();
                this.shuffleLetters();
            }},

            buildCrossword() {{
                const board = document.getElementById('crossword-board');
                board.innerHTML = '';
                if (!this.words || this.words.length === 0) return;

                let minR = Math.min(...this.words.map(w => w.row));
                let maxR = Math.max(...this.words.map(w => w.dir === 'V' ? w.row + w.word.length - 1 : w.row));
                let minC = Math.min(...this.words.map(w => w.col));
                let maxC = Math.max(...this.words.map(w => w.dir === 'H' ? w.col + w.word.length - 1 : w.col));

                const rows = maxR - minR + 1;
                const cols = maxC - minC + 1;
                const cellSize = 44, gap = 4;
                const totalW = cols * cellSize + (cols - 1) * gap;
                const totalH = rows * cellSize + (rows - 1) * gap;

                board.style.width = totalW + 'px';
                board.style.height = totalH + 'px';

                // Responsive auto-fit scaling for viewport without overflow
                const viewport = document.getElementById('crossword-viewport');
                const maxW = viewport.clientWidth - 32;
                const maxH = viewport.clientHeight - 32;
                const scale = Math.min(1, maxW / totalW, maxH / totalH);
                board.style.transform = `scale(${{scale}})`;

                this.gridCells = [];
                this.words.forEach(w => {{
                    for (let i = 0; i < w.word.length; i++) {{
                        const r = w.row - minR + (w.dir === 'V' ? i : 0);
                        const c = w.col - minC + (w.dir === 'H' ? i : 0);
                        const id = `cell-${{r}}-${{c}}`;

                        if (!document.getElementById(id)) {{
                            const div = document.createElement('div');
                            div.className = 'grid-cell';
                            div.id = id;
                            div.style.top = (r * (cellSize + gap)) + 'px';
                            div.style.left = (c * (cellSize + gap)) + 'px';
                            div.dataset.char = w.word[i];
                            div.dataset.r = r;
                            div.dataset.c = c;
                            div.onclick = () => this.handleCellClick(div);
                            board.appendChild(div);
                            this.gridCells.push({{ id, r, c, char: w.word[i], solved: false, el: div }});
                        }}
                    }}
                }});
            }},

            shuffleLetters() {{
                for (let i = this.letters.length - 1; i > 0; i--) {{
                    const j = Math.floor(Math.random() * (i + 1));
                    [this.letters[i], this.letters[j]] = [this.letters[j], this.letters[i]];
                }}
                this.drawWheel();
            }},

            drawWheel() {{
                const container = document.getElementById('wheel-letters-container');
                container.innerHTML = '';
                const radius = 95;
                const cx = 135, cy = 135;
                const step = (2 * Math.PI) / this.letters.length;

                this.letters.forEach((char, i) => {{
                    const angle = i * step - Math.PI / 2;
                    const x = cx + radius * Math.cos(angle);
                    const y = cy + radius * Math.sin(angle);

                    const node = document.createElement('div');
                    node.className = 'letter-node';
                    node.style.left = x + 'px';
                    node.style.top = y + 'px';
                    node.innerText = char;
                    node.dataset.idx = i;
                    node.dataset.x = x;
                    node.dataset.y = y;
                    container.appendChild(node);
                }});
                this.updateDragLine(null);
            }},

            handleDown(e) {{
                if (e.target.classList.contains('letter-node')) {{
                    this.isDragging = true;
                    this.selectedIndices = [e.target.dataset.idx];
                    e.target.classList.add('selected');
                    this.updateDragLine(e);
                    this.updatePreview();
                    AudioEngine.playLetter(this.selectedIndices.length - 1);
                }}
            }},

            handleMove(e) {{
                if (!this.isDragging) return;
                let clientX = e.touches ? e.touches[0].clientX : e.clientX;
                let clientY = e.touches ? e.touches[0].clientY : e.clientY;

                const el = document.elementFromPoint(clientX, clientY);
                if (el && el.classList.contains('letter-node')) {{
                    const idx = el.dataset.idx;
                    if (!this.selectedIndices.includes(idx)) {{
                        this.selectedIndices.push(idx);
                        el.classList.add('selected');
                        this.updatePreview();
                        AudioEngine.playLetter(this.selectedIndices.length - 1);
                    }} else if (this.selectedIndices.length > 1 && this.selectedIndices[this.selectedIndices.length - 2] === idx) {{
                        const popped = this.selectedIndices.pop();
                        document.querySelector(`.letter-node[data-idx="${{popped}}"]`).classList.remove('selected');
                        this.updatePreview();
                    }}
                }}
                this.updateDragLine({{ clientX, clientY }});
            }},

            handleUp(e) {{
                if (!this.isDragging) return;
                this.isDragging = false;
                const word = this.selectedIndices.map(i => this.letters[i]).join('');
                this.validateWord(word);

                this.selectedIndices = [];
                document.querySelectorAll('.letter-node').forEach(n => n.classList.remove('selected'));
                this.updateDragLine(null);
                this.updatePreview();
            }},

            updateDragLine(e) {{
                const poly = document.getElementById('wheel-drag-line');
                if (this.selectedIndices.length === 0) {{
                    poly.setAttribute('points', '');
                    return;
                }}
                let pts = [];
                this.selectedIndices.forEach(idx => {{
                    const el = document.querySelector(`.letter-node[data-idx="${{idx}}"]`);
                    pts.push(`${{el.dataset.x}},${{el.dataset.y}}`);
                }});
                if (e) {{
                    const rect = document.getElementById('wheel-assembly').getBoundingClientRect();
                    const x = (e.clientX !== undefined ? e.clientX : e.touches[0].clientX) - rect.left;
                    const y = (e.clientY !== undefined ? e.clientY : e.touches[0].clientY) - rect.top;
                    pts.push(`${{x}},${{y}}`);
                }}
                poly.setAttribute('points', pts.join(' '));
            }},

            updatePreview() {{
                const pill = document.getElementById('word-preview-pill');
                if (this.selectedIndices.length > 0) {{
                    pill.innerText = this.selectedIndices.map(i => this.letters[i]).join('');
                    pill.classList.add('active');
                    pill.style.background = 'rgba(13, 148, 136, 0.95)';
                }} else {{
                    pill.classList.remove('active');
                }}
            }},

            validateWord(word) {{
                if (!word || word.length < 2) return;
                let matched = false;

                this.words.forEach(w => {{
                    if (w.word === word) {{
                        if (!this.foundWords.has(word)) {{
                            this.foundWords.add(word);
                            matched = true;
                            AudioEngine.playWordCorrect();
                            this.revealWord(w);
                        }}
                    }}
                }});

                if (!matched) {{
                    AudioEngine.playWrong();
                    const pill = document.getElementById('word-preview-pill');
                    pill.style.background = 'rgba(220, 38, 38, 0.95)';
                    pill.classList.add('active');
                    setTimeout(() => pill.classList.remove('active'), 500);

                    // Add to bonus chest
                    SaveManager.data.bonusChest = (SaveManager.data.bonusChest || 0) + 1;
                    if (SaveManager.data.bonusChest >= 5) {{
                        SaveManager.data.bonusChest = 0;
                        SaveManager.addCoins(30);
                        AudioEngine.playVictory();
                    }}
                    SaveManager.save();
                    document.getElementById('bonus-chest-text').innerText = `${{SaveManager.data.bonusChest}}/5`;
                }}
            }},

            revealWord(w) {{
                let minR = Math.min(...this.words.map(ww => ww.row));
                let minC = Math.min(...this.words.map(ww => ww.col));

                for (let i = 0; i < w.word.length; i++) {{
                    const r = w.row - minR + (w.dir === 'V' ? i : 0);
                    const c = w.col - minC + (w.dir === 'H' ? i : 0);
                    const cell = this.gridCells.find(gc => gc.r === r && gc.c === c);
                    if (cell && !cell.solved) {{
                        cell.solved = true;
                        setTimeout(() => {{
                            cell.el.innerText = cell.char;
                            cell.el.classList.add('solved');
                        }}, i * 80);
                    }}
                }}
                setTimeout(() => this.checkWinCondition(), w.word.length * 80 + 350);
            }},

            checkWinCondition() {{
                if (this.foundWords.size === this.words.length) {{
                    AudioEngine.playVictory();
                    SaveManager.addCoins(20);
                    
                    // Show Postcard
                    const pc = this.level.postcard || {{
                        landmark: this.level.landmark || this.city.name,
                        desc: `${{this.city.name}} ilimizin eşsiz güzelliklerini başarıyla keşfettin!`,
                        bg: this.level.bg
                    }};
                    document.getElementById('post-landmark-title').innerText = pc.landmark;
                    document.getElementById('post-story-text').innerText = pc.desc;
                    document.getElementById('post-photo-img').src = pc.bg || '';
                    App.showModal('modal-postcard');
                }}
            }},

            // POWERUPS
            useBulb() {{
                if (SaveManager.spendCoins(50)) {{
                    const unsolved = this.gridCells.filter(c => !c.solved);
                    if (unsolved.length > 0) {{
                        const target = unsolved[Math.floor(Math.random() * unsolved.length)];
                        target.solved = true;
                        target.el.innerText = target.char;
                        target.el.classList.add('solved');
                        AudioEngine.playWordCorrect();
                        this.checkWinCondition();
                    }}
                }}
            }},

            useTarget() {{
                if (this.targetModeActive) return;
                if (SaveManager.spendCoins(100)) {{
                    this.targetModeActive = true;
                    this.gridCells.filter(c => !c.solved).forEach(c => c.el.classList.add('target-mode'));
                }}
            }},

            handleCellClick(el) {{
                if (!this.targetModeActive) return;
                const cell = this.gridCells.find(c => c.el === el);
                if (cell && !cell.solved) {{
                    cell.solved = true;
                    cell.el.innerText = cell.char;
                    cell.el.classList.add('solved');
                    this.targetModeActive = false;
                    this.gridCells.forEach(c => c.el.classList.remove('target-mode'));
                    AudioEngine.playWordCorrect();
                    this.checkWinCondition();
                }}
            }},

            useBomb() {{
                if (SaveManager.spendCoins(150)) {{
                    const unsolved = this.gridCells.filter(c => !c.solved);
                    const count = Math.min(3, unsolved.length);
                    for (let i = 0; i < count; i++) {{
                        const target = unsolved[i];
                        target.solved = true;
                        setTimeout(() => {{
                            target.el.innerText = target.char;
                            target.el.classList.add('solved');
                        }}, i * 100);
                    }}
                    AudioEngine.playVictory();
                    setTimeout(() => this.checkWinCondition(), count * 100 + 300);
                }}
            }}
        }};

        // 5. DEYİM AVCISI MINI-MODE
        const IdiomEngine = {{
            currentIdx: 0,
            idiom: null,
            letters: [],
            selectedIndices: [],
            isDragging: false,

            init() {{
                this.currentIdx = Math.floor(Math.random() * IDIOMS.length);
                this.loadIdiom();
                this.bindEvents();
            }},
            loadIdiom() {{
                this.idiom = IDIOMS[this.currentIdx];
                document.getElementById('idiom-clue-box').innerText = this.idiom.clue;
                document.getElementById('idiom-meaning-box').innerText = this.idiom.meaning;

                const board = document.getElementById('idiom-board');
                board.innerHTML = '';
                for (let i = 0; i < this.idiom.answer.length; i++) {{
                    const cell = document.createElement('div');
                    cell.className = 'grid-cell';
                    cell.style.position = 'relative';
                    cell.id = `id-cell-${{i}}`;
                    board.appendChild(cell);
                }}

                this.letters = this.idiom.answer.split('');
                for (let i = this.letters.length - 1; i > 0; i--) {{
                    const j = Math.floor(Math.random() * (i + 1));
                    [this.letters[i], this.letters[j]] = [this.letters[j], this.letters[i]];
                }}
                this.drawWheel();
            }},
            drawWheel() {{
                const container = document.getElementById('idiom-letters-container');
                container.innerHTML = '';
                const radius = 95, cx = 135, cy = 135;
                const step = (2 * Math.PI) / this.letters.length;

                this.letters.forEach((char, i) => {{
                    const angle = i * step - Math.PI / 2;
                    const x = cx + radius * Math.cos(angle);
                    const y = cy + radius * Math.sin(angle);

                    const node = document.createElement('div');
                    node.className = 'letter-node';
                    node.style.left = x + 'px';
                    node.style.top = y + 'px';
                    node.innerText = char;
                    node.dataset.idx = i;
                    node.dataset.x = x;
                    node.dataset.y = y;
                    container.appendChild(node);
                }});
            }},
            bindEvents() {{
                const wheel = document.getElementById('idiom-wheel-assembly');
                wheel.addEventListener('pointerdown', (e) => {{
                    if (e.target.classList.contains('letter-node')) {{
                        this.isDragging = true;
                        this.selectedIndices = [e.target.dataset.idx];
                        e.target.classList.add('selected');
                        this.updatePreview();
                        AudioEngine.playLetter(0);
                    }}
                }});
                window.addEventListener('pointermove', (e) => {{
                    if (!this.isDragging) return;
                    const el = document.elementFromPoint(e.clientX, e.clientY);
                    if (el && el.classList.contains('letter-node') && el.closest('#idiom-wheel-assembly')) {{
                        const idx = el.dataset.idx;
                        if (!this.selectedIndices.includes(idx)) {{
                            this.selectedIndices.push(idx);
                            el.classList.add('selected');
                            this.updatePreview();
                            AudioEngine.playLetter(this.selectedIndices.length - 1);
                        }}
                    }}
                }});
                window.addEventListener('pointerup', () => {{
                    if (!this.isDragging) return;
                    this.isDragging = false;
                    const word = this.selectedIndices.map(i => this.letters[i]).join('');
                    if (word === this.idiom.answer) {{
                        AudioEngine.playVictory();
                        SaveManager.addCoins(50);
                        for (let i = 0; i < word.length; i++) {{
                            const c = document.getElementById(`id-cell-${{i}}`);
                            c.innerText = word[i];
                            c.classList.add('solved');
                        }}
                        setTimeout(() => {{
                            this.currentIdx = (this.currentIdx + 1) % IDIOMS.length;
                            this.loadIdiom();
                        }}, 1500);
                    }} else {{
                        AudioEngine.playWrong();
                    }}
                    this.selectedIndices = [];
                    document.querySelectorAll('#idiom-wheel-assembly .letter-node').forEach(n => n.classList.remove('selected'));
                    this.updatePreview();
                }});
            }},
            updatePreview() {{
                const pill = document.getElementById('idiom-preview-pill');
                if (this.selectedIndices.length > 0) {{
                    pill.innerText = this.selectedIndices.map(i => this.letters[i]).join('');
                    pill.classList.add('active');
                }} else {{
                    pill.classList.remove('active');
                }}
            }}
        }};

        // 6. MAIN APPLICATION STATE MACHINE
        const App = {{
            init() {{
                SaveManager.load();
                this.updateUI();
                MapEngine.init();

                // Pointer Events for gameplay wheel
                const wheel = document.getElementById('wheel-assembly');
                wheel.addEventListener('pointerdown', (e) => GameEngine.handleDown(e));
                window.addEventListener('pointermove', (e) => GameEngine.handleMove(e));
                window.addEventListener('pointerup', (e) => GameEngine.handleUp(e));

                this.goToScreen('screen-hub');
            }},

            updateUI() {{
                const coins = SaveManager.data.coins;
                ['hub-coins', 'map-coins', 'game-coins', 'idiom-coins'].forEach(id => {{
                    const el = document.getElementById(id);
                    if (el) el.innerText = coins;
                }});
                const curCity = CITIES[SaveManager.data.unlockedCityIdx];
                if (curCity) {{
                    document.getElementById('hub-progress-badge').innerText = `İl ${{curCity.plate < 10 ? '0' + curCity.plate : curCity.plate}}/81`;
                }}
            }},

            goToScreen(screenId) {{
                document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
                const target = document.getElementById(screenId);
                if (target) target.classList.add('active');

                if (screenId === 'screen-map') {{
                    const curIdx = SaveManager.data.currentCityIdx;
                    const c = CITIES[curIdx];
                    setTimeout(() => MapEngine.panCameraTo(c.cx, c.cy, 2.2), 100);
                    MapEngine.highlightProvinces();
                }} else if (screenId === 'screen-game') {{
                    GameEngine.loadLevel();
                }} else if (screenId === 'screen-idiom') {{
                    IdiomEngine.init();
                }}
            }},

            showModal(id) {{
                const m = document.getElementById(id);
                if (m) m.classList.add('active');
            }},

            hideModal(id) {{
                const m = document.getElementById(id);
                if (m) m.classList.remove('active');
            }},

            showSettings() {{
                this.showModal('modal-settings');
            }},

            showDailyModal() {{
                document.getElementById('daily-date-str').innerText = new Date().toISOString().split('T')[0];
                this.showModal('modal-daily');
            }},

            startDailyChallenge() {{
                this.hideModal('modal-daily');
                this.goToScreen('screen-game');
            }},

            claim2xReward() {{
                this.showRewardedAd('2x');
                this.hideModal('modal-postcard');
                this.advanceLevel();
            }},

            continueAfterWin() {{
                this.hideModal('modal-postcard');
                this.advanceLevel();
            }},

            advanceLevel() {{
                const curCityIdx = SaveManager.data.currentCityIdx;
                const city = CITIES[curCityIdx];
                SaveManager.data.currentSubLevel++;

                if (SaveManager.data.currentSubLevel >= (city.levels ? city.levels.length : 1)) {{
                    // City completed! Advance to next province
                    SaveManager.data.currentSubLevel = 0;
                    const nextCityIdx = (curCityIdx + 1) % CITIES.length;
                    
                    if (curCityIdx === SaveManager.data.unlockedCityIdx) {{
                        SaveManager.data.unlockedCityIdx = nextCityIdx;
                    }}
                    
                    this.goToScreen('screen-map');
                    setTimeout(() => {{
                        MapEngine.animateTravel(curCityIdx, nextCityIdx, () => {{
                            SaveManager.data.currentCityIdx = nextCityIdx;
                            SaveManager.save();
                            MapEngine.renderPins();
                            MapEngine.highlightProvinces();
                            MapEngine.selectCity(nextCityIdx);
                        }});
                    }}, 400);

                    // Show interstitial ad every 3 cities
                    if (nextCityIdx % 3 === 0) this.showInterstitialAd();
                }} else {{
                    // Next landmark in same city
                    SaveManager.save();
                    GameEngine.loadLevel();
                }}
            }},

            // MONETIZATION HOOKS (PLAY STORE / CAPACITOR)
            showRewardedAd(type) {{
                console.log('AD HOOK: showRewardedAd', type);
                if (window.Capacitor && window.AdMob) {{
                    // Native rewarded ad call
                }}
                if (type === '2x') {{
                    SaveManager.addCoins(40);
                }} else if (type === 'hint') {{
                    SaveManager.addCoins(100);
                    this.hideModal('modal-insufficient-gold');
                }}
            }},

            watchAdForGold() {{
                this.showRewardedAd('hint');
            }},

            showInterstitialAd() {{
                console.log('AD HOOK: showInterstitialAd');
                if (window.Capacitor && window.AdMob) {{
                    // Native interstitial call
                }}
            }}
        }};

        window.onload = () => App.init();
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT)

print("index.html compiled successfully.")

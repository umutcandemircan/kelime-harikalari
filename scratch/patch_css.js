const fs = require('fs');
let text = fs.readFileSync('src/css/main.css', 'utf8');
const replacement = `#map-stage-wrapper {
            flex: 1;
            width: 100%;
            height: 100%;
            position: relative;
            background: radial-gradient(circle at center, rgba(28,37,65,0) 40%, rgba(11,19,43,0.9) 100%);
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            touch-action: none;
            user-select: none;
            cursor: grab;
        }

        #map-stage-wrapper::before {
            content: "☁️ Kilitli Dünya Coğrafyası (İtalya, Mısır)";
            position: absolute;
            bottom: 40px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 11px;
            font-weight: bold;
            color: rgba(148, 163, 184, 0.4);
            letter-spacing: 2px;
            z-index: 1;
            pointer-events: none;
        }`;

text = text.replace(/#map-stage-wrapper\s*\{[\s\S]*?cursor:\s*grab;\s*\}/, replacement);
fs.writeFileSync('src/css/main.css', text);

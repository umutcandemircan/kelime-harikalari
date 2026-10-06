const fs = require('fs');
let css = fs.readFileSync('src/css/main.css', 'utf8');

// Replace .btn-3d-turquoise with deep sea blue
css = css.replace(/\.btn-3d-turquoise/g, '.btn-3d-ocean');
css = css.replace(/background: linear-gradient\(180deg, #0d9488 0%, #0f766e 100%\);/g, 'background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);');
css = css.replace(/box-shadow: 0 4px 0 #115e59, 0 6px 12px rgba\(0, 0, 0, 0\.4\);/g, 'box-shadow: 0 4px 0 #172554, 0 6px 12px rgba(0, 0, 0, 0.4);');
css = css.replace(/box-shadow: 0 1px 0 #115e59, 0 2px 4px rgba\(0, 0, 0, 0\.4\);/g, 'box-shadow: 0 1px 0 #172554, 0 2px 4px rgba(0, 0, 0, 0.4);');

// Enhance .btn-3d for brushed gold/leather look
css = css.replace(/background: linear-gradient\(180deg, #f59e0b 0%, #d97706 100%\);/g, 'background: linear-gradient(180deg, #c28938 0%, #8b5a2b 100%);\n            color: #fdf6e2;\n            border: 1px solid #d4a373;');
css = css.replace(/box-shadow: 0 4px 0 #b45309, 0 6px 12px rgba\(0, 0, 0, 0\.4\);/g, 'box-shadow: 0 4px 0 #5c3a21, 0 6px 12px rgba(0, 0, 0, 0.5);');
css = css.replace(/box-shadow: 0 1px 0 #b45309, 0 2px 4px rgba\(0, 0, 0, 0\.4\);/g, 'box-shadow: 0 1px 0 #5c3a21, 0 2px 4px rgba(0, 0, 0, 0.5);');

// Replace .wax-seal with antique embossed seal
const oldWaxSeal = /\.wax-seal \{[\s\S]*?border: 2px dashed #fca5a5;\s*\}/;
const newWaxSeal = `.wax-seal {
            position: absolute;
            bottom: -15px;
            right: -15px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #a67c00 0%, #bf953f 50%, #b38728 51%, #fbf5b7 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6), inset 0 2px 4px rgba(255, 255, 255, 0.4);
            border: 2px solid #5c3a21;
        }`;

css = css.replace(oldWaxSeal, newWaxSeal);

const oldWaxSealSpan = /\.wax-seal span \{[\s\S]*?line-height: 1\.2;\s*\}/;
const newWaxSealSpan = `.wax-seal span {
            font-size: 8px;
            font-weight: 900;
            color: #5c3a21;
            text-align: center;
            line-height: 1.2;
            text-shadow: 0px 1px 0px rgba(255, 255, 255, 0.5);
            font-family: serif;
        }`;

css = css.replace(oldWaxSealSpan, newWaxSealSpan);

// Change world map mist to include cartography styles
const oldMapStage = /#map-stage-wrapper::before \{[\s\S]*?pointer-events: none;\s*\}/;
const newMapStage = `#map-stage-wrapper::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: 
                linear-gradient(rgba(28,37,65,0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(28,37,65,0.05) 1px, transparent 1px),
                linear-gradient(45deg, rgba(212,163,115,0.03) 1px, transparent 1px),
                linear-gradient(-45deg, rgba(212,163,115,0.03) 1px, transparent 1px);
            background-size: 40px 40px, 40px 40px, 120px 120px, 120px 120px;
            z-index: 0;
            pointer-events: none;
        }
        #map-stage-wrapper::after {
            content: "🧭 DÜNYA ATLASI — 1. SEFER: ANADOLU";
            position: absolute;
            bottom: 20px;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            font-weight: 900;
            font-family: serif;
            color: rgba(212, 163, 115, 0.15);
            letter-spacing: 4px;
            z-index: 0;
            pointer-events: none;
        }`;
css = css.replace(oldMapStage, newMapStage);

fs.writeFileSync('src/css/main.css', css);

let html = fs.readFileSync('src/template.html', 'utf8');
html = html.replace(/btn-3d-turquoise/g, 'btn-3d-ocean');
html = html.replace(/<span>SÖZCÜK<br>SEFERÎ<br>★<\/span>/g, '<span>SÖZCÜK<br>SEFERÎ<\/span>');
html = html.replace(/<span>ZAFER<br>MÜHRÜ<br>✓<\/span>/g, '<span>ZAFER<br>MÜHRÜ<\/span>');
html = html.replace(/<div class="wax-seal" style="background:#10b981;">/g, '<div class="wax-seal">');

fs.writeFileSync('src/template.html', html);

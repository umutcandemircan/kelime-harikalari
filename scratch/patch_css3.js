const fs = require('fs');
let css = fs.readFileSync('src/css/main.css', 'utf8');

const mapFocusCSS = `
        /* Map Focus States */
        #turkey-map-svg.has-focus .province-path {
            opacity: 0.3;
            transition: opacity 0.5s ease, fill 0.3s ease;
        }
        #turkey-map-svg.has-focus .province-path.focused {
            opacity: 1;
            stroke: var(--gold-primary);
            stroke-width: 2.5;
            filter: drop-shadow(0 0 12px rgba(245, 158, 11, 0.4));
        }

        /* Map Zoom States for Pins */
        #turkey-map-svg.zoomed-out .city-pin-node.unlocked {
            opacity: 0;
            pointer-events: none;
            transform: scale(0);
        }
        .city-pin-node {
            transition: opacity 0.4s ease, transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
`;

css += mapFocusCSS;
fs.writeFileSync('src/css/main.css', css);

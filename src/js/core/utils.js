// TÜRKÇE KARAKTER DÖNÜŞÜM YARDIMCISI
const trUpper = (s) => s ? s.replace(/i/g, 'İ').replace(/ı/g, 'I').toLocaleUpperCase('tr-TR') : '';
const trLower = (s) => s ? s.replace(/İ/g, 'i').replace(/I/g, 'ı').toLocaleLowerCase('tr-TR') : '';

// BESPOKE ARTISTIC ANATOLIAN FALLBACK POSTCARD (ZERO BROKEN IMAGES)
function getFallbackLandmarkSVG(landmark, city, plate) {
    const safeLandmark = (landmark || 'Tarihi Mekan').replace(/[<>&"]/g, '');
    const safeCity = (city || 'Türkiye').replace(/[<>&"]/g, '');
    const safePlate = plate ? (plate < 10 ? '0' + plate : plate) : '';
    
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" width="800" height="600">
        <defs>
            <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#0b132b"/>
                <stop offset="60%" stop-color="#16223f"/>
                <stop offset="100%" stop-color="#1c2541"/>
            </linearGradient>
            <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#f59e0b"/>
                <stop offset="50%" stop-color="#fbbf24"/>
                <stop offset="100%" stop-color="#d97706"/>
            </linearGradient>
        </defs>
        <rect width="800" height="600" fill="url(#bgGrad)"/>
        <circle cx="120" cy="80" r="1.5" fill="#f59e0b" opacity="0.6"/>
        <circle cx="280" cy="140" r="1" fill="#ffffff" opacity="0.4"/>
        <circle cx="450" cy="70" r="2" fill="#f59e0b" opacity="0.8"/>
        <circle cx="680" cy="110" r="1.5" fill="#ffffff" opacity="0.5"/>
        <circle cx="730" cy="190" r="1" fill="#f59e0b" opacity="0.6"/>
        <circle cx="90" cy="220" r="1.5" fill="#ffffff" opacity="0.4"/>
        <rect x="24" y="24" width="752" height="552" rx="16" fill="none" stroke="url(#goldGrad)" stroke-width="3" opacity="0.85"/>
        <rect x="36" y="36" width="728" height="528" rx="10" fill="none" stroke="#0d9488" stroke-width="1.5" stroke-dasharray="6,4" opacity="0.6"/>
        <g fill="#f59e0b" opacity="0.22" transform="translate(150, 220)">
            <rect x="20" y="160" width="460" height="15" rx="3"/>
            <rect x="40" y="145" width="420" height="15" rx="2"/>
            <rect x="70" y="45" width="16" height="100" rx="3"/>
            <rect x="130" y="45" width="16" height="100" rx="3"/>
            <rect x="190" y="45" width="16" height="100" rx="3"/>
            <rect x="250" y="45" width="16" height="100" rx="3"/>
            <rect x="310" y="45" width="16" height="100" rx="3"/>
            <rect x="370" y="45" width="16" height="100" rx="3"/>
            <rect x="430" y="45" width="16" height="100" rx="3"/>
            <rect x="50" y="35" width="400" height="12" rx="2"/>
            <polygon points="250,-10 40,35 460,35"/>
            <circle cx="250" cy="18" r="8" fill="#ffffff" opacity="0.6"/>
        </g>
        <g transform="translate(400, 110)">
            <circle cx="0" cy="0" r="32" fill="#0b132b" stroke="url(#goldGrad)" stroke-width="2.5"/>
            <polygon points="0,-24 7,-6 24,0 7,6 0,24 -7,6 -24,0 -7,-6" fill="url(#goldGrad)"/>
            <circle cx="0" cy="0" r="5" fill="#0d9488"/>
        </g>
        <rect x="310" y="165" width="180" height="28" rx="14" fill="#0d9488" opacity="0.3"/>
        <text x="400" y="184" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="900" fill="#f59e0b" letter-spacing="3" text-anchor="middle">${safePlate ? safePlate + ' • ' : ''}${safeCity.toUpperCase()}</text>
        <text x="400" y="430" font-family="Georgia, serif" font-size="32" font-weight="bold" fill="#f8f9fa" text-anchor="middle" letter-spacing="1">${safeLandmark}</text>
        <text x="400" y="465" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#94a3b8" letter-spacing="2" text-anchor="middle">SÖZCÜK SEFERÎ • ANADOLU KÜLTÜR MİRASI</text>
        <g transform="translate(400, 520)">
            <circle cx="0" cy="0" r="18" fill="#f59e0b" opacity="0.15" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="0" y="5" font-family="sans-serif" font-size="14" font-weight="900" fill="#f59e0b" text-anchor="middle">★</text>
        </g>
    </svg>`;
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
}
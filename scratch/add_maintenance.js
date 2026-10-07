const fs = require('fs');

// 1. Update template.html
let htmlPath = 'src/template.html';
let html = fs.readFileSync(htmlPath, 'utf-8');

const maintenanceHtml = `<body>
    <!-- MAINTENANCE OVERLAY -->
    <div id="maintenance-overlay">
        <div class="maintenance-content">
            <h1>SÖZCÜK SEFERÎ</h1>
            <h2>🛠 TEKNİK BAKIM MOLASI</h2>
            <p>Sizlere daha pürüzsüz ve keyifli bir deneyim sunabilmek için oyunumuzu kısa süreliğine bakıma aldık.</p>
            <p>Hata düzeltmeleri ve yepyeni özelliklerle çok yakında geri döneceğiz. Sabrınız için teşekkür ederiz!</p>
            <div class="maintenance-spinner"></div>
        </div>
    </div>
`;

html = html.replace('<body>', maintenanceHtml);
fs.writeFileSync(htmlPath, html, 'utf-8');

// 2. Update main.css
let cssPath = 'src/css/main.css';
let css = fs.readFileSync(cssPath, 'utf-8');

const maintenanceCss = `
/* MAINTENANCE OVERLAY */
#maintenance-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: radial-gradient(circle at center, #1c2541 0%, #0b132b 100%);
    z-index: 999999;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
    text-align: center;
    padding: 20px;
    box-sizing: border-box;
    /* Prevent interaction with background */
    pointer-events: all;
    touch-action: none;
}

.maintenance-content {
    background: rgba(0, 0, 0, 0.6);
    border: 2px solid var(--gold-primary);
    border-radius: 16px;
    padding: 40px 20px;
    max-width: 450px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.9);
    animation: fadeUp 0.5s ease-out;
}

.maintenance-content h1 {
    font-size: 32px;
    color: var(--gold-primary);
    margin-bottom: 15px;
    letter-spacing: 3px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

.maintenance-content h2 {
    font-size: 22px;
    margin-bottom: 25px;
    color: #fca311;
}

.maintenance-content p {
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 15px;
    color: #e5e7eb;
}

.maintenance-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(245, 158, 11, 0.2);
    border-top: 4px solid var(--gold-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 30px auto 0;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
`;

css += maintenanceCss;
fs.writeFileSync(cssPath, css, 'utf-8');

console.log("Maintenance overlay added successfully.");

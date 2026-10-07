const fs = require('fs');

// 1. Update template.html
let htmlPath = 'src/template.html';
let html = fs.readFileSync(htmlPath, 'utf-8');

const oldMaintenanceHtml = `<body>
    <!-- MAINTENANCE OVERLAY -->
    <div id="maintenance-overlay">
        <div class="maintenance-content">
            <h1>SÖZCÜK SEFERÎ</h1>
            <h2>🛠 TEKNİK BAKIM MOLASI</h2>
            <p>Sizlere daha pürüzsüz ve keyifli bir deneyim sunabilmek için oyunumuzu kısa süreliğine bakıma aldık.</p>
            <p>Hata düzeltmeleri ve yepyeni özelliklerle çok yakında geri döneceğiz. Sabrınız için teşekkür ederiz!</p>
            <div class="maintenance-spinner"></div>
        </div>
    </div>`;

const newMaintenanceHtml = `<body>
    <!-- MAINTENANCE OVERLAY -->
    <div id="maintenance-overlay">
        <div class="maintenance-content">
            <h1>SÖZCÜK SEFERÎ</h1>
            <h2>🛠 TEKNİK BAKIM MOLASI</h2>
            <p>Sizlere daha pürüzsüz bir deneyim sunabilmek için oyunu kısa süreliğine bakıma <b>aldım</b>.</p>
            <p>Tek bir geliştirici olarak oyunun tüm hatalarını çözmek ve yeni özellikler eklemek için çalışıyorum. Çok yakında görüşmek üzere, desteğiniz için teşekkür ederim!</p>
            <div class="maintenance-spinner"></div>
        </div>
    </div>`;

html = html.replace(oldMaintenanceHtml, newMaintenanceHtml);
fs.writeFileSync(htmlPath, html, 'utf-8');

console.log("Maintenance text updated successfully.");

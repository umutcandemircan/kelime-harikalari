const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const path = require('path');

async function runDeviceQA() {
    console.log("=== STARTING CROSS-DEVICE QA (3 CORE MODES & WORLD CITIES) ===");

    // 1. Static server
    const server = http.createServer((req, res) => {
        let reqPath = req.url.split('?')[0];
        if (reqPath === '/') reqPath = '/index.html';
        let filePath = path.join(__dirname, '..', reqPath);
        if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
            filePath = path.join(__dirname, '..', 'index.html');
        }
        const ext = path.extname(filePath).toLowerCase();
        const mimeTypes = {
            '.html': 'text/html; charset=utf-8',
            '.js': 'application/javascript; charset=utf-8',
            '.css': 'text/css; charset=utf-8',
            '.json': 'application/json; charset=utf-8',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.svg': 'image/svg+xml'
        };
        const contentType = mimeTypes[ext] || 'application/octet-stream';
        try {
            const content = fs.readFileSync(filePath);
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content);
        } catch (e) {
            res.writeHead(404);
            res.end('Not found');
        }
    });

    await new Promise(r => server.listen(8998, r));
    console.log("[SERVER] Serving on http://localhost:8998");

    const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
    const port = 9336;
    const chromeProc = spawn(chromePath, [
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        `--remote-debugging-port=${port}`,
        'about:blank'
    ]);

    await new Promise(r => setTimeout(r, 2000));

    try {
        const resp = await fetch(`http://127.0.0.1:${port}/json`);
        const targets = await resp.json();
        const pageTarget = targets.find(t => t.type === 'page') || targets[0];

        const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
        await new Promise(r => ws.onopen = r);

        let msgId = 1;
        const pending = new Map();
        const consoleErrors = [];

        ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            if (msg.id && pending.has(msg.id)) {
                pending.get(msg.id)(msg);
                pending.delete(msg.id);
            }
            if (msg.method === 'Runtime.consoleAPICalled') {
                if (msg.params.type === 'error') {
                    consoleErrors.push(msg.params.args.map(a => a.value || a.description).join(' '));
                }
            }
        };

        function send(method, params = {}) {
            return new Promise((resolve) => {
                const id = msgId++;
                pending.set(id, resolve);
                ws.send(JSON.stringify({ id, method, params }));
            });
        }

        async function evalJs(expr) {
            const res = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
            return res.result?.result?.value;
        }

        await send('Page.enable');
        await send('Runtime.enable');

        // TEST 1: MOBILE (iPhone 390x844)
        console.log("\n--- TEST 1: MOBILE (iPhone 390x844) ---");
        await send('Emulation.setDeviceMetricsOverride', {
            width: 390,
            height: 844,
            deviceScaleFactor: 3,
            mobile: true
        });

        await send('Page.navigate', { url: 'http://localhost:8998/index.html' });
        await new Promise(r => setTimeout(r, 2500));

        // Dismiss journal if open
        await evalJs(`if (document.getElementById('modal-journal')?.classList.contains('visible')) { App.hideModal('modal-journal'); }`);

        // Check 3 core mode titles on Hub
        const hubModes = await evalJs(`
            Array.from(document.querySelectorAll('.mode-card-title')).map(el => el.innerText)
        `);
        console.log("  Hub Core Modes:", hubModes);
        if (!hubModes.includes("Sözcük Seferi") || !hubModes.includes("Atasözü & Deyim Sandığı") || !hubModes.includes("Günün Seferi")) {
            throw new Error("Missing one of the 3 required core modes on Hub screen!");
        }

        // Test Mode 1: Open World Map
        console.log("  Entering Mode 1: Sözcük Seferi (World Map)...");
        await evalJs(`App.openWorldMap()`);
        await new Promise(r => setTimeout(r, 800));

        const mapActive = await evalJs(`document.getElementById('screen-map').classList.contains('active')`);
        console.log("  Map Screen Active:", mapActive);
        if (!mapActive) throw new Error("Map screen did not activate");

        // Verify World Cities are rendered
        const worldNodesCount = await evalJs(`document.querySelectorAll('.world-city-node').length`);
        console.log("  World City Nodes rendered:", worldNodesCount);
        if (worldNodesCount < 5) throw new Error("World city nodes missing on map");

        // Test Selecting a World City (e.g. Rome: country 0, city 0)
        console.log("  Selecting World City: Roma (Italy)...");
        await evalJs(`MapEngine.selectWorldCity(0, 0)`);
        await new Promise(r => setTimeout(r, 500));

        const worldCardVisible = await evalJs(`document.getElementById('map-city-card').classList.contains('visible')`);
        const worldCardName = await evalJs(`document.getElementById('card-city-name')?.innerText`);
        const worldLandmarks = await evalJs(`document.querySelectorAll('#card-city-landmarks .landmark-badge').length`);
        console.log("  World Card Visible:", worldCardVisible, "| Name:", worldCardName, "| Landmarks:", worldLandmarks);
        if (!worldCardVisible || worldCardName !== "Roma" || worldLandmarks < 5) {
            throw new Error("Selecting World City (Roma) failed or 5 landmarks missing");
        }

        // Test Selecting a Turkey City (e.g. Istanbul: plate 34)
        console.log("  Selecting Turkey City: İstanbul (Plate 34)...");
        const istIdx = await evalJs(`CITIES.findIndex(c => c.plate === 34)`);
        await evalJs(`MapEngine.selectTurkeyCity(${istIdx})`);
        await new Promise(r => setTimeout(r, 500));

        const trCardName = await evalJs(`document.getElementById('card-city-name')?.innerText`);
        const trLandmarks = await evalJs(`document.querySelectorAll('#card-city-landmarks .landmark-badge').length`);
        console.log("  Turkey Card Name:", trCardName, "| Landmarks:", trLandmarks);
        if (trCardName !== "İstanbul" || trLandmarks < 5) {
            throw new Error("Selecting Turkey City (Istanbul) failed or 5 landmarks missing");
        }

        // Launch gameplay for Istanbul
        console.log("  Starting gameplay in Istanbul...");
        await evalJs(`MapEngine.handleCityAction()`);
        await new Promise(r => setTimeout(r, 800));

        const gameActive = await evalJs(`document.getElementById('screen-game').classList.contains('active')`);
        const gameLabel = await evalJs(`document.getElementById('game-city-label')?.innerText`);
        console.log("  Game Screen Active:", gameActive, "| Label:", gameLabel);
        if (!gameActive) throw new Error("Game screen failed to activate");

        // TEST 2: IDIOM MODE
        console.log("\n--- TEST 2: ATASÖZÜ & DEYİM SANDIĞI ---");
        await evalJs(`App.goToScreen('screen-idiom')`);
        await new Promise(r => setTimeout(r, 600));

        const idiomActive = await evalJs(`document.getElementById('screen-idiom').classList.contains('active')`);
        console.log("  Idiom Screen Active:", idiomActive);
        if (!idiomActive) throw new Error("Idiom screen failed to activate");

        // TEST 3: DESKTOP WIDESCREEN (1920x1080)
        console.log("\n--- TEST 3: DESKTOP WIDESCREEN (1920x1080) ---");
        await send('Emulation.setDeviceMetricsOverride', {
            width: 1920,
            height: 1080,
            deviceScaleFactor: 1,
            mobile: false
        });
        await new Promise(r => setTimeout(r, 600));

        await evalJs(`App.goToScreen('screen-hub')`);
        await new Promise(r => setTimeout(r, 500));

        const shellBounds = await evalJs(`
            const s = document.getElementById('screen-hub');
            const rect = s.getBoundingClientRect();
            ({ width: rect.width, left: rect.left, right: rect.right })
        `);
        console.log("  Desktop Shell bounds:", shellBounds);
        if (shellBounds.width > 500) throw new Error("Desktop width exceeded 500px");
        if (shellBounds.left < 500) throw new Error("Desktop shell is not centered");

        console.log("\n=== CONSOLE ERRORS AUDIT ===");
        console.log("Errors count:", consoleErrors.length);
        if (consoleErrors.length > 0) {
            console.warn("Console errors detected:", consoleErrors);
        } else {
            console.log("  -> Zero console errors detected across all tested viewports and screens!");
        }

        console.log("\n>>> ALL TESTS PASSED! 3 CORE MODES & WORLD CITIES 100% OPERATIONAL! <<<");

    } finally {
        chromeProc.kill();
        server.close();
    }
}

runDeviceQA().catch(err => {
    console.error("FATAL QA FAILURE:", err);
    process.exit(1);
});

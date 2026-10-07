const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const path = require('path');

async function runV2UserJourneyTest() {
    console.log("==================================================");
    console.log("   SÖZCÜK SEFERÎ V2 END-TO-END USER JOURNEY QA    ");
    console.log("==================================================");

    // 1. Static Web Server
    const server = http.createServer((req, res) => {
        let reqPath = req.url.split('?')[0];
        if (reqPath === '/') reqPath = '/index.html';
        let filePath = path.join(__dirname, '..', '..', reqPath);
        if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
            filePath = path.join(__dirname, '..', '..', 'index.html');
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

    const PORT = 8999;
    await new Promise(r => server.listen(PORT, r));
    console.log(`[SERVER] Running at http://localhost:${PORT}`);

    // 2. Launch Headless Chrome
    const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
    const cdpPort = 9338;
    const chromeProc = spawn(chromePath, [
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        `--remote-debugging-port=${cdpPort}`,
        'about:blank'
    ]);

    await new Promise(r => setTimeout(r, 2000));

    try {
        const resp = await fetch(`http://127.0.0.1:${cdpPort}/json`);
        const targets = await resp.json();
        const pageTarget = targets.find(t => t.type === 'page') || targets[0];

        const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
        await new Promise(r => ws.onopen = r);

        let msgId = 1;
        function send(method, params = {}) {
            return new Promise((resolve, reject) => {
                const id = msgId++;
                const handler = (event) => {
                    const data = JSON.parse(event.data);
                    if (data.id === id) {
                        ws.removeEventListener('message', handler);
                        if (data.error) reject(data.error);
                        else resolve(data.result);
                    }
                };
                ws.addEventListener('message', handler);
                ws.send(JSON.stringify({ id, method, params }));
            });
        }

        async function evaluate(expression) {
            const res = await send('Runtime.evaluate', {
                expression,
                returnByValue: true,
                awaitPromise: true
            });
            return res.result ? res.result.value : null;
        }

        // Enable Page & Console
        await send('Page.enable');
        await send('Runtime.enable');

        const consoleErrors = [];
        ws.addEventListener('message', (event) => {
            const data = JSON.parse(event.data);
            if (data.method === 'Runtime.consoleAPICalled' && data.params.type === 'error') {
                consoleErrors.push(data.params.args.map(a => a.value || a.description).join(' '));
            }
        });

        // Test Viewport 1: Mobile 390x844
        await send('Emulation.setDeviceMetricsOverride', {
            width: 390,
            height: 844,
            deviceScaleFactor: 2,
            mobile: true
        });

        console.log(`[TEST] Navigating to http://localhost:${PORT}/index.html...`);
        await send('Page.navigate', { url: `http://localhost:${PORT}/index.html` });
        await new Promise(r => setTimeout(r, 1800));

        // STEP 1: Boot & Version Check
        console.log("\n[STEP 1] Checking Core Boot & Versioning...");
        const appVer = await evaluate(`window.App ? App.APP_VERSION : null`);
        console.log(`  -> App.APP_VERSION: ${appVer}`);
        if (appVer !== '2.0.0') throw new Error(`App version mismatch: expected 2.0.0, got ${appVer}`);

        const schemaVer = await evaluate(`SaveManager ? SaveManager.CURRENT_SCHEMA_VERSION : null`);
        console.log(`  -> SaveManager schema: ${schemaVer}`);
        if (schemaVer !== 4) throw new Error(`Schema version mismatch: expected 4, got ${schemaVer}`);

        // STEP 2: Screen Hub -> 3D Globe
        console.log("\n[STEP 2] Navigating: Hub -> 3D World Globe...");
        await evaluate(`ScreenRouter.goTo('screen-globe')`);
        await new Promise(r => setTimeout(r, 600));
        
        const globeActive = await evaluate(`document.getElementById('screen-globe').classList.contains('active')`);
        const globeCanvasW = await evaluate(`document.getElementById('globe-3d-canvas').width`);
        console.log(`  -> screen-globe active: ${globeActive}, Canvas width: ${globeCanvasW}px`);
        if (!globeActive) throw new Error("screen-globe failed to activate");

        // STEP 3: 3D Globe -> Country Map (Turkey 81 Provinces)
        console.log("\n[STEP 3] Navigating: 3D Globe -> Turkey Country Map...");
        await evaluate(`Globe3D.transitionToPlayableCountry(Globe3D.COUNTRIES[0])`);
        await new Promise(r => setTimeout(r, 900));

        const countryActive = await evaluate(`document.getElementById('screen-country').classList.contains('active')`);
        const provincePathsCount = await evaluate(`document.querySelectorAll('.province-path').length`);
        console.log(`  -> screen-country active: ${countryActive}, Provinces loaded: ${provincePathsCount}/81`);
        if (!countryActive || provincePathsCount !== 81) throw new Error("Turkey country map failed to load 81 provinces");

        // STEP 4: Select City (Istanbul) -> City Exploration (5 Landmarks)
        console.log("\n[STEP 4] Selecting Istanbul -> Opening City Exploration Screen (5 Landmarks)...");
        // Plate 34 is Istanbul (index 33 in 0-indexed CITIES)
        await evaluate(`CountryMap.selectCity(33)`);
        await new Promise(r => setTimeout(r, 400));
        await evaluate(`CityExploration.openCity(33)`);
        await new Promise(r => setTimeout(r, 500));

        const cityActive = await evaluate(`document.getElementById('screen-city').classList.contains('active')`);
        const cityTitle = await evaluate(`document.getElementById('city-explore-title').innerText`);
        const landmarkCardsCount = await evaluate(`document.querySelectorAll('.landmark-card').length`);
        console.log(`  -> screen-city active: ${cityActive}, City: ${cityTitle}, Landmarks rendered: ${landmarkCardsCount}/5`);
        if (!cityActive || landmarkCardsCount !== 5) throw new Error("City exploration failed to render 5 landmark cards");

        // STEP 5: Select Landmark 1 (Ayasofya) -> Game Screen
        console.log("\n[STEP 5] Selecting Landmark 1 -> Crossword Gameplay Screen...");
        await evaluate(`CityExploration.selectLandmark(0)`);
        await new Promise(r => setTimeout(r, 500));

        const gameActive = await evaluate(`document.getElementById('screen-game').classList.contains('active')`);
        const cellsCount = await evaluate(`document.querySelectorAll('.grid-cell').length`);
        const wheelLetters = await evaluate(`GameEngine.letters.join('')`);
        const cityLabel = await evaluate(`document.getElementById('game-city-label').innerText`);
        console.log(`  -> screen-game active: ${gameActive}, Grid cells: ${cellsCount}, Wheel: [${wheelLetters}]`);
        console.log(`  -> Header: ${cityLabel}`);
        if (!gameActive || cellsCount === 0 || !wheelLetters) throw new Error("Gameplay screen failed to build puzzle grid and wheel");

        // STEP 6: Word Validation Service Check
        console.log("\n[STEP 6] Testing Central WordValidator Authority...");
        const valGood = await evaluate(`WordValidator.validateWord("DENİZ")`);
        const valBad = await evaluate(`WordValidator.validateWord("AMK")`);
        console.log(`  -> Valid word 'DENİZ':`, valGood);
        console.log(`  -> Blocked word 'AMK':`, valBad);
        if (!valGood.valid || valBad.valid) throw new Error("WordValidator failed policy or dictionary check");

        // STEP 7: City Completion Ceremony (Grand Finale for Level 25)
        console.log("\n[STEP 7] Simulating City Completion Ceremony (25 Levels Complete)...");
        await evaluate(`
            CityCompletionCeremony.start(CITIES[33], () => {
                ScreenRouter.goTo('screen-country');
            })
        `);
        await new Promise(r => setTimeout(r, 1200));

        const ceremonyModalActive = await evaluate(`document.getElementById('modal-city-ceremony').classList.contains('active')`);
        const stampedSeals = await evaluate(`document.querySelectorAll('.ceremony-seal-slot.stamped').length`);
        console.log(`  -> Ceremony modal active: ${ceremonyModalActive}, Stamped seals: ${stampedSeals}/5`);
        if (!ceremonyModalActive) throw new Error("Ceremony modal failed to activate");

        // Close ceremony and verify province completed in SaveManager
        await evaluate(`document.getElementById('ceremony-continue-btn').click()`);
        await new Promise(r => setTimeout(r, 500));
        const provinceDone = await evaluate(`SaveManager.data.completedProvinces.includes(34)`);
        console.log(`  -> SaveManager recorded Istanbul (plate 34) completed: ${provinceDone}`);
        if (!provinceDone) throw new Error("Province completion not recorded in SaveManager");

        // STEP 8: Feedback / Bug Report Submission
        console.log("\n[STEP 8] Testing Frictionless Bug & Feedback Reporting...");
        await evaluate(`FeedbackModal.open()`);
        await new Promise(r => setTimeout(r, 300));
        await evaluate(`
            document.getElementById('feedback-message-input').value = "Otomatik V2 E2E QA Testi Başarılı!";
            FeedbackModal.submit();
        `);
        await new Promise(r => setTimeout(r, 600));

        const feedbackCount = await evaluate(`SaveManager.data.feedbackHistory.length`);
        console.log(`  -> SaveManager feedback history count: ${feedbackCount}`);
        if (feedbackCount === 0) throw new Error("Feedback submission failed to record");

        // STEP 9: Cross-Device Responsiveness (Tablet 768x1024 & Desktop 1920x1080)
        console.log("\n[STEP 9] Checking Cross-Device Responsive Viewports...");
        // Tablet
        await send('Emulation.setDeviceMetricsOverride', { width: 768, height: 1024, deviceScaleFactor: 2, mobile: true });
        await new Promise(r => setTimeout(r, 400));
        let bodyW = await evaluate(`document.body.clientWidth`);
        console.log(`  -> Tablet (768x1024): body width = ${bodyW}px`);

        // Desktop / Smartboard
        await send('Emulation.setDeviceMetricsOverride', { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false });
        await new Promise(r => setTimeout(r, 400));
        bodyW = await evaluate(`document.body.clientWidth`);
        console.log(`  -> Desktop / Smartboard (1920x1080): body width = ${bodyW}px`);

        // Check console errors
        console.log("\n[STEP 10] Checking Console Errors...");
        const fatalErrors = consoleErrors.filter(e => !e.includes('favicon'));
        if (fatalErrors.length > 0) {
            console.warn("Console Errors found:", fatalErrors);
            throw new Error(`Fatal console errors encountered: ${fatalErrors.join(', ')}`);
        } else {
            console.log("  -> 0 Console Errors detected!");
        }

        console.log("\n==================================================");
        console.log("   V2 END-TO-END USER JOURNEY QA: 100% PASSED!   ");
        console.log("==================================================");

        ws.close();
    } finally {
        chromeProc.kill();
        server.close();
    }
}

runV2UserJourneyTest().catch(err => {
    console.error("E2E QA TEST FAILED:", err);
    process.exit(1);
});

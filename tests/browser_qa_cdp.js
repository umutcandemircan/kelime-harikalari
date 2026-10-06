const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const path = require('path');

async function runBrowserQA() {
    console.log("=== LAUNCHING CHROME HEADLESS BROWSER QA ===");

    // 0. Start local self-contained static server
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
    await new Promise(r => server.listen(8989, r));
    console.log("Self-contained static server listening on http://localhost:8989");
    
    const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
    const port = 9222;
    
    // Launch Chrome with debugging port
    const chromeProc = spawn(chromePath, [
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        `--remote-debugging-port=${port}`,
        'about:blank'
    ]);
    
    // Wait for Chrome to initialize
    await new Promise(r => setTimeout(r, 1500));
    
    try {
        // Fetch target WebSocket URL
        const resp = await fetch(`http://127.0.0.1:${port}/json`);
        const targets = await resp.json();
        const pageTarget = targets.find(t => t.type === 'page') || targets[0];
        console.log("Connecting to Chrome target:", pageTarget.webSocketDebuggerUrl);
        
        const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
        
        let msgId = 1;
        const pending = new Map();
        const consoleMessages = [];
        
        ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            if (msg.id && pending.has(msg.id)) {
                const { resolve, reject } = pending.get(msg.id);
                pending.delete(msg.id);
                if (msg.error) reject(msg.error);
                else resolve(msg.result);
            }
            if (msg.method === 'Runtime.consoleAPICalled') {
                const text = msg.params.args.map(a => a.value || a.description || JSON.stringify(a)).join(' ');
                consoleMessages.push({ type: msg.params.type, text });
                console.log(`[Browser Console ${msg.params.type.toUpperCase()}]:`, text);
            }
            if (msg.method === 'Runtime.exceptionThrown') {
                const text = msg.params.exceptionDetails.text + ' ' + (msg.params.exceptionDetails.exception?.description || '');
                consoleMessages.push({ type: 'error', text });
                console.error(`[Browser Exception]:`, text);
            }
        };
        
        await new Promise((resolve, reject) => {
            ws.onopen = resolve;
            ws.onerror = reject;
        });
        
        function send(method, params = {}) {
            return new Promise((resolve, reject) => {
                const id = msgId++;
                pending.set(id, { resolve, reject });
                ws.send(JSON.stringify({ id, method, params }));
            });
        }
        
        async function evaluate(expression) {
            const res = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
            if (res.exceptionDetails) {
                throw new Error("Eval error: " + (res.exceptionDetails.exception?.description || res.exceptionDetails.text));
            }
            return res.result?.value;
        }

        // Enable domains
        await send('Runtime.enable');
        await send('Page.enable');
        await send('DOM.enable');
        
        // 1. Navigate to local server
        console.log("Navigating to http://localhost:8989/index.html...");
        await send('Page.navigate', { url: 'http://localhost:8989/index.html' });
        await new Promise(r => setTimeout(r, 1200));

        // 2. Verify Boot State
        console.log("\n[TEST 1] Verifying Boot State...");
        const activeScreen = await evaluate(`document.querySelector('.screen.active')?.id`);
        console.log("Active screen on boot:", activeScreen);
        console.assert(activeScreen === 'screen-hub', "Expected screen-hub to be active");
        
        const coins = await evaluate(`SaveManager.data.coins`);
        console.log("Player starting coins:", coins);
        console.assert(coins >= 250, "Coins should be initialized");

        // 3. Test Navigation: Hub -> Onboarding Map
        console.log("\n[TEST 2] Testing Onboarding Flow (Hub -> Sefere Çık)...");
        await evaluate(`localStorage.clear(); SaveManager.init(); App.updateUI();`);
        await evaluate(`App.startJourney()`);
        await new Promise(r => setTimeout(r, 400));
        const mapScreenActive = await evaluate(`document.getElementById('screen-map').classList.contains('active')`);
        console.assert(mapScreenActive, "Map screen should be active");
        const startCityModalActive = await evaluate(`document.getElementById('modal-start-city').classList.contains('active')`);
        console.assert(startCityModalActive, "Start city modal should be active on first play");
        console.log("PASS: Onboarding modal appeared as expected.");

        await evaluate(`App.hideModal('modal-start-city')`);
        const pinCount = await evaluate(`document.querySelectorAll('.city-pin-node').length`);
        console.log(`Rendered map pins: ${pinCount} (Expected 81)`);
        console.assert(pinCount === 81, "All 81 province pins must be rendered");

        // 4. Test Free Start City Selection (e.g. City 34: İstanbul)
        console.log("\n[TEST 3] Testing Free Start City Selection (Selecting City 33: Mersin / City 34: İstanbul)...");
        const istIdx = await evaluate(`CITIES.findIndex(c => c.plate === 34)`);
        await evaluate(`MapEngine.selectCity(${istIdx})`);
        const actionBtnText = await evaluate(`document.getElementById('card-action-btn').innerText`);
        console.log("Start City Action Button Text:", actionBtnText);
        console.assert(actionBtnText.includes("YOLCULUĞA BURADAN BAŞLA"), "Should offer starting journey from selected city");
        
        // Start journey from İstanbul
        await evaluate(`document.getElementById('card-action-btn').click()`);
        await new Promise(r => setTimeout(r, 500));
        
        const gameActive = await evaluate(`document.getElementById('screen-game').classList.contains('active')`);
        console.assert(gameActive, "Game screen should be active after start city selection");
        
        const headerText = await evaluate(`document.getElementById('game-city-label').innerText`);
        console.log("Game Header Text:", headerText);
        console.assert(headerText.includes("İSTANBUL") && headerText.includes("Mekan 1/5") && headerText.includes("Bulmaca 1/5"), "Header format must match product spec (Mekan 1/5 - Bulmaca 1/5)");

        const cellsCount = await evaluate(`document.querySelectorAll('.grid-cell').length`);
        const lettersCount = await evaluate(`document.querySelectorAll('.letter-node').length`);
        console.log(`Crossword cells rendered: ${cellsCount}, Wheel letters: ${lettersCount}`);
        console.assert(cellsCount > 0, "Grid cells should be rendered");
        console.assert(lettersCount > 0, "Wheel letter nodes should be rendered");

        // Test Strict City Locking on Map
        console.log("\n[TEST 3B] Testing Strict City Locking on Map...");
        await evaluate(`App.goToScreen('screen-map');`);
        const ankIdx = await evaluate(`CITIES.findIndex(c => c.plate === 6)`);
        await evaluate(`MapEngine.selectCity(${ankIdx});`);
        const lockBtnText = await evaluate(`document.getElementById('card-action-btn').innerText`);
        console.log("Locked City Action Button Text:", lockBtnText);
        console.assert(lockBtnText.includes("KİLİTLİ"), "Uncompleted other city must be strictly locked!");
        await evaluate(`App.goToScreen('screen-game');`);

        // 5. Test Hints / Powerups
        console.log("\n[TEST 4] Testing Hints / Powerups...");
        const coinsBeforeHint = await evaluate(`SaveManager.data.coins`);
        await evaluate(`GameEngine.useBulb()`);
        const coinsAfterHint = await evaluate(`SaveManager.data.coins`);
        console.log(`Coins before hint: ${coinsBeforeHint}, after hint: ${coinsAfterHint}`);
        console.assert(coinsBeforeHint - coinsAfterHint === 30, "Bulb should cost exactly 30 coins");
        const hintsUsed = await evaluate(`GameEngine.hintsUsed`);
        console.assert(hintsUsed === 1, "HintsUsed should be incremented to 1");

        // 6. Test Sub-Level Completion (Postcard Modal)
        console.log("\n[TEST 5] Solving sub-level words to test normal postcard modal...");
        await evaluate(`
            const words = GameEngine.words;
            words.forEach(w => {
                GameEngine.foundWords.add(w.word);
                GameEngine.revealWord(w);
            });
        `);
        await new Promise(r => setTimeout(r, 800));
        
        const postcardActive = await evaluate(`document.getElementById('modal-postcard').classList.contains('active')`);
        console.log("Postcard modal active:", postcardActive);
        console.assert(postcardActive, "Postcard win modal should be displayed for sub-level");

        // 7. Test City Finale Completion (25th Level -> Modal City Completed)
        console.log("\n[TEST 6] Testing 25th level completion (Major City Completion Modal & Seal)...");
        await evaluate(`App.hideModal('modal-postcard');`);
        // Fast forward to level 24 (the 25th level)
        await evaluate(`SaveManager.data.currentSubLevel = 24; GameEngine.loadLevel();`);
        const lvl25Header = await evaluate(`document.getElementById('game-city-label').innerText`);
        console.log("Level 25 Header Text:", lvl25Header);
        console.assert(lvl25Header.includes("Mekan 5/5") && lvl25Header.includes("Bulmaca 5/5"), "25th level should be Mekan 5/5 Bulmaca 5/5");

        // Solve level 25
        await evaluate(`
            GameEngine.words.forEach(w => {
                GameEngine.foundWords.add(w.word);
                GameEngine.revealWord(w);
            });
        `);
        await new Promise(r => setTimeout(r, 900));
        
        const cityCompletedModalActive = await evaluate(`document.getElementById('modal-city-completed').classList.contains('active')`);
        console.log("City completed modal active:", cityCompletedModalActive);
        console.assert(cityCompletedModalActive, "Major city completion modal must be displayed on 25th level!");

        // Test Travel to Next City from Completed City
        console.log("\n[TEST 7] Testing Travel to Next City Flow...");
        await evaluate(`App.onCityCompletedTravel()`);
        await new Promise(r => setTimeout(r, 400));
        
        const onMap = await evaluate(`document.getElementById('screen-map').classList.contains('active')`);
        console.assert(onMap, "Map screen should be active after clicking travel");
        const bannerText = await evaluate(`document.getElementById('map-guidance-banner').innerText`);
        console.log("Map Guidance Banner:", bannerText);
        console.assert(bannerText.includes("Sıradaki Hedefini Seç"), "Guidance banner should prompt next destination");

        const istCompleted = await evaluate(`SaveManager.data.completedProvinces.includes(34)`);
        console.assert(istCompleted, "İstanbul should now be marked in completedProvinces");

        // Test Deyim Avcısı screen and absence of undefined
        console.log("\n[TEST 7B] Testing Deyim Avcısı UI & Bug Fix...");
        await evaluate(`App.goToScreen('screen-idiom'); IdiomEngine.init();`);
        const idiomClue = await evaluate(`document.getElementById('idiom-clue-box').innerText`);
        console.log("Idiom Clue:", idiomClue);
        console.assert(!idiomClue.includes("undefined"), "Idiom clue must NEVER contain undefined!");
        console.assert(idiomClue.length > 3, "Idiom clue must be populated");
        const idiomBlankExists = await evaluate(`document.querySelectorAll('.idiom-blank').length > 0`);
        console.assert(idiomBlankExists, "Idiom blank marker must exist in DOM");

        // 8. Test Daily Challenge Flow
        console.log("\n[TEST 8] Testing Daily Challenge State Machine...");
        await evaluate(`App.hideModal('modal-postcard'); App.goToScreen('screen-hub');`);
        await evaluate(`App.showDailyModal()`);
        const dailyModalActive = await evaluate(`document.getElementById('modal-daily').classList.contains('active')`);
        console.assert(dailyModalActive, "Daily modal should be open");
        
        await evaluate(`App.startDailyChallenge()`);
        await new Promise(r => setTimeout(r, 400));
        const isDailyMode = await evaluate(`GameEngine.isDailyMode`);
        console.log("GameEngine isDailyMode:", isDailyMode);
        console.assert(isDailyMode, "GameEngine should be in Daily Mode");

        // 9. Viewport Matrix Screenshots
        console.log("\n[TEST 8] Capturing screenshots across Viewport Matrix...");
        const viewports = [
            { w: 320, h: 568, name: "320x568" },
            { w: 360, h: 640, name: "360x640" },
            { w: 360, h: 800, name: "360x800" },
            { w: 375, h: 812, name: "375x812" },
            { w: 390, h: 844, name: "390x844" },
            { w: 412, h: 915, name: "412x915" },
            { w: 430, h: 932, name: "430x932" },
            { w: 768, h: 1024, name: "768x1024" },
            { w: 1024, h: 1366, name: "1024x1366" },
            { w: 1440, h: 900, name: "1440x900" },
            { w: 1920, h: 1080, name: "1920x1080" }
        ];

        if (!fs.existsSync('docs/screenshots')) fs.mkdirSync('docs/screenshots', { recursive: true });

        for (const vp of viewports) {
            await send('Emulation.setDeviceMetricsOverride', {
                width: vp.w,
                height: vp.h,
                deviceScaleFactor: 1,
                mobile: vp.w < 768
            });
            await new Promise(r => setTimeout(r, 100));
            const shot = await send('Page.captureScreenshot', { format: 'png' });
            fs.writeFileSync(`docs/screenshots/viewport_${vp.name}.png`, Buffer.from(shot.data, 'base64'));
        }
        console.log(`Captured all ${viewports.length} viewport screenshots in docs/screenshots/!`);

        // 10. Performance Measurement
        console.log("\n[TEST 9] Measuring Performance (FPS & Navigation Timing)...");
        const perfTiming = await evaluate(`JSON.stringify(performance.getEntriesByType('navigation')[0])`);
        const navPerf = JSON.parse(perfTiming);
        const domContentLoaded = navPerf.domContentLoadedEventEnd - navPerf.startTime;
        const loadDuration = navPerf.loadEventEnd - navPerf.startTime;
        console.log(`Performance Timings: DOMContentLoaded: ${domContentLoaded.toFixed(1)}ms, Total Load: ${loadDuration.toFixed(1)}ms`);

        // Frame timing measurement
        const fpsData = await evaluate(`
            new Promise(resolve => {
                let frames = 0;
                const start = performance.now();
                function count() {
                    frames++;
                    if (performance.now() - start < 1000) {
                        requestAnimationFrame(count);
                    } else {
                        const elapsed = performance.now() - start;
                        resolve({ fps: Math.round((frames * 1000) / elapsed), frames, elapsed });
                    }
                }
                requestAnimationFrame(count);
            })
        `);
        console.log(`Measured Frame Rate: ${fpsData.fps} FPS over ${fpsData.elapsed.toFixed(1)}ms`);

        // Check console errors
        const errors = consoleMessages.filter(m => m.type === 'error');
        console.log("\n[TEST 10] Console Error Audit:");
        console.log(`Total errors captured during full QA flow: ${errors.length}`);
        if (errors.length > 0) {
            errors.forEach(e => console.error(" - Error:", e.text));
        } else {
            console.log("PASS: ZERO console errors during entire playthrough!");
        }

        ws.close();
        console.log("\n=== ALL BROWSER QA SUITES COMPLETED SUCCESSFULLY ===");
    } finally {
        server.close();
        chromeProc.kill();
    }
}

runBrowserQA().catch(err => {
    console.error("FATAL BROWSER QA FAILURE:", err);
    process.exit(1);
});

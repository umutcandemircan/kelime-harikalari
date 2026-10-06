const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

async function runLiveE2E() {
    console.log("=== LAUNCHING CHROME HEADLESS E2E ON LIVE SITE ===");
    
    const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
    const port = 9222;
    
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
            }
            if (msg.method === 'Runtime.exceptionThrown') {
                const text = msg.params.exceptionDetails.text + ' ' + (msg.params.exceptionDetails.exception?.description || '');
                consoleMessages.push({ type: 'error', text });
            }
            if (msg.method === 'Network.responseReceived') {
                const status = msg.params.response.status;
                if (status === 404) {
                    consoleMessages.push({ type: 'error', text: '404 NOT FOUND: ' + msg.params.response.url });
                }
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

        await send('Runtime.enable');
        await send('Page.enable');
        await send('DOM.enable');
        await send('Network.enable');

        if (!fs.existsSync('docs/screenshots')) {
            fs.mkdirSync('docs/screenshots', { recursive: true });
        }

        // --- STEP 1: CANLI SİTEYİ VE TEMİZ OTURUMU AÇ ---
        console.log("\n[STEP 1] Canlı siteyi aç, önbelleği temizle ve ekran görüntüsü al...");
        await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
        
        const LIVE_URL = 'https://umutcandemircan.github.io/kelime-harikalari/';
        await send('Page.navigate', { url: LIVE_URL });
        await new Promise(r => setTimeout(r, 2000));
        
        // Clear caches & localStorage
        await evaluate(`
            localStorage.clear();
            caches.keys().then(keys => Promise.all(keys.map(k => caches.delete(k))));
        `);
        // Hard reload
        await send('Page.reload', { ignoreCache: true });
        await new Promise(r => setTimeout(r, 2000));
        
        let shot = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('docs/screenshots/live_01_hub.png', Buffer.from(shot.data, 'base64'));
        console.log("Saved docs/screenshots/live_01_hub.png");

        // --- STEP 2: ONBOARDING & SERBEST ŞEHİR SEÇİMİ ---
        console.log("\n[STEP 2] Onboarding ve şehir seçimi testi...");
        await evaluate(`App.startJourney()`);
        await new Promise(r => setTimeout(r, 500));
        
        const modalVisible = await evaluate(`document.getElementById('modal-start-city').classList.contains('active')`);
        console.assert(modalVisible, "Onboarding modal didn't appear!");
        
        // Select City 34 (Istanbul)
        await evaluate(`App.hideModal('modal-start-city')`);
        const istIdx = await evaluate(`CITIES.findIndex(c => c.plate === 34)`);
        await evaluate(`MapEngine.selectCity(${istIdx})`);
        await new Promise(r => setTimeout(r, 500));
        
        shot = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('docs/screenshots/live_02_city_selected.png', Buffer.from(shot.data, 'base64'));
        console.log("Saved docs/screenshots/live_02_city_selected.png");
        
        await evaluate(`document.getElementById('card-action-btn').click()`);
        await new Promise(r => setTimeout(r, 1000));

        // --- STEP 3: BULMACA VE HİYERARŞİ DOĞRULAMASI ---
        console.log("\n[STEP 3] Bulmaca ve hiyerarşi doğrulaması...");
        const headerText = await evaluate(`document.getElementById('game-city-label').innerText`);
        console.log("Header Text:", headerText);
        
        const cellCount = await evaluate(`document.querySelectorAll('.grid-cell').length`);
        const letterCount = await evaluate(`document.querySelectorAll('.letter-node').length`);
        console.log(`Cells: ${cellCount}, Letters on wheel: ${letterCount}`);
        
        shot = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('docs/screenshots/live_03_gameplay_start.png', Buffer.from(shot.data, 'base64'));
        console.log("Saved docs/screenshots/live_03_gameplay_start.png");

        // --- STEP 4: GERÇEK GİRDİ (POINTER EVENT) SİMÜLASYONU ---
        console.log("\n[STEP 4] Gerçek girdi ile kelime çözme simülasyonu...");
        
        // Calculate coordinates of the first valid word's letters on the wheel
        await evaluate(`
            (async () => {
                const targetWord = GameEngine.words[0].word;
                const asm = document.getElementById('wheel-assembly');
                
                // Get letter nodes and their screen coordinates
                const nodes = Array.from(document.querySelectorAll('.letter-node'));
                
                const points = [];
                for (let i = 0; i < targetWord.length; i++) {
                    const letter = targetWord[i];
                    // Find an unused node that matches the letter
                    const node = nodes.find(n => n.innerText === letter && !points.find(p => p.node === n));
                    if (node) {
                        const rect = node.getBoundingClientRect();
                        points.push({ node: node, x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 });
                    }
                }
                
                if (points.length !== targetWord.length) {
                    console.error("Could not find all nodes for word: " + targetWord);
                    return;
                }

                const dispatchPointerEvent = (type, node, x, y) => {
                    const event = new PointerEvent(type, {
                        bubbles: true, cancelable: true, clientX: x, clientY: y, pointerId: 1, isPrimary: true
                    });
                    node.dispatchEvent(event);
                    if (type === 'pointermove' || type === 'pointerup') {
                        window.dispatchEvent(event);
                    }
                };

                // Dispatch pointerdown on the first letter
                dispatchPointerEvent('pointerdown', points[0].node, points[0].x, points[0].y);
                
                // Dispatch pointermove to subsequent letters
                for (let i = 1; i < points.length; i++) {
                    await new Promise(r => setTimeout(r, 50));
                    dispatchPointerEvent('pointermove', points[i].node, points[i].x, points[i].y);
                }
                
                // Dispatch pointerup
                await new Promise(r => setTimeout(r, 50));
                dispatchPointerEvent('pointerup', points[points.length - 1].node, points[points.length - 1].x, points[points.length - 1].y);
            })();
        `);
        
        await new Promise(r => setTimeout(r, 1000));
        
        const isWordFound = await evaluate(`GameEngine.foundWords.has(GameEngine.words[0].word)`);
        console.log("Is target word found via PointerEvents?:", isWordFound);
        
        shot = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('docs/screenshots/live_04_word_solved.png', Buffer.from(shot.data, 'base64'));
        console.log("Saved docs/screenshots/live_04_word_solved.png");

        // --- STEP 5: GÜNLÜK BULMACA VE DEYİMLER MODU DENETİMİ ---
        console.log("\n[STEP 5] Günlük bulmaca ve deyimler modları...");
        await evaluate(`App.goToScreen('screen-hub')`);
        await new Promise(r => setTimeout(r, 500));
        
        await evaluate(`App.showDailyModal()`);
        await new Promise(r => setTimeout(r, 500));
        shot = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('docs/screenshots/live_05_daily.png', Buffer.from(shot.data, 'base64'));
        console.log("Saved docs/screenshots/live_05_daily.png");
        
        await evaluate(`App.hideModal('modal-daily'); App.goToScreen('screen-idiom')`);
        await new Promise(r => setTimeout(r, 500));
        shot = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('docs/screenshots/live_06_idioms.png', Buffer.from(shot.data, 'base64'));
        console.log("Saved docs/screenshots/live_06_idioms.png");

        // --- STEP 6: KONSOL VE RAPORLAMA ---
        console.log("\n[STEP 6] Console & Error Audit...");
        const errors = consoleMessages.filter(m => m.type === 'error');
        console.log(`Total errors captured during E2E flow: ${errors.length}`);
        if (errors.length > 0) {
            errors.forEach(e => console.log(" -", e.text));
        }

        console.log("\n=== E2E AUDIT COMPLETE ===");
        ws.close();
    } finally {
        chromeProc.kill();
    }
}

runLiveE2E().catch(err => {
    console.error("FATAL E2E FAILURE:", err);
    process.exit(1);
});

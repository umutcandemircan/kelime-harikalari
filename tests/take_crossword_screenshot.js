const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const path = require('path');

async function captureScreen() {
    const server = http.createServer((req, res) => {
        let reqPath = req.url.split('?')[0];
        if (reqPath === '/') reqPath = '/index.html';
        let filePath = path.join(__dirname, '..', reqPath);
        if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
            filePath = path.join(__dirname, '..', 'index.html');
        }
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(fs.readFileSync(filePath));
    });

    await new Promise(r => server.listen(8999, r));

    const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
    const port = 9338;
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
        ws.onmessage = (e) => {
            const m = JSON.parse(e.data);
            if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
        };
        const send = (method, params = {}) => new Promise(r => {
            const id = msgId++;
            pending.set(id, r);
            ws.send(JSON.stringify({ id, method, params }));
        });

        await send('Page.enable');
        await send('Runtime.enable');
        await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
        await send('Page.navigate', { url: 'http://localhost:8999/index.html' });
        await new Promise(r => setTimeout(r, 2000));

        // Start game in Izmir
        await send('Runtime.evaluate', { expression: `
            App.hideModal('modal-journal');
            MapEngine.selectedCityIdx = CITIES.findIndex(c => c.plate === 35);
            MapEngine.playSelectedTurkeyCity();
        ` });
        await new Promise(r => setTimeout(r, 1200));

        // Capture screenshot
        const shot = await send('Page.captureScreenshot', { format: 'png' });
        const buf = Buffer.from(shot.result.data, 'base64');
        fs.writeFileSync('scratch/crossword_fixed_preview.png', buf);
        console.log("Captured updated crossword preview to scratch/crossword_fixed_preview.png");

    } finally {
        chromeProc.kill();
        server.close();
    }
}

captureScreen().catch(console.error);

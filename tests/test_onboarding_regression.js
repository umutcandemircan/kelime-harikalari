const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8991;
const CHROME_PORT = 9244;

async function runOnboardingSuite() {
    console.log("==================================================");
    console.log("   SÖZCÜK SEFERÎ V2 ONBOARDING REGRESSION SUITE   ");
    console.log("==================================================");

    // 1. Static server
    const server = http.createServer((req, res) => {
        let reqPath = req.url.split('?')[0];
        if (reqPath === '/') reqPath = '/index.html';
        const filePath = path.join(__dirname, '..', reqPath);
        if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
            const ext = path.extname(filePath);
            const mimes = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json' };
            res.writeHead(200, { 'Content-Type': (mimes[ext] || 'text/plain') + '; charset=utf-8' });
            res.end(fs.readFileSync(filePath));
        } else {
            res.writeHead(404);
            res.end('Not found');
        }
    });
    await new Promise(r => server.listen(PORT, r));
    console.log(`[SERVER] Started at http://localhost:${PORT}`);

    // 2. Launch Chrome
    const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        `--remote-debugging-port=${CHROME_PORT}`,
        'about:blank'
    ]);
    await new Promise(r => setTimeout(r, 1500));

    const targetsRes = await fetch(`http://localhost:${CHROME_PORT}/json`);
    const targets = await targetsRes.json();
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

    let msgId = 1;
    const pending = new Map();
    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data.toString());
        if (msg.id && pending.has(msg.id)) {
            const resolve = pending.get(msg.id);
            pending.delete(msg.id);
            resolve(msg);
        }
    };

    function send(method, params = {}) {
        return new Promise(resolve => {
            const id = msgId++;
            pending.set(id, resolve);
            ws.send(JSON.stringify({ id, method, params }));
        });
    }

    await new Promise((resolve) => {
        ws.onopen = resolve;
    });

    await send('Page.enable');
    await send('Runtime.enable');
    await send('DOM.enable');

    async function evaluate(expression) {
        const res = await send('Runtime.evaluate', {
            expression,
            returnByValue: true,
            awaitPromise: true
        });
        if (res.result && res.result.exceptionDetails) {
            throw new Error(`Eval failed: ${JSON.stringify(res.result.exceptionDetails)}`);
        }
        return res.result?.result?.value;
    }

    async function inspectElement(selector) {
        return await evaluate(`(() => {
            const el = document.querySelector("${selector}");
            if (!el) return { exists: false };
            const rect = el.getBoundingClientRect();
            const cs = window.getComputedStyle(el);
            return {
                exists: true,
                id: el.id,
                className: el.className,
                innerText: el.innerText.trim(),
                disabled: el.disabled || false,
                display: cs.display,
                visibility: cs.visibility,
                opacity: cs.opacity,
                pointerEvents: cs.pointerEvents,
                zIndex: cs.zIndex,
                rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
                visible: cs.display !== 'none' && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0 && rect.width > 0 && rect.height > 0
            };
        })()`);
    }

    async function resetStorageAndReload() {
        await send('Page.navigate', { url: `http://localhost:${PORT}/index.html` });
        await new Promise(r => setTimeout(r, 600));
        await evaluate(`try { localStorage.clear(); } catch(e) {}`);
        await send('Page.navigate', { url: `http://localhost:${PORT}/index.html` });
        await new Promise(r => setTimeout(r, 1000));
    }

    let allTestsPassed = true;

    // ----------------------------------------------------
    // TEST 1: test_onboarding_start ("SEFER BAŞLASIN!" user flow via real DOM click)
    // ----------------------------------------------------
    console.log("\n[TEST 1] test_onboarding_start: First visit -> 4 steps -> Click 'SEFER BAŞLASIN!' -> Hub");
    await resetStorageAndReload();

    let modalInfo = await inspectElement('#modal-onboarding');
    console.log("  -> Initial #modal-onboarding visible:", modalInfo.visible, "(display:", modalInfo.display, "zIndex:", modalInfo.zIndex, ")");
    if (!modalInfo.visible) {
        console.error("FAIL: Onboarding modal should be visible on first visit!");
        allTestsPassed = false;
    }

    // Step through 3 times to reach step 4 ("Hata & Geri Bildirim" / "SEFER BAŞLASIN! 🚀")
    for (let i = 0; i < 3; i++) {
        await evaluate(`document.getElementById("onboard-btn-next").click()`);
    }

    const step3Info = await evaluate(`(() => ({
        step: OnboardingModal.currentStep,
        title: document.getElementById('onboard-title').innerText,
        btnText: document.getElementById('onboard-btn-next').innerText
    }))()`);
    console.log(`  -> At slide ${step3Info.step}: Title="${step3Info.title}", Button="${step3Info.btnText}"`);

    const finishBtnInfo = await inspectElement('#onboard-btn-next');
    console.log("  -> Button Diagnostics:");
    console.log("     - exists:", finishBtnInfo.exists);
    console.log("     - visible:", finishBtnInfo.visible);
    console.log("     - enabled:", !finishBtnInfo.disabled);
    console.log("     - pointer-events:", finishBtnInfo.pointerEvents);
    console.log("     - z-index:", finishBtnInfo.zIndex);
    console.log("     - innerText:", finishBtnInfo.innerText);

    // Assert before click
    const beforeVisible = await evaluate(`window.getComputedStyle(document.getElementById('modal-onboarding')).display !== 'none'`);
    console.log("  -> BEFORE click: modal visible ===", beforeVisible);

    // CLICK "SEFER BAŞLASIN! 🚀" using real click
    await evaluate(`document.getElementById('onboard-btn-next').click()`);
    await new Promise(r => setTimeout(r, 200));

    // Assert after click
    const afterModalInfo = await inspectElement('#modal-onboarding');
    const afterScreen = await evaluate(`ScreenRouter.currentScreen`);
    const hubActive = await evaluate(`document.getElementById('screen-hub').classList.contains('active')`);
    const onboardingSaved = await evaluate(`SaveManager.data.onboardingCompleted`);

    console.log("  -> AFTER click:");
    console.log("     - modal visible ===", afterModalInfo.visible, `(display: ${afterModalInfo.display}, pointer-events: ${afterModalInfo.pointerEvents})`);
    console.log("     - active screen ===", afterScreen);
    console.log("     - hub active ===", hubActive);
    console.log("     - onboardingCompleted in save ===", onboardingSaved);

    if (afterModalInfo.visible === false && hubActive === true && onboardingSaved === true) {
        console.log("  ✓ PASS: test_onboarding_start passed!");
    } else {
        console.error("  ✕ FAIL: test_onboarding_start failed!");
        allTestsPassed = false;
    }

    // ----------------------------------------------------
    // TEST 2: test_onboarding_skip ("Atla" button click -> Hub)
    // ----------------------------------------------------
    console.log("\n[TEST 2] test_onboarding_skip: First visit -> Click 'Atla' directly -> Hub");
    await resetStorageAndReload();

    const skipBtnInfo = await inspectElement('#onboard-btn-skip');
    console.log("  -> Skip Button Diagnostics:");
    console.log("     - exists:", skipBtnInfo.exists);
    console.log("     - visible:", skipBtnInfo.visible);
    console.log("     - enabled:", !skipBtnInfo.disabled);
    console.log("     - pointer-events:", skipBtnInfo.pointerEvents);

    // Click "Atla"
    await evaluate(`document.getElementById('onboard-btn-skip').click()`);
    await new Promise(r => setTimeout(r, 200));

    const afterSkipModal = await inspectElement('#modal-onboarding');
    const afterSkipScreen = await evaluate(`ScreenRouter.currentScreen`);
    const skipOnboardingSaved = await evaluate(`SaveManager.data.onboardingCompleted`);

    console.log("  -> AFTER skip click:");
    console.log("     - modal visible ===", afterSkipModal.visible, `(display: ${afterSkipModal.display})`);
    console.log("     - active screen ===", afterSkipScreen);
    console.log("     - onboardingCompleted in save ===", skipOnboardingSaved);

    if (afterSkipModal.visible === false && afterSkipScreen === 'screen-hub' && skipOnboardingSaved === true) {
        console.log("  ✓ PASS: test_onboarding_skip passed!");
    } else {
        console.error("  ✕ FAIL: test_onboarding_skip failed!");
        allTestsPassed = false;
    }

    // ----------------------------------------------------
    // TEST 3: test_onboarding_first_run_persistence (Page reload after completion)
    // ----------------------------------------------------
    console.log("\n[TEST 3] test_onboarding_first_run_persistence: Reload page -> Onboarding does NOT re-appear");
    await send('Page.navigate', { url: `http://localhost:${PORT}/index.html` });
    await new Promise(r => setTimeout(r, 1200));

    const reloadedModal = await inspectElement('#modal-onboarding');
    const reloadedScreen = await evaluate(`ScreenRouter.currentScreen`);
    console.log("  -> After reload modal visible ===", reloadedModal.visible, `(display: ${reloadedModal.display})`);
    console.log("  -> After reload active screen ===", reloadedScreen);

    if (reloadedModal.visible === false && reloadedScreen === 'screen-hub') {
        console.log("  ✓ PASS: test_onboarding_first_run_persistence passed!");
    } else {
        console.error("  ✕ FAIL: test_onboarding_first_run_persistence failed!");
        allTestsPassed = false;
    }

    // ----------------------------------------------------
    // TEST 4: test_onboarding_mouse_click (CDP Synthesized Mouse Click)
    // ----------------------------------------------------
    console.log("\n[TEST 4] test_onboarding_mouse_click: Native CDP Mouse Event dispatching");
    await resetStorageAndReload();

    // Get exact center coordinate of button
    const btnBox = await inspectElement('#onboard-btn-next');
    const clickX = Math.round(btnBox.rect.x + btnBox.rect.width / 2);
    const clickY = Math.round(btnBox.rect.y + btnBox.rect.height / 2);
    console.log(`  -> Dispatching Mouse Click at (${clickX}, ${clickY})...`);

    // Advance 3 times to last slide with CDP Mouse Events
    for (let step = 0; step < 3; step++) {
        await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: clickX, y: clickY, button: 'left', clickCount: 1 });
        await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: clickX, y: clickY, button: 'left', clickCount: 1 });
        await new Promise(r => setTimeout(r, 100));
    }

    const currentTitle = await evaluate(`document.getElementById('onboard-title').innerText`);
    console.log("  -> Current slide title after 3 CDP mouse clicks:", currentTitle);

    // Final click on "SEFER BAŞLASIN! 🚀"
    await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: clickX, y: clickY, button: 'left', clickCount: 1 });
    await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: clickX, y: clickY, button: 'left', clickCount: 1 });
    await new Promise(r => setTimeout(r, 200));

    const cdpModalAfter = await inspectElement('#modal-onboarding');
    console.log("  -> Modal visible after CDP mouse finish ===", cdpModalAfter.visible);

    if (cdpModalAfter.visible === false) {
        console.log("  ✓ PASS: test_onboarding_mouse_click passed!");
    } else {
        console.error("  ✕ FAIL: test_onboarding_mouse_click failed!");
        allTestsPassed = false;
    }

    // ----------------------------------------------------
    // TEST 5: test_onboarding_touch (Touch / Pointer Tap Event simulation)
    // ----------------------------------------------------
    console.log("\n[TEST 5] test_onboarding_touch: Pointer / Touch Tap simulation");
    await resetStorageAndReload();

    // Simulate pointerdown + pointerup + click on next button
    await evaluate(`(() => {
        const btn = document.getElementById('onboard-btn-next');
        const touch = new PointerEvent('pointerdown', { bubbles: true, cancelable: true, pointerType: 'touch' });
        btn.dispatchEvent(touch);
        const up = new PointerEvent('pointerup', { bubbles: true, cancelable: true, pointerType: 'touch' });
        btn.dispatchEvent(up);
        btn.click();
    })()`);

    const stepAfterTouch = await evaluate(`OnboardingModal.currentStep`);
    console.log("  -> Step advanced to:", stepAfterTouch);

    // Fast-forward to last step and tap finish
    await evaluate(`OnboardingModal.currentStep = 3; OnboardingModal.renderStep();`);
    await evaluate(`(() => {
        const btn = document.getElementById('onboard-btn-next');
        btn.click();
    })()`);
    await new Promise(r => setTimeout(r, 200));

    const touchModalAfter = await inspectElement('#modal-onboarding');
    console.log("  -> Modal visible after touch finish ===", touchModalAfter.visible);

    if (touchModalAfter.visible === false) {
        console.log("  ✓ PASS: test_onboarding_touch passed!");
    } else {
        console.error("  ✕ FAIL: test_onboarding_touch failed!");
        allTestsPassed = false;
    }

    // ----------------------------------------------------
    // TEST 6: test_onboarding_keyboard (Keyboard Enter and Escape handling)
    // ----------------------------------------------------
    console.log("\n[TEST 6] test_onboarding_keyboard: Keyboard Enter to advance & Escape to skip");
    await resetStorageAndReload();

    // Advance using Enter key
    await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });
    await new Promise(r => setTimeout(r, 100));

    const stepAfterEnter = await evaluate(`OnboardingModal.currentStep`);
    console.log("  -> Step after Enter key:", stepAfterEnter);

    // Now press Escape to skip
    await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 });
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 });
    await new Promise(r => setTimeout(r, 200));

    const keyModalAfter = await inspectElement('#modal-onboarding');
    console.log("  -> Modal visible after Escape key ===", keyModalAfter.visible);

    if (stepAfterEnter === 1 && keyModalAfter.visible === false) {
        console.log("  ✓ PASS: test_onboarding_keyboard passed!");
    } else {
        console.error("  ✕ FAIL: test_onboarding_keyboard failed!");
        allTestsPassed = false;
    }

    console.log("\n==================================================");
    if (allTestsPassed) {
        console.log("   ALL 6 ONBOARDING REGRESSION TESTS PASSED!      ");
    } else {
        console.log("   SOME TESTS FAILED - SEE DETAILS ABOVE         ");
    }
    console.log("==================================================");

    ws.close();
    chrome.kill();
    server.close();
    process.exit(allTestsPassed ? 0 : 1);
}

runOnboardingSuite().catch(err => {
    console.error("Suite encountered error:", err);
    process.exit(1);
});

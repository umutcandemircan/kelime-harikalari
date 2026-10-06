import re

with open('src/js/game/MapEngine.js', 'r', encoding='utf8') as f:
    js = f.read()

# 1. Update startLerpLoop for zooming classes
old_loop = """            if (svg) {
                svg.setAttribute('viewBox', `${this.vbX} ${this.vbY} ${this.vbW} ${this.vbH}`);
            }"""
new_loop = """            if (svg) {
                svg.setAttribute('viewBox', `${this.vbX} ${this.vbY} ${this.vbW} ${this.vbH}`);
                if (this.vbW > 700) {
                    svg.classList.add('zoomed-out');
                } else {
                    svg.classList.remove('zoomed-out');
                }
            }"""
js = js.replace(old_loop, new_loop)

# 2. Update focusOnCity to add focused class
old_focus = """        this.targetVbW = newW;
        this.targetVbH = newH;
        this.targetVbX = cx - newW / 2;
        this.targetVbY = cy - newH / 2;
        this.clampBounds();
    },"""

new_focus = """        this.targetVbW = newW;
        this.targetVbH = newH;
        this.targetVbX = cx - newW / 2;
        this.targetVbY = cy - newH / 2;
        this.clampBounds();
        
        const svg = document.getElementById('turkey-map-svg');
        if (svg) {
            svg.classList.add('has-focus');
            document.querySelectorAll('.province-path').forEach(el => el.classList.remove('focused'));
            if (path) path.classList.add('focused');
        }
    },"""
js = js.replace(old_focus, new_focus)

# 3. Update closeCard to remove focus class
old_close = """    closeCard() {
        const card = document.getElementById('map-city-card');
        if (card) card.classList.remove('active');
    },"""
new_close = """    closeCard() {
        const card = document.getElementById('map-city-card');
        if (card) card.classList.remove('active');
        const svg = document.getElementById('turkey-map-svg');
        if (svg) {
            svg.classList.remove('has-focus');
            document.querySelectorAll('.province-path').forEach(el => el.classList.remove('focused'));
        }
    },"""
js = js.replace(old_close, new_close)

# 4. Make sure onPointerDown removes focus and closes card to allow free roaming
old_pointer_down = """    onPointerDown(e) {
        if (e.target.closest('#map-city-card') || e.target.closest('.map-controls-floating')) return;
        this.isPanning = true;"""
new_pointer_down = """    onPointerDown(e) {
        if (e.target.closest('#map-city-card') || e.target.closest('.map-controls-floating')) return;
        
        // If they click outside the card on the map, close the card and remove focus
        if (!e.target.closest('.city-pin-node') && !e.target.closest('.province-path')) {
             this.closeCard();
        }
        
        this.isPanning = true;"""
js = js.replace(old_pointer_down, new_pointer_down)

with open('src/js/game/MapEngine.js', 'w', encoding='utf8') as f:
    f.write(js)

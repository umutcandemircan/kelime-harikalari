import re

js_path = 'src/js/game/MapEngine.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Variables for touch/pinch
touch_vars = """    scale: 1.8,
    panX: 0,
    panY: 0,
    isPanning: false,
    startX: 0,
    startY: 0,
    startPanX: 0,
    startPanY: 0,
    dragDistance: 0,
    
    // Pinch to Zoom
    isPinching: false,
    startPinchDist: 0,
    startPinchScale: 1,"""

js = re.sub(
    r'    scale: 1\.8,[\s\S]*?dragDistance: 0,',
    touch_vars,
    js
)

# Bind Events
old_bind = r"""            stage\.addEventListener\('pointerdown', \(e\) => this\.onPointerDown\(e\)\);
            window\.addEventListener\('pointermove', \(e\) => this\.onPointerMove\(e\)\);
            window\.addEventListener\('pointerup', \(e\) => this\.onPointerUp\(e\)\);
            window\.addEventListener\('pointercancel', \(e\) => this\.onPointerUp\(e\)\);"""

new_bind = """            stage.addEventListener('touchstart', (e) => this.onTouchStart(e), { passive: false });
            stage.addEventListener('touchmove', (e) => this.onTouchMove(e), { passive: false });
            stage.addEventListener('touchend', (e) => this.onTouchEnd(e), { passive: false });
            stage.addEventListener('touchcancel', (e) => this.onTouchEnd(e), { passive: false });
            
            stage.addEventListener('pointerdown', (e) => { if(e.pointerType === 'mouse') this.onPointerDown(e); });
            window.addEventListener('pointermove', (e) => { if(e.pointerType === 'mouse') this.onPointerMove(e); });
            window.addEventListener('pointerup', (e) => { if(e.pointerType === 'mouse') this.onPointerUp(e); });"""

js = re.sub(old_bind, new_bind, js)

# Inject touch handlers
touch_handlers = """
    onTouchStart(e) {
        if (e.target.closest('#map-city-card') || e.target.closest('.map-controls-floating')) return;
        if (!e.target.closest('.city-pin-node') && !e.target.closest('.province-path')) {
            this.closeCard();
        }
        
        if (e.touches.length === 2) {
            e.preventDefault();
            this.isPinching = true;
            this.isPanning = false;
            const dx = e.touches[0].clientX - e.touches[1].clientX;
            const dy = e.touches[0].clientY - e.touches[1].clientY;
            this.startPinchDist = Math.hypot(dx, dy);
            this.startPinchScale = this.scale;
        } else if (e.touches.length === 1) {
            this.isPanning = true;
            this.isPinching = false;
            this.startX = e.touches[0].clientX;
            this.startY = e.touches[0].clientY;
            this.startPanX = this.panX;
            this.startPanY = this.panY;
            this.dragDistance = 0;
        }
        const viewport = document.getElementById('map-viewport');
        if (viewport) viewport.style.transition = 'none';
    },

    onTouchMove(e) {
        if (this.isPinching && e.touches.length === 2) {
            e.preventDefault();
            const dx = e.touches[0].clientX - e.touches[1].clientX;
            const dy = e.touches[0].clientY - e.touches[1].clientY;
            const dist = Math.hypot(dx, dy);
            
            const centerX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
            const centerY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
            
            const newScale = this.startPinchScale * (dist / this.startPinchDist);
            this.setZoom(newScale, centerX, centerY, false);
            
        } else if (this.isPanning && e.touches.length === 1) {
            e.preventDefault();
            const dx = e.touches[0].clientX - this.startX;
            const dy = e.touches[0].clientY - this.startY;
            this.dragDistance = Math.hypot(dx, dy);
            
            this.panX = this.startPanX + dx;
            this.panY = this.startPanY + dy;
            this.applyTransform(false);
        }
    },

    onTouchEnd(e) {
        if (this.isPinching && e.touches.length < 2) {
            this.isPinching = false;
            if (e.touches.length === 1) {
                // Resume panning with 1 finger
                this.isPanning = true;
                this.startX = e.touches[0].clientX;
                this.startY = e.touches[0].clientY;
                this.startPanX = this.panX;
                this.startPanY = this.panY;
            }
        } else if (this.isPanning && e.touches.length === 0) {
            this.isPanning = false;
            this.applyTransform(true);
        }
    },
"""

js = js.replace('    onPointerDown(e) {', touch_handlers + '\n    onPointerDown(e) {')

# Fix clamping in applyTransform
old_apply = r"""    applyTransform\(smooth = false\) \{
        const viewport = document\.getElementById\('map-viewport'\);
        if \(\!viewport\) return;
        viewport\.style\.transition = smooth \? 'transform 0\.5s cubic-bezier\(0\.25, 1, 0\.5, 1\)' : 'none';
        viewport\.style\.transform = `translate3d\(\$\{this\.panX\}px, \$\{this\.panY\}px, 0\) scale\(\$\{this\.scale\}\)`;
    \},"""

new_apply = """    applyTransform(smooth = false) {
        const viewport = document.getElementById('map-viewport');
        if (!viewport) return;
        
        // Boundary Clamping
        const container = document.getElementById('map-stage-wrapper') || document.body;
        const vpW = container.clientWidth;
        const vpH = container.clientHeight;
        const mapW = 1100 * this.scale;
        const mapH = 500 * this.scale;
        
        const minX = vpW - mapW - 50;
        const maxX = 50;
        const minY = vpH - mapH - 50;
        const maxY = 50;
        
        if (this.panX > maxX) this.panX = maxX;
        if (this.panX < minX) this.panX = minX;
        if (this.panY > maxY) this.panY = maxY;
        if (this.panY < minY) this.panY = minY;
        
        viewport.style.transition = smooth ? 'transform 0.5s cubic-bezier(0.25, 1, 0.5, 1)' : 'none';
        viewport.style.transform = `translate3d(${this.panX}px, ${this.panY}px, 0) scale(${this.scale})`;
    },"""
js = re.sub(old_apply, new_apply, js)

# Change scale bounds to 1.0 to 4.5
js = re.sub(r'Math\.max\(0\.65, Math\.min\(3\.8', 'Math.max(1.0, Math.min(4.5', js)
js = js.replace('this.setZoom(Math.min(3.8, this.scale * 1.3));', 'this.setZoom(Math.min(4.5, this.scale * 1.3));')
js = js.replace('this.setZoom(Math.max(0.65, this.scale / 1.3));', 'this.setZoom(Math.max(1.0, this.scale / 1.3));')


# Focus on city styling (add 'focused' class)
old_select = r"""        const paths = document\.querySelectorAll\('\.province-path'\);
        paths\.forEach\(p => p\.classList\.remove\('active-city'\)\);
        const p = document\.querySelector\(`\.province-path\[data-plate="\$\{city\.plate\}"\]`\);
        if \(p\) p\.classList\.add\('active-city'\);"""

new_select = """        const paths = document.querySelectorAll('.province-path');
        paths.forEach(p => { p.classList.remove('active-city'); p.classList.remove('focused'); });
        const p = document.querySelector(`.province-path[data-plate="${city.plate}"]`);
        if (p) { p.classList.add('active-city'); p.classList.add('focused'); }"""

js = re.sub(old_select, new_select, js)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("MapEngine patched.")

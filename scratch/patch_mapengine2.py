import re

js_path = 'src/js/game/MapEngine.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

old_setzoom = r"""    setZoom\(newScale, focalX, focalY\) \{
        const container = document\.getElementById\('map-stage-wrapper'\) \|\| document\.getElementById\('map-viewport'\)\?\.parentElement \|\| document\.body;
        const vpW = container\.clientWidth \|\| 360;
        const vpH = container\.clientHeight \|\| 500;
        
        const focusX = \(focalX !== undefined\) \? focalX : \(vpW / 2\);
        const focusY = \(focalY !== undefined\) \? focalY : \(vpH / 2\);

        // Keep focal point stationary during zoom
        const mapX = \(focusX - this\.panX\) / this\.scale;
        const mapY = \(focusY - this\.panY\) / this\.scale;

        this\.scale = Math\.max\(1\.0, Math\.min\(4\.5, newScale\)\);
        this\.panX = focusX - \(mapX \* this\.scale\);
        this\.panY = focusY - \(mapY \* this\.scale\);
        this\.applyTransform\(true\);
        this\.updateZoomClasses\(\);
    \},"""

new_setzoom = """    setZoom(newScale, focalX, focalY, smooth = true) {
        const container = document.getElementById('map-stage-wrapper') || document.getElementById('map-viewport')?.parentElement || document.body;
        const vpW = container.clientWidth || 360;
        const vpH = container.clientHeight || 500;
        
        const focusX = (focalX !== undefined) ? focalX : (vpW / 2);
        const focusY = (focalY !== undefined) ? focalY : (vpH / 2);

        // Keep focal point stationary during zoom
        const mapX = (focusX - this.panX) / this.scale;
        const mapY = (focusY - this.panY) / this.scale;

        this.scale = Math.max(1.0, Math.min(4.5, newScale));
        this.panX = focusX - (mapX * this.scale);
        this.panY = focusY - (mapY * this.scale);
        this.applyTransform(smooth);
        this.updateZoomClasses();
    },"""

js = re.sub(old_setzoom, new_setzoom, js)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("setZoom patched.")

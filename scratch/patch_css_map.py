import re

css_path = 'src/css/main.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Add GPU acceleration, perspective, and background texture
old_stage = r"""        #map-stage-wrapper::before \{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-image: 
                linear-gradient\(rgba\(28,37,65,0\.05\) 1px, transparent 1px\),
                linear-gradient\(90deg, rgba\(28,37,65,0\.05\) 1px, transparent 1px\),
                linear-gradient\(45deg, rgba\(212,163,115,0\.03\) 1px, transparent 1px\),
                linear-gradient\(-45deg, rgba\(212,163,115,0\.03\) 1px, transparent 1px\);
            background-size: 40px 40px, 40px 40px, 120px 120px, 120px 120px;
            z-index: 0;
            pointer-events: none;
        \}"""
new_stage = """        #map-stage-wrapper::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: 
                radial-gradient(circle at 80% 20%, rgba(212,163,115,0.08) 0%, transparent 40%),
                linear-gradient(rgba(28,37,65,0.08) 1px, transparent 1px),
                linear-gradient(90deg, rgba(28,37,65,0.08) 1px, transparent 1px),
                linear-gradient(45deg, rgba(212,163,115,0.05) 1px, transparent 1px),
                linear-gradient(-45deg, rgba(212,163,115,0.05) 1px, transparent 1px);
            background-size: 100% 100%, 60px 60px, 60px 60px, 180px 180px, 180px 180px;
            z-index: 0;
            pointer-events: none;
        }"""
css = re.sub(old_stage, new_stage, css)

# 2.5D transform for map-viewport
old_viewport = r"""        #map-viewport \{
            width: 1100px;
            height: 500px;
            position: absolute;
            top: 0;
            left: 0;
            transform-origin: 0 0;
            will-change: transform;
            transition: transform 0\.5s cubic-bezier\(0\.25, 1, 0\.5, 1\);
        \}"""
new_viewport = """        #map-viewport {
            width: 1100px;
            height: 500px;
            position: absolute;
            top: 0;
            left: 0;
            transform-origin: 0 0;
            will-change: transform;
            transition: transform 0.5s cubic-bezier(0.25, 1, 0.5, 1);
            transform-style: preserve-3d;
        }
        
        #map-stage-wrapper {
            perspective: 1200px;
            background-color: #0d1629;
            background-image: url('data:image/svg+xml;utf8,<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="100" r="90" fill="none" stroke="rgba(212,163,115,0.05)" stroke-width="1"/><path d="M100 10 L100 190 M10 100 L190 100 M35 35 L165 165 M35 165 L165 35" stroke="rgba(212,163,115,0.05)" stroke-width="1"/></svg>');
            background-repeat: no-repeat;
            background-position: center center;
            background-size: contain;
        }"""
css = re.sub(old_viewport, new_viewport, css)

# Add elevated pin glow
new_glow = """
        .province-path.focused {
            transform: translateZ(20px);
            filter: drop-shadow(0 15px 15px rgba(0,0,0,0.6));
        }
        .turkey-svg {
            transform: rotateX(6deg) translateZ(0);
            transform-style: preserve-3d;
        }
"""
css += new_glow

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS cartography patched.")

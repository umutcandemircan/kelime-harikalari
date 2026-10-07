// 3D INTERACTIVE WEBGL / CARTOGRAPHIC WORLD GLOBE ENGINE (V2)
// High-performance, zero-dependency 3D sphere with inertia, interactive country pins,
// atmospheric glow, and cinematic camera transition into playable regions.
const Globe3D = {
    canvas: null,
    ctx: null,
    isWebGL: false,
    width: 0,
    height: 0,
    radius: 180,
    
    // Camera & Rotation State
    yaw: 0.6,    // Longitude rotation (radians)
    pitch: 0.35, // Latitude rotation (radians)
    targetYaw: 0.6,
    targetPitch: 0.35,
    distance: 600,
    targetDistance: 600,
    
    // Inertia & Physics
    velYaw: 0,
    velPitch: 0,
    isDragging: false,
    lastMouseX: 0,
    lastMouseY: 0,
    lastTouchDist: 0,
    isPinching: false,
    dragMoved: false,
    
    // Auto-rotation
    idleTimer: null,
    isAutoRotating: true,
    
    // Animation frame
    animId: null,
    isTransitioning: false,

    // Country Data on the 3D Sphere (Coordinates in Degrees Lat / Lng)
    COUNTRIES: [
        { id: 'tr', name: 'Türkiye', flag: '🇹🇷', lat: 39.0, lng: 35.2, status: 'playable', subtitle: '81 İl • 405 Mekân' },
        { id: 'fr', name: 'Fransa', flag: '🇫🇷', lat: 48.8, lng: 2.3, status: 'locked', subtitle: 'Paris • Çok Yakında' },
        { id: 'it', name: 'İtalya', flag: '🇮🇹', lat: 41.9, lng: 12.5, status: 'locked', subtitle: 'Roma • Çok Yakında' },
        { id: 'gb', name: 'Birleşik Krallık', flag: '🇬🇧', lat: 51.5, lng: -0.1, status: 'locked', subtitle: 'Londra • Çok Yakında' },
        { id: 'de', name: 'Almanya', flag: '🇩🇪', lat: 52.5, lng: 13.4, status: 'locked', subtitle: 'Berlin • Çok Yakında' },
        { id: 'es', name: 'İspanya', flag: '🇪🇸', lat: 40.4, lng: -3.7, status: 'locked', subtitle: 'Madrid • Çok Yakında' },
        { id: 'gr', name: 'Yunanistan', flag: '🇬🇷', lat: 38.0, lng: 23.7, status: 'locked', subtitle: 'Atina • Çok Yakında' },
        { id: 'eg', name: 'Mısır', flag: '🇪🇬', lat: 30.0, lng: 31.2, status: 'locked', subtitle: 'Kahire • Çok Yakında' },
        { id: 'us', name: 'ABD', flag: '🇺🇸', lat: 40.7, lng: -74.0, status: 'locked', subtitle: 'New York • Çok Yakında' },
        { id: 'jp', name: 'Japonya', flag: '🇯🇵', lat: 35.7, lng: 139.7, status: 'locked', subtitle: 'Tokyo • Çok Yakında' },
        { id: 'br', name: 'Brezilya', flag: '🇧🇷', lat: -22.9, lng: -43.2, status: 'locked', subtitle: 'Rio • Çok Yakında' },
        { id: 'au', name: 'Avustralya', flag: '🇦🇺', lat: -33.8, lng: 151.2, status: 'locked', subtitle: 'Sidney • Çok Yakında' }
    ],

    // Vector polygon approximations for major continental landmasses (Lat, Lng pairs)
    CONTINENTS: [
        // Europe & Asia (Eurasia)
        [
            {lat: 70, lng: 30}, {lat: 65, lng: 60}, {lat: 60, lng: 100}, {lat: 65, lng: 140}, {lat: 60, lng: 170},
            {lat: 40, lng: 145}, {lat: 30, lng: 122}, {lat: 20, lng: 110}, {lat: 10, lng: 100}, {lat: 15, lng: 80},
            {lat: 25, lng: 65}, {lat: 30, lng: 50}, {lat: 36, lng: 36}, {lat: 41, lng: 29}, {lat: 38, lng: 24},
            {lat: 36, lng: -5}, {lat: 44, lng: -9}, {lat: 50, lng: -4}, {lat: 58, lng: 5}, {lat: 71, lng: 25}
        ],
        // Africa
        [
            {lat: 36, lng: -5}, {lat: 37, lng: 10}, {lat: 32, lng: 32}, {lat: 12, lng: 44}, {lat: 0, lng: 42},
            {lat: -15, lng: 40}, {lat: -34, lng: 20}, {lat: -30, lng: 15}, {lat: -10, lng: 12}, {lat: 5, lng: 0},
            {lat: 15, lng: -17}, {lat: 28, lng: -13}, {lat: 36, lng: -5}
        ],
        // North America
        [
            {lat: 70, lng: -160}, {lat: 70, lng: -90}, {lat: 60, lng: -65}, {lat: 45, lng: -60}, {lat: 30, lng: -80},
            {lat: 25, lng: -80}, {lat: 15, lng: -90}, {lat: 20, lng: -105}, {lat: 32, lng: -117}, {lat: 50, lng: -128},
            {lat: 60, lng: -145}, {lat: 65, lng: -168}, {lat: 70, lng: -160}
        ],
        // South America
        [
            {lat: 12, lng: -72}, {lat: 8, lng: -60}, {lat: -5, lng: -35}, {lat: -22, lng: -41}, {lat: -35, lng: -55},
            {lat: -54, lng: -68}, {lat: -40, lng: -73}, {lat: -15, lng: -75}, {lat: -2, lng: -80}, {lat: 12, lng: -72}
        ],
        // Australia
        [
            {lat: -12, lng: 132}, {lat: -15, lng: 145}, {lat: -25, lng: 153}, {lat: -38, lng: 145}, {lat: -35, lng: 115},
            {lat: -22, lng: 114}, {lat: -15, lng: 125}, {lat: -12, lng: 132}
        ]
    ],

    init() {
        this.canvas = document.getElementById('globe-3d-canvas');
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.resize();
        window.addEventListener('resize', () => this.resize());

        this.bindEvents();
        this.startLoop();
        
        // Focus on Turkey on load
        this.focusOnCountry('tr', false);
    },

    resize() {
        if (!this.canvas) return;
        const rect = this.canvas.parentElement ? this.canvas.parentElement.getBoundingClientRect() : { width: window.innerWidth, height: window.innerHeight };
        this.width = rect.width || window.innerWidth;
        this.height = rect.height || window.innerHeight;
        
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        this.canvas.width = this.width * dpr;
        this.canvas.height = this.height * dpr;
        if (this.ctx) {
            this.ctx.resetTransform?.();
            this.ctx.scale(dpr, dpr);
        }

        // Responsive radius: fills 68% of min viewport
        this.radius = Math.min(this.width, this.height) * 0.38;
        this.distance = this.radius * 2.8;
        this.targetDistance = this.distance;
    },

    bindEvents() {
        if (!this.canvas) return;

        // Pointer / Mouse events
        this.canvas.addEventListener('pointerdown', (e) => this.onPointerDown(e));
        window.addEventListener('pointermove', (e) => this.onPointerMove(e));
        window.addEventListener('pointerup', (e) => this.onPointerUp(e));
        window.addEventListener('pointercancel', (e) => this.onPointerUp(e));

        // Wheel Zoom
        this.canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            this.resetIdleTimer();
            const delta = e.deltaY * 0.4;
            const minR = Math.min(this.width, this.height) * 0.22;
            const maxR = Math.min(this.width, this.height) * 0.65;
            this.radius = Math.max(minR, Math.min(maxR, this.radius - delta * 0.2));
        }, { passive: false });

        // Touch Pinch Zoom
        this.canvas.addEventListener('touchstart', (e) => {
            if (e.touches.length === 2) {
                this.isPinching = true;
                this.isDragging = false;
                const dx = e.touches[0].clientX - e.touches[1].clientX;
                const dy = e.touches[0].clientY - e.touches[1].clientY;
                this.lastTouchDist = Math.hypot(dx, dy);
            }
        }, { passive: true });

        this.canvas.addEventListener('touchmove', (e) => {
            if (this.isPinching && e.touches.length === 2) {
                const dx = e.touches[0].clientX - e.touches[1].clientX;
                const dy = e.touches[0].clientY - e.touches[1].clientY;
                const dist = Math.hypot(dx, dy);
                const scale = dist / (this.lastTouchDist || dist);
                this.lastTouchDist = dist;
                
                const minR = Math.min(this.width, this.height) * 0.22;
                const maxR = Math.min(this.width, this.height) * 0.65;
                this.radius = Math.max(minR, Math.min(maxR, this.radius * scale));
            }
        }, { passive: true });

        this.canvas.addEventListener('touchend', () => {
            this.isPinching = false;
        }, { passive: true });
    },

    onPointerDown(e) {
        if (this.isTransitioning) return;
        this.isDragging = true;
        this.dragMoved = false;
        this.isAutoRotating = false;
        this.lastMouseX = e.clientX;
        this.lastMouseY = e.clientY;
        this.velYaw = 0;
        this.velPitch = 0;
        this.resetIdleTimer();
    },

    onPointerMove(e) {
        if (!this.isDragging) return;
        const dx = e.clientX - this.lastMouseX;
        const dy = e.clientY - this.lastMouseY;
        
        if (Math.hypot(dx, dy) > 4) {
            this.dragMoved = true;
        }

        // Sensitivity
        const speed = 0.0055;
        this.yaw += dx * speed;
        this.pitch = Math.max(-1.3, Math.min(1.3, this.pitch + dy * speed));
        
        this.velYaw = dx * speed;
        this.velPitch = dy * speed;

        this.lastMouseX = e.clientX;
        this.lastMouseY = e.clientY;
        this.resetIdleTimer();
    },

    onPointerUp(e) {
        if (!this.isDragging) return;
        this.isDragging = false;

        // If it was a clean tap (not dragged), check for click on 3D pins
        if (!this.dragMoved && e) {
            this.handleGlobeClick(e.clientX, e.clientY);
        }

        this.resetIdleTimer();
    },

    resetIdleTimer() {
        clearTimeout(this.idleTimer);
        this.idleTimer = setTimeout(() => {
            this.isAutoRotating = true;
        }, 3200);
    },

    focusOnCountry(countryId, animate = true) {
        const country = this.COUNTRIES.find(c => c.id === countryId);
        if (!country) return;

        // Convert lat/lng to target yaw & pitch
        // lng is X rotation, lat is Y rotation
        const targetLngRad = (country.lng * Math.PI) / 180;
        const targetLatRad = (country.lat * Math.PI) / 180;

        // Sphere faces camera when yaw brings lng to front (0 meridian)
        this.targetYaw = -targetLngRad - Math.PI / 2;
        this.targetPitch = targetLatRad;

        if (!animate) {
            this.yaw = this.targetYaw;
            this.pitch = this.targetPitch;
        } else {
            this.isAutoRotating = false;
            // Shortest rotational path
            while (this.targetYaw - this.yaw > Math.PI) this.yaw += Math.PI * 2;
            while (this.targetYaw - this.yaw < -Math.PI) this.yaw -= Math.PI * 2;
        }
    },

    // 3D SPHERICAL PROJECTION MATHEMATICS
    latLngTo3D(latDeg, lngDeg, r = this.radius) {
        const phi = (90 - latDeg) * (Math.PI / 180);
        const theta = (lngDeg + 180) * (Math.PI / 180);

        // Raw 3D point in world space
        let x = -(r * Math.sin(phi) * Math.cos(theta));
        let z = r * Math.sin(phi) * Math.sin(theta);
        let y = r * Math.cos(phi);

        // Apply Yaw (Y-axis rotation)
        const cosY = Math.cos(this.yaw);
        const sinY = Math.sin(this.yaw);
        let x1 = x * cosY - z * sinY;
        let z1 = x * sinY + z * cosY;

        // Apply Pitch (X-axis rotation)
        const cosP = Math.cos(this.pitch);
        const sinP = Math.sin(this.pitch);
        let y2 = y * cosP - z1 * sinP;
        let z2 = y * sinP + z1 * cosP;

        // Perspective 2D projection
        const fov = 800;
        const dist = 700 - z2;
        const scale = dist > 0 ? fov / dist : 0;
        const projX = (this.width / 2) + x1;
        const projY = (this.height / 2) - y2;

        return {
            x: projX,
            y: projY,
            z: z2,
            visible: z2 > -10, // On front hemisphere
            scale
        };
    },

    handleGlobeClick(clientX, clientY) {
        const rect = this.canvas.getBoundingClientRect();
        const clickX = clientX - rect.left;
        const clickY = clientY - rect.top;

        // Check if user tapped a country pin (highest z first)
        const pins = this.COUNTRIES.map(c => {
            const p = this.latLngTo3D(c.lat, c.lng);
            return { country: c, proj: p };
        }).filter(item => item.proj.visible);

        pins.sort((a, b) => b.proj.z - a.proj.z);

        for (const item of pins) {
            const dist = Math.hypot(clickX - item.proj.x, clickY - item.proj.y);
            const hitbox = item.country.status === 'playable' ? 38 : 28;
            if (dist <= hitbox) {
                this.selectCountry(item.country);
                return;
            }
        }
    },

    selectCountry(country) {
        AudioEngine.playPop(3);
        Telemetry.log('globe_country_selected', { countryId: country.id, status: country.status });

        if (country.status === 'playable') {
            // Cinematic zoom transition into Turkey's 81-city map
            this.transitionToPlayableCountry(country);
        } else {
            // Show preview modal with 5 iconic landmarks
            this.showLockedCountryModal(country);
        }
    },

    transitionToPlayableCountry(country) {
        this.isTransitioning = true;
        this.focusOnCountry(country.id, true);

        // Smooth camera zoom
        const startR = this.radius;
        const endR = this.radius * 3.2;
        const startTime = performance.now();
        const duration = 750;

        const zoomStep = (now) => {
            const elapsed = now - startTime;
            const progress = Math.min(1, elapsed / duration);
            const ease = progress * (2 - progress); // Ease-out

            this.radius = startR + (endR - startR) * ease;

            if (progress < 1) {
                requestAnimationFrame(zoomStep);
            } else {
                this.isTransitioning = false;
                this.radius = startR; // Reset for next time
                if (window.ScreenRouter) {
                    ScreenRouter.goTo('screen-country', { countryId: country.id });
                }
            }
        };

        requestAnimationFrame(zoomStep);
    },

    showLockedCountryModal(country) {
        const modal = document.getElementById('modal-country-preview');
        if (!modal) return;

        const title = document.getElementById('country-preview-title');
        const flag = document.getElementById('country-preview-flag');
        const desc = document.getElementById('country-preview-desc');
        const list = document.getElementById('country-preview-landmarks');

        if (title) title.innerText = country.name;
        if (flag) flag.innerText = country.flag;
        
        const countryData = (window.COUNTRIES_DATA || []).find(c => c.id === country.id);
        if (desc && countryData) {
            desc.innerText = countryData.description || 'Bu ülkenin simge mekânları ve kelime seferleri hazırlanıyor.';
        }
        if (list && countryData && countryData.sampleLandmarks) {
            list.innerHTML = countryData.sampleLandmarks.map(lm => `
                <li class="landmark-preview-pill">
                    <span class="pill-dot">✦</span>
                    <span class="pill-text">${lm}</span>
                </li>
            `).join('');
        }

        modal.classList.remove('hidden');
    },

    isPaused: false,

    startLoop() {
        if (this.animId) cancelAnimationFrame(this.animId);
        this.isPaused = false;
        const render = () => {
            if (!this.isPaused) {
                this.update();
                this.draw();
                this.animId = requestAnimationFrame(render);
            }
        };
        this.animId = requestAnimationFrame(render);
    },

    pause() {
        this.isPaused = true;
        if (this.animId) {
            cancelAnimationFrame(this.animId);
            this.animId = null;
        }
    },

    resume() {
        if (this.isPaused || !this.animId) {
            this.startLoop();
        }
    },

    update() {
        if (this.isTransitioning) return;

        // Apply inertia physics
        if (!this.isDragging) {
            if (this.isAutoRotating) {
                this.yaw += 0.0018; // Gentle celestial spin
            } else {
                this.yaw += this.velYaw;
                this.pitch = Math.max(-1.3, Math.min(1.3, this.pitch + this.velPitch));
                this.velYaw *= 0.92;
                this.velPitch *= 0.92;
            }
        }
    },

    draw() {
        if (!this.ctx || this.width === 0) return;
        const ctx = this.ctx;
        const cx = this.width / 2;
        const cy = this.height / 2;
        const r = this.radius;

        ctx.clearRect(0, 0, this.width, this.height);

        // 1. Atmosphere Rim Glow (Multi-layer radial gradient)
        const atmoGrad = ctx.createRadialGradient(cx, cy, r * 0.85, cx, cy, r * 1.35);
        atmoGrad.addColorStop(0, 'rgba(56, 96, 92, 0.45)');
        atmoGrad.addColorStop(0.5, 'rgba(212, 175, 55, 0.15)');
        atmoGrad.addColorStop(1, 'rgba(15, 23, 42, 0)');
        ctx.fillStyle = atmoGrad;
        ctx.beginPath();
        ctx.arc(cx, cy, r * 1.35, 0, Math.PI * 2);
        ctx.fill();

        // 2. Ocean Sphere
        const oceanGrad = ctx.createRadialGradient(cx - r * 0.3, cy - r * 0.35, r * 0.1, cx, cy, r);
        oceanGrad.addColorStop(0, '#1e293b');
        oceanGrad.addColorStop(0.65, '#0f172a');
        oceanGrad.addColorStop(1, '#070d1e');
        ctx.fillStyle = oceanGrad;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.fill();

        // 3. Latitude & Longitude Meridians
        ctx.save();
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.clip(); // Clip inside sphere

        ctx.strokeStyle = 'rgba(212, 175, 55, 0.12)';
        ctx.lineWidth = 1;

        // Longitudes every 30 deg
        for (let lng = -180; lng <= 180; lng += 30) {
            ctx.beginPath();
            let first = true;
            for (let lat = -80; lat <= 80; lat += 10) {
                const pt = this.latLngTo3D(lat, lng, r);
                if (pt.visible) {
                    if (first) { ctx.moveTo(pt.x, pt.y); first = false; }
                    else ctx.lineTo(pt.x, pt.y);
                } else {
                    first = true;
                }
            }
            ctx.stroke();
        }

        // Latitudes every 30 deg
        for (let lat = -60; lat <= 60; lat += 30) {
            ctx.beginPath();
            let first = true;
            for (let lng = -180; lng <= 180; lng += 10) {
                const pt = this.latLngTo3D(lat, lng, r);
                if (pt.visible) {
                    if (first) { ctx.moveTo(pt.x, pt.y); first = false; }
                    else ctx.lineTo(pt.x, pt.y);
                } else {
                    first = true;
                }
            }
            ctx.stroke();
        }

        // 4. Continent Outlines
        ctx.fillStyle = 'rgba(56, 96, 92, 0.42)';
        ctx.strokeStyle = '#d4af37';
        ctx.lineWidth = 1.2;

        this.CONTINENTS.forEach(poly => {
            ctx.beginPath();
            let first = true;
            poly.forEach(coord => {
                const pt = this.latLngTo3D(coord.lat, coord.lng, r);
                if (pt.visible) {
                    if (first) { ctx.moveTo(pt.x, pt.y); first = false; }
                    else ctx.lineTo(pt.x, pt.y);
                }
            });
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
        });

        // Sphere highlight / rim shadow
        const rimGrad = ctx.createRadialGradient(cx + r * 0.6, cy + r * 0.6, r * 0.2, cx, cy, r);
        rimGrad.addColorStop(0, 'rgba(0, 0, 0, 0.65)');
        rimGrad.addColorStop(0.7, 'rgba(0, 0, 0, 0.1)');
        rimGrad.addColorStop(1, 'rgba(212, 175, 55, 0.18)');
        ctx.fillStyle = rimGrad;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore(); // End sphere clipping

        // 5. Draw 3D Interactive Country Pins
        const visiblePins = this.COUNTRIES.map(c => {
            const pt = this.latLngTo3D(c.lat, c.lng, r);
            return { country: c, pt };
        }).filter(item => item.pt.visible);

        // Sort by Z (render frontmost last)
        visiblePins.sort((a, b) => a.pt.z - b.pt.z);

        visiblePins.forEach(({ country, pt }) => {
            this.drawPin(ctx, country, pt.x, pt.y, pt.z);
        });
    },

    drawPin(ctx, country, px, py, pz) {
        const isPlayable = country.status === 'playable';
        const alpha = Math.max(0.3, Math.min(1, (pz + this.radius * 0.5) / (this.radius * 1.2)));

        ctx.save();
        ctx.globalAlpha = alpha;

        if (isPlayable) {
            // Pulsating golden beacon for playable Turkey
            const pulse = (Math.sin(performance.now() * 0.005) + 1) * 0.5;
            
            // Outer radiant aura
            ctx.fillStyle = `rgba(212, 175, 55, ${0.25 + pulse * 0.25})`;
            ctx.beginPath();
            ctx.arc(px, py, 18 + pulse * 6, 0, Math.PI * 2);
            ctx.fill();

            // Inner pin circle
            ctx.fillStyle = '#d4af37';
            ctx.beginPath();
            ctx.arc(px, py, 10, 0, Math.PI * 2);
            ctx.fill();

            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 2.5;
            ctx.stroke();

            // Flag badge
            ctx.font = 'bold 13px system-ui, sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = '#ffffff';
            ctx.fillText(country.flag, px, py);

            // Prominent Title Banner
            ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
            const label = `🇹🇷 ${country.name} (BAŞLA)`;
            ctx.font = 'bold 12px system-ui, sans-serif';
            const textW = ctx.measureText(label).width + 16;
            
            ctx.beginPath();
            ctx.roundRect(px - textW / 2, py - 28, textW, 20, 10);
            ctx.fill();
            ctx.strokeStyle = '#d4af37';
            ctx.lineWidth = 1.5;
            ctx.stroke();

            ctx.fillStyle = '#f59e0b';
            ctx.fillText(label, px, py - 18);
        } else {
            // Subtle locked pin
            ctx.fillStyle = '#1e293b';
            ctx.beginPath();
            ctx.arc(px, py, 7.5, 0, Math.PI * 2);
            ctx.fill();

            ctx.strokeStyle = '#64748b';
            ctx.lineWidth = 1.5;
            ctx.stroke();

            ctx.font = '9px system-ui, sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = '#94a3b8';
            ctx.fillText('🔒', px, py);

            // Label
            ctx.font = '10px system-ui, sans-serif';
            ctx.fillStyle = '#cbd5e1';
            ctx.fillText(`${country.flag} ${country.name}`, px, py - 13);
        }

        ctx.restore();
    }
};

if (typeof window !== 'undefined') {
    window.Globe3D = Globe3D;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Globe3D;
}

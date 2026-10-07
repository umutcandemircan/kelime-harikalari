// TÜRKÇE KARAKTER DÖNÜŞÜM YARDIMCILARI & ASSET FALLBACK UTILITIES
const trUpper = (s) => s ? s.replace(/i/g, 'İ').replace(/ı/g, 'I').toLocaleUpperCase('tr-TR') : '';
const trLower = (s) => s ? s.replace(/İ/g, 'i').replace(/I/g, 'ı').toLocaleLowerCase('tr-TR') : '';

// High-resolution verified Anatolian photography fallback
const DEFAULT_HERITAGE_PHOTO = 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=1280&q=80';

function setupPhotoWithFallback(imgEl, photoUrl, containerEl) {
    if (!imgEl) return;
    if (containerEl) {
        containerEl.classList.add('skeleton-shimmer');
    }
    imgEl.onload = () => {
        if (containerEl) {
            containerEl.classList.remove('skeleton-shimmer');
            containerEl.classList.remove('polaroid-fallback');
        }
    };
    imgEl.onerror = () => {
        if (containerEl) {
            containerEl.classList.remove('skeleton-shimmer');
            containerEl.classList.add('polaroid-fallback');
        }
        if (imgEl.src !== DEFAULT_HERITAGE_PHOTO) {
            imgEl.src = DEFAULT_HERITAGE_PHOTO;
        }
        imgEl.onerror = null;
    };
    imgEl.src = photoUrl || DEFAULT_HERITAGE_PHOTO;
}

if (typeof window !== 'undefined') {
    window.trUpper = trUpper;
    window.trLower = trLower;
    window.setupPhotoWithFallback = setupPhotoWithFallback;
    window.DEFAULT_HERITAGE_PHOTO = DEFAULT_HERITAGE_PHOTO;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { trUpper, trLower, setupPhotoWithFallback, DEFAULT_HERITAGE_PHOTO };
}

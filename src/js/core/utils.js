// TÜRKÇE KARAKTER DÖNÜŞÜM YARDIMCISI
const trUpper = (s) => s ? s.replace(/i/g, 'İ').replace(/ı/g, 'I').toLocaleUpperCase('tr-TR') : '';
const trLower = (s) => s ? s.replace(/İ/g, 'i').replace(/I/g, 'ı').toLocaleLowerCase('tr-TR') : '';

// AUTHENTIC ANATOLIAN DEFAULT PHOTOGRAPHY FALLBACK (NO FAKE SVGS WITH BANNERS)
const DEFAULT_HERITAGE_PHOTO = 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=1280&q=80';

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
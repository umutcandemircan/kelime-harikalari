// TÜRKÇE KARAKTER DÖNÜŞÜM YARDIMCISI
const trUpper = (s) => s ? s.replace(/i/g, 'İ').replace(/ı/g, 'I').toLocaleUpperCase('tr-TR') : '';
const trLower = (s) => s ? s.replace(/İ/g, 'i').replace(/I/g, 'ı').toLocaleLowerCase('tr-TR') : '';
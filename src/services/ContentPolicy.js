// CONTENT POLICY FILTER SERVICE (VERSIONED)
const ContentPolicy = {
    VERSION: '2.0.0',
    
    // Normalized inappropriate keywords (profanity, vulgarity, adult terms)
    BLOCKED_TERMS: new Set([
        "AMK", "AQ", "SIK", "OROSPU", "PIC", "PİÇ", "YARRAK", "YARAK", "GOT", "GÖT",
        "IBNE", "İBNE", "KAHPE", "SİKİŞ", "SIKIS", "PEZEVENK", "SIKTIR", "SİKTİR",
        "AMCIK", "TASSAK", "TAŞŞAK", "DÖL", "DOL", "BOŞAL", "BOSAL", "PORNO",
        "EROTIK", "EROTİK", "SEKS", "SEX", "FAHISE", "FAHİŞE", "GEY", "LEZBIYEN"
    ]),

    normalize(word) {
        if (!word || typeof word !== 'string') return '';
        return word
            .trim()
            .replace(/i/g, 'İ')
            .replace(/ı/g, 'I')
            .toUpperCase();
    },

    /**
     * Checks if a word violates the family-friendly game content policy.
     * @param {string} word - The candidate word to check
     * @returns {{ allowed: boolean, reason?: string }}
     */
    check(word) {
        const clean = this.normalize(word);
        if (!clean) {
            return { allowed: false, reason: 'EMPTY_WORD' };
        }

        // Exact match against normalized blocklist
        if (this.BLOCKED_TERMS.has(clean)) {
            return {
                allowed: false,
                reason: 'INAPPROPRIATE_CONTENT'
            };
        }

        return { allowed: true };
    }
};

if (typeof window !== 'undefined') {
    window.ContentPolicy = ContentPolicy;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ContentPolicy;
}

// CENTRAL WORD VALIDATION AUTHORITY (V2)
const WordValidator = {
    DICTIONARY_VERSION: '2.0.0',
    CONTENT_POLICY_VERSION: '2.0.0',
    
    dictSet: null,

    init(dictArray) {
        if (dictArray && Array.isArray(dictArray)) {
            this.dictSet = new Set(dictArray.map(w => ContentPolicy.normalize(w)));
        } else if (typeof window !== 'undefined' && window.TDK_DICT_FULL) {
            this.dictSet = new Set(window.TDK_DICT_FULL.map(w => ContentPolicy.normalize(w)));
        } else {
            this.dictSet = new Set();
        }
    },

    getDictSet() {
        if (!this.dictSet) {
            this.init();
        }
        return this.dictSet;
    },

    /**
     * Single authority for word validation in the game.
     * @param {string} rawWord - The input word to validate
     * @param {string} [dictVer] - Optional dictionary version snapshot
     * @param {string} [policyVer] - Optional content policy version
     * @returns {{ valid: boolean, word: string, reason?: string }}
     */
    validateWord(rawWord, dictVer = this.DICTIONARY_VERSION, policyVer = this.CONTENT_POLICY_VERSION) {
        const word = ContentPolicy.normalize(rawWord);
        
        if (!word || word.length < 2) {
            return { valid: false, word, reason: 'TOO_SHORT' };
        }

        // 1. Content Policy Check
        const policyResult = ContentPolicy.check(word);
        if (!policyResult.allowed) {
            return {
                valid: false,
                word,
                reason: policyResult.reason || 'CONTENT_POLICY_VIOLATION'
            };
        }

        // 2. Dictionary Snapshot Check
        const dict = this.getDictSet();
        if (!dict.has(word)) {
            return {
                valid: false,
                word,
                reason: 'NOT_IN_DICTIONARY'
            };
        }

        return { valid: true, word };
    }
};

if (typeof window !== 'undefined') {
    window.WordValidator = WordValidator;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WordValidator;
}

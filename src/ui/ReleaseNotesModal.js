// RELEASE NOTIFICATION MODAL ("NELER YENİ?")
const ReleaseNotesModal = {
    checkAndShow() {
        const lastSeen = SaveManager.data.lastSeenVersion;
        const current = SaveManager.CURRENT_APP_VERSION;

        if (lastSeen !== current) {
            SaveManager.data.lastSeenVersion = current;
            SaveManager.save();
            this.open();
        }
    },

    open() {
        const modal = document.getElementById('modal-release-notes');
        if (modal) modal.classList.remove('hidden');
    },

    close() {
        const modal = document.getElementById('modal-release-notes');
        if (modal) modal.classList.add('hidden');
    }
};

if (typeof window !== 'undefined') {
    window.ReleaseNotesModal = ReleaseNotesModal;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReleaseNotesModal;
}

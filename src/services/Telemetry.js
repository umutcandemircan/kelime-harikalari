// PRIVACY-FIRST LOCAL TELEMETRY SERVICE
const Telemetry = {
    ENABLED: true,
    MAX_BUFFER: 50,
    events: [],

    log(eventName, payload = {}) {
        if (!this.ENABLED) return;
        const entry = {
            event: eventName,
            payload,
            timestamp: new Date().toISOString()
        };
        this.events.push(entry);
        if (this.events.length > this.MAX_BUFFER) {
            this.events.shift();
        }
        if (typeof console !== 'undefined' && console.debug) {
            console.debug(`[Telemetry] ${eventName}`, payload);
        }
    },

    getRecentEvents() {
        return [...this.events];
    },

    clear() {
        this.events = [];
    }
};

if (typeof window !== 'undefined') {
    window.Telemetry = Telemetry;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Telemetry;
}

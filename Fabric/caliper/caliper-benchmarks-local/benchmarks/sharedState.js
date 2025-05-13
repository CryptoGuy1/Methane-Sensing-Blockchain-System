'use strict';

class SharedState {
    constructor() {
        this.assetIds = [];
        this.lock = false;
    }

    addAssetId(id) {
        if (!this.lock) {
            this.assetIds.push(id);
        }
    }

    getAssetIds() {
        return this.assetIds;
    }

    lockState() {
        this.lock = true;
    }

    isEmpty() {
        return this.assetIds.length === 0;
    }
}

module.exports = new SharedState();  // Ensure this exports a singleton instance

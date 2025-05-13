'use strict';
const { WorkloadModuleBase } = require('@hyperledger/caliper-core');
const { v4: uuidv4 } = require('uuid');
const sharedState = require('./sharedState');

class CreateAssetWorkload extends WorkloadModuleBase {
    constructor() {
        super();
    }

    async submitTransaction() {
        // Create an asset object 
        let asset = {
            ID: uuidv4(),
            Timestamp: new Date().toISOString(),
            MethaneLevel: Math.floor(Math.random() * 4000).toString() // Random methane level
        };

        try {
            let args = {
                contractId: 'basic', // Ensure contractId matches your chaincode name
                contractFunction: 'CreateAsset',
                contractArguments: [
                    asset.ID,
                    asset.Timestamp,
                    asset.MethaneLevel
                ],
                timeout: 30
            };
            
            const result = await this.sutAdapter.sendRequests(args);
            
            // Only add to shared state if transaction was successful
            if (result && result[0] && result[0].status === 'success') {
                sharedState.addAssetId(asset.ID);  // Store only the asset ID
                console.log(`Asset created: ${asset.ID}`);
            } else {
                console.error('Asset creation failed', result);
            }
        } catch (error) {
            console.error('Error creating asset:', error);
        }
    }
}

function createWorkloadModule() {
    return new CreateAssetWorkload();
}

module.exports.createWorkloadModule = createWorkloadModule;

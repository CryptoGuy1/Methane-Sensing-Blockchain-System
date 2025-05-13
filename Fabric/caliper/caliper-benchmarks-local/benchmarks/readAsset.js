'use strict';
const { WorkloadModuleBase } = require('@hyperledger/caliper-core');
const { v4: uuidv4 } = require('uuid');

class MyWorkload extends WorkloadModuleBase {
    constructor() {
        super();
        this.assetIds = []; // Array to store asset IDs
    }

    async initializeWorkloadModule(
        workerIndex,
        totalWorkers,
        roundIndex,
        roundArguments,
        sutAdapter,
        sutContext
    ) {
        await super.initializeWorkloadModule(
            workerIndex,
            totalWorkers,
            roundIndex,
            roundArguments,
            sutAdapter,
            sutContext
        );

        for (let i = 0; i < this.roundArguments.assets; i++) {
            const assetId = uuidv4();
            const timestamp = new Date().toISOString();
            console.log(`Worker ${this.workerIndex}: Creating asset ${assetId}`);
            this.assetIds.push(assetId); // Store asset ID
            const request = {
                contractId: this.roundArguments.contractId,
                contractFunction: 'CreateAsset',
                invokerIdentity: 'User1',
                contractArguments: [assetId, timestamp, '0'], // Pass assetId, timestamp, and methanelevel
                readOnly: false,
            };
            await this.sutAdapter.sendRequests(request);
        }
    }

    async submitTransaction() {
        const randomIndex = Math.floor(Math.random() * this.assetIds.length);
        const assetId = this.assetIds[randomIndex]; // Get asset ID for the chosen asset
     
        const myArgs = {
            contractId: this.roundArguments.contractId,
            contractFunction: 'ReadAsset',
            invokerIdentity: 'User1',
            contractArguments: [assetId], // Use asset ID
            readOnly: true,
        };
     
        await this.sutAdapter.sendRequests(myArgs);
    }
     
    async cleanupWorkloadModule() {
        for (const assetId of this.assetIds) {
            const request = {
                contractId: this.roundArguments.contractId,
                contractFunction: 'DeleteAsset',
                invokerIdentity: 'User1',
                contractArguments: [assetId], // Use asset ID
                readOnly: false,
            };
            await this.sutAdapter.sendRequests(request);
        }
    }
}

function createWorkloadModule() {
    return new MyWorkload();
}

module.exports.createWorkloadModule = createWorkloadModule;
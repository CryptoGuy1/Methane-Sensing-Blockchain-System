const grpc = require('@grpc/grpc-js');
const { connect, GatewayError } = require('@hyperledger/fabric-gateway');
const { TextDecoder } = require('util');
const { newGrpcConnection, newIdentity, newSigner } = require('./connect');
const {Board, Led} = require('johnny-five');

const channelName = 'mychannel';
const chaincodeName = 'basic';

const utf8Decoder = new TextDecoder();

async function main() {
    const client = await newGrpcConnection();
    const gateway = connect({
        client,
        identity: await newIdentity(),
        signer: await newSigner(),
        evaluateOptions: () => {
            return { deadline: Date.now() + 5000 }; // 5 seconds
        },
        endorseOptions: () => {
            return { deadline: Date.now() + 15000 }; // 15 seconds
        },
        submitOptions: () => {
            return { deadline: Date.now() + 5000 }; // 5 seconds
        },
        commitStatusOptions: () => {
            return { deadline: Date.now() + 60000 }; // 1 minute
        },
    });

    try {
        const network = gateway.getNetwork(channelName);
        
        console.log('\n*** Start chaincode event listening');
        const events = await network.getChaincodeEvents(chaincodeName);

        // Initialize the Johnny-Five board
        const board = new Board();
        let led;

        board.on('ready', () => {
            led = new Led(13);
            console.log('Board is ready');
        });

        console.log('Waiting for chaincode events...');

        try {
            for await (const event of events) {
                const payload = parseJson(event.payload);
                console.log(payload, event.payload);
                console.log(`\n<-- Chaincode event received: ${event.eventName} -`, payload);
                if (event.eventName === 'HighMethaneLevel') {
                //const eventPayload = JSON.parse(event.payload.toString());
                //console.log(eventPayload);
                console.log(`Event received: ${event.eventName} with payload: ${event.payload.toString()}`);

                if (led && payload.Methanelevel > 3000) {
                    led.on();
                    console.log('LED is ON due to high methane level');
                    setTimeout(() => {
                        led.off();
                        console.log('LED is OFF');
                    }, 5000); // Turn off after 5 seconds
                }
            }
            }
        } catch (error) {
            if (error instanceof GatewayError && error.code === grpc.status.CANCELLED) {
                console.log('Event stream has been closed');
            } else {
                console.error(`Error processing events: ${error}`);
            }
        }
    } finally {
        gateway.close();
        client.close();
    }
}

main().catch((error) => {
    console.error('******** FAILED to run the application:', error);
    process.exitCode = 1;
});

function parseJson(jsonBytes) {
    const json = utf8Decoder.decode(jsonBytes);
    return JSON.parse(json);
}

const Web3 = require('web3');
const { Board, Led } = require('johnny-five');
const contractJson = require('../build/contracts/AssetContract.json');

const web3 = new Web3('ws://localhost:8546'); // WebSocket connection to Besu
const board = new Board();
let led;

board.on('ready', async () => {
    console.log('Board is ready');
    led = new Led(13);

    const networkId = await web3.eth.net.getId();
    const deployedAddress = contractJson.networks[networkId].address;
    const contract = new web3.eth.Contract(contractJson.abi, deployedAddress);

    console.log('Listening for HighMethaneLevel events...');
    contract.events.HighMethaneLevel()
        .on('data', (event) => {
            const { id, timestamp, methaneLevel } = event.returnValues;
            console.log(`High Methane Event: ${methaneLevel} ppm at ${timestamp}`);

            if (Number(methaneLevel) > 3000) {
                led.on();
                console.log('LED ON 🚨');

                setTimeout(() => {
                    led.off();
                    console.log('LED OFF');
                }, 5000);
            }
        })
        .on('error', console.error);
});

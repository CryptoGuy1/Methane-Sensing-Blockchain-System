const path = require('path');
const fs = require('fs-extra');
const Web3 = require('web3');
const Web3Quorum = require('web3js-quorum');
const express = require('express');
const bodyParser = require('body-parser');

// WARNING: the keys here are demo purposes ONLY. Please use a tool like EthSigner for production, rather than hard coding private keys
const { tessera, besu } = require('../keys.js');
const chainId = 1337;
// abi and bytecode generated from simplestorage.sol:
// > solcjs --bin --abi simplestorage.sol
const contractJsonPath = path.resolve(
  __dirname,
  '../../',
  'contracts',
  'AssetContract.json'
);
const contractJson = JSON.parse(fs.readFileSync(contractJsonPath));
const contractBytecode = contractJson.evm.bytecode.object;
const contractAbi = contractJson.abi;

// Besu doesn't support eth_sendTransaction so we use the eea_sendRawTransaction(https://besu.hyperledger.org/en/latest/Reference/API-Methods/#eea_sendrawtransaction) for things like simple value transfers, contract creation or contract invocation
async function createContract(
  clientUrl,
  fromPrivateKey,
  fromPublicKey,
  toPublicKey
) {
  const web3 = new Web3(clientUrl);
  const web3quorum = new Web3Quorum(web3, chainId);
  // initialize the default constructor with a value `47 = 0x2F`; this value is appended to the bytecode
  const contractConstructorInit = web3.eth.abi
    .encodeParameter('uint256', '47')
    .slice(2);
  const txOptions = {
    data: '0x' + contractBytecode + contractConstructorInit,
    privateKey: fromPrivateKey,
    privateFrom: fromPublicKey,
    privateFor: [toPublicKey],
  };
  console.log('Creating contract...');
  // Generate and send the Raw transaction to the Besu node using the eea_sendRawTransaction(https://besu.hyperledger.org/en/latest/Reference/API-Methods/#eea_sendrawtransaction) JSON-RPC call
  const txHash = await web3quorum.priv.generateAndSendRawTransaction(txOptions);
  console.log('Getting contractAddress from txHash: ', txHash);
  const privateTxReceipt = await web3quorum.priv.waitForTransactionReceipt(
    txHash
  );
  console.log('Private Transaction Receipt: ', privateTxReceipt);
  return privateTxReceipt;
}

async function getValueAtAddress(
  clientUrl,
  nodeName = 'node',
  address,
  contractAbi,
  fromPrivateKey,
  fromPublicKey,
  toPublicKey
) {
  const web3 = new Web3(clientUrl);
  const web3quorum = new Web3Quorum(web3, chainId);
  const contract = new web3quorum.eth.Contract(contractAbi);
  // eslint-disable-next-line no-underscore-dangle
  const functionAbi = contract._jsonInterface.find((e) => {
    return e.name === 'getAssets';
  });
  const functionParams = {
    to: address,
    data: functionAbi.signature,
    privateKey: fromPrivateKey,
    privateFrom: fromPublicKey,
    privateFor: [toPublicKey],
  };
  const transactionHash = await web3quorum.priv.generateAndSendRawTransaction(
    functionParams
  );
  // console.log(`Transaction hash: ${transactionHash}`);
  const result = await web3quorum.priv.waitForTransactionReceipt(
    transactionHash
  );
  console.log(
    '' + nodeName + ' value from deployed contract is: ' + result.output
  );
  const decodedOutput = web3quorum.eth.abi.decodeParameters(
    functionAbi.outputs, // Array of output types from ABI
    result.output
  );
  console.log(decodedOutput)
  const response = [];
for (const assetData of decodedOutput['0']) {
  const methaneLevel = assetData[0]; // Access methaneLevel value
  const timestamp = assetData[1]; // Access timestamp value
  response.push({ methaneLevel, timestamp }); // Add object to response array
}
console.log(response)
  /*const methaneLevel = decodedOutput[0].toNumber(); // Convert uint256 to number
  const timestamp = decodedOutput[1];
console.log(methaneLevel, timestamp)*/  
  return response;
}

async function setValueAtAddress(
  clientUrl,
  address,
  methaneLevel,
  timestamp,
  contractAbi,
  fromPrivateKey,
  fromPublicKey,
  toPublicKey
) {
  const web3 = new Web3(clientUrl);
  const web3quorum = new Web3Quorum(web3, chainId);
  const contract = new web3quorum.eth.Contract(contractAbi);
  // eslint-disable-next-line no-underscore-dangle
  const functionAbi = contract._jsonInterface.find((e) => {
    return e.name === 'createAsset';
  });
  const functionArgs = web3quorum.eth.abi
    .encodeParameters(functionAbi.inputs, [methaneLevel, timestamp])
    .slice(2);
  const functionParams = {
    to: address,
    data: functionAbi.signature + functionArgs,
    privateKey: fromPrivateKey,
    privateFrom: fromPublicKey,
    privateFor: [toPublicKey],
  };
  const transactionHash = await web3quorum.priv.generateAndSendRawTransaction(
    functionParams
  );
  console.log(`Transaction hash: ${transactionHash}`);
  const result = await web3quorum.priv.waitForTransactionReceipt(
    transactionHash
  );
  return result;
}

async function main() {
  try {
    const privateTxReceipt = await createContract(
      besu.member1.url,
      besu.member1.accountPrivateKey,
      tessera.member1.publicKey,
      tessera.member3.publicKey
    );
    console.log('Address of transaction: ', privateTxReceipt.contractAddress);

    // Wait for the blocks to propagate to the other nodes
    await new Promise((r) => setTimeout(r, 20000));

    console.log(
      "Use the smart contract's 'get' function to read the contract's constructor initialized value .. "
    );
    await getValueAtAddress(
      besu.member1.url,
      'Member1',
      privateTxReceipt.contractAddress,
      contractAbi,
      besu.member1.accountPrivateKey,
      tessera.member1.publicKey,
      tessera.member3.publicKey
    );

    const app = express();
    app.use(bodyParser.json());

    app.get('/assets', async (req, res) => {
      try {
        const value = await getValueAtAddress(
          besu.member1.url,
          'Member1',
          privateTxReceipt.contractAddress,
          contractAbi,
          besu.member1.accountPrivateKey,
          tessera.member1.publicKey,
          tessera.member3.publicKey
        );
        res.send(value);
      } catch (error) {
        res.status(500).send(error.toString());
      }
    });

    // REST API to set value in the contract
    app.post('/assets', async (req, res) => {
      const { methaneLevel, timestamp } = req.body;
      try {
         await setValueAtAddress(
          besu.member1.url,
          privateTxReceipt.contractAddress,
          methaneLevel, 
          timestamp,
          contractAbi,
          besu.member1.accountPrivateKey,
          tessera.member1.publicKey,
          tessera.member3.publicKey
        );
        const data = {
          status: "OK",
          message: "SUCCESSFUL",
          data: null
        }
        res.send(data);
      } catch (error) {
        res.status(500).send(error.toString());
      }
    });

    const PORT = process.env.PORT || 3002;
    app.listen(PORT, () => {
      console.log(`Server is running on port ${PORT}`);
    });
  } catch (error) {
    console.error(error);
  }
}

if (require.main === module) {
  main();
}

module.exports = exports = main;

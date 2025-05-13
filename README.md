# Methane Sensing Blockchain System

This repository contains a comprehensive implementation of a real-time methane sensing system built using both **Hyperledger Fabric** and **Hyperledger Besu (Quorum)**. The system stores methane concentration data on-chain and triggers a physical LED alert via Arduino using the **Johnny-Five** library when dangerous levels are detected.

This README includes setup instructions for both platforms, benchmark execution with **Caliper**, and integration with a custom backend REST API.

---

## 🧰 Prerequisites

Ensure the following are installed:

* Git
* Curl
* Docker (v24+) and Docker Compose (v1.29+)
* Node.js (v18+)
* Redis
* Python 3
* JQ, Go, Python, Java (for Fabric)

---

## 📦 Step-by-Step: Hyperledger Fabric Setup

### A. Install Fabric and Its Samples

```bash
mkdir ~/fabric
cd ~/fabric
curl -sSLO https://raw.githubusercontent.com/hyperledger/fabric/main/scripts/install-fabric.sh
chmod +x install-fabric.sh
./install-fabric.sh
```

### B. Clone This Repository

```bash
# Clone your implementation repo 
git clone https://github.com/your-username/methane-blockchain-sensor.git
```

### C. Place Custom Code
cd ~/fabric/fabric-samples/asset-transfer-basic
```bash
cp -r methane-blockchain-sensor/methane_sensor_chaincode ./
cp -r methane-blockchain-sensor/methane_sensor_backend ./
```

---

## 🚀 Fabric Network Launch

### Step 1: Start Network

```bash
cd ../../test-network
./network.sh up
```

Verify containers:

```bash
docker ps -a
```

### Step 2: Create Channel

```bash
./network.sh createChannel -c mychannel
```

### Step 3: Deploy Chaincode

```bash
./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/methane_sensor_chaincode -ccl typescript
```

---

## 🔄 Interact with Chaincode

### Step 4.1: Set Fabric Environment Variables

```bash
export PATH=${PWD}/../bin:$PATH
export FABRIC_CFG_PATH=$PWD/../config/
```

### Step 4.2: Set Org1 Environment

```bash
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051
```

### Step 4.3: Initialize Ledger

```bash
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com \
--tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem \
-C mychannel -n basic \
--peerAddresses localhost:7051 \
--tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt \
--peerAddresses localhost:9051 \
--tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt \
-c '{"function":"InitLedger","Args":[]}'
```

### Step 4.4: Query Ledger

```bash
peer chaincode query -C mychannel -n basic -c '{"Args":["GetAllAssets"]}'
```

---

## 💡 Fabric: Johnny-Five Event Listener

```bash
cd ~/fabric/fabric-samples/asset-transfer-basic/j5
node johnny5.js
```

---

## 🌐 Fabric: REST Server Setup
cd ~/fabric/fabric-samples/asset-transfer-basic/methane-sensor-backend/
### Step 1: Install and Build

```bash
cd ../
npm install
npm run build
```

### Step 2: Export Environment Variables

```bash
export PRIVATE_KEY_FILE_ORG1=<path>
export CERTIFICATE_FILE_ORG1=<path>
export CONNECTION_PROFILE_FILE_ORG1=<path>
export PRIVATE_KEY_FILE_ORG2=<path>
export CERTIFICATE_FILE_ORG2=<path>
export CONNECTION_PROFILE_FILE_ORG2=<path>
```

### Step 3: Generate ENV

```bash
TEST_NETWORK_HOME=~/fabric/fabric-samples/test-network
npm run generateEnv
```

### Step 4: Start Redis

```bash
export REDIS_PASSWORD=$(uuidgen)
npm run start:redis
```

> If you get a port binding error, run:

```bash
docker stop <container_id>
docker rm <container_id>
```

Then restart Redis.

### Step 5: Start Dev Server

```bash
npm run start:dev
```

---

## ⚖️ Benchmarking with Caliper (Fabric)

### Step 1: Install and Bind

```bash
npm install --only=prod @hyperledger/caliper-cli@0.6 -g

npx caliper bind --caliper-bind-sut fabric:2.2
```

### Step 2: Run Benchmark

```bash
cd ~/fabric/fabric-samples/caliper-benchmarks-local/benchmarks
npx caliper launch manager \
--caliper-workspace ./ \
--caliper-networkconfig ../networks/networkConfig.yaml \
--caliper-benchconfig myAssetBenchmark.yaml \
--caliper-flow-only-test
```

---

## ⚙️ Hyperledger Besu (Quorum) Setup

### Step 1: Install Quorum Test Network

```bash
cd ~
git clone https://github.com/ConsenSys/quorum-test-network.git
cd quorum-test-network
```

### Step 2: Stop Existing Network (if running)

```bash
sudo ./stop.sh
sudo ./remove.sh
```

### Step 3: Start the Besu Network

```bash
sudo ./run.sh
```

### Step 4: Place Custom Files

* Copy your smart contract (`AssetContract.sol`) into the contracts folder
* Copy the event listener script `johnny5_besu.js` into `scripts/privacy`

### Step 5: Deploy Smart Contract Using Remix

1. Open [Remix IDE](https://remix.ethereum.org)
2. Paste `AssetContract.sol` into a new file
3. Compile with Solidity v0.8+
4. Connect MetaMask to `http://localhost:8545`
5. Deploy the contract
6. Copy the contract's **ABI** from Remix
7. Paste the ABI into a local JSON file (e.g. `contractABI.json`) used in `johnny5_besu.js`

### Step 6: Run Besu Transaction Server

```bash
node scripts/privacy/besutxserver.js
```

> Runs on port `3002`

### Step 7: Run the Johnny-Five Event Listener

```bash
cd scripts/privacy
node johnny5_besu.js
```

This listens for the `HighMethaneLevel` event and triggers an LED on Arduino.

---

## 📊 Benchmarking with Caliper (Besu)

### Step 1: Install and Bind Caliper

```bash
npx caliper bind --caliper-bind-sut besu:latest
```

### Step 2: Start the 1-Node Clique Network

```bash
docker-compose -f ./networks/besu/1node-clique/docker-compose.yml up -d
```

Check container status:

```bash
docker ps -a
```

### Step 3: Run Benchmark

```bash
cd quorum-test-network/caliper-benchmarks/benchmarks
npx caliper launch manager \
--caliper-benchconfig scenario/simple/config.yaml \
--caliper-networkconfig ../../networks/besu/1node-clique/networkconfig.json \
--caliper-workspace .
```

---

## ✅ System Overview

| Component      | Fabric                              | Besu (Quorum)               |
| -------------- | ----------------------------------- | --------------------------- |
| Chaincode      | methane_sensor_chaincode/assetTr.ts | contracts/AssetContract.sol |
| Event Listener | johnny5.js (Fabric Gateway)         | johnny5_besu.js (Web3.js)  |
| Backend        | methane_sensor_backend            | besutxserver.js + Remix ABI |
| Benchmark Tool | Caliper                             | Caliper                     |

---

## 📬 License

MIT License. Developed for academic research and IoT/blockchain integration testing.

For support or questions, contact- [bnweke@uwyo.edu].

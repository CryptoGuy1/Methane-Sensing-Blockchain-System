// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AssetContract {
    struct Asset {
        string id;
        string timestamp;
        uint256 methaneLevel;
    }

    mapping(string => Asset) private assets;
    string[] private assetIds;

    event AssetCreated(string id, string timestamp, uint256 methaneLevel);
    event HighMethaneLevel(string id, string timestamp, uint256 methaneLevel);
    event AssetUpdated(string id, string timestamp, uint256 methaneLevel);
    event AssetDeleted(string id);

    function createAsset(
        string memory id,
        string memory timestamp,
        uint256 methaneLevel
    ) external {
        require(bytes(id).length > 0, "ID is required");
        require(bytes(timestamp).length > 0, "Timestamp is required");
        require(assets[id].methaneLevel == 0, "Asset already exists");

        assets[id] = Asset(id, timestamp, methaneLevel);
        assetIds.push(id);

        emit AssetCreated(id, timestamp, methaneLevel);
        if (methaneLevel > 3000) {
            emit HighMethaneLevel(id, timestamp, methaneLevel);
        }
    }

    function readAsset(
        string memory id
    ) external view returns (string memory, string memory, uint256) {
        Asset memory asset = assets[id];
        require(asset.methaneLevel > 0, "Asset does not exist");
        return (asset.id, asset.timestamp, asset.methaneLevel);
    }

    function updateAsset(
        string memory id,
        string memory timestamp,
        uint256 methaneLevel
    ) external {
        require(assets[id].methaneLevel > 0, "Asset does not exist");

        assets[id] = Asset(id, timestamp, methaneLevel);
        emit AssetUpdated(id, timestamp, methaneLevel);

        if (methaneLevel > 3000) {
            emit HighMethaneLevel(id, timestamp, methaneLevel);
        }
    }

    function deleteAsset(string memory id) external {
        require(assets[id].methaneLevel > 0, "Asset does not exist");

        delete assets[id];
        emit AssetDeleted(id);
    }

    function assetExists(string memory id) external view returns (bool) {
        return assets[id].methaneLevel > 0;
    }

    function getAllAssets() external view returns (Asset[] memory) {
        Asset[] memory result = new Asset[](assetIds.length);
        for (uint256 i = 0; i < assetIds.length; i++) {
            result[i] = assets[assetIds[i]];
        }
        return result;
    }
}

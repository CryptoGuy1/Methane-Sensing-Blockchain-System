import { Context, Contract, Info, Returns, Transaction } from 'fabric-contract-api';
import stringify from 'json-stringify-deterministic';
import sortKeysRecursive from 'sort-keys-recursive';
import { Asset } from './asset';
import { v4 as uuidv4 } from 'uuid';

@Info({
  title: 'AssetTransfer',
  description: 'Smart contract for storing and fetching methane level data',
})
export class AssetTransferContract extends Contract {
  @Transaction()
  public async InitLedger(ctx: Context): Promise<void> {
    const assets: Asset[] = [
      {
        ID:"18b64e7f-7c45-435c-b57d-7ea7d56f1d50",
        Timestamp: '01/01/2023, 00:00:00',
        Methanelevel: 0,
      },
    ];
    for (const asset of assets) {
      asset.docType = 'asset';
      await ctx.stub.putState(
        asset.ID,
        Buffer.from(stringify(sortKeysRecursive(asset)))
      );
      console.info(`Asset ${asset.ID} initialized`);
    }
  }

  @Transaction()
  public async CreateAsset(
    ctx: Context,
    id: string,
    timestamp: string,
    methanelevel: number
  ): Promise<void> {
    const assetId = id || uuidv4();
    const exists = await this.AssetExists(ctx, assetId);
    if (exists) {
      throw new Error(`Asset with ID ${assetId} already exists`);
    }
    const asset = {
      ID: assetId,
      Timestamp: timestamp,
      Methanelevel: methanelevel,
    };

    console.log(asset);
    if (methanelevel > 3000) {
      console.log(methanelevel);
      console.log(methanelevel > 3000);
      ctx.stub.setEvent('HighMethaneLevel', Buffer.from(JSON.stringify(asset)));
      console.log("Event emitted");
    }
    await ctx.stub.putState(
      assetId,
      Buffer.from(stringify(sortKeysRecursive(asset)))
    );
  }

  @Transaction(false)
  public async ReadAsset(ctx: Context, id: string): Promise<string> {
    const assetJSON = await ctx.stub.getState(id);
    if (!assetJSON || assetJSON.length === 0) {
      throw new Error(`Asset with ID ${id} does not exist`);
    }
    return assetJSON.toString();
  }

  @Transaction()
  public async UpdateAsset(
    ctx: Context,
    id: string,
    timestamp: string,
    methanelevel: number
  ): Promise<void> {
    const exists = await this.AssetExists(ctx, id);
    if (!exists) {
      throw new Error(`Asset with ID ${id} does not exist`);
    }
    const updatedAsset = {
      ID: id,
      Timestamp: timestamp,
      Methanelevel: methanelevel,
    };
    return ctx.stub.putState(
      id,
      Buffer.from(stringify(sortKeysRecursive(updatedAsset)))
    );
  }

  @Transaction()
  public async DeleteAsset(ctx: Context, id: string): Promise<void> {
    const exists = await this.AssetExists(ctx, id);
    if (!exists) {
      throw new Error(`Asset with ID ${id} does not exist`);
    }
    return ctx.stub.deleteState(id);
  }

  @Transaction(false)
  @Returns('boolean')
  public async AssetExists(ctx: Context, id: string): Promise<boolean> {
    const assetJSON = await ctx.stub.getState(id);
    return assetJSON && assetJSON.length > 0;
  }

  @Transaction(false)
  @Returns('string')
  public async GetAllAssets(ctx: Context): Promise<string> {
    const allResults = [];
    const iterator = await ctx.stub.getStateByRange('', '');
    let result = await iterator.next();
    while (!result.done) {
      const strValue = Buffer.from(result.value.value.toString()).toString('utf8');
      let record;
      try {
        record = JSON.parse(strValue);
      } catch (err) {
        console.log(err);
        record = strValue;
      }
      allResults.push(record);
      result = await iterator.next();
    }
    return JSON.stringify(allResults);
  }
}
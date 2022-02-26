import mongoose from "mongoose";

require("dotenv").config();

class Database {
  private connection: typeof mongoose | undefined;
  private mongoDevUri: string = process.env.MONGO_DB_URI;

  constructor() {}

  public run = async (): Promise<void> => {
    await this.connect();
  };

  public getStatus = () => {
    return mongoose.connection.readyState;
  };

  protected getMongoUri = (): string => {
    return this.mongoDevUri;
  };

  private async connect(): Promise<void> {
    if (this.getStatus() === 1) return;
    if (this.getStatus() === 2) return;
    if (!this.mongoDevUri) return;

    const mongoUri: string = this.getMongoUri();
    (mongoose as any).Promise = global.Promise;
    try {
      console.log("db connecting...");
      await mongoose.connect(mongoUri);
      console.log("db connect succesful! :)");
    } catch (error) {
      console.log("db connect failed");
      console.log(error);
    }
  }

  public async truncate(): Promise<void> {
    if (!mongoose.connection.readyState) return;
    console.log("edu-rank-db truncate collections...", process.env.NODE_ENV);

    const { collections } = mongoose.connection;
    const promises = Object.keys(collections).map((collection) =>
      mongoose.connection.collection(collection).deleteMany({})
    );
    await Promise.all(promises);
  }

  public async disconnect(): Promise<void> {
    if (!mongoose.connection.readyState) return;
    console.log("edu-rank-db disconnecting...", process.env.NODE_ENV);

    await mongoose.disconnect();
  }
}

export default new Database();

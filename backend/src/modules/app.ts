import express, { Request, Response, NextFunction } from "express";
import cors from "cors";
import helmet from "helmet";
import database from "./database";
import { errorHandler } from "../middlewares/error-handler";
import { orderRouter } from "../components/orders/order.routes";
import xmlbodyparser from "express-xml-bodyparser";

require("dotenv").config();

declare global {
  namespace Express {
    interface Request {
      rawBody: string | undefined;
    }
  }
}

const { version } = require(process.env.NODE_ENV === "production"
  ? "../package.json"
  : "../../package.json");

class App {
  public app: express.Application;

  constructor() {}

  public async run() {
    await this.runApp();
  }

  private async runApp(): Promise<void> {
    const lastRun = new Date();
    this.app = express();
    this.app.use(helmet());
    this.app.use(cors());
    this.app.use(express.json({ limit: "50mb" }));
    this.app.use(express.urlencoded({ extended: false }));
    this.app.use(xmlbodyparser());

    this.app.use("/orders", orderRouter);
    this.app.get("/healthcheck", (req, res, next) => {
      res.json({
        status: "success",
        payload: {
          databaseStatus: database.getStatus(),
          environment: process.env.NODE_ENV,
          version,
          lastRun,
        },
      });
      next();
    });
    this.app.use(errorHandler);
  }
}

export default new App();

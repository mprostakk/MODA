import { convertToOrder, parseXML, validateXML } from "./order.helpers";
import { Request, Response, NextFunction } from "express";
import { Controller, success } from "../../utils";
import fs from "fs";
import { Order } from "./order.models";
import { OrderMongoModel } from "./order.schemas";

export class OrderController {
  @Controller
  async append(req: Request, res: Response, next: NextFunction) {
    const { rawBody: xmlOrder } = req;
    if (!xmlOrder) throw new Error("request body is not valid");
    // const xmlBuffer = fs.readFileSync("src/mocks/examples.xml");
    // const xmlOrder = xmlBuffer.toString();
    const xmlValidationResult = await validateXML(xmlOrder);
    if (!xmlValidationResult.valid) throw new Error("xml is not valid");

    const jsonOrder = parseXML(xmlOrder);
    const order: Order = convertToOrder(jsonOrder);

    const orderDocument = new OrderMongoModel(order);
    await orderDocument.save();

    res.status(200).json(success({ orderDocument }));
  }

  @Controller
  async list(req: Request, res: Response, next: NextFunction) {
    const orderDocuments = await OrderMongoModel.find();
    res.status(200).json(success({ orderDocuments }));
  }

  @Controller
  async delete(req: Request, res: Response, next: NextFunction) {
    await OrderMongoModel.deleteMany();
    res.status(200).json(success({}));
  }
}

export default new OrderController();

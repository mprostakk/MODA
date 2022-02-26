import orderController from "./order.controllers";
import express, { Router } from "express";

export const orderRouter: Router = express.Router();

orderRouter.post("/append", orderController.append);
orderRouter.get("/list", orderController.list);
orderRouter.delete("/delete", orderController.delete);

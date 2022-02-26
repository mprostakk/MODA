import { Request, Response, NextFunction } from "express";
import { ValidationError } from "joi";
import { error } from "../utils";

export const errorHandler = (
  err: any,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  if (!err) return next();
  if (!err.statusCode) err.statusCode = 500;
  if (err.name && err.name === "ValidationError") {
    const validationError: ValidationError = err;
    return res.status(err.statusCode).send(
      error({
        ...err,
        message: `Validation Failed: ${
          err.details?.body?.length && err.details.body[0]?.message
        }`,
        details: undefined,
      })
    );
  }

  res.status(err.statusCode).send(error(err.message));
};

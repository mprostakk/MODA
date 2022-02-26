import { schema } from "express-validation";
import Joi from "joi";

export type Status = "empty" | "pending" | "success" | "error";

export interface ResponseBody<P = {}, E = {}> {
  status: Status;
  payload?: P;
  error?: E;
}

export const success = <P>(payload: P): ResponseBody<P, any> => ({
  status: "success",
  payload,
});

export const error = <E>(error: E): ResponseBody<any, E> => ({
  status: "error",
  error,
});

export function Controller(
  target: Object,
  propertyKey: string | symbol,
  descriptor: PropertyDescriptor
) {
  const originalMethod: any = descriptor.value;
  descriptor.value = async (...args: any[]) => {
    try {
      await originalMethod.apply(this, args);
    } catch (error) {
      const [req, res, next] = args;
      console.error("!", error);
      console.log(req.query);
      next(error);
    }
  };
}

export const JoiObjectId = Joi.string()
  .regex(/^[0-9a-fA-F]{24}$/)
  .required();

export const Partial = (joiObject: Joi.ObjectSchema<any>) => {
  const keys: string[] = [];
  for (const entry of (joiObject as any)._ids._byKey.entries()) {
    keys.push(entry[0]);
  }
  return joiObject.fork(keys, (schema) => schema.optional());
};

export const Omit = (joiObject: Joi.ObjectSchema<any>, excludeKey: string) => {
  return joiObject.keys({
    [excludeKey]: Joi.forbidden(),
  });
};

import {
  Order,
  Address,
  Restaurant,
  OrderedDish,
  Deliverer,
  Customer,
  Dish,
} from "./order.models";
import { Document, Schema, Model, model } from "mongoose";

export class OrderDocument extends Document {
  id: string;
  created_date: string;
  total_cost: string;
  state: string;
  destination_address: Address;
  restaurant: Restaurant;
  ordered_dishes: OrderedDish[];
  deliverer: Deliverer;
  customer: Customer;
  user_note: string;
  external_invoice_id: string;
  external_payment_id: string;
}

export const AddressSchema: Schema = new Schema({
  country: { type: String, required: true },
  city: { type: String, required: true },
  state: { type: String, required: true },
  zip_code: { type: String, required: true },
  street_name: { type: String, required: true },
  building_number: { type: String, required: false },
});

export const CustomerSchema: Schema = new Schema({
  user_id: { type: String, required: true },
  nip: { type: String, required: true },
  invoice_address: { type: AddressSchema, required: true },
});

export const DelivererSchema: Schema = new Schema({
  user_id: { type: String, required: true },
});

export const RestaurantSchema: Schema = new Schema({
  restaurant_id: { type: String, required: true },
  name: { type: String, required: true },
  nip: { type: String, required: true },
  invoice_address: { type: AddressSchema, required: true },
});

export const DishTypeSchema: Schema = new Schema({
  name: { type: String, required: true },
});

export const DishSchema: Schema = new Schema({
  name: { type: String, required: true },
  price: { type: String, required: true },
  dish_types: { type: [DishTypeSchema], required: true },
});

export const OrderedDishSchema: Schema = new Schema({
  quantity: { type: String, required: true },
  cost: { type: String, required: true },
  dish: { type: DishSchema, required: true },
});

export const OrderSchema: Schema = new Schema({
  id: { type: String, required: true },
  created_date: { type: String, required: true },
  total_cost: { type: String, required: true },
  state: { type: String, required: true },
  destination_address: { type: AddressSchema, required: true },
  restaurant: { type: RestaurantSchema, required: true },
  ordered_dishes: { type: [OrderedDishSchema], required: true },
  deliverer: { type: DelivererSchema, required: true },
  customer: { type: CustomerSchema, required: true },
  user_note: { type: String, required: true },
  external_invoice_id: { type: String, required: true },
  external_payment_id: { type: String, required: true },
});

export const OrderMongoModel: Model<OrderDocument> = model<OrderDocument>(
  "orders",
  OrderSchema
);

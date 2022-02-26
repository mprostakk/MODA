export type Address = {
  country: string;
  city: string;
  state: string;
  zip_code: string;
  street_name: string;
  building_number?: string;
};

export type Customer = {
  user_id: string;
  nip: string;
  invoice_address: Address;
};

export type Deliverer = {
  user_id: string;
};

export type Restaurant = {
  restaurant_id: string;
  name: string;
  nip: string;
  invoice_address: Address;
};

export type DishType = {
  name: string;
};

export type Dish = {
  name: string;
  price: string;
  dish_types: DishType[];
};

export type OrderedDish = {
  quantity: string;
  cost: string;
  dish: Dish;
};

export type Order = {
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
};

import { Order } from "./order.models";
import xsdSchemaValidator from "xsd-schema-validator";
import { XMLParser } from "fast-xml-parser";

const xmlSchemaPath = "src/resources/xml_schema.xsd";

export const validateXML = async (xmlString: string) => {
  return new Promise<{ valid: boolean; messages: string[]; result: string }>(
    (resolve, reject) => {
      xsdSchemaValidator.validateXML(
        xmlString,
        xmlSchemaPath,
        (error, result) => {
          if (error || !result.valid) reject(error);
          else resolve(result);
        }
      );
    }
  );
};

export const parseXML = (xmlString: string): JSONObject => {
  const xmlParser = new XMLParser({
    ignoreAttributes: false,
    attributeNamePrefix: "",
  });
  const xmlData = xmlParser.parse(xmlString);
  return Array.isArray(xmlData.Orders.Order)
    ? xmlData.Orders.Order[0]
    : xmlData.Orders.Order;
};

export const convertToOrder = (jsonObject: JSONObject): Order => {
  return {
    id: jsonObject.id,
    created_date: jsonObject.created_date,
    total_cost: jsonObject.total_cost,
    state: jsonObject.state,
    destination_address: jsonObject.destination_address.address,
    restaurant: {
      restaurant_id: jsonObject.Ordered_Dish[0].Dish.Restaurant.restaurant_id,
      name: jsonObject.Ordered_Dish[0].Dish.Restaurant.name,
      nip: jsonObject.Ordered_Dish[0].Dish.Restaurant.nip,
      invoice_address:
        jsonObject.Ordered_Dish[0].Dish.Restaurant.invoice_address.address,
    },
    ordered_dishes: jsonObject.Ordered_Dish.map((jsonOrderedDish) => ({
      quantity: jsonOrderedDish.quantity,
      cost: jsonOrderedDish.cost,
      dish: {
        name: jsonOrderedDish.Dish.name,
        price: jsonOrderedDish.Dish.price,
        dish_types:
          typeof jsonOrderedDish.Dish.dish_type === "string"
            ? jsonOrderedDish.Dish.dish_type.length
              ? [{ name: jsonOrderedDish.Dish.dish_type }]
              : []
            : typeof jsonOrderedDish.Dish.dish_type.name === "string"
            ? [{ name: jsonOrderedDish.Dish.dish_type.name }]
            : Array.isArray(jsonOrderedDish.Dish.dish_type.name)
            ? jsonOrderedDish.Dish.dish_type.name.map((name) => ({ name }))
            : [],
      },
    })),
    deliverer: jsonObject.Deliverer,
    customer: {
      user_id: jsonObject.Customer.user_id,
      nip: jsonObject.Customer.nip,
      invoice_address: jsonObject.Customer.invoice_address.address,
    },
    user_note: jsonObject.user_note,
    external_invoice_id: jsonObject.external_invoice_id,
    external_payment_id: jsonObject.external_payment_id,
  };
};

export type JSONObject = {
  destination_address: {
    address: {
      country: string;
      city: string;
      state: string;
      zip_code: string;
      street_name: string;
      building_number?: string;
    };
  };
  Ordered_Dish: Array<{
    Dish: {
      dish_type: string | { name: string | string[] };
      description?: string;
      Restaurant?: {
        invoice_address: {
          address: {
            country: string;
            city: string;
            state: string;
            zip_code: string;
            street_name: string;
            building_number?: string;
          };
        };
        restaurant_id: string;
        name: string;
        nip: string;
      };
      name: string;
      price: string;
    };
    quantity: string;
    cost: string;
  }>;
  Deliverer: { user_id: string };
  Customer: {
    invoice_address: {
      address: {
        country: string;
        city: string;
        state: string;
        zip_code: string;
        street_name: string;
        building_number?: string;
      };
    };
    user_id: string;
    nip: string;
  };
  user_note: string;
  external_invoice_id: string;
  external_payment_id: string;
  id: string;
  created_date: string;
  total_cost: string;
  state: string;
};

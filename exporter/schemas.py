from dataclasses import dataclass
from typing import Optional

import lxml.builder
import lxml.etree
from lxml import etree


@dataclass
class _Base:
    def __post_init__(self):
        self._maker = lxml.builder.ElementMaker()

    def create_xml_element(self):
        raise NotImplementedError()


@dataclass
class Address(_Base):
    country: str
    city: str
    state: str
    zip_code: str
    street_name: str
    building_number: Optional[str]

    def create_xml_element(self):
        m = self._maker
        return m.address(
            m.country(self.country),
            m.city(self.city),
            m.state(self.state),
            m.zip_code(self.zip_code),
            m.street_name(self.street_name),
            m.building_number(self.building_number),
        )


@dataclass
class Customer(_Base):
    user_id: int
    nip: str
    invoice_address: Address

    def create_xml_element(self):
        m = self._maker
        return m.Customer(
            {"user_id": str(self.user_id), "nip": self.nip},
            m.invoice_address(self.invoice_address.create_xml_element()),
        )


@dataclass
class Deliverer(_Base):
    user_id: int

    def create_xml_element(self):
        m = self._maker
        return m.Deliverer({"user_id": str(self.user_id)})


@dataclass
class Restaurant(_Base):
    restaurant_id: int
    name: str
    nip: str
    invoice_address: Address

    def create_xml_element(self):
        m = self._maker
        return m.Restaurant(
            {
                "restaurant_id": str(self.restaurant_id),
                "name": self.name,
                "nip": self.nip,
            },
            m.invoice_address(self.invoice_address.create_xml_element()),
        )


@dataclass
class DishType(_Base):
    name: str

    def create_xml_element(self):
        m = self._maker
        return m.name(self.name)


@dataclass
class Dish(_Base):
    name: str
    price: str
    dish_types: list[DishType]

    def create_xml_element_with_restaurant(self, restaurant: Optional[Restaurant]):
        m = self._maker
        dish_types_xml = [x.create_xml_element() for x in self.dish_types]

        r = []
        if restaurant is not None:
            r.append(restaurant.create_xml_element())

        return m.Dish(
            {"name": self.name, "price": str(self.price)}, 
            m.dish_type(
                *dish_types_xml
            ), 
            *r
        )


@dataclass
class OrderedDish(_Base):
    quantity: int
    cost: str
    dish: Dish

    def create_xml_element_with_restaurant(self, restaurant: Optional[Restaurant]):
        m = self._maker
        return m.Ordered_Dish(
            {"quantity": str(self.quantity), "cost": str(self.cost)},
            self.dish.create_xml_element_with_restaurant(restaurant),
        )


@dataclass
class Order(_Base):
    id: int
    created_date: str
    total_cost: str
    state: str
    destination_address: Address
    restaurant: Restaurant
    ordered_dishes: list[OrderedDish]
    deliverer: Optional[Deliverer]
    customer: Customer
    user_note: str
    external_invoice_id: str
    external_payment_id: str

    def create_xml_element(self):
        schema_location = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")
        m = lxml.builder.ElementMaker(
            nsmap={
                None: "https://www.ia.pw.edu.pl/MODA",
                "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            },
        )

        ordered_dishes_elements = [
            self.ordered_dishes[0].create_xml_element_with_restaurant(self.restaurant)
        ]

        ordered_dishes_elements.extend(
            [x.create_xml_element_with_restaurant(None) for x in self.ordered_dishes[1:]]
        )
        
        deliverer = []
        if self.deliverer is not None:
            deliverer.append(self.deliverer.create_xml_element())

        return m.Orders(
            {schema_location: "https://www.ia.pw.edu.pl/MODA schema.xsd"},
            m.Order(
                {
                    "id": str(self.id),
                    "created_date": self.created_date,
                    "total_cost": str(self.total_cost),
                    "state": self.state.lower(),
                },
                m.destination_address(self.destination_address.create_xml_element()),
                *ordered_dishes_elements,
                *deliverer,
                self.customer.create_xml_element(),
                m.user_note(self.user_note),
                m.external_invoice_id(self.external_invoice_id),
                m.external_payment_id(self.external_payment_id),
            ),
        )

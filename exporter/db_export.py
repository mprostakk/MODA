import logging
from collections import namedtuple
from datetime import date, datetime

import cx_Oracle

from schemas import (Address, Customer, Deliverer, Dish, DishType, Order,
                     OrderedDish, Restaurant)


def namedtuple_factory(cursor, row):
    fields = [col[0].lower() for col in cursor.description]
    Row = namedtuple("Row", fields)
    r = []
    for index, x in enumerate(row):
        if isinstance(x, (datetime, date)):
            r.append(str(x.isoformat()))
        elif isinstance(x, int):
            r.append(x)
        else:
            r.append(str(x))

    return Row(*r)


def get_order(connection, order_id: int):
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT order_id,
    created_date,
    total_cost,
    order_state,
    zip_code,
    city,
    country,
    state,
    street_name,
    building_number,
    apartment_number,
    deliverer_user_id,
    customer_user_id,
    user_note,
    external_invoice_id,
    external_payment_id
    FROM orders
    WHERE order_id = :order_id
    """,
        order_id=order_id,
    )
    row = cursor.fetchone()
    return namedtuple_factory(cursor, row)


def get_customer(connection, user_id: int):
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT user_id,
    zip_code,
    country,
    city,
    state,
    street_name,
    building_number,
    apartment_number,
    nip
    FROM users
    WHERE user_id = :user_id
    """,
        user_id=user_id,
    )
    row = cursor.fetchone()
    return namedtuple_factory(cursor, row)


def get_deliverer(connection, user_id: int):
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT user_id
    FROM users
    WHERE user_id = :user_id
    """,
        user_id=user_id,
    )
    row = cursor.fetchone()
    return namedtuple_factory(cursor, row)


def get_restaurant(connection, restaurant_id: int):
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT restaurant_id,
    name,
    zip_code,
    country,
    city,
    state,
    street_name,
    building_number,
    apartment_number,
    nip
    FROM restaurants
    WHERE restaurant_id = :restaurant_id
    """,
        restaurant_id=restaurant_id,
    )
    row = cursor.fetchone()
    return namedtuple_factory(cursor, row)


def get_dish_types(connection, dish_id: int) -> list[DishType]:
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT 
    name
    FROM food_types
    inner join dish_types
    on dish_types.food_type_id = food_types.food_type_id
    WHERE dish_types.dish_id = :dish_id
    """,
        dish_id=dish_id,
    )

    dish_types = []
    for row in cursor:
        dish_type = namedtuple_factory(cursor, row)
        dish_types.append(DishType(name=dish_type.name))

    return dish_types


def get_dishes(connection, order_id: int):
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT 
    dishes.dish_id as dish_id, 
    restaurant_id, 
    name, 
    description, 
    is_available, 
    price, 
    photo_url, 
    quantity, 
    cost
    FROM dishes
    inner join ordered_dishes
    on dishes.dish_id = ordered_dishes.dish_id
    WHERE order_id = :order_id
    """,
        order_id=order_id,
    )

    ordered_dishes = []
    restaurant_id = -1

    for row in cursor:        
        ordered_dish = namedtuple_factory(cursor, row)
        restaurant_id = ordered_dish.restaurant_id
        dish_types = get_dish_types(connection, ordered_dish.dish_id)

        dish = Dish(name=ordered_dish.name, price=ordered_dish.price, dish_types=dish_types)
        ordered_dishes.append(
            OrderedDish(dish=dish, quantity=ordered_dish.quantity, cost=ordered_dish.cost)
        )

    return ordered_dishes, restaurant_id


def parse_db_data_to_schema(
    order_info, ordered_dishes, customer_info, deliverer_info, restaurant_info
):
    order_address = Address(
        country=order_info.country,
        city=order_info.city,
        state=order_info.state,
        zip_code=order_info.zip_code,
        street_name=order_info.street_name,
        building_number=order_info.building_number,
    )
    customer_invoice_address = Address(
        country=customer_info.country,
        city=customer_info.city,
        state=customer_info.state,
        zip_code=customer_info.zip_code,
        street_name=customer_info.street_name,
        building_number=customer_info.building_number,
    )
    restaurant_invoice_address = Address(
        country=restaurant_info.country,
        city=restaurant_info.city,
        state=restaurant_info.state,
        zip_code=restaurant_info.zip_code,
        street_name=restaurant_info.street_name,
        building_number=restaurant_info.building_number,
    )
    customer = Customer(
        user_id=customer_info.user_id,
        nip=customer_info.nip,
        invoice_address=customer_invoice_address,
    )

    deliverer = None
    if deliverer_info is not None:
        deliverer = Deliverer(user_id=deliverer_info.user_id)

    restaurant = Restaurant(
        restaurant_id=restaurant_info.restaurant_id,
        name=restaurant_info.name,
        nip=restaurant_info.nip,
        invoice_address=restaurant_invoice_address,
    )

    order = Order(
        id=order_info.order_id,
        created_date=order_info.created_date,
        total_cost=order_info.total_cost,
        state=order_info.order_state,
        destination_address=order_address,
        deliverer=deliverer,
        customer=customer,
        user_note=order_info.user_note,
        external_invoice_id=order_info.external_invoice_id,
        external_payment_id=order_info.external_payment_id,
        ordered_dishes=ordered_dishes,
        restaurant=restaurant,
    )
    return order


def get_order_from_db(
    lib_dir: str, user: str, password: str, host: str, port: int, service_name: str, order_id: int
):
    logging.info("Init oracle client")
    cx_Oracle.init_oracle_client(lib_dir=lib_dir)
    dsn = cx_Oracle.makedsn(host, port, service_name=service_name)

    with cx_Oracle.connect(user=user, password=password, dsn=dsn, encoding="UTF-8") as connection:
        logging.info("Created connection with database")

        order_info = get_order(connection, order_id=order_id)
        ordered_dishes, restaurant_id = get_dishes(connection, order_id=order_id)
        customer_info = get_customer(connection, user_id=order_info.customer_user_id)
        deliverer_info = get_deliverer(connection, user_id=order_info.deliverer_user_id)
        restaurant_info = get_restaurant(connection, restaurant_id=restaurant_id)

    order = parse_db_data_to_schema(
        order_info, ordered_dishes, customer_info, deliverer_info, restaurant_info
    )
    return order

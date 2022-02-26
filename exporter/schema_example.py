from schemas import (Address, Customer, Deliverer, Dish, DishType, Order,
                     OrderedDish, Restaurant)


def create_example_order():
    order_address = Address(
        country="1", city="1", state="1", zip_code="1", street_name="1", building_number="1"
    )
    restaurant_invoice_address = Address(
        country="1", city="1", state="1", zip_code="1", street_name="1", building_number="1"
    )
    customer_invoice_address = Address(
        country="1", city="1", state="1", zip_code="1", street_name="1", building_number="1"
    )

    customer = Customer(user_id=1, nip="ABCDEFGHIJ", invoice_address=customer_invoice_address)
    deliverer = Deliverer(user_id=2)

    dish_types = DishType(name="miesne")
    dish = Dish(name="miesne", price="10.10", dish_types=[dish_types])
    ordered_dish = OrderedDish(quantity=1, cost="10.10", dish=dish)
    restaurant = Restaurant(
        restaurant_id=1, name="1", nip="ABCDEFGHIJ", invoice_address=restaurant_invoice_address
    )

    order = Order(
        id=1,
        created_date="1993-08-21T08:38:36.81",
        total_cost="10.10",
        state="delivered",
        destination_address=order_address,
        deliverer=deliverer,
        customer=customer,
        user_note="Klatka 8, II piętro",
        external_invoice_id="f2558774-77ce-11ec-90d6-0242ac120003",
        external_payment_id="f2558774-77ce-11ec-90d6-0242ac120003",
        ordered_dishes=[ordered_dish, ordered_dish],
        restaurant=restaurant,
    )

    return order

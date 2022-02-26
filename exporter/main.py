import logging
import os

from dotenv import load_dotenv

from db_export import get_order_from_db
from helpers import (create_xml_from_order, save_xml_to_file,
                     validate_xml_schema)
from schema_example import create_example_order
from schemas import Order
from send_to_client import send_order_to_client_as_xml

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO
)

load_dotenv()

SCHEMA_FILE_PATH = "xml/xml_schema.xsd"


def export_order_to_service(order_id: int):
    order: Order = get_order_from_db(
        os.getenv("INSTANT_CLIENT_LIB_DIR"),
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_HOST"),
        int(os.getenv("DB_PORT")),
        os.getenv("DB_SERVICE_NAME"),
        order_id,
    )

    # Uncomment for local debugging purposes
    # order: Order = create_example_order()
    logging.info("Successfully retrieved order from database")

    xml_order = create_xml_from_order(order)
    logging.info("Created xml from order")

    validate_xml_schema(xml_order, SCHEMA_FILE_PATH)
    logging.info("Created xml order is valid")

    send_order_to_client_as_xml(os.getenv("CUSTOM_SERVICE_URL"), xml_order)
    logging.info("Successfully sent order as xml to external service")

    # Uncomment for local debugging purposes
    # save_xml_to_file("output.xml", xml_order)


def main():
    export_order_to_service(order_id=3)


if __name__ == "__main__":
    main()

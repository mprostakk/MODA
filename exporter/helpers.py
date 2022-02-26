import lxml.etree
import xmlschema

from schemas import Order


def create_xml_from_order(order: Order) -> bytes:
    order_document = order.create_xml_element()
    return lxml.etree.tostring(
        order_document, pretty_print=True, xml_declaration=True, encoding="UTF-8"
    )


def validate_xml_schema(source_xml: bytes, xsd_file_path: str):
    schema = xmlschema.XMLSchema(xsd_file_path)
    schema.validate(source_xml)

    if not schema.is_valid(source_xml):
        raise NotImplementedError()


def save_xml_to_file(filename: str, xml_data: bytes):
    with open(filename, "w") as f:
        f.write(xml_data.decode("utf-8"))

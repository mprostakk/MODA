import requests as requests


class OrderClientException(Exception):
    pass


def send_order_to_client_as_xml(url: str, order_as_xml: bytes) -> None:
    headers = {"Content-Type": "application/xml"}
    r = requests.post(f"{url}/orders/append", data=order_as_xml, headers=headers)
    if r.status_code != 200:
        raise OrderClientException()

# aiosmartpost - Itella SmartPost API wrapper for humans 📦

**WORK IN PROGRESS! NOT READY FOR PRODUCTION USE**

[Official SmartPost API Docs](https://uus.smartpost.ee/ariklient/ostukorvi-rippmenuu-lisamise-opetus/automaatse-andmevahetuse-opetus)

This solution:
* has both async and sync API
* has 100% type-annotated code
* is tested in real-world project in Estonia

## Quickstart
Examples use async version of `Client`, but you can use import below instead and remove `await` keywords:
```python
from smartpost.sync import Client
```

Fetch list of available Estonian destinations:
```python
>>> from smartpost import Client
>>> client = Client("user", "pass")  # credentials can be omitted in this case
>>> await client.get_ee_terminals()
[Destination(place_id=101, name='Viljandi Männimäe Selver', ...), ...]
```

Add new shipment order and get A5 PDF with label for it:
```python
>>> from smartpost import Client
>>> from smartpost.errors import ShipmentOrderError
>>> from smartpost.models import Recipient, EETerminalDestination, ShipmentOrder
>>> client = Client("user", "pass")
>>> recipient = Recipient("John Doe", "+37255555555", "john.doe@example.com")
>>> terminal = EETerminalDestination(102)
>>> order_id = 547
>>> order = ShipmentOrder(recipient, terminal, reference=str(order_id))
>>> try:
>>>     orders_info = await client.add_shipment_orders([order])
>>> except ShipmentOrderError as exc:
>>>     print("Failed to add shipment order:")
>>>     for error_details in exc.errors:
>>>         print(f"Order #{error_details['reference']} error: {str(error_details)}")
>>>
>>> orders_info
[OrderInfo(barcode='XXXXXXXXXXXXXXXX', reference=None, sender=None, doorcode=None)]


>>> pdf_bytes = await client.get_labels_pdf("A5", [orders_info[0].barcode])
>>> with open("/tmp/test.pdf", "wb") as file:
...   file.write(pdf_bytes)
... 
57226
```

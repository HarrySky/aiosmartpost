# aiosmartpost - Itella SmartPost NEW API wrapper for humans 📦

**WORK IN PROGRESS! NOT READY FOR PRODUCTION USE**

[Official NEW SmartPost API Docs](https://itella.ee/wp-content/uploads/2023/02/smartpost-api-documentation-13.pdf)

This solution:
* has both async and sync API
* has 100% type-annotated code
* is tested in real-world project in Estonia

## Quickstart
Examples use async version of `Client`. At the moment sync version is not implemented for new API.

Fetch list of available Estonian destinations:
```python
>>> from smartpost import Client
>>> client = Client("API-...-KEY")
>>> await client.get_ee_terminals()
[Place(place_id='01007225', name='Tallinna Arsenali Keskus', city='Tallinn', ...), ...]
```

Add new shipment order and get A5 PDF with label for it:
```python
>>> from smartpost import Client
>>> from smartpost.errors import ShipmentOrderError
>>> from smartpost.models import Recipient, EETerminalDestination, ShipmentOrder
>>> client = Client("API-...-KEY")
>>> order_id = 547
>>> order = ShipmentOrder(
>>>     source={"country": "ee"},
>>>     recipient={"name": "John Doe", "phone": "+358400953521", "email": "client-mail@example.org"},
>>>     destination={"country": "ee", "place_id" : '01007225'},
>>>     additionalservices={"labelprinted": True},
>>>     reference=str(order_id)
>>> )
>>> try:
>>>     new_orders = await client.add_shipment_orders([order], ["report-email@example.org"])
>>> except ShipmentOrderError as exc:
>>>     print("Failed to add shipment order:")
>>>     for error_details in exc.errors:
>>>         print(f"Order #{error_details['reference']} error: {str(error_details)}")
>>>
>>>     raise
>>>
>>> new_orders
[Order(barcode='XXXXXXXXXXXXXXXX', reference=None, sender=None)]


>>> pdf_bytes = await client.get_labels_pdf("A5", [new_orders[0].barcode])
>>> with open("/tmp/test.pdf", "wb") as file:
...   file.write(pdf_bytes)
... 
57226
```

# aiosmartpost - Itella SmartPost API wrapper for humans 📦

**WORK IN PROGRESS! NOT READY FOR PRODUCTION USE**

[Official SmartPost API Docs](https://uus.smartpost.ee/ariklient/ostukorvi-rippmenuu-lisamise-opetus/automaatse-andmevahetuse-opetus)

This solution:
* has both async and sync API
* has 100% type-annotated code

## Quickstart

Examples use async version of `Client`, but you can use this import instead:
```python
from smartpost.sync import Client
```

Fetch list of available Estonian destinations:
```python
>>> from smartpost import Client
>>> client = Client("user", "pass")  # credentials can be omitted in this case
>>> await client.ee_destinations()
[Destination(place_id=101, name='Viljandi Männimäe Selver', ...), ...]
```

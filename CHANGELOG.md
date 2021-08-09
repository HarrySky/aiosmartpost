# Changelog

All notable changes to this package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

This package is following [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

## Unreleased

Nothing here yet

<!--
### Security

### Changed

### Added

### Fixed

### Removed
-->

## 0.3.1 (August 9th, 2021)

### Fixed

- Use key "orders" instead of "errors" in API errors processing

## 0.3.0 (August 9th, 2021)

### Changed

- Raise `ShipmentOrderError` in `Client.add_shipment_orders` on error
- Process optional fields in `ShipmentOrder.to_xml`

## 0.2.0 (April 13th, 2021)

### Changed

- Change `ee_destinations` name in `smartpost.Client` to `get_ee_terminals` to better communicate what is actually returned
- Change `ee_express_destinations` name in `smartpost.Client` to `get_ee_express_terminals` to better communicate what is actually returned

### Added

- Add `get_fi_terminals` method to `smartpost.Client` for getting Finnish terminals list
- Add `get_fi_post_offices` method to `smartpost.Client` for getting Finnish post offices list
- Add `add_shipment_orders` method to `smartpost.Client` for adding new shipment orders to SmartPost system
- Add `get_labels_pdf` method to `smartpost.Client` for getting PDF files with shipment order labels

## 0.1.0 (April 13th, 2021)

### Added

- Add async `Client` wrapper (`smartpost.Client`)
- Add `ee_destinations` method to `smartpost.Client` for getting Estonian destinations list
- Add `ee_express_destinations` method to `smartpost.Client` for getting Estonian destinations with express delivery list

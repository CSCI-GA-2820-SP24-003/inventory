# NYU DevOps Project Inventory Squad

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/CSCI-GA-2820-SP24-003/inventory/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP24-003/inventory/actions)
[![Build Status](https://github.com/CSCI-GA-2820-SP24-003/inventory/actions/workflows/bdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP24-003/inventory/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP24-003/inventory/graph/badge.svg?token=IM6VUBAEYC)](https://codecov.io/gh/CSCI-GA-2820-SP24-003/inventory)

## Description

The inventory resource keeps track of how many of each product we have in our warehouse. At a minimum it will reference a product and the quantity on hand. Inventory also tracks restock levels and the condition of the item (i.e., new, open box, used). Restock levels will help you know when to order more products. Being able to query products by their condition (e.g., new, used) is very useful.

## Database Schema
| Column | Data type | Condition |
| --- | --- | --- |
| `id` | `int` | `id > 0` |
| `quantity` | `int` | `quantity > 0` |
| `inventory_name` | `string` | N/A |
| `category` | `string` | N/A |
| `condition` | `Enum` | `condition in set(NEW, OPENED, USED)` |
| `restock_level` | `<integer>` | `restock_level > 0` |

## API endpoints

| Method | URI | Description | Input |
| --- | --- | ------ | --- |
| `GET` | `/inventory/` | List all items in the inventory | Item Attribute(s) |
| `GET` | `/inventory/<int:id>` | Given the correct `id` this retrieves the inventory | Item ID |
| `DELETE` | `/inventory/<int:id>` | Given the correct `id` this deletes the entry | Item ID |
| `PUT` | `/inventory/<int:id>` | Given the correct `id` this updates the entry | Item Attributes |
| `POST` | `/inventory` | Given the inventory parameters, create a new inventory entry | Item Attributes |
| `PUT` | `/inventory/<int:id>/restock` | Click on the restock button will increase the `quantity` of an item if it is below `restock_level` | Item Attributes |

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.

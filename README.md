# NYU DevOps Project Inventory Squad

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

## Description

The inventory resource keeps track of how many of each product we have in our warehouse. At a minimum it will reference a product and the quantity on hand. Inventory also tracks restock levels and the condition of the item (i.e., new, open box, used). Restock levels will help you know when to order more products. Being able to query products by their condition (e.g., new, used) is very useful.

## Database Schema
| Column | Data type | Condition |
| --- | --- | --- |
| `id` | `<integer>` | `id > 0` |
| `quantity` | `<integer>` | `quantity > 0` |
| `inventory_name` | `<string>` | `name = string` |
| `category` | `<string>` | `category = string` |

## API endpoints

| Method | URI | Description | Content-Type |
| --- | --- | ------ | --- |
| `GET` | `/inventory/` | List all items in the inventory | N/A |
| `GET` | `/inventory/<int:id>` | Given the correct `id` this retrieves the inventory | N/A |
| `DELETE` | `/inventory/<int:id>` | Given the correct `id` this deletes the entry | N/A |
| `PUT` | `/inventory/<int:id>` | Given the correct `id` this updates the entry | N/A |
| `POST` | `/inventory` | Given the inventory parameters, create a new inventory entry | application/json |

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.

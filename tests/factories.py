# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""

import factory
from factory.fuzzy import FuzzyChoice
from service.models import Inventory, Condition


class InventoryFactory(factory.Factory):
    """Creates fake inventories that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Inventory

    id = factory.Sequence(lambda n: n)
    inventory_name = FuzzyChoice(choices=["Apple", "Iphone", "telephone"])
    category = FuzzyChoice(choices=["Fruits", "Electronic"])
    quantity = FuzzyChoice(choices=[20, 90, 40])
    condition = FuzzyChoice(choices=[Condition.NEW, Condition.OPENED, Condition.USED])
    restock_level = FuzzyChoice(choices=[100, 70, 120])

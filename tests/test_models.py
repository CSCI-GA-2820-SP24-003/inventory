"""
Test cases for Inventory Model
"""

import os
import logging
from unittest import TestCase
from unittest.mock import patch
from wsgi import app
from service.models import Inventory, Condition, DataValidationError, db
from tests.factories import InventoryFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  YourResourceModel   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCaseBase(TestCase):
    """Test Cases for Inventory Model"""

    # pylint: disable=duplicate-code
    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Inventory).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()


######################################################################
#  P E T   M O D E L   T E S T   C A S E S
######################################################################
class TestInventoryModel(TestCaseBase):
    """Inventory Model CRUD Tests"""

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_inventory(self):
        """It should Create a inventory and assert that it exists"""
        inventory = Inventory(
            inventory_name="Apple",
            category="Fruits",
            quantity=20,
            condition=Condition.NEW,
            restock_level=100,
        )
        self.assertEqual(str(inventory), "<Inventory Apple id=[None]>")
        self.assertTrue(inventory is not None)
        self.assertEqual(inventory.id, None)
        self.assertEqual(inventory.inventory_name, "Apple")
        self.assertEqual(inventory.category, "Fruits")
        self.assertEqual(inventory.quantity, 20)
        self.assertEqual(inventory.condition, Condition.NEW)
        self.assertEqual(inventory.restock_level, 100)
        inventory = Inventory(
            inventory_name="Peach",
            category="Fruits",
            quantity=10,
            condition=Condition.NEW,
            restock_level=100,
        )
        self.assertEqual(inventory.inventory_name, "Peach")
        self.assertEqual(inventory.quantity, 10)

    def test_add_a_inventory(self):
        """It should Create a inventory and add it to the database"""
        inventories = Inventory.all()
        self.assertEqual(inventories, [])
        inventory = Inventory(
            inventory_name="Apple",
            category="Fruits",
            quantity=20,
            condition=Condition.NEW,
            restock_level=100,
        )
        self.assertTrue(inventory is not None)
        self.assertEqual(inventory.id, None)
        inventory.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(inventory.id)
        inventories = Inventory.all()
        self.assertEqual(len(inventories), 1)

    def test_read_a_inventory(self):
        """It should Read a Inventory"""
        inventory = InventoryFactory()
        logging.debug(inventory)
        inventory.id = None
        inventory.create()
        self.assertIsNotNone(inventory.id)
        # Fetch it back
        found_inventory = Inventory.find(inventory.id)
        self.assertEqual(found_inventory.id, inventory.id)
        self.assertEqual(found_inventory.inventory_name, inventory.inventory_name)
        self.assertEqual(found_inventory.category, inventory.category)
        self.assertEqual(found_inventory.condition, inventory.condition)
        self.assertEqual(found_inventory.restock_level, inventory.restock_level)

    def test_update_a_inventory(self):
        """It should Update a Inventory"""
        inventory = InventoryFactory()
        logging.debug(inventory)
        inventory.id = None
        inventory.create()
        logging.debug(inventory)
        self.assertIsNotNone(inventory.id)
        # Change it an save it
        inventory.category = "k9"
        original_id = inventory.id
        inventory.update()
        self.assertEqual(inventory.id, original_id)
        self.assertEqual(inventory.category, "k9")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        inventories = Inventory.all()
        self.assertEqual(len(inventories), 1)
        self.assertEqual(inventories[0].id, original_id)
        self.assertEqual(inventories[0].category, "k9")

    def test_update_no_id(self):
        """It should not Update a Inventory with no id"""
        inventory = InventoryFactory()
        logging.debug(inventory)
        inventory.id = None
        self.assertRaises(DataValidationError, inventory.update)

    def test_delete_a_inventory(self):
        """It should Delete a Inventory"""
        inventory = InventoryFactory()
        inventory.create()
        self.assertEqual(len(Inventory.all()), 1)
        # delete the inventory and make sure it isn't in the database
        inventory.delete()
        self.assertEqual(len(Inventory.all()), 0)

    def test_list_all_inventories(self):
        """It should List all inventories in the database"""
        inventories = Inventory.all()
        self.assertEqual(inventories, [])
        # Create 5 Inventories
        for _ in range(5):
            inventory = InventoryFactory()
            inventory.create()
        # See if we get back 5 inventories
        inventories = Inventory.all()
        self.assertEqual(len(inventories), 5)

    def test_serialize_a_inventory(self):
        """It should serialize a Inventory"""
        inventory = InventoryFactory()
        data = inventory.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], inventory.id)
        self.assertIn("inventory_name", data)
        self.assertEqual(data["inventory_name"], inventory.inventory_name)
        self.assertIn("category", data)
        self.assertEqual(data["category"], inventory.category)
        self.assertIn("quantity", data)
        self.assertEqual(data["quantity"], inventory.quantity)
        self.assertIn("condition", data)
        self.assertEqual(data["condition"], inventory.condition.name)
        self.assertIn("restock_level", data)
        self.assertEqual(data["restock_level"], inventory.restock_level)

    def test_deserialize_a_inventory(self):
        """It should de-serialize a Inventory"""
        data = InventoryFactory().serialize()
        inventory = Inventory()
        inventory.deserialize(data)
        self.assertNotEqual(inventory, None)
        self.assertEqual(inventory.id, None)
        self.assertEqual(inventory.inventory_name, data["inventory_name"])
        self.assertEqual(inventory.category, data["category"])
        self.assertEqual(inventory.quantity, data["quantity"])
        self.assertEqual(inventory.condition.name, data["condition"])
        self.assertEqual(inventory.restock_level, data["restock_level"])

    def test_deserialize_missing_data(self):
        """It should not deserialize a Inventory with missing data"""
        data = {"id": 1, "inventory_name": "Apple", "category": "Fruits"}
        inventory = Inventory()
        self.assertRaises(DataValidationError, inventory.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        inventory = Inventory()
        self.assertRaises(DataValidationError, inventory.deserialize, data)

    def test_deserialize_bad_quantity(self):
        """It should not deserialize a bad quantity attribute"""
        test_inventory = InventoryFactory()
        data = test_inventory.serialize()
        data["quantity"] = "aaa"
        inventory = Inventory()
        self.assertRaises(DataValidationError, inventory.deserialize, data)

    def test_deserialize_bad_restock_level(self):
        """It should not deserialize a bad restock_level attribute"""
        test_inventory = InventoryFactory()
        data = test_inventory.serialize()
        data["restock_level"] = "aaa"
        inventory = Inventory()
        self.assertRaises(DataValidationError, inventory.deserialize, data)


######################################################################
#  T E S T   E X C E P T I O N   H A N D L E R S
######################################################################
class TestExceptionHandlers(TestCaseBase):
    """Inventory Model Exception Handlers"""

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        inventory = InventoryFactory()
        self.assertRaises(DataValidationError, inventory.create)

    @patch("service.models.db.session.commit")
    def test_update_exception(self, exception_mock):
        """It should catch a update exception"""
        exception_mock.side_effect = Exception()
        inventory = InventoryFactory()
        self.assertRaises(DataValidationError, inventory.update)

    @patch("service.models.db.session.commit")
    def test_delete_exception(self, exception_mock):
        """It should catch a delete exception"""
        exception_mock.side_effect = Exception()
        inventory = InventoryFactory()
        self.assertRaises(DataValidationError, inventory.delete)


######################################################################
#  Q U E R Y   T E S T   C A S E S
######################################################################
class TestModelQueries(TestCaseBase):
    """Inventory Model Query Tests"""

    def test_find_inventory(self):
        """It should Find a Inventory by ID"""
        inventories = InventoryFactory.create_batch(5)
        for inventory in inventories:
            inventory.create()
        logging.debug(inventories)
        # make sure they got saved
        self.assertEqual(len(Inventory.all()), 5)
        # find the 2nd inventory in the list
        inventory = Inventory.find(inventories[1].id)
        self.assertIsNot(inventory, None)
        self.assertEqual(inventory.id, inventories[1].id)
        self.assertEqual(inventory.inventory_name, inventories[1].inventory_name)
        self.assertEqual(inventory.category, inventories[1].category)
        self.assertEqual(inventory.quantity, inventories[1].quantity)

    def test_find_by_category(self):
        """It should Find Inventories by Category"""
        inventories = InventoryFactory.create_batch(10)
        for inventory in inventories:
            inventory.create()
        category = inventories[0].category
        count = len(
            [inventory for inventory in inventories if inventory.category == category]
        )
        found = Inventory.find_by_category(category)
        self.assertEqual(found.count(), count)
        for inventory in found:
            self.assertEqual(inventory.category, category)

    def test_find_by_name(self):
        """It should Find a Inventories by Name"""
        inventories = InventoryFactory.create_batch(10)
        for inventory in inventories:
            inventory.create()
        name = inventories[0].inventory_name
        count = len(
            [inventory for inventory in inventories if inventory.inventory_name == name]
        )
        found = Inventory.find_by_inventory_name(name)
        self.assertEqual(found.count(), count)
        for inventory in found:
            self.assertEqual(inventory.inventory_name, name)

    def test_find_by_quantity(self):
        """It should Find a Inventories by Quantity"""
        inventories = InventoryFactory.create_batch(10)
        for inventory in inventories:
            inventory.create()
        quantity = inventories[0].quantity
        count = len(
            [inventory for inventory in inventories if inventory.quantity == quantity]
        )
        found = Inventory.find_by_quantity(quantity)
        self.assertEqual(found.count(), count)
        for inventory in found:
            self.assertEqual(inventory.quantity, quantity)

    def test_find_by_condition(self):
        """It should Find Inventories by Condition"""
        inventories = InventoryFactory.create_batch(10)
        for inventory in inventories:
            inventory.create()
        condition = inventories[0].condition
        count = len(
            [inventory for inventory in inventories if inventory.condition == condition]
        )
        found = Inventory.find_by_condition(condition)
        self.assertEqual(found.count(), count)
        for inventory in found:
            self.assertEqual(inventory.condition, condition)

    def test_find_by_restock_level(self):
        """It should Find a Inventories by Restock_level"""
        inventories = InventoryFactory.create_batch(10)
        for inventory in inventories:
            inventory.create()
        restock_level = inventories[0].restock_level
        count = len(
            [
                inventory
                for inventory in inventories
                if inventory.restock_level == restock_level
            ]
        )
        found = Inventory.find_by_restock_level(restock_level)
        self.assertEqual(found.count(), count)
        for inventory in found:
            self.assertEqual(inventory.restock_level, restock_level)

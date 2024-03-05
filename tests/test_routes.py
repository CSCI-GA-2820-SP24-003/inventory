"""
TestYourResourceModel API Service Test Suite
"""
import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Inventory
from .factories import InventoryFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)

BASE_URL = "/inventory"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceService(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Inventory).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    def _create_items(self, count):
        """Factory method to create items in bulk"""
        items = []
        for _ in range(count):
            test_item = InventoryFactory()
            response = self.client.post(BASE_URL, json=test_item.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test item",
            )
            new_item = response.get_json()
            test_item.id = new_item["id"]
            items.append(test_item)
        return items

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_item_list(self):
        """It should Get a list of items"""
        self._create_items(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_get_inventory(self):
        """It should Get a single Inventory"""
        # get the id of a inventory
        test_inventory = self._create_items(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_inventory.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["inventory_name"], test_inventory.inventory_name)

    def test_delete_inventory_success(self):
        """ Test deleting an inventory """
        # Create a test inventory item
        test_inventory = InventoryFactory()
        response = self.client.post(BASE_URL, json=test_inventory.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        id = response.json["id"]

        resp = self.client.delete(f"/inventory/{id}")

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        deleted_inventory = Inventory.find(test_inventory.id)
        self.assertIsNone(deleted_inventory)

    def test_delete_non_existent_inventory(self):
        """ Test deleting a non-existent inventory """
        # Make a DELETE request to delete an inventory item with a non-existent ID
        non_existent_inventory_id = 99999
        resp = self.client.delete(f"/inventory/{non_existent_inventory_id}")

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Inventory not found", resp.data.decode())

    def test_update_inventory(self):
        """It should Update an existing Inventory"""
        # create a inventory to update
        test_inventory = InventoryFactory()
        response = self.client.post(BASE_URL, json=test_inventory.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the inventory
        new_inventory = response.get_json()
        logging.debug(new_inventory)
        new_inventory["category"] = "unknown"
        response = self.client.put(f"{BASE_URL}/{new_inventory['id']}", json=new_inventory)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_inventory = response.get_json()
        self.assertEqual(updated_inventory["category"], "unknown")

    def test_update_non_existent_inventory(self):
        """ Test updating a non-existent inventory """
        # Make a PUT request to update an inventory item with a non-existent ID
        non_existent_inventory_id = 99999
        updated_inventory = {
            "inventory_name": "Updated Name",
            "category": "Updated Category",
            "quantity": 100
        }
        resp = self.client.put(
            f"/inventory/{non_existent_inventory_id}", json=updated_inventory
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_inventory_with_category_filter(self):
        """Test listing inventory with category filter"""
        test_inventory_1 = InventoryFactory(category="Category1")
        test_inventory_2 = InventoryFactory(category="Category2")
        test_inventory_3 = InventoryFactory(category="Category1")
        self.client.post("/inventory", json=test_inventory_1.serialize())
        self.client.post("/inventory", json=test_inventory_2.serialize())
        self.client.post("/inventory", json=test_inventory_3.serialize())

        response = self.client.get("/inventory?category=Category1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(len(data), 2)
        for item in data:
            self.assertEqual(item["category"], "Category1")

    def test_list_inventory_with_name_filter(self):
        """Test listing inventory with name filter"""
        test_inventory_1 = InventoryFactory(inventory_name="Item1")
        test_inventory_2 = InventoryFactory(inventory_name="Item2")
        test_inventory_3 = InventoryFactory(inventory_name="Item1")

        self.client.post("/inventory", json=test_inventory_1.serialize())
        self.client.post("/inventory", json=test_inventory_2.serialize())
        self.client.post("/inventory", json=test_inventory_3.serialize())

        response = self.client.get("/inventory?name=Item1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.get_json()
        self.assertEqual(len(data), 2)
        for item in data:
            self.assertEqual(item["inventory_name"], "Item1")

    def test_create_inventory(self):
        """It should Create a new Inventory"""
        test_inventory = InventoryFactory()
        logging.debug("Test Inventory: %s", test_inventory.serialize())
        response = self.client.post(BASE_URL, json=test_inventory.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_inventory = response.get_json()
        self.assertEqual(new_inventory["inventory_name"], test_inventory.inventory_name)
        self.assertEqual(new_inventory["category"], test_inventory.category)
        self.assertEqual(new_inventory["quantity"], test_inventory.quantity)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_inventory = response.get_json()
        self.assertEqual(new_inventory["inventory_name"], test_inventory.inventory_name)
        self.assertEqual(new_inventory["category"], test_inventory.category)
        self.assertEqual(new_inventory["quantity"], test_inventory.quantity)

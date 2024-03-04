"""
TestYourResourceModel API Service Test Suite
"""
import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Inventory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


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

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_delete_inventory_success(self):
        """ Test deleting an inventory """
        # Create a test inventory item
        inventory = Inventory(inventory_name="Test Product", category="Test Category", quantity=10)
        inventory.create()
        inventory_id = inventory.id

        resp = self.client.delete(f"/inventory/{inventory_id}")

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        deleted_inventory = Inventory.find(inventory_id)
        self.assertIsNone(deleted_inventory)
    
    def test_delete_non_existent_inventory(self):
        """ Test deleting a non-existent inventory """
        # Make a DELETE request to delete an inventory item with a non-existent ID
        non_existent_inventory_id = 99999
        resp = self.client.delete(f"/inventory/{non_existent_inventory_id}")

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Inventory not found", resp.data.decode())


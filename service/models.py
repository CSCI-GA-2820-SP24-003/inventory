"""
Models for YourResourceModel

All of the models are stored in this module
"""

import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DatabaseConnectionError(Exception):
    """Custom Exception when database connection fails"""


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Condition(Enum):
    """Enumeration of valid Inventory condition"""

    NEW = 0
    OPENED = 1
    USED = 3


class Inventory(db.Model):
    """
    Class that represents a Inventory
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    inventory_name = db.Column(db.String(63), nullable=False)
    category = db.Column(db.String(63), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    condition = db.Column(
        db.Enum(Condition), nullable=False, server_default=(Condition.NEW.name)
    )
    restock_level = db.Column(db.Integer, nullable=False)

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return f"<Inventory {self.inventory_name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Inventory to the database
        """
        logger.info("Creating %s", self.inventory_name)
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a Inventory to the database
        """
        logger.info("Saving %s", self.inventory_name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Inventory from the data store"""
        logger.info("Deleting %s", self.inventory_name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self) -> dict:
        """Serializes a Inventory into a dictionary"""
        return {
            "id": self.id,
            "inventory_name": self.inventory_name,
            "category": self.category,
            "quantity": self.quantity,
            "condition": self.condition.name,
            "restock_level": self.restock_level,
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Inventory from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.inventory_name = data["inventory_name"]
            self.category = data["category"]
            if isinstance(data["quantity"], int):
                self.quantity = data["quantity"]
            else:
                raise DataValidationError(
                    "Invalid type for int [quantity]: " + str(type(data["quantity"]))
                )
            self.condition = getattr(Condition, data["condition"])
            if isinstance(data["restock_level"], int):
                self.restock_level = data["restock_level"]
            else:
                raise DataValidationError(
                    "Invalid type for int [restock_level]: "
                    + str(type(data["restock_level"]))
                )
        except KeyError as error:
            raise DataValidationError(
                "Invalid Inventory: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Inventory: body of request contained bad or no data "
                + str(error)
            ) from error
        except AttributeError as error:
            raise DataValidationError(
                "Invalid Condition Word. Expect: NEW, OPENED, USED; Got: " + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Inventories in the database"""
        logger.info("Processing all Inventories")
        return cls.query.all()

    @classmethod
    def find(cls, inventory_id: int):
        """Finds a Inventories by it's ID"""
        logger.info("Processing lookup for id %s ...", inventory_id)
        return cls.query.get(inventory_id)

    @classmethod
    def search(cls, args: dict):
        """Finds an item by multiple criteria"""
        logger.info("Processing query for multiple filter %s ...", args)
        query_filter = []
        if args["name"]:
            query_filter.append(cls.inventory_name == args["name"])
        if args["category"]:
            query_filter.append(cls.category == args["category"])
        if args["quantity"]:
            query_filter.append(cls.quantity == int(args["quantity"]))
        if args["restock_level"]:
            query_filter.append(cls.restock_level == int(args["restock_level"]))
        if args["condition"]:
            query_filter.append(cls.condition == args["condition"])
        return cls.query.filter(*query_filter)

    @classmethod
    def remove_all(cls):
        """Removes all documents from the database (use for testing)"""
        for document in cls.database:  # pylint: disable=(not-an-iterable
            document.delete()

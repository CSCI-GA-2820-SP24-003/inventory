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


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Condition(Enum):
    """Enumeration of valid Inventory condition"""

    NEW = 0
    OPEN = 1
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
    def find_by_inventory_name(cls, name: str) -> list:
        """Returns all Inventories with the given name

        Args:
            name (string): the name of the Inventories you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.inventory_name == name)

    @classmethod
    def find_by_category(cls, category: str) -> list:
        """Returns all of the Inventories in a category"""
        logger.info("Processing category query for %s ...", category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_quantity(cls, quantity: int) -> list:
        """Returns all of the Inventories in a quantity"""
        logger.info("Processing quantity query for %s ...", quantity)
        return cls.query.filter(cls.quantity == quantity)

    @classmethod
    def find_by_condition(cls, condition: Condition = Condition.NEW) -> list:
        """Returns all of the Inventories in a condition"""
        logger.info("Processing quantity query for %s ...", condition)
        return cls.query.filter(cls.condition == condition)

    @classmethod
    def find_by_restock_level(cls, restock_level: int) -> list:
        """Returns all of the Inventories in a restock_level"""
        logger.info("Processing quantity query for %s ...", restock_level)
        return cls.query.filter(cls.restock_level == restock_level)

######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
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
######################################################################

"""
Inventory Store Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Items from the inventory of Items in the InventoryShop
"""

from flask import jsonify, abort
from flask import current_app as app  # Import Flask application
from flask_restx import Resource, fields, reqparse
from service.models import Inventory, Condition
from service.common import status  # HTTP Status Codes
from . import api


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Return the health status of the service"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return app.send_static_file("index.html")


# Define the model so that the docs reflect what can be sent
inventory_item = api.model(
    "InventoryItem",
    {
        "inventory_name": fields.String(
            required=True, description="The name of an item"
        ),
        "category": fields.String(
            required=True,
            description="The category of an item",
        ),
        "quantity": fields.Integer(
            required=True, description="The quantity of an item"
        ),
        "condition": fields.String(
            enum=Condition._member_names_,
            description="The condition of an item (NEW, OPENED, USED)",
        ),
        "restock_level": fields.Integer(
            required=True, description="The restock level of an item"
        ),
    },
)

item_model = api.inherit(
    "ItemModel",
    inventory_item,
    {
        "id": fields.Integer(  # "_id": fields.String won't work
            readOnly=True, description="The unique id assigned internally by service"
        ),
    },
)

# Tell RESTX how to handle query string arguments
item_args = reqparse.RequestParser()
item_args.add_argument(
    "name", type=str, location="args", required=False, help="List items by name"
)
item_args.add_argument(
    "category", type=str, location="args", required=False, help="List items by category",
)
item_args.add_argument(
    "quantity", type=int, location="args", required=False, help="List items by quantity",
)
item_args.add_argument(
    "condition", type=str, choices=('NEW', 'OPENED', 'USED'),
    location="args", required=False, help="List items by condition",
)
item_args.add_argument(
    "restock_level", type=int, location="args", required=False, help="List items by restock_level",
)

######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
#  PATH: /inventory/{id}
######################################################################
@api.route("/inventory/<id>")
@api.param("id", "The inventory identifier")
class InventoryResource(Resource):
    """
    InventoryResource class

    Allows the manipulation of a single inventory item
    GET /inventory{id} - Returns an item with the id
    PUT /inventory{id} - Update an item with the id
    DELETE /inventory{id} -  Deletes an item with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE AN ITEM
    # ------------------------------------------------------------------
    @api.doc("get_item")
    @api.response(404, "Item not found")
    @api.marshal_with(item_model)
    def get(self, id):
        """
        Retrieve a single item

        This endpoint will return an item based on it's id
        """
        app.logger.info("Request for item with id: %s", id)
        item = Inventory.find(id)
        if not item:
            error(status.HTTP_404_NOT_FOUND, f"Item with id '{id}' was not found.")
        app.logger.info("Returning item: %s", item.inventory_name)
        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING PET
    # ------------------------------------------------------------------
    @api.doc("update_item")
    @api.response(404, "Item not found")
    @api.response(400, "The posted Item data was not valid")
    @api.expect(item_model)
    @api.marshal_with(item_model)
    def put(self, id):
        """
        Update an item

        This endpoint will update an item based the body that is posted
        """
        app.logger.info("Request to update item with id [%s]", id)
        item = Inventory.find(id)
        if not item:
            error(status.HTTP_404_NOT_FOUND, f"Item with id: '{id}' was not found.")
        data = api.payload
        app.logger.debug("Payload = %s", data)
        item.deserialize(data)
        item.id = id
        item.update()
        app.logger.info("Item %s updated.", item.inventory_name)
        return item.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE AN ITEM
    # ------------------------------------------------------------------
    @api.doc("delete_item")
    @api.response(204, "Item deleted")
    def delete(self, id):
        """
        Delete an item.
        This endpoint will delete an item based on the id.
        """
        app.logger.info("Request to Delete an item with id [%s]", id)
        item = Inventory.find(id)
        if item:
            item.delete()
            app.logger.info("Item %s deleted", item.inventory_name)
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /inventory
######################################################################
@api.route("/inventory", strict_slashes=False)
class InventoryCollection(Resource):
    """Handles all interactions with collections of Inventory"""

    # ------------------------------------------------------------------
    # LIST ALL ITEMS IN THE INVENTORY
    # ------------------------------------------------------------------
    @api.doc("list_items")
    @api.expect(item_args, validate=True)
    @api.marshal_list_with(item_model)
    def get(self):
        """Returns all of the Items"""
        app.logger.info("Request for item list")
        inventory = []
        args = item_args.parse_args()

        if args:
            app.logger.info("Returning filtered list.")
            inventory = Inventory.search(args)
        else:
            app.logger.info("Returning unfiltered list.")
            inventory = Inventory.all()
        
        results = [item.serialize() for item in inventory]
        app.logger.info("Returning %d items", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW ITEM
    # ------------------------------------------------------------------
    @api.doc("create_item")
    @api.response(400, "The posted data was not valid")
    @api.expect(inventory_item)
    @api.marshal_with(item_model, code=201)
    def post(self):
        """
        Creates an item

        This endpoint will create an item based the data in the body that is posted
        """
        app.logger.info("Request to create an item")
        item = Inventory()
        app.logger.debug("Payload = %s", api.payload)
        item.deserialize(api.payload)
        item.create()
        app.logger.info("Item %s created.", item.inventory_name)
        location_url = api.url_for(InventoryResource, id=item.id, _external=True)
        return item.serialize(), status.HTTP_201_CREATED, {"Location": location_url}

    # ------------------------------------------------------------------
    # DELETE ALL PETS (for testing only)
    # ------------------------------------------------------------------
    @api.doc("delete_all_items", security="apikey")
    @api.response(204, "All Items deleted")
    def delete(self):
        """
        Delete all Items

        This endpoint will delete all Items only if the system is under test
        """
        app.logger.info("Request to Delete all items...")
        if "TESTING" in app.config and app.config["TESTING"]:
            Inventory.remove_all()
            app.logger.info("Removed all Items from the database")
        else:
            app.logger.warning("Request to clear database while system not under test")

        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /inventory/{id}/restock
######################################################################
@api.route("/inventory/<id>/restock")
@api.param("id", "The Inventory identifier")
class RestockResource(Resource):
    """Restock actions on an item"""

    @api.doc("restock_item")
    @api.response(404, "Item not found")
    @api.response(400, "Bad quantity: quantity not enough for restock")
    def put(self, id):
        """
        Restock an item

        This endpoint will restock an item and change the quantity
        """
        app.logger.info("Request to restock with id: %s", id)
        item = Inventory.find(id)
        if not item:
            error(status.HTTP_404_NOT_FOUND, f"Item with id '{id}' was not found.")
        
        if item.quantity > item.restock_level: 
            error(
                status.HTTP_400_BAD_REQUEST,
                f'No need to restock: '
                f'quantity [{item.quantity}] greater than '
                f'restock level [{item.restock_level}]',
            )
        
        # add the number of items sold to restock_level
        # the more we sold, the more we add, vice versa
        # (may use more sophisticated rule)
        item.quantity = 2*item.restock_level-item.quantity
        item.update()
        app.logger.info("Item %s restocked.", item.inventory_name)
        return item.serialize(), status.HTTP_200_OK


######################################################################
# Logs error messages before aborting
######################################################################
def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    abort(status_code, reason)


# Below code no longer needed because reqparse does checks for us
# ######################################################################
# # Checks the ContentType of a request
# ######################################################################
# def check_content_type(content_type):
#     """Checks that the media type is correct"""
#     if "Content-Type" not in request.headers:
#         app.logger.error("No Content-Type specified.")
#         error(
#             status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#             f"Content-Type must be {content_type}",
#         )

#     if request.headers["Content-Type"] == content_type:
#         return

#     app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
#     error(
#         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#         f"Content-Type must be {content_type}",
#     )

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

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Inventory
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

######################################################################
# LIST ALL ITEMS
######################################################################
@app.route("/inventory", methods=["GET"])
def list_inventory():
    """Returns all of the Items"""
    app.logger.info("Request for item list")

    inventory = []

    # See if any query filters were passed in
    category = request.args.get("category")
    name = request.args.get("name")
    if category:
        inventory = Inventory.find_by_category(category)
    elif name:
        inventory = Inventory.find_by_inventory_name(name)
    else:
        inventory = Inventory.all()

    results = [item.serialize() for item in inventory]
    app.logger.info("Returning %d inventory", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# CREATE A NEW INVENTORY
######################################################################
@app.route("/inventory", methods=["POST"])
def create_inventory():
    """
    Creates an Inventory

    This endpoint will create a Inventory based the data in the body that is posted
    """
    app.logger.info("Request to create an inventory")
    check_content_type("application/json")

    inventory = Inventory()
    inventory.deserialize(request.get_json())
    inventory.create()
    message = inventory.serialize()
    location_url = url_for("get_inventory", id=inventory.id, _external=True)

    app.logger.info("Inventory with ID: %d created.", inventory.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# READ AN INVENTORY
######################################################################
@app.route("/inventory/<int:id>", methods=["GET"])
def get_inventory(id):
    """
    Retrieve a single Inventory

    This endpoint will return a Inventory based on it's id
    """
    app.logger.info("Request for inventory with id: %s", id)

    inventory = Inventory.find(id)
    if not inventory:
        error(status.HTTP_404_NOT_FOUND, f"Inventory with id '{id}' was not found.")

    app.logger.info("Returning inventory: %s", inventory.inventory_name)
    return jsonify(inventory.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A INVENTORY
######################################################################
@app.route('/inventory/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    """
    Delete an Inventory.
    This endpoint will delete an Inventory based on the id.
    """
    app.logger.info("Request to delete inventory with key ({})".format(id))

    # Find the inventory by id
    inventory = Inventory.find(id)

    if inventory is None:
        return '', status.HTTP_204_NO_CONTENT

    # Delete the inventory
    inventory.delete()

    app.logger.info("Inventory with id {} deleted".format(id))

    # Return a response with 204 No Content status code
    return '', status.HTTP_204_NO_CONTENT


######################################################################
# UPDATE AN EXISTING INVENTORY
######################################################################
@app.route("/inventory/<int:id>", methods=["PUT"])
def update_inventories(id):
    """
    Update a Inventory

    This endpoint will update a Inventory based the body that is posted
    """
    app.logger.info("Request to update inventory with id: %d", id)
    check_content_type("application/json")

    inventory = Inventory.find(id)
    if not inventory:
        error(status.HTTP_404_NOT_FOUND, f"Inventory with id: '{id}' was not found.")

    inventory.deserialize(request.get_json())
    inventory.id = id
    inventory.update()

    app.logger.info("Inventory with ID: %d updated.", inventory.id)
    return jsonify(inventory.serialize()), status.HTTP_200_OK


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        error(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    error(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# Logs error messages before aborting
######################################################################
def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    abort(status_code, reason)

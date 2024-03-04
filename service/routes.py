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
Pet Store Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Pets from the inventory of pets in the PetShop
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
        # If inventory is not found, return 404 Not Found
        app.logger.error("Inventory with id {} not found".format(id))
        return jsonify(message="Inventory not found"), status.HTTP_404_NOT_FOUND
    
    # Delete the inventory
    inventory.delete()
    
    app.logger.info("Inventory with id {} deleted".format(id))
    
    # Return a response with 204 No Content status code
    return 'deleted successfully', status.HTTP_204_NO_CONTENT

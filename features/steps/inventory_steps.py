import requests
from behave import given

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204


@given('the following items')
def step_impl(context):
    """ Delete all items and load new ones """

    # List all of the items and delete them one by one
    rest_endpoint = f"{context.base_url}/api/inventory"  # need the prefix api after refactor
    context.resp = requests.get(rest_endpoint)
    assert(context.resp.status_code == HTTP_200_OK)
    for inventory in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{inventory['id']}")
        assert(context.resp.status_code == HTTP_204_NO_CONTENT)

    # load the database with new items
    for row in context.table:
        payload = {
            "inventory_name": row['name'],
            "category": row['category'],
            "quantity": int(row['quantity']),
            "condition": row['condition'],
            "restock_level": int(row['restock_level'])
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        assert(context.resp.status_code == HTTP_201_CREATED)


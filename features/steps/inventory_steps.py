"""
Web Steps
"""

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
from behave import when, then

ID_PREFIX = "inventory_"


@when('I visit the "Home Page"')
def step_impl(context):
    """Make a call to the base URL"""
    context.driver.get(context.base_url)


@then('I should see "{message}" in the title')
def step_impl(context, message):
    """Check the document title for a message"""
    assert message in context.driver.title

@then('I should not see "404 Not Found"')
def step_impl(context):
    assert "404 Not Found" not in context.driver.title

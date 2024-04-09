Feature: The inventory service back-end
    As an e-commerce platform manager
    I need a RESTful catalog service
    So that I can keep track of all my inventory

 Background:
    Given the following inventories
        | name       | category     | quantity  | condition  | restock_level  |
        | iphone     | electronics  | 20        | NEW        | 100            |
        | apple      | fruit        | 30        | NEW        | 110            |
        | ipad       | electronics  | 40        | USED       | 120            |
        | peach      | fruit        | 50        | OPEN       | 130            |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Inventory
    When I visit the "Home Page"
    And I set the "Name" to "ipod"
    And I set the "Category" to "electronics"
    And I set the "Quantity" to "60"
    And I select "New" in the "Condition" dropdown
    And I set the "Restock_level" to "150"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Category" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "ipod" in the "Name" field
    And I should see "electronics" in the "Category" field
    And I should see "60" in the "Quantity" field
    And I should see "New" in the "Condition" dropdown
    And I should see "150" in the "Restock_level" field

Scenario: List all inventories
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "iphone" in the results
    And I should see "ipad" in the results

Scenario: Search for electronics
    When I visit the "Home Page"
    And I set the "Category" to "electronics"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "iphone" in the results
    And I should not see "apple" in the results
    And I should not see "peach" in the results

Scenario: Search for Condition
    When I visit the "Home Page"
    And I select "New" in the "Condition" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "iphone" in the results
    And I should see "apple" in the results
    And I should not see "peach" in the results

Scenario: Update a Inventory
    When I visit the "Home Page"
    And I set the "Name" to "iphone"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "iphone" in the "Name" field
    And I should see "electronics" in the "Category" field
    When I change "Name" to "huawei"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "huawei" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "huawei" in the results
    And I should not see "iphone" in the results

Scenario: Restock
    When I visit the "Home Page"
    And I set the "Name" to "ipod"
    And I set the "Category" to "electronics"
    And I set the "Quantity" to "60"
    And I select "New" in the "Condition" dropdown
    And I set the "Restock_level" to "150"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Category" field should be empty
    When I paste the "Id" field
    And I set the "Restock_quantity" to "30"
    And I press the "Restock" button   
    Then I should see the message "Success"
    And I should see "ipod" in the "Name" field
    And I should see "90" in the "Quantity" field
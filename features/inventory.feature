Feature: The inventory service back-end
    As an e-commerce platform manager
    I need a RESTful catalog service
    So that I can keep track of all my inventory

# Background:
#     Given the following pets
#         | name       | category | available | gender  | birthday   |
#         | fido       | dog      | True      | MALE    | 2019-11-18 |
#         | kitty      | cat      | True      | FEMALE  | 2020-08-13 |
#         | leo        | lion     | False     | MALE    | 2021-04-01 |
#         | sammy      | snake    | True      | UNKNOWN | 2018-06-04 |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Inventory Demo RESTful Service" in the title
    And I should not see "404 Not Found"
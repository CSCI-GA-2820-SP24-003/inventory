$(function () {

    let root = "/api/inventory";

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#inventory_id").val(res.id);
        $("#inventory_name").val(res.inventory_name);
        $("#inventory_category").val(res.category);
        $("#inventory_quantity").val(res.quantity);
        $("#inventory_condition").val(res.condition);
        $("#inventory_restock_level").val(res.restock_level);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#inventory_name").val("");
        $("#inventory_category").val("");
        $("#inventory_quantity").val("");
        $("#inventory_condition").val("");
        $("#inventory_restock_level").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Inventory
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#inventory_name").val();
        let category = $("#inventory_category").val();
        let quantity = parseInt($("#inventory_quantity").val(), 10);
        let condition = $("#inventory_condition").val();
        let restock_level = parseInt($("#inventory_restock_level").val(), 10);

        let data = {
            "inventory_name": name,
            "category": category,
            "quantity": quantity,
            "condition": condition,
            "restock_level": restock_level
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "${root}",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Inventory
    // ****************************************

    $("#update-btn").click(function () {

        let inventory_id = $("#inventory_id").val();
        let name = $("#inventory_name").val();
        let category = $("#inventory_category").val();
        let quantity = parseInt($("#inventory_quantity").val(), 10);
        let condition = $("#inventory_condition").val();
        let restock_level = parseInt($("#inventory_restock_level").val(), 10);

        let data = {
            "inventory_name": name,
            "category": category,
            "quantity": quantity,
            "condition": condition,
            "restock_level": restock_level
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `${root}/${inventory_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Inventory
    // ****************************************

    $("#retrieve-btn").click(function () {

        let inventory_id = $("#inventory_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `${root}/${inventory_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Inventory
    // ****************************************

    $("#delete-btn").click(function () {

        let inventory_id = $("#inventory_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `${root}/${inventory_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Inventory has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#inventory_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Restock a Inventory
    // ****************************************

    $("#restock-btn").click(function () {

        let inventory_id = $("#inventory_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `${root}/${inventory_id}/restock`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });



    // ****************************************
    // Search for a Inventory
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#inventory_name").val();
        let category = $("#inventory_category").val();
        let quantity = $("#inventory_quantity").val();
        let condition = $("#inventory_condition").val();
        let restock_level = $("#inventory_restock_level").val();

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (quantity) {
            if (queryString.length > 0) {
                queryString += '&quantity=' + quantity
            } else {
                queryString += 'quantity=' + quantity
            }
        }
        if (condition) {
            if (queryString.length > 0) {
                queryString += '&condition=' + condition
            } else {
                queryString += 'condition=' + condition
            }
        }
        if (restock_level) {
            if (queryString.length > 0) {
                queryString += '&restock_level=' + restock_level
            } else {
                queryString += 'restock_level=' + restock_level
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `${root}?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Category</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-2">Condition</th>'
            table += '<th class="col-md-2">Restock_level</th>'
            table += '</tr></thead><tbody>'
            let firstInventory = "";
            for(let i = 0; i < res.length; i++) {
                let inventory = res[i];
                table +=  `<tr id="row_${i}"><td>${inventory.id}</td><td>${inventory.inventory_name}</td><td>${inventory.category}</td><td>${inventory.quantity}</td><td>${inventory.condition}</td><td>${inventory.restock_level}</td></tr>`;
                if (i == 0) {
                    firstInventory = inventory;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstInventory != "") {
                update_form_data(firstInventory)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})

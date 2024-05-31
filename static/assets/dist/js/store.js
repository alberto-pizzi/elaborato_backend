function getTotalItems(response){
    if (response.total_items !== undefined) {
        $('#cart-total').text('Cart (' + response.total_items + ')');
    } else {
        console.error('Error: total items not found into response');
    }
}

function getAjaxErrorMessage(xhr, status, error) {
        console.error('Error during AJAX request:', status, error);
    }

function toggleCartOptions(response, add_button){
    let remove_button = add_button.closest('.product_data').find('.cart-options');
    if (response.cart_item_quantity !== undefined) {
        if (response.cart_item_quantity > 0) {
            remove_button.show();
        } else {
            remove_button.hide();
        }
    }
    else {
        console.error('Error: item quantity not found into response');
    }
}

$('.add-to-cart-button').click(function (e){
   e.preventDefault();

   let product_id = $(this).closest('.product_data').find('.prod_id').val();
   let product_qty = 1;
   let token = $('input[name=csrfmiddlewaretoken]').val();
   let addButton = $(this);
   $.ajax({
       method: "POST",
       url: "order/add-to-cart",
       data: {
           'product_id': product_id,
           'product_qty': product_qty,
           csrfmiddlewaretoken: token
       },
       dataType: "json",
       success: function (response){
           getTotalItems(response);
           toggleCartOptions(response, addButton);
       },
       error: getAjaxErrorMessage
   });

});

$('.remove-from-cart').click(function (e){
   e.preventDefault();

   let product_id = $(this).closest('.product_data').find('.prod_id').val();
   let product_qty = 1;
   let token = $('input[name=csrfmiddlewaretoken]').val();
   let addButton = $(this);
   $.ajax({
       method: "POST",
       url: "order/remove-from-cart",
       data: {
           'product_id': product_id,
           'product_qty': product_qty,
           csrfmiddlewaretoken: token
       },
       dataType: "json",
       success: function (response){
           getTotalItems(response);
           toggleCartOptions(response, addButton);
       },
       error: getAjaxErrorMessage
   });

});


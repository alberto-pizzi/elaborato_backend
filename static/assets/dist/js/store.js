

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

//TODO review this code



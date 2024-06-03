
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

function getProductQuantity(){
    let selectElement = document.querySelector('select#select-quantity');

    if (selectElement.value === '20+'){
        let inputElement = document.querySelector('input#select-quantity');
        return parseInt(inputElement.value)
    }
    else{
        return parseInt(selectElement.value)
    }
}

document.getElementById('select-quantity').addEventListener('change', function() {
    let moreQuantityInput = document.querySelector('input#select-quantity')
    if (this.value === '20+') {
        moreQuantityInput.classList.remove('d-none');
        moreQuantityInput.classList.add('d-block');
    }
    else{
        moreQuantityInput.classList.add('d-none');
        moreQuantityInput.classList.remove('d-block');
    }
});


$('.add-to-cart').click(function (e){
   e.preventDefault();

   let product_id = $(this).closest('.product_data').find('.prod_id').val();
   let product_size = $('select#select-size').val();
   let product_color = $('select#select-color').val();
   let token = $('input[name=csrfmiddlewaretoken]').val();
   let addButton = $(this);

   let ajax_url = document.getElementById('ajax_url').value

   $.ajax({
       method: "POST",
       url: ajax_url,
       data: {
           'product_id': product_id,
           'product_qty': getProductQuantity(),
           'product_size': product_size,
           'product_color': product_color,
           csrfmiddlewaretoken: token
       },
       dataType: "json",
       success: function (response){
           getTotalItems(response);
           //toggleCartOptions(response, addButton);
       },
       error: getAjaxErrorMessage
   });

});

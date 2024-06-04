
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


function updateSizes(response){
    $('.size-selector').prop('disabled',false);
    response.sizes_out_of_stock.forEach(function (item){
        let sizeId = 'size_' + item
        console.log('size id for: ', response.sizes_out_of_stock);
        document.getElementById(sizeId).disabled = true;
    });
}

function updateProductPrice(response){
    $('#product-price').text(response.new_price);
    console.log('cambio prezzo');
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

document.getElementById('select-color').addEventListener('change', function() {
    let product_id = $(this).closest('.product_data').find('.prod_id').val();
    let product_color = $('select#select-color').val();

    let token = $('input[name=csrfmiddlewaretoken]').val();

    let ajax_url = $('#update-product-url').val();

    //let size_selected = $('input[name="size"]:checked').val();

   $.ajax({
       method: "POST",
       url: ajax_url,
       data: {
           'prod_id': product_id,
           'product_color_id': product_color,
           //'product_size_id_selected': size_selected,
           csrfmiddlewaretoken: token
       },
       dataType: "json",
       success: function (response){
           console.log('ritorno successo');
           updateSizes(response);
           updateProductPrice(response);
           //toggleCartOptions(response, addButton);
       },
       error: getAjaxErrorMessage
   });



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

// FIXME remove redundancy
function getAjaxErrorMessage(xhr, status, error) {
        console.error('Error during AJAX request:', status, error);
    }

function removeCartItem(item){
    item.addClass('d-none');
}

function updateCart(response){
    $('#total-price').text(response.total_price);
    $('#total-items').text(response.total_items);
}

$('.remove-from-cart').click(function (e){
   e.preventDefault();

   let product_id = $(this).closest('.product_data').find('.prod_id').val();
   let item = $(this).closest('.product_data');
   let product_qty = 1
   let token = $('input[name=csrfmiddlewaretoken]').val();
   let addButton = $(this);

   let ajax_url = document.getElementById('remove-from-cart').value
   $.ajax({
       method: "POST",
       url: ajax_url,
       data: {
           'product_id': product_id,
           'product_qty': product_qty,
           csrfmiddlewaretoken: token
       },
       dataType: "json",
       success: function (response){
           console.log('success');
           removeCartItem(item);
           updateCart(response);
       },
       error: getAjaxErrorMessage
   });

});

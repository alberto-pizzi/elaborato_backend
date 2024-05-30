$('.add-to-cart-button').click(function (e){
   e.preventDefault();

   let product_id = $(this).closest('.product_data').find('.prod_id').val();
   console.log("Product ID: ", product_id);
   let product_qty = 1;
   let token = $('input[name=csrfmiddlewaretoken]').val();
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

            if (response.total_items !== undefined) {
                $('#cart-total').text('Cart (' + response.total_items + ')');
            } else {
                console.error('Error: total items not found into response');
            }
       },
       error: function(xhr, status, error) {
        console.error('Error during AJAX request:', status, error);
    }
   });

});

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
        let sizeId = 'size_' + item;
        document.getElementById(sizeId).disabled = true;
    });
}

function updateProductPrice(response){
    $('#product-price').text(response.new_price);
}

function updateProductImage(response){
    $('#product-image').attr('src',response.new_image_url);
}

function getSizeSelected(){
    let radio = document.getElementsByName('size');
    for (let i = 0; i < radio.length; i++){
        if (radio[i].checked){
            return radio[i].value;
        }
    }
    return null;
}

function showNotification(response) {
    if (response.result_message !== undefined) {
        console.log(response.result_message);
        let banner = $('#notification-banner');
        $('#notification-text').text(response.result_message);
        banner.removeClass('d-none');
        banner.addClass(response.alert_class);

        setTimeout(() => {
            banner.removeClass(response.alert_class);
            banner.addClass('d-none');
        }, 3000);
    }
    else{
        console.error('Error: total items not found into response');
    }
}

function showMessage(message,alertClass) {
    if (message !== undefined) {
        let banner = $('#notification-banner');
        $('#notification-text').text(message);
        banner.removeClass('d-none');
        banner.addClass(alertClass);

        setTimeout(() => {
            banner.removeClass(alertClass);
            banner.addClass('d-none');
        }, 3000);
    }
    else{
        console.error('Error showing message');
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

let selectColor = document.getElementById('select-color');

if (selectColor) {

    selectColor.addEventListener('change', function () {
        let product_id = $(this).closest('.product_data').find('.prod_id').val();
        let product_color = $('select#select-color').val();
        let token = $('input[name=csrfmiddlewaretoken]').val();
        let ajax_url = $('#update-product-url').val();


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
            success: function (response) {
                updateSizes(response);
                updateProductPrice(response);
                updateProductImage(response)
                //toggleCartOptions(response, addButton);
            },
            error: getAjaxErrorMessage
        });


    });
}


function checkFilledFields(size,color){
    let radioOptions = document.getElementsByName('size');
    let radioSelected = false;

    let isOk = true;

    if (radioOptions) {
        for (let i = 0; i < radioOptions.length; i++) {
            if (radioOptions[i].checked) {
                radioSelected = true;
                break;
            }
        }
    }


    let select = document.getElementById('select-color');
    let selectSelected;
    if (select) {
        let selectValue = select.value;

        if (selectValue) {
            selectSelected = selectValue !== '';
        }
    }

    console.log('size: ',radioOptions);
    if ((radioOptions.length > 0) && !radioSelected){
        isOk = false;
    }

    console.log('color: ',select);
    if (select && !selectSelected){
        isOk = false;
    }

    if (!isOk){
        showMessage("Select all fields required, please","alert-warning");
        return false;
    }
    else{
        return true;
    }
}

$('.add-to-cart').click(function (e){
   e.preventDefault();
   let product_id = $(this).closest('.product_data').find('.prod_id').val();
   let product_size = getSizeSelected();
   let product_color = $('select#select-color').val();
   let token = $('input[name=csrfmiddlewaretoken]').val();
   let addButton = $(this);

   let ajax_url = $('#ajax_url').val();

   if (checkFilledFields(product_size,product_color)) {
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
           success: function (response) {
               getTotalItems(response);
               showNotification(response);
           },
           error: getAjaxErrorMessage
       });
   }

});

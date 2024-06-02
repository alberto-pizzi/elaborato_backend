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


// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })
})()


function getAddressSelected(){
    let radio = document.getElementsByName('address');
    for (let i = 0; i < radio.length; i++){
        if (radio[i].checked){
            return radio[i].value;
        }
    }
    return null;
}


let save_element = document.getElementById('save-user');

if (save_element) {
    $('#sign-up-hidden-form .required-field').removeAttr('required');
    save_element.addEventListener('click', function () {
        let hiddenForm = document.getElementById('sign-up-hidden-form');
        if (this.checked) {
            hiddenForm.classList.remove('d-none');
            $('#sign-up-hidden-form .required-field').attr('required', 'required');
        } else {
            $('#sign-up-hidden-form .required-field').removeAttr('required');
            hiddenForm.classList.add('d-none');
        }
    });
}

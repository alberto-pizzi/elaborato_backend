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

// TODO implement required toggle per hiding form
document.getElementById('save-user').addEventListener('click', function() {
    let hiddenForm = document.getElementById('sign-up-hidden-form');
    if (this.checked) {
        hiddenForm.classList.remove('d-none');
    } else {
        hiddenForm.classList.add('d-none');
    }
});
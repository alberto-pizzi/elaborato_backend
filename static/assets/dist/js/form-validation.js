function validateForm() {

    // FIXME improve server-side validation (Ajax response)
    let pass1 = $('#password1');
    let pass2 = $('#password2');

    let valid = true;



    const excludedIds = ['email', 'password1', 'password2','username'];

    const requiredFields = document.querySelectorAll('#signup-form input[required],#signup-form select[required]');

    if (!validatePassword() || !validateEmail()){
        valid = false;
    }


    requiredFields.forEach(field => {



        if (!excludedIds.includes(field.id)) {

        if (field.value !== ''){
            returnSuccess(true,field);
        }
        else{
            valid = false;
            returnSuccess(false,field);
        }

        }
    });


    return valid;

}

function returnSuccess(isSuccess, inputField) {
    if (isSuccess) {
        $(inputField).addClass('is-valid');
        $(inputField).removeClass('is-invalid');
    } else {
        $(inputField).removeClass('is-valid');
        $(inputField).addClass('is-invalid');
    }
}

function validatePassword() {
    const passwordField = $('#password1')
    const passwordInput = passwordField.val().trim();

    const hasUpper = /[A-Z]/.test(passwordInput);
    const hasLower = /[a-z]/.test(passwordInput);
    const hasNumber = /\d/.test(passwordInput);

    if (hasUpper && hasLower && hasNumber) {
        returnSuccess(true, passwordField);
        return true;
    } else {
        returnSuccess(false, passwordField);
        return false;
    }

}

function checkConfirmPassword(){
    let pass1 = $('#password1').val().trim();
    let pass2 = $('#password2');

    if (pass2.val().trim() !== '' && pass1 === pass2.val().trim() && validatePassword()) {
        returnSuccess(true, pass2);
        return true;
    } else {
        returnSuccess(false, pass2);
        return false;
    }
}


function checkEmail(alreadyExists) {
    let emailField = $('#email');
    let errorField = $('#email-error-message');
    errorField.text('Your email is required.');

    if (emailField.val().includes('@') && emailField.val().includes('.') && emailField.val().length >= 5) {
        if (alreadyExists) {
            returnSuccess(false, emailField);
            errorField.text(emailField.val() + ' already exists.');
            return false;
        } else {
            returnSuccess(true, emailField);
            return true;
        }
    } else {
        returnSuccess(false, emailField);
        return false;
    }
}

function checkUsername(alreadyExists) {
    let usernameField = $('#username');
    let errorField = $('#username-error-message');
    errorField.text('Your username is required.');
    if (alreadyExists) {
        returnSuccess(false, usernameField);
        errorField.text(usernameField.val() + ' already exists.');
        return false;
    } else {
        returnSuccess(true, usernameField);
        return true;
    }
}

function isEmailValid() {
    let emailField = $('#email');
    let email = emailField.val().trim()
    let errorField = $('#email-error-message');
    errorField.text('Your email is invalid.');

    if (email.includes('@') && email.includes('.') && email.length >= 5) {
        returnSuccess(true, emailField);
        return true;
    } else {
        returnSuccess(false, emailField);
        return false;
    }
}

function validateEmail(e) {
  const email = document.querySelector('#email');
  const re = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/i;
  const reSpaces = /^\S*$/;

  if (reSpaces.test(email.value) && re.test(email.value)) {
    email.classList.remove('is-invalid');
    email.classList.add('is-valid');

    return true;
  } else {
    email.classList.add('is-invalid');
    email.classList.remove('is-valid');

    return false;
  }
}

function validateUsername(e) {
  const username = document.querySelector('#username');
  const errorField = $('#username-error-message');
    errorField.text('Username is required.');


  if (username.value !== '') {
    username.classList.remove('is-invalid');
    username.classList.add('is-valid');

    return true;
  } else {
    username.classList.add('is-invalid');
    username.classList.remove('is-valid');

    return false;
  }
}


function isPasswordValid() {
    let passwordField = $('#password1');
    let password = passwordField.val().trim()


    if (password.length >= 8) {
        returnSuccess(true, passwordField);
        return true;
    } else {
        returnSuccess(false, passwordField);
        return false;
    }
}


$('#password1').on('blur', function () {
    let pass1 = $(this).val().trim();
    validatePassword();
    checkConfirmPassword();

});

$('#password2').on('blur', function () {
    checkConfirmPassword();
});

/*
$('#email').on('blur', function () {
    let email = $(this).val().trim();
    checkEmail(email, this);
});

 */


function checkUsernameWithServer(usernameField){
    let username = $(usernameField).val().trim();
    if (username) {
        let ajax_url = document.getElementById('check-username').value;
        let token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: ajax_url,
            data: {
                'username': username,
                csrfmiddlewaretoken: token
            },
            dataType: 'json',
            success: function (data) {
                checkUsername(data.exists);
            },
            error: function (xhr, status, error) {
                console.error('AJAX error:', error);
            }
        });
    }
}

$('#username').on('blur', function () {
    checkUsernameWithServer(this);
    validateUsername();
});

function checkEmailWithServer(emailField){
    let email = $(emailField).val().trim();
    if (email) {
        let ajax_url = document.getElementById('check-email').value;
        let token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: ajax_url,
            data: {
                'email': email,
                csrfmiddlewaretoken: token
            },
            dataType: 'json',
            success: function (data) {
                checkEmail(data.exists);
            },
            error: function (xhr, status, error) {
                console.error('AJAX error:', error);
            }
        });
    }
}


$('#email').on('blur', function () {
    checkEmailWithServer(this)
});


// TODO implement form validation
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById("signup-form");

    form.addEventListener(
        "submit",
        (e) => {


            let email = $('#email');
            let username = $('#username');
            checkUsernameWithServer(username);
            checkEmailWithServer(email);

            if (!form.checkValidity() ||
          !validateEmail() ) {
                e.preventDefault();
                e.stopPropagation();
            }
            else{
                form.classList.add("was-validated");
            }




            console.log("submit");
        },
        false
    );
});
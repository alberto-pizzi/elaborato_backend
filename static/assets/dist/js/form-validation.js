function validateForm() {

    let pass1 = $('#password1');
    let email = $('#email');

    return checkPassword(pass1.val().trim(), pass1) && checkPassword(email.val().trim(), email);

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

function checkPassword(passwordInput, passwordField) {
    if (passwordInput !== '' && passwordInput.length >= 8) {
        returnSuccess(true, passwordField);
        return true;
    } else {
        returnSuccess(false, passwordField);
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

$('#password1').on('blur', function () {
    let pass1 = $(this).val().trim();
    checkPassword(pass1, this);

});

$('#password2').on('blur', function () {
    let pass1 = $('#password1').val().trim();
    let pass2 = $(this).val().trim();

    if (pass2 !== '' && pass1 === pass2) {
        returnSuccess(true, this);
    } else {
        returnSuccess(false, this);
    }
});

$('#email').on('blur', function () {
    let email = $(this).val().trim();
    checkEmail(email, this);
});

$('#username').on('blur', function () {
    let username = $(this).val().trim();
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
});

$('#email').on('blur', function () {
    let email = $(this).val().trim();
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
});
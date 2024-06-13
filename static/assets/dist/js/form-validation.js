function validateForm() {

    let fname = document.getElementById('fname').value;

    if (fname.length < 3) {
        alert('Il nome deve contenere almeno 3 caratteri.');
        return false;
    }

    return true;
}
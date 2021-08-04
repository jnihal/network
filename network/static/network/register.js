document.addEventListener('DOMContentLoaded', function() {

    const profile = document.getElementById('personal-info');
    const login = document.getElementById('login-info');

    const register = document.getElementById('register');
    const next = document.getElementById('next');
    const back = document.getElementById('back');

    profile.style.display = 'block';
    login.style.display = 'none';
    register.style.display = 'none';
    next.style.display = 'block';
    back.style.display = 'none';

    next.addEventListener('click', function() {

        

        if (validate()) {
            profile.style.display = 'none';
            login.style.display = 'block';
            register.style.display = 'block';
            next.style.display = 'none';
            back.style.display = 'block';
        } else {
            return;
        }
    })

    back.addEventListener('click', function() {
        profile.style.display = 'block';
        login.style.display = 'none';
        register.style.display = 'none';
        next.style.display = 'block';
        back.style.display = 'none';
    })

})

function validate() {

    const full_name = document.getElementById('name-field');
    names = full_name.getElementsByTagName('input');
    for (i = 0; i < names.length; i++) {
        if (names[i].value == "") {
            names[i].reportValidity();
            return false
        }
    }

    return true;
}

function loadImage(event) {
    var image = document.getElementById('image-output');
    image.src = URL.createObjectURL(event.target.files[0]);
};
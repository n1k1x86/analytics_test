/*
window.addEventListener("DOMContentLoaded", function () {
    let signInBtn = document.getElementById('sign_in_btn');

    signInBtn.addEventListener("click", function (){
        const username = document.getElementById('username_input').value;
        const password = document.getElementById('password_input').value;
        const cookie_value = getCookie('csrftoken');
        const url = document.location.href;
        const home_url = document.location.protocol + '//' + document.location.host;


        const data = {
            'username': username,
            'password': password
        }

        fetch(url, {
            method: "POST",
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': cookie_value
            },
            body: JSON.stringify(data)
        }).then(function (response){
            const status = response.status;
            return response.json();
        }).then(function (data){
            if (data.status === 200){
                _paq.push(['setUserId', data.username]);
                _paq.push(['trackPageView']);
                window.document.location.href = home_url;
            }
        }).catch(error => console.error('Error:', error));
    })
})
*/

let goToRegister = () => {
        const corner_url = document.location.protocol + '//' + document.location.host;
        window.location.href = corner_url + '/register/';
};

let getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
let goToPost = (target) => {
    const post_id = target.id
    window.open(`${post_id}/`);
}

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

let logOut = () => {
    const cookie_value = getCookie('csrftoken');
    const url = document.location.protocol + '//' + document.location.host + '/logout/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': cookie_value
        },
    }).then(function(response){
        _paq.push(['resetUserId']);
        _paq.push(['appendToTrackingUrl', 'new_visit=1']);
        _paq.push(['trackPageView']);
        _paq.push(['appendToTrackingUrl', '']);

        window.location.href = document.location.protocol + '//' + document.location.host + '/login/';
    }).catch(error => console.error('Error:', error));
}
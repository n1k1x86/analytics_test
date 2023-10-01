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
}

let createPost = (data) => {
    let reviewsContainer = document.getElementById('reviews_container');
    let newReview = document.createElement("div");
    newReview.id = 'review_' + data['review_id'];

    let review_text_p = document.createElement('p');
    review_text_p.textContent = data['review_text'];

    console.log(data);
    let review_author_p = document.createElement("p");
    review_author_p.textContent = 'by ' + data['review_author'];
    //<button id="review_delete_{{ review.id }}" onClick="deletePost(this)">delete post</button>


    let review_del_btn = document.createElement('button');
    review_del_btn.id = 'review_delete_' + data['review_id'];
    review_del_btn.setAttribute('onClick', 'deletePost(this)');
    review_del_btn.textContent = 'delete post';


    newReview.appendChild(review_text_p);
    newReview.appendChild(review_author_p);
    newReview.appendChild(review_del_btn);

    reviewsContainer.appendChild(newReview);
}


let sendPostReview = (target) => {
    let review_textarea = document.getElementById('review_textarea');
    const review_text = review_textarea.value;
    const url = document.location.href + 'leave_review/';
    const cookie_value = getCookie('csrftoken');

    const data= {
            review_text: review_text,
    }

    fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': cookie_value
        },
    }).then(function(response){
      console.log(response);
      return response.json();
    }).then(function(result){
        createPost(result);
    }).catch(error => console.error('Error:', error));

    review_textarea.value = '';
};

let deletePost = (target) => {
    let review_id_raw = target.id.split('_').slice(-1)[0]
    let review_id = 'review_' + review_id_raw
    let review = document.getElementById(review_id);

    const url = document.location.href + 'delete_review/';
    const cookie_value = getCookie('csrftoken');

    const data= {
            review_id: review_id_raw,
    }

    fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': cookie_value
        },
    }).then(function(response){
        review.remove();
        return response.json()})
   .then(function(data)
        {console.log(data)
   }).catch(error => console.error('Error:', error));
};

let changeLikeBtn = (target) => {
    let heart = target.textContent;

    if (heart === "\u2665") {
        target.textContent = "\u2661";
        target.setAttribute('onClick', 'likePost(this)')
    }else{
        target.textContent = "\u2665";
        target.setAttribute('onClick', 'cancelLikePost(this)')
    }
}

let changeLikeValue = (data) => {
    let likes = data['likes'];
    let likes_elem = document.getElementById("post_" + data['post_id'] + "_likes")
    likes_elem.textContent = likes;
}

let likePost = (target) => {
    const url = document.location.href + 'like_post/';
    const cookie_value = getCookie('csrftoken');

    let data = {
        cancel_like: false
    }


    fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': cookie_value
        },
    }).then(function(response){
        changeLikeBtn(target);
        return response.json();
    }).then(function(data){
        changeLikeValue(data);
    }).catch(error => console.error('Error:', error));
};

let cancelLikePost = (target) => {
    const url = document.location.href + 'like_post/';
    const cookie_value = getCookie('csrftoken');

    let data = {
        cancel_like: true
    }

    fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': cookie_value
        },
    }).then(function(response){
        changeLikeBtn(target);
        return response.json();
    }).then(function(data){
        changeLikeValue(data);
    }).catch(error => console.error('Error:', error));
};

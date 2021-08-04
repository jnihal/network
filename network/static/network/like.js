document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#like-button').forEach((like) => {
        const id = like.dataset.postId;
        const count = document.getElementById(`like-count-${id}`);
        const csrftoken = getCookie('csrftoken');

        like.addEventListener('click', () => {
            console.log('clicked')
            fetch(`/like/${id}`, {
                method: 'POST',
                headers: { "X-CSRFToken": csrftoken }
            })
            .then(response => response.json())
            .then(result => {
                if (result.liked) {
                    like.innerText = 'favorite';
                    like.className = 'material-icons-round btn btn-bg-transparent p-0 like-button';
                    count.innerText = `${result.like_count}`
                } else {
                    like.innerText = 'favorite_border';
                    like.className = 'material-icons-round btn btn-bg-transparent p-0 unlike-button';
                    count.innerText = `${result.like_count}`
                }
            });
        });
    })
});

function getCookie(name) {
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
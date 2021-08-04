document.addEventListener('DOMContentLoaded', () => {
    const follow = document.getElementById('follow');
    const id = follow.dataset.userId;
    const count = document.getElementById('follower_count');
    const csrftoken = getCookie('csrftoken');

    follow.addEventListener('click', () => {
        fetch(`/follow/${id}`, {
            method: 'POST',
            headers: { "X-CSRFToken": csrftoken }
        })
        .then(response => response.json())
        .then(result => {
            if (result.following) {
                follow.innerText = 'Unfollow';
                follow.className = 'btn btn-outline-danger rounded-pill';
                count.innerText = `${result.follower_count}`
            } else {
                follow.innerText = 'Follow';
                follow.className = 'btn btn-outline-primary rounded-pill';
                count.innerText = `${result.follower_count}`
            }
        });
    });
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
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('#edit-button').forEach((edit) => {
        const id = edit.dataset.postId;
        const save = document.getElementById(`save-button-${id}`);
        const content = document.getElementById(`content-${id}`);
        const textarea = document.getElementById(`textarea-${id}`);
        const csrftoken = getCookie('csrftoken');

        edit.addEventListener('click', () => {
            edit.hidden = true;
            save.hidden = false; 
            
            content.hidden = true;
            textarea.hidden = false;
        });

        save.addEventListener('click', () => {
            const value = textarea.value;

            fetch(`/edit/${id}`, {
                method: 'POST',
                headers: { "X-CSRFToken": csrftoken },
                body: JSON.stringify({
                  content: value
                })
            })
            .then(response => response.json())
            .then(result => {
                console.log(result.message)
            });

            content.innerText = value;

            edit.hidden = false;
            save.hidden = true;

            document.getElementById(`content-${id}`).hidden = false;
            document.getElementById(`textarea-${id}`).hidden = true;
        })
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
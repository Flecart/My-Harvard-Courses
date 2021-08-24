// i put this here so its available everywhere later
// https://docs.djangoproject.com/en/3.2/ref/csrf/
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


function showData(data) {
    console.log(data)
    if (data.hasOwnProperty("error")) {
        // TODO: display some kind of errors
    }


    // Appending the post for each post in response
    const cards = document.querySelector("#post");
    cards.innerHTML = "";
    data['posts'].forEach(post => {
        liked_block = post.is_liked ? 
        `
        <div id="like-${post.id}" data-liked="1">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-suit-heart-fill" viewBox="0 0 16 16">
                <path d="M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0 3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z"/>
            </svg>
            ${ post.likes }
        </div>
        ` : `
        <div id="like-${post.id}" data-liked="0">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="blue" class="bi bi-suit-heart-fill" viewBox="0 0 16 16">
                <path d="M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0 3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z"/>
            </svg>
            ${ post.likes }
        </div>
        `

        edit_block = post.can_edit ?
        `
        <button id="edit-${post.id}" class="btn btn-primary"> Edit Post </button>
        ` : ""

        cards.innerHTML += `
        <div class="mb-4">
            <div class="card col-6 m-auto p-0">
                <div class="card-header">
                    <a href="/profile/${post.user}"><strong> ${post.user}</strong></a>
                    ${ post.timestamp }
                    ` + liked_block + `
                </div>
                <div id="card-body" class="card-body">
                    <p id="body-${post.id}" class="card-text">${ post.body }</p>
                    ` + edit_block + `
                </div>
            </div>
        </div>
        `
    });
    
    // bug: dunno why, if i don't put this as separate like here doesnt get the event
    data['posts'].forEach(post => {

        // Adding like event listener
        const like_block = document.querySelector(`#like-${post.id}`)
        like_block.onclick = () => {
            is_liked = parseInt(like_block.dataset.liked, 10);
            like_block.innerHTML = is_liked ? 
            `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="blue" class="bi bi-suit-heart-fill" viewBox="0 0 16 16">
                <path d="M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0 3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z"/>
            </svg>
            ${ post.is_liked ? post.likes - 1 : post.likes }
            ` : `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="red" class="bi bi-suit-heart-fill" viewBox="0 0 16 16">
                <path d="M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0 3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z"/>
            </svg>
            ${ post.is_liked ? post.likes : post.likes + 1 }
            `;

            fetch("api/like", {
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                method: "PUT",
                body: JSON.stringify({
                    post_id: post.id
                })
            })
            .then(response => response.json())
            .then(result => console.log(result))

            // ternary but faster
            like_block.dataset.liked ^= 1;
        };

        // adding edit event listener
        if (post.can_edit) {
            const edit_block = document.querySelector(`#edit-${post.id}`)
            edit_block.onclick = () => {
                document.querySelector("#edit-zone").hidden = false;
                document.querySelector("#edit-textarea").value = post.body;
                console.log(`${post.id} edit button was clicked`)
                
                // dinamically assigning the edit_button confirm
                edit_button = document.querySelector("#edit-button");
                edit_button.onclick = () => {
                    let new_body = document.querySelector("#edit-textarea").value;
                    console.log(`${post.id} edit confirm button was clicked`)
                    // requesting to the server:
                    fetch("api/edit", {
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        method: "POST",
                        body: JSON.stringify({
                            body: new_body,
                            post_id: post.id
                        })
                    })
                    .then(response => response.json())
                    .then(message => console.log(message));
    
                    // updating the front-end
                    document.querySelector(`#body-${post.id}`).innerHTML = new_body;
                    document.querySelector("#edit-zone").hidden = true;
                }
            }

           
        }

    });

    // empty checker
    if (data['posts'].length == 0) {
        cards.innerHTML = `
        <div class="my-4">
            <div class="col-6 m-auto p-0">
                <p>
                    You aren't following anybody
                </p>
                <a href="/">
                    <button class="btn btn-primary">Return to home</button>
                </a>
            </div>
        </div>
        `
    }


    // Front-end pagination disabler
    const previous = document.querySelector("#previous");
    const next = document.querySelector("#next");

    if (!data['has_next']) {
        next.disabled = true;
    } else {
        next.disabled = false;
    }

    if (!data['has_previous']) {
        previous.disabled = true;
    } else {
        previous.disabled = false;
    }
}
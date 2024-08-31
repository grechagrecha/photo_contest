// джяваскирп

var dict = {
    'published': 'Your published posts',
    'on_validation': 'Your posts on validation',
    'on_deletion': 'Your posts on deletion'
}

function getPostStateParameter() {
    var params = {}
    prmstr = window.location.search.slice(1)
    prmarr = prmstr.split("&");
    for (var i = 0; i < prmarr.length; i++) {
        tmparr = prmarr[i].split('=');
        params[tmparr[0]] = tmparr[1];
    }

    return params['post_state'] || 'published'
}

function changeHeaderText(post_state) {
    your_posts_header = document.getElementById('your_posts')
    
    if (dict[post_state]) {
        your_posts_header.innerHTML = dict[post_state]
    }
}

document.addEventListener('DOMContentLoaded', function () {
    input = document.getElementById('post_state')
    post_state = getPostStateParameter()

    if (dict[post_state]) {
        input.value = post_state
    }
    else {
        input.value = published
    }
    changeHeaderText(post_state)

})

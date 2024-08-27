console.log('Hello World!');

var input = document.getElementById('post_state');
function loadSettings() {
    if (localStorage['post_state']) {
        input.value = localStorage['post_state'];
    }
}

function saveSettings() {
    localStorage['post_state'] = input.value;
}
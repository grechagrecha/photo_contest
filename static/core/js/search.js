let sendAjaxRequest = function (endpoint, request_parameters) {
    return $.ajax({
        url: endpoint, type: "GET", dataType: "json", data: request_parameters,

        success: function (response) {
            populatePage(response);
            let like_buttons = $("button[name*='like-button']");

            like_buttons.on("click", function () {
                endpoint = $(this).attr("data-like-url");
                request_parameters = {};

                sendLikeAjaxRequest(endpoint, request_parameters);
            });
        }, error: function (response) {
            console.log(response);
        },
    });
};

let sendLikeAjaxRequest = function (endpoint, request_parameters) {
    let csrf_token = window.CSRF_TOKEN;
    return $.ajax({
        url: endpoint, type: "POST", dataType: "json", data: request_parameters, statusCode: {
            200: function (response) {
                refreshLikeButtons(response);
            }, 401: function (response) {
                message = response.responseJSON.message;
                console.log(response);
                alert(message);
            },
        }, beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }, success: function (response) {
            console.log(response);
        }, error: function (response) {
            console.log(response);
        },
    });
};

let getCurrentPostsIds = function () {
    let post_ids = [];
    $("#post-section")
        .children()
        .each(function () {
            post_ids.push(this.id);
        });
    return post_ids.join(", ");
};

let refreshLikeButtons = function () {
    $.getJSON($("#post-section").attr("data-get-likes-url"), {
        post_ids: getCurrentPostsIds(),
    }, (response) => {
        let like_buttons = $("button[name*='like-button']")
        like_buttons.each((btn_idx, btn) => {
            if (response.includes(btn.id)) {
                $(btn).toggleClass('btn-primary', false)
                $(btn).toggleClass('btn-danger', true)
            } else {
                $(btn).toggleClass('btn-primary', true)
                $(btn).toggleClass('btn-danger', false)
            }
        })
    });
};

let parseAndFillTemplate = function (post, post_template) {
    let csrf_token = window.CSRF_TOKEN;

    for (const fieldname in post) {
        regexp = "{{ " + fieldname + " }}";
        post_template = post_template.replaceAll(regexp, post[fieldname]);
        post_template = post_template.replaceAll("{{ csrf_token }}", csrf_token[2]);
    }
    return post_template;
};

let populatePage = function (response) {
    const post_section = $("#post-section");

    let posts = response.data;
    let post_template = $.get({
        url: post_section.attr("data-url"), async: false,
    }).responseText;

    post_section.empty();

    posts.forEach((post) => {
        post_section
            .append(parseAndFillTemplate(post, post_template))
            .hide()
            .fadeIn(350);
    });
    refreshLikeButtons()
};

document.addEventListener("DOMContentLoaded", (event) => {
    const url_params = new URLSearchParams(window.location.search);
    const current_page = url_params.get("page");
    const search_input = $("#search-input");
    const sort_input = $("#ajax-sort");
    const search_endpoint = $("#ajax-search").attr("data-url");
    const delay_in_ms = 400;

    let scheduled_function = false;

    search_input.val(localStorage.getItem("search_input_val"));
    sort_input.val(localStorage.getItem("sort_input_val"));

    sendAjaxRequest(search_endpoint, {
        search_query: search_input.val(), sort_order: sort_input.val(), page: current_page, async: false
    });

    search_input.on("keyup", function (key) {
        localStorage.setItem("search_input_val", search_input.val());

        if ((search_input.val().length >= 3) || (search_input.val().length === 0)) {
            let request_parameters = {
                search_query: $(this).val().trim(), sort_order: sort_input.val(), page: current_page,
            };

            if (scheduled_function) {
                clearTimeout(scheduled_function);
            }

            scheduled_function = setTimeout(sendAjaxRequest, delay_in_ms, search_endpoint, request_parameters);
        }
    });

    sort_input.on("change", function () {
        localStorage.setItem("sort_input_val", sort_input.val());

        let request_parameters = {
            search_query: search_input.val().trim(), sort_order: $(this).val(), page: current_page,
        };

        if (scheduled_function) {
            clearTimeout(scheduled_function);
        }

        scheduled_function = setTimeout(sendAjaxRequest, delay_in_ms, search_endpoint, request_parameters);
    });
});

let sendAjaxRequest = function (endpoint, request_parameters) {
  return $.ajax({
    url: endpoint,
    type: "GET",
    dataType: "json",
    data: request_parameters,
    success: function (response) {
      populatePage(response);
    },
    error: "404",
  });
};

let parseAndFillTemplate = function (post, post_template) {
  for (const fieldname in post) {
    regexp = "{{ " + fieldname + " }}";
    post_template = post_template.replaceAll(regexp, post[fieldname]);
  }
  return post_template;
};

let populatePage = function (response) {
  const post_section = $("#post-section");

  let posts = response.data;
  let post_template = $.get({
    url: post_section.attr("data-url"),
    async: false,
  }).responseText;

  post_section.empty();

  posts.forEach((post) => {
    post_section
      .append(parseAndFillTemplate(post, post_template))
      .hide()
      .fadeIn(350);
  });
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
    search_query: search_input.val(),
    sort_order: sort_input.val(),
    page: current_page,
  });

  search_input.on("keyup", function (key) {
    localStorage.setItem("search_input_val", search_input.val());

    request_parameters = {
      search_query: $(this).val().trim(),
      sort_order: sort_input.val(),
      page: current_page,
    };

    if (scheduled_function) {
      clearTimeout(scheduled_function);
    }

    scheduled_function = setTimeout(
      sendAjaxRequest,
      delay_in_ms,
      search_endpoint,
      request_parameters
    );
  });

  sort_input.on("change", function () {
    localStorage.setItem("sort_input_val", sort_input.val());

    request_parameters = {
      search_query: search_input.val().trim(),
      sort_order: $(this).val(),
      page: current_page,
    };

    if (scheduled_function) {
      clearTimeout(scheduled_function);
    }

    scheduled_function = setTimeout(
      sendAjaxRequest,
      delay_in_ms,
      search_endpoint,
      request_parameters
    );
  });
});

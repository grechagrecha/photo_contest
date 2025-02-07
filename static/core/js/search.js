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
      .fadeIn(200);
  });
};

document.addEventListener("DOMContentLoaded", (event) => {
  const search_input = $("#search-input");
  const sort_input = $("#ajax-sort");
  const search_endpoint = $("#ajax-search").attr("data-url");
  const delay_in_ms = 700;

  let scheduled_function = false;

  // TODO: Make search and sort input values save and load from cookies on page reload

  search_input.val(localStorage.getItem("search_input_val"));
  sort_input.val(localStorage.getItem("sort_input_val"));

  sendAjaxRequest(search_endpoint, "");

  search_input.on("keyup", function (key) {
    localStorage.setItem("search_input_val", search_input.val());

    request_parameters = {
      search_query: $(this).val().trim(),
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

  sort_input.on("click", function () {
    localStorage.setItem("sort_input_val", sort_input.val());
  });
});

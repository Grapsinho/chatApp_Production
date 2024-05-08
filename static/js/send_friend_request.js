function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Check if this cookie string begins with the name provided
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
var csrftoken = getCookie("csrftoken");

$(document).on("click", ".add-friend-button", function () {
  const add_friend_id = document.querySelector(".add-friend-button");

  $.ajax({
    type: "POST",
    url: "/add_friend/friend_request/",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    data: {
      "user_id": add_friend_id.dataset.id,
    },
    success: function (response) {
      add_friend_id.textContent = "Request Sent";
      add_friend_id.style.fontSize = "13px";
      add_friend_id.style.pointerEvents = "none";
    },
    error: function (xhr, errmsg, err) {
      console.log(`Error!`);
      console.log(err);
    },
  });
});

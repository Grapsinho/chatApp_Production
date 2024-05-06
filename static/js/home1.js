// start: Sidebar
document
  .querySelector(".chat-sidebar-profile-toggle")
  .addEventListener("click", function (e) {
    e.preventDefault();
    this.parentElement.classList.toggle("active");
  });

document.addEventListener("click", function (e) {
  if (!e.target.matches(".chat-sidebar-profile, .chat-sidebar-profile *")) {
    document.querySelector(".chat-sidebar-profile").classList.remove("active");
  }
});
// end: Sidebar

// update user
let full_name = document.querySelector(".user_fullName");
let bio = document.querySelector(".user_bio");
let user_avatar = document.querySelector(".user_avatar");
let user_photo_curr = document.querySelector(".user-photo-curr");

function sanitizeInput(userInput) {
  // Remove all HTML tags from user input
  let sanitizedInput = userInput.replace(/(<([^>]+)>)/gi, "");
  return sanitizedInput;
}

let jwtToken = localStorage.getItem("access_token");

console.log(jwtToken);

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

$(".update_btn-profile").on("click", function () {
  const full_nameVal = full_name.value;
  const bioVal = bio.value;
  const vend_email = document.querySelector("#vend_email").value;

  if (!full_nameVal) {
    alert("Please fill full name field!");
    return false;
  }

  let formData = new FormData();

  try {
    formData.append("avatar", user_avatar.files[0]);
    formData.append("full_name", sanitizeInput(full_nameVal));
    formData.append("bio", sanitizeInput(bioVal));
  } catch {
    formData.append("full_name", sanitizeInput(full_nameVal));
    formData.append("bio", sanitizeInput(bioVal));
  }

  $.ajax({
    url: `${location.protocol}//${location.host}/auth/${sanitizeInput(
      vend_email
    )}/update_user/`,
    type: "PUT",
    headers: {
      "X-CSRFToken": csrftoken,
      "Authorization": `Bearer ${jwtToken}`,
    },
    contentType: false,
    processData: false,
    data: formData,
    success: function (data) {
      window.location.href = `/`;
    },
    error: function (xhr, status, error) {
      // Given token not valid for any token type

      try {
        if (
          xhr.responseJSON.detail == "Given token not valid for any token type"
        ) {
          window.location.href = `${location.protocol}//${location.host}/auth/logout/`;
        }
      } catch (error) {
        console.log(error);
      }

      // Handle error response from the backend
      // console.error("Error sending data:", error.erro12r);
      // // Optionally, you can display an error message to the user

      if (xhr.responseJSON.non_field_errors[0]) {
        alert(`Error: ${xhr.responseJSON.non_field_errors[0]}`);
      }
    },
  });
});
// update user end

// start: Coversation
document
  .querySelectorAll(".conversation-item-dropdown-toggle")
  .forEach(function (item) {
    item.addEventListener("click", function (e) {
      e.preventDefault();
      if (this.parentElement.classList.contains("active")) {
        this.parentElement.classList.remove("active");
      } else {
        document
          .querySelectorAll(".conversation-item-dropdown")
          .forEach(function (i) {
            i.classList.remove("active");
          });
        this.parentElement.classList.add("active");
      }
    });
  });

document.addEventListener("click", function (e) {
  if (
    !e.target.matches(
      ".conversation-item-dropdown, .conversation-item-dropdown *"
    )
  ) {
    document
      .querySelectorAll(".conversation-item-dropdown")
      .forEach(function (i) {
        i.classList.remove("active");
      });
  }
});

document.querySelectorAll(".conversation-form-input").forEach(function (item) {
  item.addEventListener("input", function () {
    this.rows = this.value.split("\n").length;
  });
});

document.querySelectorAll("[data-conversation]").forEach(function (item) {
  item.addEventListener("click", function (e) {
    e.preventDefault();
    document.querySelectorAll(".conversation").forEach(function (i) {
      i.classList.remove("active");
    });
    document.querySelector(this.dataset.conversation).classList.add("active");
  });
});

document.querySelectorAll(".conversation-back").forEach(function (item) {
  item.addEventListener("click", function (e) {
    e.preventDefault();
    this.closest(".conversation").classList.remove("active");
    document.querySelector(".conversation-default").classList.add("active");
  });
});
// end: Coversation

const add_friend_appr = document.querySelectorAll(".add_friend_appr");

add_friend_appr.forEach((element) => {
  element.addEventListener("click", () => {
    let friendId = element.dataset.id;

    element.style.pointerEvents = "None";

    $.ajax({
      type: "POST",
      url: "/add_friend/approve_friend_request/",
      headers: {
        "X-CSRFToken": csrftoken,
      },
      data: {
        "user_id": friendId,
      },
      success: function (response) {
        element.textContent = "Accepted";
        element.style.backgroundColor = "#cfd4cf";
        element.style.borderColor = "#cfd4cf";
        element.style.color = "black";
      },
      error: function (xhr, errmsg, err) {
        console.log(`Error!`);
        console.log(err);
      },
    });
  });
});

const decline_friend_request = document.querySelectorAll(
  ".decline_friend_request"
);

decline_friend_request.forEach((element) => {
  element.addEventListener("click", () => {
    let friendId = element.dataset.id;

    element.style.pointerEvents = "None";

    $.ajax({
      type: "POST",
      url: "/add_friend/decline_friend_request/",
      headers: {
        "X-CSRFToken": csrftoken,
      },
      data: {
        "user_id": friendId,
      },
      success: function (response) {
        element.textContent = "Declined";
        element.style.backgroundColor = "#cfd4cf";
        element.style.borderColor = "#cfd4cf";
        element.style.color = "black";
      },
      error: function (xhr, errmsg, err) {
        console.log(`Error!`);
        console.log(err);
      },
    });
  });
});

const delete_message_dec = document.querySelectorAll(".delete_message_dec");
let notification_count = document.querySelector(".notification_count");

delete_message_dec.forEach((element) => {
  element.addEventListener("click", () => {
    const messageId = element.dataset.id;

    $.ajax({
      type: "POST",
      url: "/add_friend/delete_friend_request/",
      headers: {
        "X-CSRFToken": csrftoken,
      },
      data: {
        "id": messageId,
      },
      success: function (response) {
        element.parentElement.remove();
        let count = parseInt(notification_count.textContent) - 1;
        notification_count.textContent = count;
      },
      error: function (xhr, errmsg, err) {
        console.log(`Error!`);
        console.log(err);
      },
    });
  });
});

function scrollToBottom() {
  const chatContainer = document.querySelector(".conversation-main");
  chatContainer.scrollTop =
    chatContainer.scrollHeight - chatContainer.clientHeight;
}

// eseigi darcha is ro wavshalo mesiji da morcha mere viwyeb saitis shemowmebas tavidan bolomde

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
          alert("You Should Login Again");

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

function deleteBtn_dropDown() {
  // this is for delete button dropdown
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

  // ends here
}

// es arivic ristvisaa mara inputebs exeba amitomac nvm
document.querySelectorAll(".conversation-form-input").forEach(function (item) {
  item.addEventListener("input", function () {
    this.rows = this.value.split("\n").length;
  });
});
// ends here

// mokled es aris is divi ra saxeli da bolo mesiji roa iuzeris egaa megobrbeis chamonatvali ra
document.querySelectorAll(".freind_chats").forEach(function (item) {
  item.addEventListener("click", function (e) {
    e.preventDefault();

    let chat_id = this.dataset.chat_id.slice(13);

    let conversation_div = document.querySelector(".for_chat");

    conversation_div.id = `conversation-${chat_id}`;

    $.ajax({
      url: `${location.protocol}//${location.host}/chat/get_chats_betweenUsers`,
      type: "GET",
      data: {
        "id": chat_id,
      },
      success: function (data) {
        const send_message_button = document.querySelector(
          ".send_message_button"
        );
        const user_img_html = document.querySelector(
          ".conversation-user-image"
        );
        const user_name_html = document.querySelector(
          ".conversation-user-name"
        );
        const link_to_user_profileChat = document.querySelector(
          ".link_to_user_profileChat"
        );
        const conversation_wrapper = $(".conversation-wrapper");
        conversation_wrapper.empty();

        send_message_button.setAttribute("data-chat_id", chat_id);
        user_img_html.src = `static${data.top_info.img_url}`;
        link_to_user_profileChat.href = `${location.protocol}//${location.host}/profile/${data.top_info.email}/`;
        user_name_html.textContent = data.top_info.user_full_name;

        const allMessages = data.chat_messages.friend.concat(
          data.chat_messages.my
        );
        allMessages.sort((a, b) => new Date(a[2]) - new Date(b[2]));

        allMessages.forEach((element) => {
          const isMyMessage = data.chat_messages.my.includes(element);
          const messageType = isMyMessage
            ? "me my_messages_chat"
            : "user_messages_chat";

          conversation_wrapper.append(`
                <li class="conversation-item ${messageType}" style="width: 60%;">
                    <div class="conversation-item-side">
                        <img class="conversation-item-image" src="static${
                          element[3]
                        }" alt="" />
                    </div>
                    <div class="conversation-item-content">
                        <div class="conversation-item-wrapper">
                            <div class="conversation-item-box">
                                <div class="conversation-item-text">
                                    <p data-messIdText="${element[4]}">${
            element[0]
          }</p>
                                    <div class="conversation-item-time" data-messIdTime="${
                                      element[4]
                                    }">${element[1]}</div>
                                </div>
                                ${
                                  isMyMessage
                                    ? `
                                <div class="conversation-item-dropdown">
                                    <button type="button" class="conversation-item-dropdown-toggle">
                                        <i class="ri-more-2-line"></i>
                                    </button>
                                    <ul class="conversation-item-dropdown-list">
                                        <li>
                                            <button type="button" class="delete_message_btn" data-messId="${element[4]}">
                                                <i class="ri-delete-bin-line"></i> Delete
                                            </button>
                                        </li>
                                    </ul>
                                </div>`
                                    : ""
                                }
                            </div>
                        </div>
                    </div>
                </li>
            `);
        });

        scrollToBottom();
        deleteBtn_dropDown();

        const delete_message_btn = document.querySelectorAll(
          ".delete_message_btn"
        );
        const socket2 = new WebSocket(
          `wss://${host}/wss/chat/delete_message/${chat_id}/`
        );

        function sendMessage2(messageId, chat_id) {
          const messageData = {
            type: "send",
            message_id: messageId,
            chat_pk: chat_id,
          };

          // Convert message data to JSON and send it via WebSocket
          socket2.send(JSON.stringify(messageData));
        }

        delete_message_btn.forEach((element) => {
          element.addEventListener("click", () => {
            let messageId = element.dataset.messid;
            sendMessage2(messageId, chat_id);
          });
        });

        socket2.onmessage = function (event) {
          let mes = JSON.parse(event.data);
          let message_text = document.querySelector(
            `[data-messidtext="${mes.message_id}"]`
          );
          let message_time = document.querySelector(
            `[data-messidtime="${mes.message_id}"]`
          );

          message_text.textContent = mes.new_text;
          message_time.textContent = mes.del_time;
        };

        $(".send_message_button").click(function () {
          var message = $(".message_content").val();
          let sender_id = document.querySelector("#sender_id").value;
          $(".message_content").val("");
          sendMessage(message, sender_id, chat_id);
        });

        const socket = new WebSocket(`wss://${host}/wss/chat/${chat_id}/`);

        socket.onmessage = function (event) {
          let mes = JSON.parse(event.data);

          let last_message_chat = document.querySelector(
            `[data-lastmessagechatid="${mes.chat_id}"]`
          );

          if (mes.sender_id == document.querySelector("#sender_id").value) {
            last_message_chat.textContent = mes.message;
            conversation_wrapper.append(`
                    <li class="conversation-item me my_messages_chat" style="width: 60%;">
                        <div class="conversation-item-side">
                            <img class="conversation-item-image" src="static${mes.sender_img}" alt="" />
                        </div>
                        <div class="conversation-item-content">
                            <div class="conversation-item-wrapper">
                                <div class="conversation-item-box">
                                    <div class="conversation-item-text">
                                        <p data-messIdText="${mes.message_id}">${mes.message}</p>
                                        <div class="conversation-item-time" data-messIdTime="${mes.message_id}">${mes.message_time}</div>
                                    </div>
                                    <div class="conversation-item-dropdown">
                                        <button type="button" class="conversation-item-dropdown-toggle">
                                            <i class="ri-more-2-line"></i>
                                        </button>
                                        <ul class="conversation-item-dropdown-list">
                                            <li>
                                                <button type="button" class="delete_message_btn" data-messId="${mes.message_id}">
                                                    <i class="ri-delete-bin-line"></i> Delete
                                                </button>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
            `);
          } else {
            conversation_wrapper.append(`
                    <li class="conversation-item user_messages_chat" style="width: 60%;">
                        <div class="conversation-item-side">
                            <img class="conversation-item-image" src="static${mes.sender_img}" alt="" />
                        </div>
                        <div class="conversation-item-content">
                            <div class="conversation-item-wrapper">
                                <div class="conversation-item-box">
                                    <div class="conversation-item-text">
                                        <p data-messIdText="${mes.message_id}">${mes.message}</p>
                                        <div class="conversation-item-time" data-messIdTime="${mes.message_id}">${mes.message_time}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </li>
                `);
          }

          scrollToBottom();
          deleteBtn_dropDown();

          const delete_message_btn2 = document.querySelectorAll(
            ".delete_message_btn"
          );

          delete_message_btn2.forEach((element) => {
            element.addEventListener("click", () => {
              let messageId = element.dataset.messid;
              sendMessage2(messageId, chat_id);
            });
          });
        };

        function sendMessage(messageContent, senderId, chatPk) {
          const messageData = {
            type: "send",
            message: messageContent,
            sender_id: senderId,
            chat_pk: chatPk,
          };
          socket.send(JSON.stringify(messageData));
        }
      },
      error: function (xhr, status, error) {
        // Given token not valid for any token type
        console.log(xhr);
        console.log(error);
      },
    });

    document.querySelectorAll(".conversation").forEach(function (i) {
      i.classList.remove("active");
    });
    // anu amit im divs vxsnit romelis aidc wamovida backidan
    document.querySelector(`#${this.dataset.chat_id}`).classList.add("active");
  });
});
// ends here

// this is for responsive its for go back button ekrani daapatareve da naxav ra
document.querySelectorAll(".conversation-back").forEach(function (item) {
  item.addEventListener("click", function (e) {
    e.preventDefault();
    this.closest(".conversation").classList.remove("active");
    document.querySelector(".conversation-default").classList.add("active");
  });
});
// end: Coversation

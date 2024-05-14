function sanitizeInput(userInput) {
  // Remove all HTML tags from user input
  let sanitizedInput = userInput.replace(/(<([^>]+)>)/gi, "");
  return sanitizedInput;
}

let host = window.location.host;
let socket = new WebSocket(`ws://${host}/ws/live_search/`);
let search_results = document.querySelector("#search_results");

search_results.style.display = "none";
const type_button = document.querySelector(".type-button");

type_button.style.pointerEvents = "none";

socket.onmessage = function (event) {
  let data = JSON.parse(event.data);
  let searchResults = data.search_results;
  let product_name = document.querySelector(".product_detail");
  spinner.style.display = "none";

  // Update your UI with the search results, e.g., by adding them to a div or list.
  let resultsContainer = document.getElementById("search-results");
  //resultsContainer.innerHTML = "";

  for (let i = 0; i < searchResults.length; i++) {
    let result = searchResults[i];

    if (searchResults.length < 3) {
      type_button.style.pointerEvents = "none";
    } else {
      type_button.style.pointerEvents = "all";
    }

    if (result.full_name) {
      product_name.innerHTML += `
        
            <a href="${location.protocol}//${location.host}/profile/${result.email}/" class="result_a_tag">
              <div class="d-flex align-items-center gap-2">
                <img
                  src="static/images/${result.avatar}"
                  style="border-radius: 50%; width: 50px; height: 50px"
                />
                <div style="display: flex; flex-direction: column; color: black;">
                  <span>${result.full_name}</span>
                </div>
              </div>
            </a>
        `;

      search_results.style.display = "block";
    } else {
      product_name.innerHTML = result.message;
    }

    searchInput.addEventListener("input", function () {
      product_name.innerHTML = "";
    });

    if (searchInput.value == "") {
      product_name.innerHTML = "";
      type_button.style.pointerEvents = "none";
      search_results.style.display = "none";
    }
  }
};
socket.onerror = function (error) {
  console.log(error);
};

let timeout;
let spinner = document.getElementById("spinner");

// Send search queries when the user types
let searchInput = document.querySelector(".search-input");
searchInput.addEventListener("input", function () {
  spinner.style.display = "block";
  clearTimeout(timeout);
  timeout = setTimeout(() => {
    let searchQuery = this.value;
    socket.send(sanitizeInput(searchQuery));
  }, 1000);
});

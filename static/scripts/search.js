import { getCookie } from "./general.js";

document.querySelector(".header-search-button").onclick = () => {
  document.querySelector(".search-container").style.display = "block";
};


document.querySelector(".search-cancel-button").onclick = () => {
  document.querySelector(".search-container").style.display = "none";
};

// js on keyup
const searchInput = document.querySelector("#search-input");
searchInput.addEventListener("keyup", (e) => {
  const searchValue = searchInput.value;
  if (searchValue) {
    const url = '/'
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ "searchValue": searchValue })
    })
      .then(response => response.json())
      .then(data => {
        let matchingProducts = "";
        data.forEach((product) => {
          matchingProducts += `<a class="matching-item" href="/products/${product.id}">${product.name}</a>`
        })
        matchingProducts
          ? (document.querySelector(".matching-items-container").innerHTML = matchingProducts)
          : (document.querySelector(".matching-items-container").innerHTML = '<p class="matching-item" style="color:red;background:none">Item Not Found</p>')
      })
  } else {
    document.querySelector(".matching-items-container").innerHTML = "";
  }
}
)

// js when search  button is clicked
const searchButton = document.querySelector(".search-button");
searchButton.addEventListener("click", () => {
  const searchValue = searchInput.value;
  if (searchValue) {
    const url = '/'
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ "searchValue": searchValue })
    })
      .then(response => response.json())
      .then(data => {
        let matchingProducts = "";
        data.forEach((product) => {
          matchingProducts += `
            <a href="/products/${product.id}" class="search-product">
              <div class="search-product-image">
                <img class="search-image" src="../media/${product.cover_image}" alt="${product.name}">
              </div>
              <div class="search-product-details">
                <p class="p-name">${product.name}</p>
                ${product.discounted_price
              ? `<p>Ksh ${product.discounted_price}</p> <strike>Ksh ${product.price}</strike>`
              : `<p>Ksh ${product.price}</p>`}
              </div>
            </a>`
        })
        matchingProducts
          ? (document.querySelector(".matching-items-container").innerHTML = matchingProducts)
          : (document.querySelector(".matching-items-container").innerHTML = '<p class="matching-item" style="color:red;background:none">Item Not Found</p>')
      })
  } else {
    document.querySelector(".matching-items-container").innerHTML = "";
  }
}
)


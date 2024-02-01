// function to retrieve csrf_token from cookies
export function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Check if the cookie name matches the CSRF token name
      if (cookie.substring(0, name.length + 1) === name + "=") {
        // Extract the CSRF token value
        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1)
        );
        break;
      }
    }
  }
  return cookieValue;

}

export function updateCart() {
  // update cart when 'add-to-cart' button is clicked
  document.querySelectorAll('.add-to-cart-button').forEach((button) => {
    button.onclick = () => {
      const productId = parseInt(button.dataset.productId);
      const url = "/cart/add-to-cart"
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ "productId": productId })
      })
        .then(response => response.json())
        .then(data => {
          document.querySelector(`.js-item-quantity-${productId}`).innerText = data.item_quantity;
          button.style.display = 'none'
          document.querySelector(`.js-update-cart-buttons-${productId}`).style.display = 'flex';
          document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'flex';
          setTimeout(() => {
            document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'none';
          }, 2000);
        })
    }
  })

  // update cart when 'increase' button is clicked
  document.querySelectorAll('.increase-cart-button').forEach((button) => {
    button.onclick = () => {
      const productId = parseInt(button.dataset.productId);
      const url = "/cart/increase-cart"
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ "productId": productId })
      })
        .then(response => response.json())
        .then(data => {
          document.querySelector(`.js-item-quantity-${productId}`).innerHTML = data.itemQuantity;
          document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'flex';
          setTimeout(() => {
            document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'none';
          }, 2000);
        })
    }
  })
  // update cart when 'decrease' button is clicked
  document.querySelectorAll('.decrease-cart-button').forEach((button) => {
    button.onclick = () => {
      const productId = parseInt(button.dataset.productId);
      const url = "/cart/decrease-cart"
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ "productId": productId })
      })
        .then(response => response.json())
        .then(data => {
          if (data.itemQuantity) {
            document.querySelector(`.js-item-quantity-${productId}`).innerHTML = data.itemQuantity;
            document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'flex';
            setTimeout(() => {
              document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'none';
            }, 2000);
          } else {
            document.querySelector(`.js-update-cart-buttons-${productId}`).style.display = 'none';
            document.querySelector(`.js-add-to-cart-button-${productId}`).style.display = 'block';
            document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'flex';
            setTimeout(() => {
              document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'none';
            }, 2000);
          }
        })
    }
  })
}

export function updateLike() {
  const outlineButtons = document.querySelectorAll('.heart-icon-outline');
  const fillButtons = document.querySelectorAll('.heart-icon-fill');

  outlineButtons.forEach((button) => {
    button.onclick = () => {
      const productId = parseInt(button.dataset.productId);
      const url = "/likes/updatelike"
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ "productId": productId, "action": "like" })
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'liked') {
            button.remove();
            document.querySelector(`.js-like-container-${productId}`).innerHTML = `
            <img
            class="heart-icon-fill js-heart-icon-fill-${productId}"
            src="/static/images/icons/heart-fill.png"      
            alt="fill-icon"
            data-product-id="${productId}"
            /> 
            `
            updateLike()
          }
        })
    }
  })


  fillButtons.forEach((button) => {
    button.onclick = () => {
      const productId = parseInt(button.dataset.productId);
      const url = "/likes/updatelike"
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ "productId": productId, "action": "unlike" })
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'unliked') {
            button.remove();
            document.querySelector(`.js-like-container-${productId}`).innerHTML = `
            <img
            class="heart-icon-outline js-heart-icon-outline-${productId}"
            src="/static/images/icons/heart-outline.png"      
            alt="outline-icon"
            data-product-id="${productId}"
            /> 
            `
            updateLike()
          }
        })
    }
  })

}

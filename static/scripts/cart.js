// Function to retrieve the CSRF token from cookies
function getCookie(name) {
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

// increase cart quantity when 'add button' is clicked
document.querySelectorAll('.increase-button').forEach((button) => {
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
        document.querySelector('.js-cart-total').textContent = `Ksh ${data.totalCartPrice}`;
        document.querySelector('.summary-items-count').textContent = data.totalCartQuantity;
        document.querySelector(`.js-count-${productId}`).textContent = data.itemQuantity;
        data.totalCartQuantity === 1
          ? document.querySelector('.header-items-count').textContent = '1 item'
          : document.querySelector('.header-items-count').textContent = `${data.totalCartQuantity} items`;
        document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'flex';
        setTimeout(() => {
          document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'none';
        }, 2000);
      })
  }
})

// decrease cart quantity when 'minus button' is clicked
document.querySelectorAll('.decrease-button').forEach((button) => {
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
        data.totalCartPrice && (document.querySelector('.js-cart-total').textContent = `Ksh ${data.totalCartPrice}`);
        data.totalCartQuantity && (document.querySelector('.summary-items-count').textContent = data.totalCartQuantity);
        if (data.itemQuantity === 0) {
          const cartContainer = document.querySelector(`.js-cart-item-container-${productId}`)
          cartContainer.style.animationPlayState = 'running';
          cartContainer.onanimationend = () => {
            cartContainer.remove()
          }
        } else {
          document.querySelector(`.js-count-${productId}`).innerText = data.itemQuantity;
          document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'flex';
          setTimeout(() => {
            document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'none';
          }, 2000);
        }
        if (data.totalCartQuantity === 0) {
          document.querySelector('.header-items-count').textContent = 'no item';
          document.querySelector('.main').innerHTML = `
          <div class="empty-cart">
            <img src="../static/images/icons/shopping-cart.png" /> Your Cart is Empty
          </div>
          <a href="/" class="start-shopping-button">Start Shopping</a>`
        } else if (data.totalCartQuantity === 1) {
          document.querySelector('.header-items-count').textContent = '1 item';
        } else {
          document.querySelector('.header-items-count').textContent = `${data.totalCartQuantity} items`;
        }
      })
  }
})

// delete cart-item when 'delete button' is clicked
document.querySelectorAll('.delete-button').forEach((button) => {
  button.onclick = () => {
    const cartId = parseInt(button.dataset.cartId);
    const url = "/cart/delete-cart"
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ "cartId": cartId })
    })
      .then(response => response.json())
      .then(data => {
        const cartContainer = document.querySelector(`.js-cart-item-container-${cartId}`)
        cartContainer.style.animationPlayState = 'running';
        cartContainer.onanimationend = () => {
          cartContainer.remove()
        }
        data.totalCartPrice && (document.querySelector('.js-cart-total').textContent = `Ksh ${data.totalCartPrice}`);
        data.totalCartQuantity && (document.querySelector('.summary-items-count').textContent = data.totalCartQuantity);
        if (data.totalCartQuantity === 0) {
          document.querySelector('.header-items-count').textContent = 'no item';
          document.querySelector('.main').innerHTML = `
    <div class="empty-cart">
      <img src="../static/images/icons/shopping-cart.png" /> Your Cart is Empty
    </div>
    <a href="/" class="start-shopping-button">Start Shopping</a>`
        } else if (data.totalCartQuantity === 1) {
          document.querySelector('.header-items-count').textContent = '1 item';
        } else {
          document.querySelector('.header-items-count').textContent = `${data.totalCartQuantity} items`;
        }
      })
  }
})

//empty the cart when 'empty cart button' is clicked
const emptyCartButton = document.querySelector('.empty-cart-button')
if (emptyCartButton) {//this if statement ensures that the code can only run if the 'empty cart button' exits to avoid getting an error
  emptyCartButton.onclick = () => {
    const url = "/cart/empty-cart"
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ "#": "#" })
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'deleted') {
          document.querySelector('.header-items-count').textContent = 'no item';
          document.querySelectorAll('.cart-item-container').forEach((cartItem) => {
            cartItem.remove()
          })
          document.querySelector('.main').innerHTML = `
        <div class="empty-cart">
          <img src="../static/images/icons/shopping-cart.png" /> Your Cart is Empty
        </div>
        <a href="/" class="start-shopping-button">Start Shopping</a>
      `
        }
      })

  }
}

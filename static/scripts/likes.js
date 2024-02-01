import { updateCart, getCookie } from "./general.js";

// add product to cart
updateCart()

// remove the liked product from the page when heart fill button is clicked
const likeButtons = document.querySelectorAll('.heart-icon-fill');

likeButtons.forEach((button) => {
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
          const product = document.querySelector(`.js-product-${productId}`);
          product.style.animationPlayState = 'running';
          product.onanimationend = () => {
            product.remove()
            !document.querySelector('.product') && (document.querySelector('.products-container').innerHTML = '<p class="empty-message">No Liked Products</p>')
          }
        }
      })
  }
})

// remove the liked brand from the page when heart fill button is clicked
const likes = document.querySelectorAll('.fill');

likes.forEach((button) => {
  button.onclick = () => {
    const brandId = parseInt(button.dataset.brandId);
    const url = "/likes/liked_brands"
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ "brandId": brandId, "action": "unlike" })
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'unliked') {
          const brand = document.querySelector(`.js-brand-${brandId}`);
          brand.style.animationPlayState = 'running';
          brand.onanimationend = () => {
            brand.remove()
            !document.querySelector('.brand-container') && (document.querySelector('.brands-grid').innerHTML = '<p class="empty-message">No Liked Brands</p>')
          }
        }
      })
  }
})
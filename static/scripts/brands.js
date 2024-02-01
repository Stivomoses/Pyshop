import { getCookie } from "./general.js";

function brandLike() {
  const outlineButtons = document.querySelectorAll('.outline');
  const fillButtons = document.querySelectorAll('.fill');

  outlineButtons.forEach((button) => {
    button.onclick = () => {
      const brandId = parseInt(button.dataset.brandId);
      const url = "/likes/liked_brands"
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ "brandId": brandId, "action": "like" })
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'liked') {
            button.remove();
            document.querySelector(`.js-like-container-${brandId}`).innerHTML = `
            <img class="fill js-fill-${brandId}" data-brand-id="${brandId}" src="/static/images/icons/heart-fill.png">
            `;
            brandLike()
          }
        })
    }
  })


  fillButtons.forEach((button) => {
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
            button.remove()
            document.querySelector(`.js-like-container-${brandId}`).innerHTML = `
            <img class="outline js-outline-${brandId}" data-brand-id="${brandId}" src="/static/images/icons/heart-outline.png">
            `;
            brandLike()
          }
        })
    }
  })

}

brandLike()

// check liked brands on reload
const likes = JSON.parse(document.querySelector('#likes').textContent);

likes.forEach((like) => {
  const productId = like.brand_id;
  const fill = document.querySelector(`.js-fill-${productId}`);
  const outline = document.querySelector(`.js-outline-${productId}`);
  fill && (fill.style.display = 'block');
  outline && (outline.style.display = 'none');
})
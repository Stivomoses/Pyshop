import { updateCart, updateLike, getCookie } from "./general.js"

updateCart();
updateLike();

const sizes = document.querySelectorAll('.size')

sizes.forEach((size) => {
  size.onclick = () => {
    if (document.querySelector('.size-active')) {
      document.querySelector('.size-active').classList.remove('size-active')
      size.classList.add('size-active')
    } else {
      size.classList.add('size-active')
    }
  }
})

const colors = document.querySelectorAll('.color')

colors.forEach((color) => {
  color.onclick = () => {
    const borderColor = color.dataset.color;
    if (document.querySelector('.color-container .active')) {
      document.querySelector('.color-container .active').style.borderColor = '#eee';
      document.querySelector('.color-container .active').classList.remove('active')
      color.classList.add('active')
      color.style.borderColor = borderColor;
    } else {
      color.classList.add('active')
    }
  }
})


const bigImage = document.querySelector('.big-img')

const smallImages = document.querySelectorAll('.small-img')
smallImages && smallImages[0].parentElement.classList.add('small-img-active')

smallImages.forEach((image) => {
  image.onclick = () => {
    active(image)
    bigImage.src = image.src
  }
})

function active(image) {
  const active = document.querySelector('.small-img-active');
  active && active.classList.remove('small-img-active')
  image.parentElement.classList.add('small-img-active');
}


// add to cart functionality specifically for the details page
const cartButton = document.querySelector('.details-add-to-cart-button');
const productId = parseInt(cartButton.dataset.productId);
const orderButton = document.querySelector('.order-btn');
const cartVariations = document.querySelector('.cart-variations');
const okButton = document.querySelector('.ok');
const cancelButton = document.querySelector('.cancel');


cancelButton.onclick = () => {
  cartVariations.style.display = 'none';
}

orderButton.onclick = () => {
  cartVariations.style.display = 'flex';
}


cartButton.onclick = () => {
  cartVariations.style.display = 'flex';
}

okButton.onclick = () => {
  const images = document.querySelectorAll('.variation-small-img');
  const sizes = document.querySelectorAll('.variation-size');
  let activeImageId;
  let activeSizeId;

  // checking the active images 
  images.forEach((image) => {
    if (image.parentElement.classList.contains('small-img-active')) {
      activeImageId = parseInt(image.dataset.imageId);
    }
  })
  if (!activeImageId) {
    images.forEach((image) => {
      image.parentElement.classList.add('error');
      image.parentElement.onanimationend = (e) => {
        e.target.classList.remove('error');
      }
    })
  }

  // checking the active sizes
  sizes.forEach((size) => {
    if (size.classList.contains('size-active')) {
      activeSizeId = parseInt(size.dataset.sizeId);
    }
  })
  if (sizes && !activeSizeId) {
    sizes.forEach((size) => {
      size.classList.add('error');
      size.onanimationend = (e) => {
        e.target.classList.remove('error');
      }
    })
  }

  if (activeImageId && ((sizes && activeSizeId) || (!activeSizeId))) {
    const url = "/cart/add-to-cart"
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ "productId": productId, "imageId": activeImageId, "sizeId": (activeSizeId && activeSizeId) })
    })
      .then(response => response.json())
      .then(data => {
        cartButton.style.display = 'none';
        cartVariations.style.display = 'none';
        document.querySelector(`.js-item-quantity-${productId}`).innerText = data.item_quantity;
        document.querySelector(`.js-update-cart-buttons-${productId}`).style.display = 'flex';
        document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'flex';
        setTimeout(() => {
          document.querySelector(`.js-cart-success-message-${productId}`).style.display = 'none';
        }, 2000);
      })
  }

}

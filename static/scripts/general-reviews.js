
const stars = document.querySelectorAll('.star');

stars.forEach((star) => {
  star.onclick = () => {
    const value = star.dataset.value;
    const allStars = document.querySelectorAll('.img-stars');
    const isActive = document.querySelector('.active-star');
    if (isActive) {
      isActive.classList.remove('active-star')
    }
    star.classList.add('active-star');
    allStars.forEach((star) => {
      star.classList.contains(`js-star-${value}`)
        ? (star.style.display = 'block')
        : (star.style.display = 'none')
    })
  }
})


const submit = document.querySelector('.submit');

submit && (submit.addEventListener('click', (e) => {
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

  const stars = document.querySelectorAll('.star');
  let activeStar = 0;
  stars.forEach((star) => {
    if (star.classList.contains('active-star')) {
      activeStar = parseInt(star.dataset.value);
    }
  })

  const comment = document.querySelector('#comment').value;

  const url = "/reviews/"

  if (activeStar && comment) {
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ "star": activeStar, "comment": comment })
    })
      .then(response => response.json())
      .then(data => {
        if (data === "Added") {
          document.querySelector('.success').style.display = 'flex';
          setTimeout(() => {
            e.target.parentElement.remove();
            window.location.reload(true);
          }, 2000)
        }
      })
  } else {
    if (!activeStar) {
      stars.forEach((star) => {
        star.classList.add('error');
        star.onanimationend = () => {
          star.classList.remove('error')
        }
      })
    }
    if (!comment) {
      const commentContainer = document.querySelector('#comment');
      commentContainer.classList.add('error');
      commentContainer.onanimationend = () => {
        commentContainer.classList.remove('error')
      }
    }
  }
})
)

const reviewMessage = document.querySelector('.review-message');

reviewMessage && (reviewMessage.onclick = () => {
  document.querySelectorAll('.link-primary').forEach((link) => {
    link.classList.add('error')
    link.onanimationend = () => {
      link.classList.remove('error')
    }
  })
}
)
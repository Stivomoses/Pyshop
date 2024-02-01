// header js
const hamburgerMenu = document.querySelectorAll(".hamburger-menu");
const menuContainer = document.querySelector(".menu-container");

hamburgerMenu.forEach((hamburger) => {
  hamburger.onclick = () => {
    menuContainer.classList.remove("menu-hide");
    menuContainer.classList.add("menu-show");
  };
})

document.querySelector(".menu-cancel").onclick = () => {
  menuContainer.classList.remove("menu-show");
  menuContainer.classList.add("menu-hide");
}


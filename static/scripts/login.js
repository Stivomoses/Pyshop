function showPassword() {
  const password = document.querySelector('.password');
  const checkbox = document.getElementById('checkbox');

  checkbox.addEventListener('click', () => {
    if (password.type === 'password') {
      password.setAttribute('type', 'text')
    } else {
      password.setAttribute('type', 'password')
    }
  })
}

showPassword()
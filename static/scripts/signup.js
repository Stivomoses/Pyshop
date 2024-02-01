function showPassword() {
  const passwords = document.querySelectorAll('.password');
  const checkbox = document.getElementById('checkbox');

  checkbox.addEventListener('click', () => {
    passwords.forEach((password) => {
      if (password.type === 'password') {
        password.setAttribute('type', 'text')
      } else {
        password.setAttribute('type', 'password')
      }
    })
  })
}

showPassword()
console.log('Hi');

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('contact-form');
  const alertContainer = document.getElementById('alert-container');

  if (form && alertContainer) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();

      const nombre = document.getElementById('nombre').value.trim();
      const correo = document.getElementById('correo').value.trim();
      const asunto = document.getElementById('asunto').value.trim();
      const mensaje = document.getElementById('mensaje').value.trim();

      if (nombre && correo && asunto && mensaje) {
        alertContainer.classList.remove('d-none');
        form.reset();
        setTimeout(function () {
          alertContainer.classList.add('d-none');
        }, 5000);
      } else {
        alert('Por favor, llena todos los campos.');
      }
    });
  }

  const cards = document.querySelectorAll('.card');
  cards.forEach((card) => {
    card.classList.add('card-hover-effect');
  });
});

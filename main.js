// script.js
document.addEventListener('DOMContentLoaded', () => {
  console.log('JavaScript loaded and running!');

  // Example: Simple click handler
  const button = document.querySelector('#my-button');
  if (button) {
    button.addEventListener('click', () => {
      alert('Button clicked!');
    });
  }
});

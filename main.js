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

// Example: Requesting an AI Quiz from your Python backend
async function fetchAIPracticeQuiz() {
  const response = await fetch('https://your-backend-url.onrender.com/api/generate-quiz', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ subject: 'Algebra II', topic: 'Factoring Polynomials' })
  });

  const data = await response.json();
  if (data.success) {
    document.querySelector('#quiz-container').innerHTML = data.quiz;
  }
}

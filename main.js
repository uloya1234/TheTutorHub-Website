// script.js

// 1. Define your base URL (NO trailing # or trailing slash)
const API_BASE_URL = 'https://thetutorhub-website-yrai.onrender.com';

document.addEventListener('DOMContentLoaded', () => {
  console.log('JavaScript loaded and running!');

  // Simple click handler example
  const button = document.querySelector('#my-button');
  if (button) {
    button.addEventListener('click', () => {
      alert('Button clicked!');
    });
  }
});

/**
 * Fetch an AI Practice Quiz from your Render Python backend
 */
async function fetchAIPracticeQuiz() {
  const quizContainer = document.querySelector('#quiz-container');
  
  if (quizContainer) {
    quizContainer.innerText = 'Generating quiz... (Render may take ~50s on cold start)';
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/generate-quiz`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        subject: 'Algebra II', 
        topic: 'Factoring Polynomials' 
      })
    });

    const data = await response.json();

    if (data.success && quizContainer) {
      quizContainer.innerHTML = data.quiz;
    } else if (quizContainer) {
      quizContainer.innerText = 'Failed to load quiz. Please try again.';
    }
  } catch (error) {
    console.error('Error fetching quiz:', error);
    if (quizContainer) {
      quizContainer.innerText = 'Error connecting to server.';
    }
  }
}

/**
 * Generic API POST helper function
 */
async function sendDataToBackend(endpoint, payload) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    return await response.json();
  } catch (error) {
    console.error('API Request failed:', error);
    return { success: false, error: 'Network error' };
  }
}

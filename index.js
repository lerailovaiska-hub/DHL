console.log('Login Page is working');

import { initializeApp } from "https://www.gstatic.com/firebasejs/12.14.0/firebase-app.js";
import { getAuth, singInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/12.14.0/firebase-auth.js";

  // Your web app's Firebase configuration
  const firebaseConfig = {
    apiKey: "AIzaSyBZHPUNPIZoQTUtB8H7Mabxl4qhRu72b7w",
    authDomain: "dhllogin-26b01.firebaseapp.com",
    projectId: "dhllogin-26b01",
    storageBucket: "dhllogin-26b01.firebasestorage.app",
    messagingSenderId: "623429925197",
    appId: "1:623429925197:web:ab7c702c72d6342fcf1f04"
  };

  // Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const loginForm      = document.querySelector('form');
const emailInput     = document.getElementById('email');
const passwordInput  = document.getElementById('password');
const emailError     = document.getElementById('email-error');
const passwordError  = document.getElementById('password-error');
const loginButton    = document.querySelector('button[type="submit"]');

// email validation
function validateEmail(email) {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailPattern.test(email);
}

emailInput.addEventListener('blur', () => {
  const email = emailInput.value.trim();
  if (email === '') return;
  if (!validateEmail(email)) {
    showError(emailError, 'Please enter a valid email address.');
  } else {
    clearError(emailError);
  }
});

// Clear password error when the user starts retyping
passwordInput.addEventListener('input', () => {
  clearError(passwordError);
});

// form submission handler
loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const email    = emailInput.value.trim();
  const password = passwordInput.value;
  let valid = true;

  // Client-side validation
  if (!validateEmail(email)) {
    showError(emailError, 'Please enter a valid email address.');
    valid = false;
  } else {
    clearError(emailError);
  }

  if (password === '') {
    showError(passwordError, 'Please enter your password.');
    valid = false;
  } else {
    clearError(passwordError);
  }

  if (!valid) return;

  // Loading state
  loginButton.textContent = 'Logging in…';
  loginButton.disabled    = true;

  try {
    await signInWithEmailAndPassword(auth, email, password);
    // ✅ Login successful — redirect to your app's main page
    window.location.href = 'afterlogin.html';
  } catch (error) {
    handleFirebaseError(error);
    loginButton.textContent = 'Login';
    loginButton.disabled    = false;
  }
});

//error handling
function handleFirebaseError(error) {
  switch (error.code) {
    case 'auth/user-not-found':
    case 'auth/invalid-credential':
    case 'auth/wrong-password':
      // Intentionally vague — don't reveal which field is wrong
      showError(emailError, 'Incorrect email or password. Please try again.');
      break;
    case 'auth/invalid-email':
      showError(emailError, 'Please enter a valid email address.');
      break;
    case 'auth/too-many-requests':
      showError(passwordError, 'Too many failed attempts. Please try again later or reset your password.');
      break;
    case 'auth/user-disabled':
      showError(emailError, 'This account has been disabled. Please contact support.');
      break;
    case 'auth/network-request-failed':
      showError(passwordError, 'Network error. Check your connection and try again.');
      break;
    default:
      showError(passwordError, 'Something went wrong. Please try again.');
      console.error('Firebase Auth error:', error.code, error.message);
  }
}

//helper functions
function showError(el, message) {
  el.textContent     = message;
  el.style.display   = 'block';
}

function clearError(el) {
  el.textContent     = '';
  el.style.display   = 'none';
}

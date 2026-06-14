//firebase
<script type="module">
  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/12.14.0/firebase-app.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

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
</script>

console.log('javascript is working');
// DOM Elements
const signupForm = document.getElementById('signup-form');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmInput = document.getElementById('confirm-password');
const signupButton = document.getElementById('signup-button');
const emailError = document.getElementById('email-error');
const passwordStrength = document.getElementById('password-strength');
const passwordError = document.getElementById('password-error');
const confirmError = document.getElementById('confirm-password-error');

// Email Validation
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

emailInput.addEventListener('blur', () => {
    const email = emailInput.value;
    if (email === '') return;
    if (!validateEmail(email)) {
        emailError.textContent = 'Please enter a valid email address.';
    } else {
        clearError(emailError);
    }
});

// Password Strength Validation
passwordInput.addEventListener('input', () => {
    const password = passwordInput.value;
    if (password.length === 0) {
    passwordStrength.textContent = '';
    passwordStrength.style.display = 'none';
    return;
    }
    passwordStrength.style.display = 'block';

    const strength = getPasswordStrength(password);

    switch (strength) {
        case 0:
        case 1:
            passwordStrength.textContent = 'Weak';
            passwordStrength.style.color = 'red';
            break;
        case 2:
        case 3:
            passwordStrength.textContent = 'Medium';
            passwordStrength.style.color = 'orange';
            break;
        case 4:
        case 5:
            passwordStrength.textContent = 'Strong';
            passwordStrength.style.color = 'green';
            break;
    }   
    if (strength < 4 && password.length > 0) {
        showError(passwordError, 'Password must be at least 8 characters and include uppercase, lowercase, number, and special character.');
    } else {
        clearError(passwordError);
    }
});

//password confirmation check
confirmInput.addEventListener('input', () => {
  if (confirmInput.value && confirmInput.value !== passwordInput.value) {
    showError(confirmError, 'Passwords do not match.');
  } else {
    clearError(confirmError);
  }
});

//form submission
signupForm.addEventListener('submit', (e) => {
  e.preventDefault();

  let valid = true;

  // Email check
  if (!validateEmail(emailInput.value.trim())) {
    showError(emailError, 'Please enter a valid email address.');
    valid = false;
  } else {
    clearError(emailError);
  }

const strength = getPasswordStrength(passwordInput.value);

  if (strength < 4) {
    showError(passwordError, 'Password must be at least 8 characters and include uppercase, lowercase, number, and special character.');
    valid = false;
  }

  // Passwords match check
  if (passwordInput.value !== confirmInput.value) {
    showError(confirmError, 'Passwords do not match.');
    valid = false;
  }

  if (!valid) return;

  // ── Success: simulate account creation ──
  signupButton.textContent = 'Creating account…';
  signupButton.disabled    = true;

  setTimeout(() => {
    // Replace this block with your real backend / Firebase / Supabase call
    alert('Account created! Redirecting to login…');
    window.location.href = 'index.html';
  }, 1500);
});

// helper functions
function getPasswordStrength(password) {
    let strength = 0;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[@$!%*?&]/.test(password)) strength++;
    if (password.length >= 8) strength++;
  return strength;
}

function showError(el, message) {
  el.textContent = message;
  el.style.display = 'block';
}

function clearError(el) {
  el.textContent = '';
  el.style.display = 'none';
}

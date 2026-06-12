console.log('javascript is working');
// DOM Elements
const signupForm = document.getElementById('signup-form');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmInput = document.getElementById('confirm-password');
const signupButton = document.getElementById('signup-button')
const emailError = document.getElementById('email-error');
const passwordStrength = document.getElementById('passwordStrength');
const passwordError = document.getElementById('password-error');

// Email Validation
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

emailInput.addEventListener('blur', () => {
    const email = emailInput.value;
    if (!validateEmail(email)) {
        emailError.textContent = 'Please enter a valid email address.';
    } else {
        emailError.textContent = '';
    }
});

// Password Strength Validation
passwordInput.addEventListener('input', () => {
    const password = passwordInput.value;
//empty password case
    if (password.length === 0) {
    passwordStrength.textContent = '';
    return;
    }

    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[@$!%*?&]/.test(password)) strength++;

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
});

// ─── Confirm password ────────────────────────────────────────────────────────
confirmInput.addEventListener('input', () => {
  if (confirmInput.value && confirmInput.value !== passwordInput.value) {
    showError(passwordError, 'Passwords do not match.');
  } else {
    clearError(passwordError);
  }
});

// ─── Form submission ─────────────────────────────────────────────────────────
document.querySelector('form').addEventListener('submit', (e) => {
  e.preventDefault();

  let valid = true;

  // Email check
  if (!validateEmail(emailInput.value.trim())) {
    showError(emailError, 'Please enter a valid email address.');
    valid = false;
  }

  // Password length check
  if (passwordInput.value.length < 8) {
    showError(passwordError, 'Password must be at least 8 characters.');
    valid = false;
  }

  // Passwords match check
  if (passwordInput.value !== confirmInput.value) {
    showError(passwordError, 'Passwords do not match.');
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

// ─── Helpers ─────────────────────────────────────────────────────────────────
function showError(el, message) {
  el.textContent = message;
  el.style.display = 'block';
}

function clearError(el) {
  el.textContent = '';
  el.style.display = 'none';
}
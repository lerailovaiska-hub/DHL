console.log('javascript is working');
// DOM Elements
const signupForm = document.getElementById('signup-form');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirm-password');
const SignupButton = document.getElementById('signup-button')

const emailError = document.getElementById('email-error');
const passwordStrength = document.getElementById('passwordStrength');
const confirmPasswordError = document.getElementById('confirm-password-error');
const passwordMatchError = document.getElementById('password-match-error');

//email validation
emailInput.addEventListener('input', () => {
    const email = emailInput.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        emailError.textContent = 'Please enter a valid email address.';
    } else {
        emailError.textContent = '';
    }

//password strength & validation
function checkPasswordStrength(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    if (password.length < minLength) {
        return 'Password must be at least 8 characters long.';
    }
    if (!hasUpperCase) {
        return 'Password must contain at least one uppercase letter.';
    }
    if (!hasLowerCase) {
        return 'Password must contain at least one lowercase letter.';
    }
    if (!hasNumber) {
        return 'Password must contain at least one number.';
    }
    if (!hasSpecialChar) {
        return 'Password must contain at least one special character.';
    }
    return null;
}

function validatePassword() {
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;
    
    // Check password strength
    const strengthMessage = checkPasswordStrength(password);
    if (strengthMessage) {
        passwordStrength.textContent = strengthMessage;
        return false;
    } else {
        passwordStrength.textContent = '';
    }
    
    // Check if passwords match
    if (password !== confirmPassword) {
        passwordMatchError.textContent = 'Passwords do not match.';
        return false;
    } else {
        passwordMatchError.textContent = '';
    }
    
    return true;
}

passwordInput.addEventListener('input', validatePassword);
confirmPasswordInput.addEventListener('input', validatePassword);

// Form submission
signupForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const isEmailValid = !emailError.textContent;
    const isPasswordValid = validatePassword();
    
    if (isEmailValid && isPasswordValid) {
        alert('Sign up successful!');
        // Here you can add code to submit the form data to the server
    } else {
        alert('Please fix the errors during sign up before submitting.');
    }
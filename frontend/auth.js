// Authentication related JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    const authOverlay = document.getElementById('authOverlay');
    const loginPopup = document.getElementById('loginPopup');
    const signupPopup = document.getElementById('signupPopup');
    const closeButtons = document.querySelectorAll('.close-auth');

    // Function to show login popup
    window.showLogin = function() {
        authOverlay.classList.add('active');
        loginPopup.style.display = 'block';
        signupPopup.style.display = 'none';
    };

    // Function to show signup popup
    window.showSignup = function() {
        authOverlay.classList.add('active');
        signupPopup.style.display = 'block';
        loginPopup.style.display = 'none';
    };
    
    // Show Login Popup
    loginBtn.addEventListener('click', showLogin);

    // Show Signup Popup
    signupBtn.addEventListener('click', showSignup);

    // Close Popups
    closeButtons.forEach(button => {
        button.addEventListener('click', closeAuthPopups);
    });

    // Close on overlay click
    authOverlay.addEventListener('click', function(e) {
        if (e.target === authOverlay) {
            closeAuthPopups();
        }
    });

    function closeAuthPopups() {
        authOverlay.classList.remove('active');
        setTimeout(() => {
            loginPopup.style.display = 'none';
            signupPopup.style.display = 'none';
        }, 300);
    }

    // Form Validation
    const forms = document.querySelectorAll('.auth-form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const button = form.querySelector('.auth-btn');
            button.classList.add('loading');
            
            // Simulate API call
            setTimeout(() => {
                button.classList.remove('loading');
                // Add your actual form submission logic here
            }, 2000);
        });
    });

    // Password Strength
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', function() {
            const strength = checkPasswordStrength(this.value);
            const strengthBar = this.parentElement.querySelector('.strength-bar');
            if (strengthBar) {
                strengthBar.className = 'strength-bar ' + strength;
            }
        });
    });

    function checkPasswordStrength(password) {
        if (password.length < 8) return 'weak';
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /\d/.test(password);
        const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        
        const strength = hasUpperCase + hasLowerCase + hasNumbers + hasSpecial;
        if (strength < 2) return 'weak';
        if (strength < 4) return 'medium';
        return 'strong';
    }

    // Escape key to close popups
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeAuthPopups();
        }
    });
});

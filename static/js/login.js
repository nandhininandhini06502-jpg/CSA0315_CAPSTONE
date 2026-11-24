// ==========================================================
// Login & Registration Validation Script
// ==========================================================

document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.querySelector('.auth-form');
    if (!loginForm) return;

    loginForm.addEventListener('submit', function (e) {
        const usernameInput = loginForm.querySelector('input[name="username"]');
        const passwordInput = loginForm.querySelector('input[name="password"]');

        let isValid = true;

        if (usernameInput && !usernameInput.value.trim()) {
            usernameInput.style.borderColor = '#ef4444';
            isValid = false;
        } else if (usernameInput) {
            usernameInput.style.borderColor = '';
        }

        if (passwordInput && !passwordInput.value.trim()) {
            passwordInput.style.borderColor = '#ef4444';
            isValid = false;
        } else if (passwordInput) {
            passwordInput.style.borderColor = '';
        }

        if (!isValid) {
            e.preventDefault();
        }
    });

    // Password visibility toggle
    document.querySelectorAll('.toggle-password').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            const input = document.getElementById(targetId) || this.previousElementSibling;
            if (input && input.type === 'password') {
                input.type = 'text';
                this.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
            } else if (input) {
                input.type = 'password';
                this.innerHTML = '<i class="fa-solid fa-eye"></i>';
            }
        });
    });
});

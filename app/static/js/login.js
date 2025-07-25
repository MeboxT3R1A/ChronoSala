document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const showPasswordBtn = document.querySelector('.show-password');
    const loginForm = document.querySelector('.login-form');

    // Toggle password visibility
    showPasswordBtn.addEventListener('click', function() {
        const icon = this.querySelector('i');
        const isVisible = passwordInput.type === 'text';
        
        passwordInput.type = isVisible ? 'password' : 'text';
        icon.classList.toggle('fa-eye');
        icon.classList.toggle('fa-eye-slash');
        
        // Feedback visual
        this.style.backgroundColor = isVisible ? 'transparent' : 'var(--cinza-200)';
    });

    // Form validation
    loginForm.addEventListener('submit', function(e) {
        let isValid = true;
        const username = document.getElementById('username');
        const password = passwordInput;

        // Reset styles
        username.style.borderColor = '';
        password.style.borderColor = '';

        // Validate username
        if (!username.value.trim()) {
            username.style.borderColor = 'var(--cor-erro)';
            isValid = false;
        }

        // Validate password
        if (!password.value.trim()) {
            password.style.borderColor = 'var(--cor-erro)';
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
            // Add error message if not exists
            if (!document.querySelector('.message.error')) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'message error';
                errorDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i><span>Preencha todos os campos</span>';
                document.querySelector('.login-messages').prepend(errorDiv);
            }
        }
    });

    // Clear validation on focus
    document.getElementById('username').addEventListener('focus', function() {
        this.style.borderColor = '';
        const errorMessage = document.querySelector('.message.error');
        if (errorMessage) errorMessage.remove();
    });

    passwordInput.addEventListener('focus', function() {
        this.style.borderColor = '';
        const errorMessage = document.querySelector('.message.error');
        if (errorMessage) errorMessage.remove();
    });
});
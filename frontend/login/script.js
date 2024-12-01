document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const togglePassword = document.querySelector('.toggle-password');
    const passwordInput = document.getElementById('password');

    // Toggle password visibility
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // Change eye icon based on password visibility
        const eyeIcon = this.querySelector('img');
        eyeIcon.src = type === 'password' ? './assets/eye-icon.svg' : './assets/eye-off-icon.svg';
    });

    // Handle form submission
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const baseUrl = 'http://127.0.0.1:5000';
        
        const username = document.getElementById('username').value;
        const password = passwordInput.value;

        try {
            const response = await fetch(`${baseUrl}/api/v1/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            const data = await response.json();

            if (data.token) {
                localStorage.setItem('token', data.token);
                window.location.href = `${baseUrl}/dashboard`;
            } else {
                alert('Tài khoản hoặc mật khẩu không chính xác');
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('Đã có lỗi xảy ra, vui lòng thử lại sau');
        }
    });
}); 
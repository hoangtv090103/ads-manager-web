const AUTH_TOKEN_KEY = 'token';

const auth = {
    // Lưu token sau khi login
    setToken(token) {
        if (token) {
            localStorage.setItem(AUTH_TOKEN_KEY, token);
            return true;
        }
        return false;
    },

    // Lấy token 
    getToken() {
        return localStorage.getItem(AUTH_TOKEN_KEY);
    },

    // Xóa token khi logout
    removeToken() {
        localStorage.removeItem(AUTH_TOKEN_KEY);
    },

    // Kiểm tra đã login chưa
    isAuthenticated() {
        return !!this.getToken();
    },

    // Thêm token vào header của request
    getAuthHeader() {
        return {
            'Authorization': `Bearer ${this.getToken()}`
        };
    }
};

// Redirect về login nếu chưa đăng nhập
function requireAuth() {
    if (!auth.isAuthenticated()) {
        window.location.href = '/frontend/login.html';
    }
}

// Thêm token vào tất cả request API
async function fetchWithAuth(url, options = {}) {
    const headers = {
        ...options.headers,
        ...auth.getAuthHeader()
    };

    try {
        const response = await fetch(url, { ...options, headers });
        
        // Nếu token hết hạn hoặc không hợp lệ
        if (response.status === 401) {
            auth.removeToken();
            window.location.href = '/frontend/login.html';
            return;
        }
        
        return response;
        
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
} 
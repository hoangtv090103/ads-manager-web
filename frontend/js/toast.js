class Toast {
    static container = null;
    static defaultDuration = 3000; // 3 seconds

    static init() {
        // Create container if not exists
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    }

    static show(options) {
        this.init();

        const {
            type = 'info', // success, error, warning, info
            title = '',
            message = '',
            duration = this.defaultDuration
        } = options;

        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        // Get icon based on type
        const icon = this.getIcon(type);

        toast.innerHTML = `
            <div class="toast-icon">
                <i class="${icon}"></i>
            </div>
            <div class="toast-content">
                ${title ? `<div class="toast-title">${title}</div>` : ''}
                <div class="toast-message">${message}</div>
            </div>
            <div class="toast-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </div>
        `;

        // Add toast to container
        this.container.appendChild(toast);

        // Remove toast after duration
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-in-out forwards';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }

    static getIcon(type) {
        switch (type) {
            case 'success':
                return 'fas fa-check-circle';
            case 'error':
                return 'fas fa-times-circle';
            case 'warning':
                return 'fas fa-exclamation-circle';
            case 'info':
            default:
                return 'fas fa-info-circle';
        }
    }

    // Convenience methods
    static success(message, title = '') {
        this.show({ type: 'success', title, message });
    }

    static error(message, title = '') {
        this.show({ type: 'error', title, message });
    }

    static warning(message, title = '') {
        this.show({ type: 'warning', title, message });
    }

    static info(message, title = '') {
        this.show({ type: 'info', title, message });
    }
} 
// Sidebar toggle function
function toggleSubmenu(element) {
    const navGroup = element.closest('.nav-group');
    const wasActive = navGroup.classList.contains('active');

    // Close all other open submenus
    document.querySelectorAll('.nav-group.active').forEach(group => {
        if (group !== navGroup) {
            group.classList.remove('active');
        }
    });

    // Toggle current submenu
    navGroup.classList.toggle('active', !wasActive);
}

// Add active state to current page menu item
document.addEventListener('DOMContentLoaded', function () {
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('.nav-item, .submenu a');

    menuItems.forEach(item => {
        const link = item.getAttribute('href');
        if (link && currentPath.includes(link)) {
            item.classList.add('active');

            // If item is in submenu, open parent menu
            const parentGroup = item.closest('.nav-group');
            if (parentGroup) {
                parentGroup.classList.add('active');
            }
        }
    });

    const user = JSON.parse(localStorage.getItem('user'));
    if (document.getElementById('user-name')) {
        document.getElementById('user-name').textContent = user.ho_va_ten;
    }
    if (document.getElementById('user-email')) {
        document.getElementById('user-email').textContent = user.email;
    }
});

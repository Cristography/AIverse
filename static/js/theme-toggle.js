/**
 * Theme Toggle - Switch between light and dark mode
 */

(function() {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;
    
    // Get saved theme from localStorage or default to 'light'
    let currentTheme = localStorage.getItem('theme') || 'light';
    
    // Apply theme on page load
    function applyTheme(theme) {
        htmlElement.setAttribute('data-theme', theme);
        
        // Update button icon
        if (themeToggleBtn) {
            const icon = themeToggleBtn.querySelector('i');
            if (theme === 'dark') {
                icon.className = 'fas fa-sun';
                themeToggleBtn.title = 'Switch to Light Mode';
            } else {
                icon.className = 'fas fa-moon';
                themeToggleBtn.title = 'Switch to Dark Mode';
            }
        }
        
        // Update navbar and other elements
        updateThemeClasses(theme);
    }
    
    // Update Bootstrap classes for theme
    function updateThemeClasses(theme) {
        const navbar = document.querySelector('.navbar');
        
        if (theme === 'dark') {
            if (navbar) {
                navbar.classList.remove('navbar-light', 'bg-light');
                navbar.classList.add('navbar-dark', 'bg-dark');
            }
            document.body.classList.add('bg-dark', 'text-light');
        } else {
            if (navbar) {
                navbar.classList.remove('navbar-dark', 'bg-dark');
                navbar.classList.add('navbar-light', 'bg-light');
            }
            document.body.classList.remove('bg-dark', 'text-light');
        }
    }
    
    // Toggle theme
    function toggleTheme() {
        currentTheme = currentTheme === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', currentTheme);
        applyTheme(currentTheme);
    }
    
    // Apply theme on load
    applyTheme(currentTheme);
    
    // Add click event listener
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', toggleTheme);
    }
})();
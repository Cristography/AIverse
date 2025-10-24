/**
 * Language Toggle - Switch between English and Arabic
 */

(function() {
    const languageToggleBtn = document.getElementById('language-toggle');
    const htmlElement = document.documentElement;
    
    // Get saved language from localStorage or default to 'en'
    let currentLanguage = localStorage.getItem('language') || 'en';
    
    // Apply language on page load
    function applyLanguage(language) {
        htmlElement.setAttribute('lang', language);
        
        // Update button text
        if (languageToggleBtn) {
            if (language === 'ar') {
                languageToggleBtn.innerHTML = '<i class="fas fa-language"></i> AR';
                htmlElement.setAttribute('dir', 'rtl'); // Right-to-left for Arabic
            } else {
                languageToggleBtn.innerHTML = '<i class="fas fa-language"></i> EN';
                htmlElement.setAttribute('dir', 'ltr'); // Left-to-right for English
            }
        }
    }
    
    // Toggle language
    function toggleLanguage() {
        currentLanguage = currentLanguage === 'en' ? 'ar' : 'en';
        localStorage.setItem('language', currentLanguage);
        applyLanguage(currentLanguage);
        
        // Note: In a real implementation, you would reload the page or
        // fetch translated content from the server
        // For now, this just changes the direction
    }
    
    // Apply language on load
    applyLanguage(currentLanguage);
    
    // Add click event listener
    if (languageToggleBtn) {
        languageToggleBtn.addEventListener('click', toggleLanguage);
    }
})();
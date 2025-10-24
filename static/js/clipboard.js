/**
 * Clipboard - Copy prompt text to clipboard
 */

(function () {
    // Show toast notification
    function showToast(message, type = 'success') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} position-fixed top-0 start-50 translate-middle-x mt-3`;
        toast.style.zIndex = '9999';
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            ${message}
        `;

        document.body.appendChild(toast);

        // Remove after 3 seconds
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    // Copy text to clipboard
    window.copyToClipboard = function (text) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text)
                .then(() => {
                    showToast('Prompt copied to clipboard!', 'success');
                })
                .catch(err => {
                    console.error('Failed to copy:', err);
                    showToast('Failed to copy prompt', 'danger');
                });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            document.body.appendChild(textArea);
            textArea.select();

            try {
                document.execCommand('copy');
                showToast('Prompt copied to clipboard!', 'success');
            } catch (err) {
                console.error('Failed to copy:', err);
                showToast('Failed to copy prompt', 'danger');
            }

            document.body.removeChild(textArea);
        }
    };
})();
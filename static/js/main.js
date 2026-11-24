// ==========================================================
// DIGITAL EVIDENCE MANAGEMENT SYSTEM - Global JavaScript
// ==========================================================

document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto-dismiss flash alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert-box');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(function () {
                if (alert.parentElement) alert.parentElement.removeChild(alert);
            }, 500);
        }, 6000);
    });

    // 2. Alert close button
    document.querySelectorAll('.close-alert').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const parent = this.closest('.alert-box');
            if (parent) {
                parent.style.opacity = '0';
                setTimeout(() => parent.remove(), 300);
            }
        });
    });

    // 3. Global Copy-to-Clipboard for SHA-256 Hashes
    window.copyHash = function (text, btnElement) {
        if (!navigator.clipboard) {
            // Fallback
            const el = document.createElement('textarea');
            el.value = text;
            document.body.appendChild(el);
            el.select();
            document.execCommand('copy');
            document.body.removeChild(el);
            showCopyFeedback(btnElement);
            return;
        }

        navigator.clipboard.writeText(text).then(function () {
            showCopyFeedback(btnElement);
        });
    };

    function showCopyFeedback(btn) {
        if (!btn) return;
        const origHtml = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-check" style="color:#10b981;"></i>';
        setTimeout(function () {
            btn.innerHTML = origHtml;
        }, 1800);
    }
});

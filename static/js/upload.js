// ==========================================================
// Evidence Upload & Drag-and-Drop Handler
// ==========================================================

document.addEventListener('DOMContentLoaded', function () {
    const dropzone = document.getElementById('uploadDropzone');
    const fileInput = document.getElementById('evidenceFileInput');
    const previewCard = document.getElementById('filePreviewCard');
    const previewName = document.getElementById('previewFileName');
    const previewSize = document.getElementById('previewFileSize');
    const previewIcon = document.getElementById('previewIcon');

    if (!dropzone || !fileInput) return;

    // Dropzone click opens file dialog
    dropzone.addEventListener('click', function (e) {
        if (e.target !== fileInput) {
            fileInput.click();
        }
    });

    // Drag-and-drop effects
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, function (e) {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, function (e) {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove('dragover');
        }, false);
    });

    dropzone.addEventListener('drop', function (e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelection(files[0]);
        }
    });

    fileInput.addEventListener('change', function () {
        if (this.files && this.files[0]) {
            handleFileSelection(this.files[0]);
        }
    });

    function handleFileSelection(file) {
        if (!previewCard) return;
        previewCard.classList.add('active');
        if (previewName) previewName.textContent = file.name;
        if (previewSize) previewSize.textContent = formatBytes(file.size);

        // Update preview icon based on extension
        const ext = file.name.split('.').pop().toLowerCase();
        if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext)) {
            previewIcon.className = 'fa-solid fa-image';
        } else if (['mp4', 'mov', 'avi', 'mkv'].includes(ext)) {
            previewIcon.className = 'fa-solid fa-video';
        } else if (['mp3', 'wav', 'ogg'].includes(ext)) {
            previewIcon.className = 'fa-solid fa-microphone-lines';
        } else if (ext === 'pdf') {
            previewIcon.className = 'fa-solid fa-file-pdf';
        } else {
            previewIcon.className = 'fa-solid fa-file-shield';
        }
    }

    function formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }
});

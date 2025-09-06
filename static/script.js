// Main functionality for image processing
document.addEventListener('DOMContentLoaded', function() {
    // Get the file input and image preview elements
    const fileInput = document.querySelector('input[type="file"]');
    const imagePreview = document.getElementById('imagePreview');
    const uploadArea = document.querySelector('.upload-area');

    // Function to remove background
    window.removeBackground = async function() {
        if (!imagePreview.src) return;
        
        const formData = new FormData();
        const blob = await fetch(imagePreview.src).then(r => r.blob());
        formData.append('image', blob);

        try {
            const response = await fetch('/remove-bg', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                imagePreview.src = URL.createObjectURL(blob);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    // Function to enhance image
    window.toggleEnhancement = async function() {
        if (!imagePreview.src) return;
        
        const formData = new FormData();
        const blob = await fetch(imagePreview.src).then(r => r.blob());
        formData.append('image', blob);

        try {
            const response = await fetch('/remove-and-upscale', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                imagePreview.src = URL.createObjectURL(blob);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    // Function to handle file upload
    function handleFileUpload(file) {
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                uploadArea.classList.add('has-image');
            };
            reader.readAsDataURL(file);
        }
    }

    // File input change handler
    fileInput.addEventListener('change', function(e) {
        handleFileUpload(e.target.files[0]);
    });

    // Drag and drop handlers
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function() {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFileUpload(e.dataTransfer.files[0]);
    });
});

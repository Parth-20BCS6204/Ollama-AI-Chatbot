document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const queryForm = document.getElementById('query-form');
    
    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(uploadForm);
        
        fetch('/upload/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log('Upload successful:', data);
            // Handle the response if needed
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
    
    queryForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(queryForm);
        
        fetch('/fetch-similar-documents/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log('Query successful:', data);
            // Handle the response if needed
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

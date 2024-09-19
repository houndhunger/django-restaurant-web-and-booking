// Wait until the DOM content is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function () {
    // Get references to the email input field, feedback message element, and the form
    const emailField = document.getElementById('id_email');
    const emailFeedback = document.getElementById('email-feedback');
    const form = document.getElementById('signup_form');

    // Add an event listener for when the email field loses focus (blur event)
    emailField.addEventListener('blur', function () {
        // Get the value of the email input field
        const email = emailField.value;
        // Proceed only if the email field is not empty
        if (email) {
            // Send an AJAX POST request to check if the email is unique
            fetch('/check-email/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    // Include the CSRF token in the request headers for security
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                // Send the email as form data
                body: new URLSearchParams({ 'email': email })
            })
            .then(response => response.json())  // Parse the JSON response from the server
            .then(data => {
                // Update the feedback message based on the server response
                if (data.is_unique) {
                    emailFeedback.textContent = 'The email address is available.';
                    emailFeedback.className = 'alert alert-success'; // Display success message
                } else {
                    emailFeedback.textContent = 'The email address is already in use.';
                    emailFeedback.className = 'alert alert-danger'; // Display error message
                }
            })
            .catch(error => {
                // Log any errors that occur during the fetch request
                console.error('Error:', error);
            });
        }
    });

    // Add an event listener for when the form is submitted
    form.addEventListener('submit', function (event) {
        // Prevent form submission if the feedback message indicates an error
        if (emailFeedback.classList.contains('alert-danger')) {
            event.preventDefault(); // Stop the form from being submitted
        }
    });
});

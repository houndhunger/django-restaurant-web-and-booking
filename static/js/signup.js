document.addEventListener('DOMContentLoaded', function () {
    const emailField = document.getElementById('id_email');
    const emailFeedback = document.getElementById('email-feedback');
    const form = document.getElementById('signup_form');

    emailField.addEventListener('blur', function () {
        const email = emailField.value;
        if (email) {
            fetch('/check-email/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: new URLSearchParams({ 'email': email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_unique) {
                    emailFeedback.textContent = 'The email address is available.';
                    emailFeedback.className = 'alert alert-success'; // Show success message
                } else {
                    emailFeedback.textContent = 'The email address is already in use.';
                    emailFeedback.className = 'alert alert-danger'; // Show error message
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });

    form.addEventListener('submit', function (event) {
        if (emailFeedback.classList.contains('alert-danger')) {
            event.preventDefault(); // Prevent form submission if email is not unique
        }
    });
});

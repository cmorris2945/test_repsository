// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('patientForm');
    const progressBar = document.getElementById('form-progress');
    const formFields = form.querySelectorAll('input, select, textarea');
    const totalFields = formFields.length;

    function updateProgress() {
        let filledFields = 0;
        formFields.forEach(field => {
            if (field.type === 'radio') {
                if (field.checked) {
                    filledFields++;
                }
            } else if (field.value.trim() !== '') {
                filledFields++;
            }
        });
        const progress = (filledFields / totalFields) * 100;
        progressBar.style.width = `${progress}%`;
    }

    formFields.forEach(field => {
        field.addEventListener('input', updateProgress);
        field.addEventListener('change', updateProgress);
    });

    updateProgress(); // Initial progress update

    form.addEventListener('submit', function(event) {
        let isValid = true;

        // Validate required fields
        const requiredFields = ['name', 'age', 'stage', 'location', 'family_history', 'genetic_testing'];
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (!validateInput(field, `Please fill out the ${field.name.replace('_', ' ')} field.`)) {
                isValid = false;
            }
        });

        // Validate age
        const age = document.getElementById('age');
        if (!validateAge(age, 'Please enter a valid age between 0 and 120.')) {
            isValid = false;
        }

        // Validate social support radio buttons
        const socialSupport = document.querySelector('input[name="social_support"]:checked');
        if (!socialSupport) {
            alert('Please select whether you need social support.');
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });

    // Function to validate input fields
    function validateInput(input, errorMessage) {
        if (input.value.trim() === '') {
            alert(errorMessage);
            input.focus();
            return false;
        }
        return true;
    }

    // Function to validate age input
    function validateAge(input, errorMessage) {
        const age = parseInt(input.value);
        if (isNaN(age) || age < 0 || age > 120) {
            alert(errorMessage);
            input.focus();
            return false;
        }
        return true;
    }

    // Add smooth scrolling for better UX when validation fails
    function smoothScroll(target) {
        const element = document.querySelector(target);
        window.scrollTo({
            top: element.offsetTop - 20,
            behavior: 'smooth'
        });
    }

    // Enhance form interactivity
    formFields.forEach(field => {
        field.addEventListener('focus', function() {
            this.parentElement.classList.add('active');
        });

        field.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.parentElement.classList.remove('active');
            }
        });
    });

    // Optional: Add a confirmation before form submission
    form.addEventListener('submit', function(event) {
        if (!confirm('Are you sure you want to submit the form?')) {
            event.preventDefault();
        }
    });
});
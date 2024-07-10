// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('patientForm');

    form.addEventListener('submit', function(event) {
        let isValid = true;

        // Validate required fields
        const requiredFields = ['name', 'age', 'stage', 'location', 'family_history', 'genetic_testing', 'treatment_preference'];
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
            return false;
        }
        return true;
    }

    // Function to validate age input
    function validateAge(input, errorMessage) {
        const age = parseInt(input.value);
        if (isNaN(age) || age < 0 || age > 120) {
            alert(errorMessage);
            return false;
        }
        return true;
    }
});
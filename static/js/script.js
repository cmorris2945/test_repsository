// static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('patientForm');

    form.addEventListener('submit', function(event) {
        let isValid = true;

        // Validate name
        const name = document.getElementById('name');
        if (name.value.trim() === '') {
            isValid = false;
            alert('Please enter your name.');
        }

        // Validate age
        const age = document.getElementById('age');
        if (age.value === '' || isNaN(age.value) || age.value < 0 || age.value > 120) {
            isValid = false;
            alert('Please enter a valid age between 0 and 120.');
        }

        // Validate stage
        const stage = document.getElementById('stage');
        if (stage.value === '') {
            isValid = false;
            alert('Please select a cancer stage.');
        }

        // Validate location
        const location = document.getElementById('location');
        if (location.value.trim() === '') {
            isValid = false;
            alert('Please enter your location.');
        }

        // Validate family history
        const familyHistory = document.getElementById('family_history');
        if (familyHistory.value === '') {
            isValid = false;
            alert('Please select your family history of breast cancer.');
        }

        // Validate genetic testing
        const geneticTesting = document.getElementById('genetic_testing');
        if (geneticTesting.value === '') {
            isValid = false;
            alert('Please indicate if you have had genetic testing.');
        }

        // Validate treatment preference
        const treatmentPreference = document.getElementById('treatment_preference');
        if (treatmentPreference.value === '') {
            isValid = false;
            alert('Please select your preferred treatment approach.');
        }

        if (!isValid) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });
});
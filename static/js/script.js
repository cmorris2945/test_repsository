document.addEventListener('DOMContentLoaded', function() {
    const consentForm = document.getElementById('consentForm');
    const patientForm = document.getElementById('patientForm');
    const agreeConsentBtn = document.getElementById('agreeConsent');
    const consentName = document.getElementById('consentName');
    const consentDate = document.getElementById('consentDate');
    const patientName = document.getElementById('name'); // Assuming this is the ID of the name field in the main form

    // Set current date automatically
    const currentDate = new Date().toISOString().split('T')[0];
    consentDate.value = currentDate;

    // Consent form handling
    agreeConsentBtn.addEventListener('click', function(event) {
        event.preventDefault();
        if (consentName.value.trim() === '') {
            alert('Please fill in your name to give consent.');
            return;
        }
        consentForm.style.display = 'none';
        patientForm.style.display = 'block';
        
        // Carry over the name to the main form
        patientName.value = consentName.value;
        
        updateProgress(); // Make sure this function is defined
    });

    // Handle the questionnaire progression
    document.getElementById('help_today').addEventListener('change', function() {
        document.getElementById('help_options').style.display = 'block';
    });

    document.getElementById('help_option').addEventListener('change', function() {
        document.getElementById('second_opinion').style.display = 'block';
    });

    document.querySelectorAll('input[name="second_opinion"]').forEach(function(radio) {
        radio.addEventListener('change', function() {
            document.getElementById('started_treatment').style.display = 'block';
        });
    });

    document.querySelectorAll('input[name="started_treatment"]').forEach(function(radio) {
        radio.addEventListener('change', function() {
            document.getElementById('additional_info').style.display = 'block';
        });
    });

    document.getElementById('gender').addEventListener('change', function() {
        document.getElementById('ehr_sync').style.display = 'block';
    });

    document.querySelectorAll('input[name="confirm_info"]').forEach(function(radio) {
        radio.addEventListener('change', function() {
            document.getElementById('final_questions').style.display = 'block';
        });
    });

    // Form validation before submission
    patientForm.addEventListener('submit', function(event) {
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
    const formFields = document.querySelectorAll('input, select, textarea');
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
    patientForm.addEventListener('submit', function(event) {
        if (!confirm('Are you sure you want to submit the form?')) {
            event.preventDefault();
        }
    });
});

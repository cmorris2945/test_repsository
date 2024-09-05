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

    // Hide all sections initially except for the first question
    const sections = ['help_options', 'second_opinion', 'started_treatment', 'additional_info', 'gender_selection', 'ehr_sync', 'ehr_sync_record', 'final_questions', 'patientProfiling', 'doctorMatch'];
    sections.forEach(section => {
        document.getElementById(section).style.display = 'none';
    });

    // Handle the questionnaire progression
    document.getElementById('help_today').addEventListener('change', function() {
        showNextSection('help_options');
    });

    document.getElementById('help_option').addEventListener('change', function() {
        showNextSection('second_opinion');
    });

    document.querySelectorAll('input[name="second_opinion"]').forEach(function(radio) {
        radio.addEventListener('change', function() {
            showNextSection('started_treatment');
        });
    });

    document.querySelectorAll('input[name="started_treatment"]').forEach(function(radio) {
        radio.addEventListener('change', function() {
            showNextSection('additional_info');
        });
    });

    document.getElementById('insurance_name').addEventListener('change', function() {
        showNextSection('gender_selection');
    });

    document.getElementById('gender').addEventListener('change', function() {
        showNextSection('ehr_sync');
        setTimeout(function () {
            document.querySelector("#ehr_sync p").innerHTML = "Data retrieved. Please verify the information below.";
            showNextSection('ehr_sync_record')
        }, 3000);  // 3000 milliseconds = 3 seconds
    });

    document.querySelectorAll('input[name="confirm_info"]').forEach(function(radio) {
        radio.addEventListener('change', function() {
            showNextSection('final_questions');
        });
    });

    document.getElementById('doctor_preferences').addEventListener('change', function() {
        showNextSection('patientProfiling');
        setTimeout(function () {
            document.querySelector("#patientProfiling p").innerHTML = "Matching done. Please select the best doctor available.";
            showNextSection('doctorMatch')
        }, 2000);  // 2000 milliseconds = 2 seconds
    });

    // Function to show the next section
    function showNextSection(sectionId) {
        document.getElementById(sectionId).style.display = 'block';
        smoothScroll('#' + sectionId);
    }

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
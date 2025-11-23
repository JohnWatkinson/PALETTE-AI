// PALETTE-AI Questionnaire Form Handler

document.getElementById('questionnaire-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const form = e.target;
    const submitButton = form.querySelector('button[type="submit"]');

    // Disable submit button
    submitButton.disabled = true;
    submitButton.textContent = 'Analyzing...';

    // Collect form data
    const formData = new FormData(form);

    // Build submission object
    const submission = {
        // Personal information (GDPR)
        first_name: formData.get('first_name'),
        last_name: formData.get('last_name'),
        email: formData.get('email'),
        language: formData.get('language'),

        // Consent (GDPR)
        privacy_consent: formData.get('privacy_consent') === 'on',
        newsletter_consent: formData.get('newsletter_consent') === 'on',

        // Questionnaire responses
        hair_color: formData.get('hair_color'),
        skin_tone: formData.get('skin_tone'),
        eye_color: formData.get('eye_color'),
        vein_color: formData.get('vein_color'),
        jewelry_preference: formData.get('jewelry_preference'),
        colors_worn: formData.getAll('colors_worn'),
        colors_avoided: formData.getAll('colors_avoided'),
        color_feedback: formData.get('color_feedback')
    };

    try {
        // Submit to API
        const response = await fetch('/api/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(submission)
        });

        if (!response.ok) {
            throw new Error('Failed to submit questionnaire');
        }

        const result = await response.json();

        // Store result in sessionStorage for results page
        sessionStorage.setItem('paletteResult', JSON.stringify(result));

        // Redirect to thank you page (will implement email later)
        window.location.href = '/thank-you';

    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
        submitButton.disabled = false;
        submitButton.textContent = 'Discover My Palette';
    }
});

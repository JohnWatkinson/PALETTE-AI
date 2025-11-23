// PALETTE-AI Translation System
// Simple client-side translations matching Maison Guida's i18n approach

const translations = {
    en: {
        // Header
        "header.title": "Palette Analysis",
        "header.intro1": "Discover your personal color season and receive a curated palette",
        "header.intro2": "tailored to your unique coloring.",

        // Personal Information
        "section.info": "Your Information",
        "label.firstName": "First Name",
        "label.lastName": "Last Name",
        "label.email": "Email Address",
        "label.language": "Language / Lingua",

        // Your Coloring
        "section.coloring": "Your Coloring",
        "label.hairColor": "Natural Hair Color",
        "label.skinTone": "Skin Tone",
        "label.eyeColor": "Eye Color",
        "label.veinColor": "Vein Color (Look at your wrist in natural light)",
        "label.jewelry": "Which metal looks better on you?",

        // Hair Color Options
        "hair.select": "Select...",
        "hair.black": "Black",
        "hair.darkBrown": "Dark Brown",
        "hair.lightBrown": "Light Brown",
        "hair.goldenBlonde": "Blonde (Golden/Warm)",
        "hair.ashBlonde": "Blonde (Ash/Cool)",
        "hair.redAuburn": "Red/Auburn",
        "hair.grayWhite": "Gray/White",

        // Skin Tone Options
        "skin.veryFair": "Very Fair (burns easily, rarely tans)",
        "skin.fair": "Fair (burns sometimes, tans gradually)",
        "skin.lightMedium": "Light-Medium (tans easily, rarely burns)",
        "skin.mediumOlive": "Medium/Olive",
        "skin.tanCaramel": "Tan/Caramel",
        "skin.deepRich": "Deep/Rich Brown",
        "skin.veryDeep": "Very Deep/Dark Brown",

        // Eye Color Options
        "eye.lightBlue": "Light Blue",
        "eye.blueGray": "Blue-Gray/Steel Blue",
        "eye.green": "Green",
        "eye.hazel": "Hazel (Green-Brown)",
        "eye.lightBrown": "Light Brown/Amber",
        "eye.darkBrown": "Dark Brown",
        "eye.black": "Black",

        // Vein Color Options
        "vein.green": "Green/Olive (Warm undertone)",
        "vein.blue": "Blue/Purple (Cool undertone)",
        "vein.both": "Both/Not Sure (Neutral)",

        // Jewelry Options
        "jewelry.gold": "Gold",
        "jewelry.silver": "Silver",
        "jewelry.both": "Both Look Good",

        // Style Questions
        "section.style": "Your Style",
        "label.colorsWorn": "What colors do you wear most often? (Select up to 5)",
        "label.colorsAvoided": "What colors do you avoid? (Select up to 5)",
        "label.feedback": "When you wear certain colors, people say you look:",

        // Color Categories
        "colors.blackNavy": "Black, Navy, Charcoal",
        "colors.brownBeige": "Brown, Beige, Camel",
        "colors.earth": "Earth tones (rust, olive, terracotta)",
        "colors.pastels": "Pastels (baby pink, mint, lavender)",
        "colors.brightJewel": "Bright jewel tones (emerald, sapphire, ruby)",
        "colors.muted": "Muted colors (dusty rose, sage, mauve)",
        "colors.white": "White, Cream, Ivory",

        // Feedback Options
        "feedback.vibrant": "Vibrant and Glowing",
        "feedback.washedOut": "Washed Out or Tired",
        "feedback.depends": "It Depends on the Color",
        "feedback.noComments": "No One Comments",

        // Consent
        "section.consent": "Privacy & Consent",
        "consent.privacy": "I have read and agree to the",
        "consent.privacyLink": "Privacy Policy",
        "consent.privacyRequired": "*",
        "consent.newsletter": "I would like to receive styling tips and updates from Maison Guida (optional)",

        // Button
        "button.submit": "Discover My Palette",
        "button.analyzing": "Analyzing..."
    },

    it: {
        // Header
        "header.title": "Analisi della Palette",
        "header.intro1": "Scopri la tua stagione cromatica personale e ricevi una palette curata",
        "header.intro2": "su misura per la tua colorazione unica.",

        // Personal Information
        "section.info": "Le Tue Informazioni",
        "label.firstName": "Nome",
        "label.lastName": "Cognome",
        "label.email": "Indirizzo Email",
        "label.language": "Language / Lingua",

        // Your Coloring
        "section.coloring": "La Tua Colorazione",
        "label.hairColor": "Colore Naturale dei Capelli",
        "label.skinTone": "Tonalità della Pelle",
        "label.eyeColor": "Colore degli Occhi",
        "label.veinColor": "Colore delle Vene (Guarda il polso alla luce naturale)",
        "label.jewelry": "Quale metallo ti sta meglio?",

        // Hair Color Options
        "hair.select": "Seleziona...",
        "hair.black": "Nero",
        "hair.darkBrown": "Castano Scuro",
        "hair.lightBrown": "Castano Chiaro",
        "hair.goldenBlonde": "Biondo (Dorato/Caldo)",
        "hair.ashBlonde": "Biondo (Cenere/Freddo)",
        "hair.redAuburn": "Rosso/Ramato",
        "hair.grayWhite": "Grigio/Bianco",

        // Skin Tone Options
        "skin.veryFair": "Molto Chiara (si scotta facilmente, raramente si abbronza)",
        "skin.fair": "Chiara (a volte si scotta, si abbronza gradualmente)",
        "skin.lightMedium": "Chiara-Media (si abbronza facilmente, raramente si scotta)",
        "skin.mediumOlive": "Media/Olivastra",
        "skin.tanCaramel": "Abbronzata/Caramello",
        "skin.deepRich": "Scura/Marrone Intenso",
        "skin.veryDeep": "Molto Scura/Marrone Scuro",

        // Eye Color Options
        "eye.lightBlue": "Azzurro Chiaro",
        "eye.blueGray": "Blu-Grigio/Azzurro Acciaio",
        "eye.green": "Verde",
        "eye.hazel": "Nocciola (Verde-Marrone)",
        "eye.lightBrown": "Marrone Chiaro/Ambra",
        "eye.darkBrown": "Marrone Scuro",
        "eye.black": "Nero",

        // Vein Color Options
        "vein.green": "Verde/Oliva (Sottotono caldo)",
        "vein.blue": "Blu/Viola (Sottotono freddo)",
        "vein.both": "Entrambi/Non Sono Sicuro (Neutro)",

        // Jewelry Options
        "jewelry.gold": "Oro",
        "jewelry.silver": "Argento",
        "jewelry.both": "Entrambi Stanno Bene",

        // Style Questions
        "section.style": "Il Tuo Stile",
        "label.colorsWorn": "Quali colori indossi più spesso? (Seleziona fino a 5)",
        "label.colorsAvoided": "Quali colori eviti? (Seleziona fino a 5)",
        "label.feedback": "Quando indossi certi colori, le persone dicono che sembri:",

        // Color Categories
        "colors.blackNavy": "Nero, Blu Navy, Antracite",
        "colors.brownBeige": "Marrone, Beige, Cammello",
        "colors.earth": "Tonalità terra (ruggine, oliva, terracotta)",
        "colors.pastels": "Pastelli (rosa baby, menta, lavanda)",
        "colors.brightJewel": "Tonalità gioiello brillanti (smeraldo, zaffiro, rubino)",
        "colors.muted": "Colori tenui (rosa antico, salvia, malva)",
        "colors.white": "Bianco, Panna, Avorio",

        // Feedback Options
        "feedback.vibrant": "Vibrante e Luminosa",
        "feedback.washedOut": "Spenta o Stanca",
        "feedback.depends": "Dipende dal Colore",
        "feedback.noComments": "Nessuno Commenta",

        // Consent
        "section.consent": "Privacy e Consenso",
        "consent.privacy": "Ho letto e accetto la",
        "consent.privacyLink": "Informativa sulla Privacy",
        "consent.privacyRequired": "*",
        "consent.newsletter": "Vorrei ricevere consigli di stile e aggiornamenti da Maison Guida (facoltativo)",

        // Button
        "button.submit": "Scopri la Mia Palette",
        "button.analyzing": "Analisi in corso..."
    }
};

// Translation function
function t(key, lang = 'en') {
    return translations[lang]?.[key] || translations.en[key] || key;
}

// Update page language
function updateLanguage(lang) {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.textContent = t(key, lang);
    });

    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        el.placeholder = t(key, lang);
    });

    // Update submit button text
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn && !submitBtn.disabled) {
        submitBtn.textContent = t('button.submit', lang);
    }
}

// Listen for language change
document.addEventListener('DOMContentLoaded', () => {
    const languageSelect = document.getElementById('language');
    if (languageSelect) {
        languageSelect.addEventListener('change', (e) => {
            updateLanguage(e.target.value);
        });
    }
});

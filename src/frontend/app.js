document.addEventListener('DOMContentLoaded', () => {
    // Localization Setup
    const langSelect = document.getElementById('lang-select');
    let currentLang = 'en';
    let translations = {};

    async function loadTranslations(lang) {
        try {
            const response = await fetch(`locales/${lang}.json`);
            translations = await response.json();
            applyTranslations();
        } catch (error) {
            console.error('Failed to load translations:', error);
        }
    }

    function applyTranslations() {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (translations[key]) {
                el.textContent = translations[key];
            }
        });
    }

    langSelect.addEventListener('change', (e) => {
        currentLang = e.target.value;
        loadTranslations(currentLang);
    });

    // Load default language
    loadTranslations(currentLang);

    // Timeline fetch mock
    fetch('/api/timeline')
        .then(res => res.json())
        .then(data => {
            if(data.status === 'success' && data.phases && data.phases.length > 0) {
                document.getElementById('timeline-info').textContent = 
                    `Phase 1 starts on ${data.phases[0].date} for regions: ${data.phases[0].regions.join(', ')}`;
            }
        }).catch(err => {
            document.getElementById('timeline-info').textContent = "Timeline unavailable.";
        });

    // Chat functionality
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatBox = document.getElementById('chat-box');

    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.className = `message ${sender}`;
        div.textContent = text;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if (!msg) return;

        addMessage(msg, 'user');
        chatInput.value = '';

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg, language: currentLang })
            });
            const data = await response.json();
            
            if (data.response) {
                // To decode html entities returned safely from backend
                const parser = new DOMParser();
                const decodedText = parser.parseFromString(data.response, "text/html").documentElement.textContent;
                addMessage(decodedText, 'bot');
            } else if (data.error) {
                 addMessage(`Error: ${data.error}`, 'bot');
            } else {
                addMessage("Error processing response.", 'bot');
            }
        } catch (error) {
            addMessage("Network error. Could not connect to assistant.", 'bot');
        }
    });
});

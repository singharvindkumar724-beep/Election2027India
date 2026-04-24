document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatLog = document.getElementById('chatLog');
    const langSelect = document.getElementById('langSelect');
    const loadCandidatesBtn = document.getElementById('loadCandidatesBtn');
    const candidatesList = document.getElementById('candidatesList');

    // Handle Candidates Load
    if (loadCandidatesBtn) {
        loadCandidatesBtn.addEventListener('click', async () => {
            triggerQuery("Show candidate profiles");
        });
    }

    // Interactive UI Buttons
    const btnFindPolling = document.getElementById('btnFindPolling');
    const navCivic = document.getElementById('navCivic');
    const navCandidates = document.getElementById('navCandidates');
    const navPolling = document.getElementById('navPolling');
    const navTimeline = document.getElementById('navTimeline');
    const btnExploreGuide = document.getElementById('btnExploreGuide');

    const triggerQuery = (query) => {
        userInput.value = query;
        chatForm.dispatchEvent(new Event('submit'));
    };

    if (btnFindPolling) btnFindPolling.addEventListener('click', () => triggerQuery("Where is my nearest polling booth?"));
    if (navCivic) navCivic.addEventListener('click', (e) => { e.preventDefault(); triggerQuery("Why should I vote and what is civic education?"); });
    if (navCandidates) navCandidates.addEventListener('click', (e) => { e.preventDefault(); triggerQuery("Show candidate profiles"); });
    if (navPolling) navPolling.addEventListener('click', (e) => { e.preventDefault(); triggerQuery("Where do I vote?"); });
    if (navTimeline) navTimeline.addEventListener('click', (e) => { e.preventDefault(); triggerQuery("What is the election timeline?"); });
    if (btnExploreGuide) btnExploreGuide.addEventListener('click', () => triggerQuery("Tell me about democracy and voting."));

    function renderCandidates(candidates) {
        if (!candidates || candidates.length === 0) {
            candidatesList.innerHTML = '<p class="text-sm text-textMuted">No candidates found.</p>';
            return;
        }
        
        candidatesList.innerHTML = '';
        candidates.forEach(c => {
            const card = document.createElement('div');
            card.className = 'bg-primary border border-[#313b35] rounded-xl p-4 flex gap-4 fade-in-up';
            
            card.innerHTML = `
                <img src="${c.PhotoUrl || 'https://via.placeholder.com/60'}" class="w-16 h-16 rounded-full object-cover border-2 border-accent" alt="${c.Name}">
                <div>
                    <h4 class="font-bold text-textMain">${c.Name}</h4>
                    <p class="text-xs text-accent font-medium mb-2">${c.Party}</p>
                    <p class="text-xs text-textMuted line-clamp-2" title="${c.ElectionPromises}">${c.ElectionPromises}</p>
                </div>
            `;
            candidatesList.appendChild(card);
        });
    }

    // Handle Chat
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = userInput.value.trim();
        if (!query) return;

        appendMessage(query, 'user');
        userInput.value = '';
        
        const typingId = showTypingIndicator();
        scrollToBottom();

        try {
            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query, lang: langSelect.value })
            });

            const data = await response.json();
            removeTypingIndicator(typingId);
            
            // If it's candidate intent, render candidates too
            if (data.intent === 'candidate_profiles' && data.response.data.candidates) {
                renderCandidates(data.response.data.candidates);
            }
            
            renderBotResponse(data);
        } catch (error) {
            console.error(error);
            removeTypingIndicator(typingId);
            appendMessage("Error connecting to the command center.", 'system');
        }
        scrollToBottom();
    });

    function appendMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `flex gap-3 fade-in-up ${sender === 'user' ? 'flex-row-reverse' : ''}`;
        
        const iconDiv = document.createElement('div');
        iconDiv.className = `w-8 h-8 rounded flex items-center justify-center shrink-0 ${sender === 'user' ? 'bg-accent text-[#000]' : 'bg-[#2b332d] text-accent'}`;
        iconDiv.innerHTML = `<i data-lucide="${sender === 'user' ? 'user' : 'bot'}" class="w-4 h-4"></i>`;

        const contentDiv = document.createElement('div');
        contentDiv.className = `p-3 rounded-2xl text-sm border ${sender === 'user' ? 'bg-accent/10 border-accent/20 rounded-tr-sm text-textMain' : 'bg-[#2b332d] border-[#313b35] rounded-tl-sm text-textMain prose'}`;
        
        // Simple markdown bullet parsing for Gemini responses
        let formattedText = text.replace(/\n\s*\*\s/g, '<br>• ');
        contentDiv.innerHTML = formattedText;

        msgDiv.appendChild(iconDiv);
        msgDiv.appendChild(contentDiv);
        chatLog.appendChild(msgDiv);
        lucide.createIcons({ root: msgDiv });
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.id = id;
        msgDiv.className = `flex gap-3 fade-in-up`;
        
        msgDiv.innerHTML = `
            <div class="w-8 h-8 rounded bg-[#2b332d] flex items-center justify-center text-accent shrink-0">
                <i data-lucide="bot" class="w-4 h-4"></i>
            </div>
            <div class="bg-[#2b332d] p-3 rounded-2xl rounded-tl-sm text-sm border border-[#313b35] flex items-center gap-1">
                <div class="w-1.5 h-1.5 rounded-full bg-textMuted typing-dot"></div>
                <div class="w-1.5 h-1.5 rounded-full bg-textMuted typing-dot" style="animation-delay: 0.2s"></div>
                <div class="w-1.5 h-1.5 rounded-full bg-textMuted typing-dot" style="animation-delay: 0.4s"></div>
            </div>
        `;
        chatLog.appendChild(msgDiv);
        lucide.createIcons({ root: msgDiv });
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function renderBotResponse(result) {
        const intent = result.intent;
        const responseData = result.response;
        const data = responseData.data;

        let replyText = "";
        
        if (intent === 'action_phase') {
            replyText = `**Nearest Location:** ${data.nearest_location}<br>${data.address}<br>Distance: ${data.distance}`;
        } else if (intent === 'planning_phase') {
            replyText = `**Upcoming Dates:**<br>` + (data.events || []).map(e => `• ${e.name} (${e.date})`).join('<br>');
        } else if (intent === 'candidate_profiles') {
            replyText = `I have loaded the candidate profiles in the side panel for you.`;
        } else if (intent === 'civic_education') {
            replyText = `**Civics 101:**<br>` + (data.facts || []).map(f => `• ${f}`).join('<br>');
        } else if (intent === 'information_phase') {
            // General Chat / Gemini response
            replyText = (data.facts || []).map(f => `• ${f}`).join('<br>');
            if (!replyText && data.message) replyText = data.message;
        } else {
            replyText = data.message || "I couldn't process that request.";
        }

        appendMessage(replyText, 'system');
    }

    function scrollToBottom() {
        chatLog.scrollTop = chatLog.scrollHeight;
    }
});

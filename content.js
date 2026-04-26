function cleanText(text) {
    return text
        .replace(/\s+/g, ' ')
        .replace(/\n+/g, ' ')
        .trim();
}

// Function to check if text is relevant (not chat history, navigation, etc.)
function isRelevantText(text) {
    const irrelevantPatterns = [
        /chat history/i,
        /chatgpt/i,
        /sidebar/i,
        /explore gpts/i,
        /previous \d+ days/i,
        /more access/i,
        /upgrade plan/i,
        /share/i,
        /you said/i,
        /chatgpt said/i
    ];
    
    return !irrelevantPatterns.some(pattern => pattern.test(text));
}

// Function to extract main content
function extractMainContent() {
    // Try to find the main content area
    const mainContent = document.querySelector('main, article, [role="main"], .main-content, #main-content, .content, #content');
    
    if (mainContent) {
        return mainContent.innerText;
    }
    
    // If no main content area found, get all text but filter out navigation, headers, footers
    const body = document.body;
    const elements = body.getElementsByTagName('*');
    let content = '';
    
    for (let element of elements) {
        // Skip hidden elements
        if (element.offsetParent === null) continue;
        
        // Skip navigation, headers, footers
        if (element.tagName === 'NAV' || 
            element.tagName === 'HEADER' || 
            element.tagName === 'FOOTER' ||
            element.classList.contains('nav') ||
            element.classList.contains('header') ||
            element.classList.contains('footer')) {
            continue;
        }
        
        // Get text content
        const text = element.innerText;
        if (text && isRelevantText(text)) {
            content += text + ' ';
        }
    }
    
    return content;
}

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'scan') {
        try {
            // Extract and clean the content
            const content = extractMainContent();
            const cleanedContent = cleanText(content);
            
            if (!cleanedContent) {
                sendResponse({ 
                    success: false, 
                    error: 'No relevant content found on this page.' 
                });
                return;
            }

            // Send the content to the backend
            fetch('http://localhost:5000/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: cleanedContent })
            })
            .then(response => response.json())
            .then(data => {
                sendResponse({ 
                    success: true, 
                    summary: data.summary,
                    key_points: data.key_points 
                });
            })
            .catch(error => {
                sendResponse({ 
                    success: false, 
                    error: 'Error communicating with the backend server.' 
                });
            });
        } catch (error) {
            sendResponse({ 
                success: false, 
                error: 'Error processing page content.' 
            });
        }
        return true; // Keep the message channel open for the async response
    }
});
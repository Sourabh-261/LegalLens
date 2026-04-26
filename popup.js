document.addEventListener('DOMContentLoaded', function() {
    const scanButton = document.getElementById('scanButton');
    const loading = document.getElementById('loading');
    const summary = document.getElementById('summary');
    const error = document.getElementById('error');
    const pointsList = document.getElementById('points');

    scanButton.addEventListener('click', async () => {
        // Show loading state
        loading.classList.remove('hidden');
        summary.classList.add('hidden');
        error.classList.add('hidden');
        pointsList.innerHTML = '';

        try {
            // Get the active tab
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

            // Send message to content script
            const response = await chrome.tabs.sendMessage(tab.id, { action: 'scan' });

            // Hide loading state
            loading.classList.add('hidden');

            if (response.success) {
                // Display summary
                summary.classList.remove('hidden');
                
                // Add key points
                if (response.key_points && response.key_points.length > 0) {
                    // Add a title for key points
                    const keyPointsTitle = document.createElement('h3');
                    keyPointsTitle.textContent = 'Key Points:';
                    pointsList.appendChild(keyPointsTitle);

                    // Add each key point
                    response.key_points.forEach(point => {
                        const li = document.createElement('li');
                        li.textContent = point;
                        pointsList.appendChild(li);
                    });

                    // Add summary section
                    const summaryTitle = document.createElement('h3');
                    summaryTitle.textContent = 'Summary:';
                    pointsList.appendChild(summaryTitle);

                    const summaryLi = document.createElement('li');
                    summaryLi.textContent = response.summary;
                    pointsList.appendChild(summaryLi);
                } else {
                    // If no key points, show the full summary
                    const li = document.createElement('li');
                    li.textContent = response.summary;
                    pointsList.appendChild(li);
                }
            } else {
                // Show error message
                error.classList.remove('hidden');
                error.textContent = response.error || 'No terms and conditions found on this page.';
            }
        } catch (err) {
            // Handle errors
            loading.classList.add('hidden');
            error.classList.remove('hidden');
            error.textContent = 'Error scanning page. Please make sure the backend server is running at http://localhost:5000';
        }
    });
});
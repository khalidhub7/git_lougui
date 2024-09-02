// home_page.js
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.querySelector('.search input');
    const searchButton = document.querySelector('.search button');

    searchButton.addEventListener('click', function() {
        const githubUsername = searchInput.value.trim();

        if (!githubUsername) {
            alert("Please enter a GitHub username");
            return;
        }

        fetch(`https://api.github.com/users/${githubUsername}`)
            .then(response => {
                if (!response.ok) {
                    if (response.status === 403) {
                        const rateLimitReset = response.headers.get('X-RateLimit-Reset');
                        const resetTime = rateLimitReset ? new Date(parseInt(rateLimitReset) * 1000) : 'unknown';
                        alert(`Rate limit reached. Reset at: ${resetTime}`);
                    } else {
                        alert("Invalid GitHub username");
                    }
                    throw new Error('Invalid GitHub username');
                }
                return response.json();
            })
            .then(() => {
                window.location.href = `http://127.0.0.1:2000/gitlougui/${githubUsername}/stats`;
            })
            .catch(error => console.error('Error:', error));
    });
});

// user_profile.js
document.addEventListener("DOMContentLoaded", function() {
    function toggleList(buttonId, listClass) {
        const toggleButton = document.getElementById(buttonId);
        const listItems = document.querySelectorAll(`.${listClass} li:nth-child(n+4)`);

        if (!toggleButton || listItems.length === 0) {
            console.error(`Toggle button with ID ${buttonId} or list items not found.`);
            return;
        }

        listItems.forEach(function(item) {
            item.style.display = "none";
        });

        toggleButton.addEventListener("click", function() {
            const isHidden = listItems[0].style.display === "none";
            
            listItems.forEach(function(item) {
                item.style.display = isHidden ? "list-item" : "none";
            });

            toggleButton.textContent = isHidden ? "Show Less" : "Show More";
        });
    }

    toggleList("repoToggle", "repo_list");
    toggleList("followerToggle", "follower_list");
    toggleList("followingToggle", "following_list");
    toggleList("activityToggle", "activity_list");

    function getUsernameFromCurrentURL() {
        const url = window.location.href;
        const regex = /\/gitlougui\/([^\/]+)\//;
        const match = url.match(regex);
        return match ? match[1] : null;
    }

    const githubUsername = getUsernameFromCurrentURL();
    const repoLinks = document.querySelectorAll('.repo_list .repo_name');

    repoLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const selectedRepo = link.textContent.trim();
            window.location.href = `http://127.0.0.1:2000/gitlougui/${githubUsername}/${selectedRepo}`;
        });
    });
});
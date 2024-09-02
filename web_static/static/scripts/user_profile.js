document.addEventListener("DOMContentLoaded", function() {
    // Function to toggle visibility
    function toggleList(buttonId, listClass) {
        const toggleButton = document.getElementById(buttonId);
        const listItems = document.querySelectorAll(`.${listClass} li:nth-child(n+4)`);

        // Initially hide the extra items
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

    // Initialize toggle for each section
    toggleList("repoToggle", "repo_list");
    toggleList("followerToggle", "follower_list");
    toggleList("followingToggle", "following_list");
    toggleList("activityToggle", "activity_list");
});

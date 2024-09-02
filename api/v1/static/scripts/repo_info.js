function toggleReadme() {
    var readmeContent = document.getElementById('readme-content');
    var toggleButton = document.getElementById('toggle-readme-button');
    if (readmeContent.style.maxHeight === '300px') {
        readmeContent.style.maxHeight = 'none';
        toggleButton.innerText = 'Show Less';
    } else {
        readmeContent.style.maxHeight = '300px';
        toggleButton.innerText = 'Show More';
    }
}

function toggleContributors() {
    var moreContributors = document.getElementById('more-contributors');
    var toggleButton = document.getElementById('toggle-contributors-button');
    if (moreContributors.style.display === 'none') {
        moreContributors.style.display = 'block';
        toggleButton.innerText = 'Show Less';
    } else {
        moreContributors.style.display = 'none';
        toggleButton.innerText = 'Show More';
    }
}

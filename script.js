window.onload = function() {
    const path = window.location.pathname;
    if (path === '/admin') {
        enableAdminMode();
    }
    loadStories();
}

function enableAdminMode() {
    document.getElementById('story-input').classList.remove('hidden');
    document.body.classList.add('admin-mode');
}

function addStory() {
    const storyText = document.getElementById('story-text').value;
    if (storyText.trim() === '') {
        alert('Please write a story before adding.');
        return;
    }
    const stories = getStories();
    stories.push(storyText);
    saveStories(stories);
    displayStories();
    document.getElementById('story-text').value = '';
}

function editStory(index) {
    const stories = getStories();
    const storyText = prompt('Edit your story in Markdown:', stories[index]);
    if (storyText !== null) {
        stories[index] = storyText;
        saveStories(stories);
        displayStories();
    }
}

function getStories() {
    return JSON.parse(localStorage.getItem('stories') || '[]');
}

function saveStories(stories) {
    localStorage.setItem('stories', JSON.stringify(stories));
}

function loadStories() {
    displayStories();
}

function displayStories() {
    const storiesDiv = document.getElementById('stories');
    storiesDiv.innerHTML = '';
    const stories = getStories();
    stories.forEach((story, index) => {
        const storyDiv = document.createElement('div');
        storyDiv.classList.add('story');
        storyDiv.innerHTML = `
            <div class="story-content">${marked.parse(story)}</div>
            <button class="edit-button" onclick="editStory(${index})">Edit</button>
        `;
        storiesDiv.appendChild(storyDiv);
    });
}

document.getElementById('searchBtn').addEventListener('click', function() {
    // Call a function to handle the search
    performSearch();
});

document.getElementById('query').addEventListener('keyup', function(event) {
    // Handle the Enter key press
    if (event.key === 'Enter') {
        performSearch();
    }
});

document.getElementById('darkModeToggle').addEventListener('change', function() {
    document.body.classList.toggle('dark-mode');
});

function performSearch() {
    var query = document.getElementById('query').value;

    // Update the fetch call to target the /search route
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'query': query})
    })
    .then(response => response.json())
    .then(data => {
        var searchResultsList = document.getElementById('search-results-list');
        searchResultsList.innerHTML = '';

        data.docs.forEach(function(doc) {
            var listItem = document.createElement('li');
            listItem.textContent = "Document ID: " + doc;

            // Append the list item to the search results list
            searchResultsList.appendChild(listItem);
        });
    })
    .catch(error => {
        console.error('Error fetching search results:', error);
    });
}

document.getElementById('query').addEventListener('keyup', function() {
    var query = this.value;

    fetch('/get_suggestions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'query': query})
    })
    .then(response => response.json())
    .then(data => {
        var suggestionsList = document.getElementById('suggestions-list');
        suggestionsList.innerHTML = '';

        data.suggestions.forEach(function(suggestion) {
            var listItem = document.createElement('li');
            listItem.textContent = suggestion;

            // Create a copy button for each suggestion
            var copyBtn = document.createElement('button');
            copyBtn.className = 'copy-btn';
            copyBtn.textContent = 'Copy';
            copyBtn.addEventListener('click', function() {
                var tempInput = document.createElement('input');
                tempInput.value = suggestion;
                document.body.appendChild(tempInput);
                tempInput.select();
                document.execCommand('copy');
                document.body.removeChild(tempInput);
            });

            listItem.appendChild(copyBtn);
            suggestionsList.appendChild(listItem);

            listItem.addEventListener('mouseover', function() {
                copyBtn.style.display = 'inline-block';
            });

            listItem.addEventListener('mouseout', function() {
                copyBtn.style.display = 'none';
            });
        });
    });
});

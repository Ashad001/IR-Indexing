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
    var queryInput = document.getElementById('query');
    var query = queryInput.value;

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

        if (data.docs.length === 0) {
            fetch('/get_corrections', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'query': query})
            })
            .then(response => response.json())
            .then(correctionData => {
                var listItem = document.createElement('li');
                listItem.innerHTML = "Did you mean: ";

                var suggestionLink = document.createElement('a');
                suggestionLink.textContent = correctionData.corrected_query;
                suggestionLink.href = '#'; 

                suggestionLink.addEventListener('click', function(event) {
                    event.preventDefault();
                    queryInput.value = correctionData.corrected_query;
                    performSearch(); // Perform the search with the corrected query i.e. minimum lavenstein distance (when will i correcly spell this)
                });

                listItem.appendChild(suggestionLink);
                searchResultsList.appendChild(listItem);
            })
            .catch(error => {
                console.error('Error fetching suggested query:', error);
            });
        } else {
            data.docs.forEach(function(doc) {
                var listItem = document.createElement('li');
                listItem.textContent = "Document ID: " + doc;

                searchResultsList.appendChild(listItem);
            });
        }
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

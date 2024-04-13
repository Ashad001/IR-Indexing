import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [correctedQuery, setCorrectedQuery] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      if (query.length > 2) {
        fetchSuggestions();
      }
    }, 300);  // Adds a 300ms delay to reduce API calls
    return () => clearTimeout(delayDebounce);
  }, [query]);

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const fetchSuggestions = async () => {
    try {
      const response = await axios.post('/get_suggestions', { query });
      setSuggestions(response.data.suggestions);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      setSuggestions([]);
    }
  };

  const search = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/search', { query });
      setSearchResults(response.data.docs.length ? response.data.docs : []);
      setCorrectedQuery('');
    } catch (error) {
      console.error('Error searching:', error);
      setSearchResults([]);
    }
    setLoading(false);
  };

  const getCorrections = async () => {
    try {
      const response = await axios.post('/get_corrections', { query });
      setCorrectedQuery(response.data.corrected_query);
      setSearchResults([]);
    } catch (error) {
      console.error('Error getting corrections:', error);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    const words = query.trim().split(' ');
    const lastWord = words[words.length - 1];
    if (suggestion.toLowerCase().startsWith(lastWord.toLowerCase())) {
      words[words.length - 1] = suggestion;
    } else {
      words.push(suggestion);
    }
    setQuery(words.join(' '));
    setSuggestions([]);
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    search();
  };

  return (
    <div>
      <form onSubmit={handleFormSubmit}>
        <input type="text" value={query} onChange={handleQueryChange} placeholder="Search here..." />
        <button type="submit" disabled={loading}>Search</button>
      </form>
      
      {suggestions.length > 0 && (
        <div>
          <h2>Suggestions:</h2>
          <ul>
            {suggestions.map((suggestion, index) => (
              <li key={index} onClick={() => handleSuggestionClick(suggestion)}>{suggestion}</li>
            ))}
          </ul>
        </div>
      )}

      {searchResults.length > 0 && (
        <div>
          <h2>Search Results:</h2>
          <ul>
            {searchResults.map((result, index) => (
              <li key={index}>{result}</li>
            ))}
          </ul>
        </div>
      )}

      {correctedQuery && (
        <div>
          <h2>Did you mean:</h2>
          <p onClick={() => setQuery(correctedQuery)} style={{cursor: 'pointer', textDecoration: 'underline'}}>{correctedQuery}</p>
        </div>
      )}
    </div>
  );
}

export default App;

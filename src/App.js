import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'

function App() {
  const [query, setQuery] = useState('');
  const [ranks, setRanks] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [correctedQuery, setCorrectedQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [summaries, setSummaries] = useState([]);

  useEffect(() => {
    if (query.length > 2) {
      fetchSuggestions();
    }
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
    }
  };

  const search = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/search', { query });
      if (response.data.docs.length > 0) {
        setSearchResults(response.data.docs);
        setRanks(response.data.ranks);
        setSummaries(response.data.summaries);
        setCorrectedQuery('');
      } else {
        getCorrections();
      }
    } catch (error) {
      console.error('Error searching:', error);
    }
    setLoading(false);
  };

  const getCorrections = async () => {
    try {
      const response = await axios.post('/get_corrections', { query });
      setCorrectedQuery(response.data.corrected_query);
      setSearchResults([]); // Clear previous results if corrections are suggested
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
    <div className="search-container">
      <h1> Vector Indexing </h1>
      <form className="search-form" onSubmit={handleFormSubmit}>
        <input className="search-input" type="text" value={query} onChange={handleQueryChange} placeholder="Search here..." />
        <button className="search-button" type="submit" disabled={loading}>Search</button>
      </form>
  
      <div className="results-container">
        {searchResults.length > 0 && (
          <div className="search-results">
            <h2>Search Results:</h2>
            <ul >
              {searchResults.map((result, index) => (
                <li key={index}>
                  <span className='document-id'> Doc: {result} </span>
                  <span className='rank-results'>Score: {ranks[index]}</span>
                  <span className='summary-results'>{summaries[index]}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
  
        {correctedQuery && (
          <div className="corrections">
            <h2>Did you mean:</h2>
            <p onClick={() => setQuery(correctedQuery)} style={{ cursor: 'pointer', textDecoration: 'underline' }}>{correctedQuery}</p>
          </div>
        )}
      </div>
  
      {suggestions.length > 0 && (
        <div className="suggestions">
          <h2>Suggestions:</h2>
          <ul>
            {suggestions.map((suggestion, index) => (
              <li key={index} onClick={() => handleSuggestionClick(suggestion)}>{suggestion}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
    }
            
export default App;

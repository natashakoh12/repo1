//main application file

import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; //layout

const App = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = async () => {
    const response = await axios.get(`http://localhost:9200/cv-transcriptions/_search`, {
      params: {
        q: `generated_text:${searchTerm} OR duration:${searchTerm} OR age:${searchTerm} OR gender:${searchTerm} OR accent:${searchTerm}`
      }
    });
    setSearchResults(response.data.hits.hits);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Search UI</h1>
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search..."
        />
        <button onClick={handleSearch}>Search</button>
        <ul>
          {searchResults.map(result => (
            <li key={result._id}>
              <p>Generated Text: {result._source.generated_text}</p>
              <p>Duration: {result._source.duration}</p>
              <p>Age: {result._source.age}</p>
              <p>Gender: {result._source.gender}</p>
              <p>Accent: {result._source.accent}</p>
            </li>
          ))}
        </ul>
      </header>
    </div>
  );
};

export default App;


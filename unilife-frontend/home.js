const searchInput  = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const resultsDiv    = document.getElementById('results');

const API_URL = 'http://127.0.0.1:5000/search';

async function runSearch() {
  const query = searchInput.value.trim();
  if (query === '') {
    resultsDiv.innerHTML = '';
    return;
  }

  resultsDiv.innerHTML = '<p>Searching…</p>';

  try {
    const response = await fetch(`${API_URL}?q=${encodeURIComponent(query)}`);
    const results  = await response.json();
    renderResults(results);
  } catch (error) {
    resultsDiv.innerHTML = '<p>Something went wrong. Please try again.</p>';
    console.error('Search error:', error);
  }
}

function renderResults(results) {
  if (results.length === 0) {
    resultsDiv.innerHTML = '<p>No results found.</p>';
    return;
  }

  resultsDiv.innerHTML = '';

  results.forEach(result => {
    const card = document.createElement('div');
    card.className = 'result-card';

    const titleEl = document.createElement(result.url ? 'a' : 'span');
    titleEl.textContent = result.title;
    if (result.url) {
      titleEl.href = result.url;
      titleEl.target = '_blank';
    }

    const sourceEl = document.createElement('p');
    sourceEl.className = 'result-source';
    sourceEl.textContent = `Source: ${result.source}`;

    card.appendChild(titleEl);
    card.appendChild(sourceEl);
    resultsDiv.appendChild(card);
  });
}

searchButton.addEventListener('click', runSearch);
searchInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') runSearch();
});
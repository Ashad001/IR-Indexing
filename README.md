# Information Retreival Using Vector Space Model

This Flask app facilitates Information Retrieval using various indexing techniques and incorporates a React frontend for enhanced user interaction. Additionally, documents are ranked using the Vector Space Model based on TF-IDF (Term Frequency-Inverse Document Frequency). The project structure is outlined below, providing an overview of the organization and key components.

## Project Structure

```plaintext
indexer/
│
├── api/
│   ├── data/
│   │   ├── ResearchPapers/
│   │   │   ├── (Research papers files)
│   │   └── Stopword-List.txt
│   ├── docs/
│   ├── logs/
│   ├── src/
│   │   ├── indexer/
│   │   ├── indexes/
│   │   ├── models/
│   │   ├── processing/
│   │   ├── vocab/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── retreival.py
│   │   └── utils.py
│   ├── .flaskenv
│   ├── app.py
│   ├── README.md
│   └── requirements.txt
│
├── node_modules/
├── public/
├── src/
│   ├── App.css
│   ├── App.js
│   ├── App.test.js
│   ├── index.css
│   ├── index.js
│   ├── logo.svg
│   ├── reportWebVitals.js
│   └── setupTests.js
│
├── .gitignore
├── package-lock.json
├── package.json
└── README.md

```

## Project Components

- **`data/`:** Contains research papers in the `ResearchPapers/` directory and a file `Stopword-List.txt` with common stop words.
  - Simply place new files in this folder, and the app will automatically index them.
  - Don't Remove `Stopword-List.txt` as it is used for stop word removal, though you can update the .txt file manually.

- **`flows/`:** Contains diagrams and drawings illustrating data flows and UI design.

- **`src/`:** Contains the source code for the app and various modules for indexing and retrieval.

- **`static/`:** Includes JavaScript (`script.js`) and CSS (`styles.css`) files for static content.

- **`templates/`:** Contains HTML template for rendering pages.
  
- **`tests/`:** Contains unit tests with corresponding test sets for various functionalities.
  
  - **`tests/test_sets:`** Add your test sets in the files
    - `golden_boolean_queries.txt`
    - `golden_proximity_queries.txt`
    - Enter Queries of the form:
      - Example Query: TOUR_QUERY 
      - Result-Set: EXPECTED_RESULTS

- **`app.py`:** The main Flask application file.

## Flow & Design
### Data Flow 
![Data Flow](flows/dataflow.png)

### UI design
![UI](flows/ui.png)


## Functionality

The app offers efficient retrieval capabilities, emphasizing performance and user experience.

### Index Generation and Metadata Logging

- Index generation occurs at the beginning and is only performed once, saving indexes to files.
- Metadata, including information about file structure and indexes, is logged for future reference.
- If indexes are requested again, the app checks  for changes in data and regenerates only the necessary indexes.

### Performance Logging

- Essential performance metrics are logged, providing insights into processing times for index formation, search operations, and more.
- This information helps in monitoring and optimizing the efficiency of the retrieval system.

### Query Processing

- The app prompts users to enter queries, whether boolean or proximity-based.
- The algorithm determines the query type and performs the search accordingly.
- Suggestions for words are provided to users, enhancing the query input experience.
- Trie-based searching is employed for efficient and fast word suggestions.

### Search Results Presentation

- Documents are ranked using the Vector Space Model based on TF-IDF scores.
- If documents match the user's query, the app presents the corresponding document IDs along with their relevance scores.
- In the absence of matching documents, the app attempts to correct the query using Levenshtein distance on a word-by-word basis.
- The corrected query is presented to the user, and if the original and corrected queries are identical, the user is informed that no documents match the query.
- Each document in the search result is accompanied by a static summary. Hovering over the document displays its rank/score.

### Logging User Interaction

- The app logs important information about user queries, errors, and search results.
- This logging allows for a comprehensive review of user interactions, aiding in system analysis and improvement.

The combined features ensure a seamless and efficient experience for users interacting with the IR-Indexing app, promoting effective information retrieval and user-friendly query processing.

## Running the Project

To run the project, follow these steps:

1. Set up a Python environment and install dependencies:

    ```bash
    cd api 
    python -m venv venv
    venv\Scripts\activate
    ```
    
    ```bash
    pip install -r requirements.txt
    ```

2. Run the Flask app:

    ```bash
    cd .. (to go back to the root directory)
    npm install
    yarn start-api
    ```

3. Open a web browser and navigate to `http://127.0.0.1:5000/` to interact with the app.

For the React frontend:

1. Start the React development server:

    ```bash
    yarn start
    ```

2. The React app will be running on `http://localhost:3000/` by default.



## Acknowledgements 
- The Porter Stemmer implementation is based on the original algorithm by Martin Porter.
  -  Source: [https://vijinimallawaarachchi.com/2017/05/09/porter-stemming-algorithm/](https://vijinimallawaarachchi.com/2017/05/09/porter-stemming-algorithm/)
  -   GitHub Repository: [https://github.com/jedijulia/porter-stemmer/blob/master/stemmer.py](https://github.com/jedijulia/porter-stemmer/)

- The Levenshtein distance algorithm is based on the original algorithm by Vladimir Levenshtein.
  - Source: [https://en.wikipedia.org/wiki/Levenshtein_distance](https://en.wikipedia.org/wiki/Levenshtein_distance)
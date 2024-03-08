from flask import Flask, render_template, request, jsonify
from src.processor import processor  # Make sure to import the necessary modules
from src.word_suggestor import WordSuggestor
from src.tokenizer import Tokenizer
from src.boolean_model import BooleanModel
from src.extended_boolean import ExtendedBooleanModel
import json
import re
import os
from typing import List, Dict
app = Flask(__name__)

class InformationRetrievalSystem:
    def __init__(self):
        self.title = "Information Retrieval System"
        self.description = "This is a simple information retrieval system that uses the extended boolean model to search for documents in a collection of research papers."
        self.dict_set = None
        self.inv_idx = None
        self.pos_idx = None
        all_docs = os.listdir('./data/ResearchPapers')
        processor(data_dir="./data/ResearchPapers/")
        self.load_data("./docs")
        
        self.suggestions_cache = {}
        self.word_suggestor = WordSuggestor(self.dict_set)
        self.tokenizer = Tokenizer()
        self.boolean_model = BooleanModel(self.inv_idx, all_docs=all_docs)
        self.extended_boolean_model = ExtendedBooleanModel(self.pos_idx, all_docs=all_docs)

    def load_data(self, docs_dir: str) -> None:
        with open(docs_dir + "/dict-set.json", 'r') as f:
            self.dict_set = json.load(f)
        with open(docs_dir + "/inv-index.json", 'r') as f:
            self.inv_idx = json.load(f)
        with open(docs_dir + "/pos-index.json", 'r') as f:
            self.pos_idx = json.load(f)
        

    def cache_suggestions(self, word, suggestions):
        self.suggestions_cache[word] = suggestions

    def get_cached_suggestions(self, word):
        return self.suggestions_cache.get(word, [])
    
    def search(self, query: str) -> List:
        query_type = self.query_type(query)
        if query_type == 'boolean':
            return self.boolean_search(query)
        elif query_type == 'proximity':
            return self.proximity_search(query)
        else:
            error = "Your Query Should Be of the Form\n WORD1 AND WORD2 OR WORD3 AND NOT WORD4\n OR\n WORD1 WORD2 /k"
            return [error]
    
    def boolean_search(self, query: str) -> List:
        return self.boolean_model.search(query)
    
    def proximity_search(self, query: str) -> List:
        return self.extended_boolean_model.search(query)
    
    
    def query_type(self, query: str) -> str:
        if re.search(r'AND|OR|NOT', query):
            return 'boolean'
        elif re.search(r'/(\d*)$', query):
            return 'proximity'
        
        

app_instance = InformationRetrievalSystem()

@app.route('/')
def index():
    return render_template('index.html', title=app_instance.title, description=app_instance.description)

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    data = request.get_json()
    query = data['query']
    print(query)
    if query:
        check_word = app_instance.tokenizer.tokenize(query)[-1]
        if check_word is not None and len(check_word) > 1:
            suggestions = app_instance.get_cached_suggestions(check_word)
            if not suggestions:
                suggestions = app_instance.word_suggestor.find_words(check_word)
                app_instance.cache_suggestions(check_word, suggestions)
            return jsonify({'suggestions': suggestions})

    return jsonify({'suggestions': []})

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data['query']
    docs: List[int] = app_instance.search(query)
    print(docs)
    return jsonify({'docs': docs})

if __name__ == '__main__':
    app.run(debug=True)

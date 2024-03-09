from typing import List
from flask import Flask, render_template, request, jsonify
from src.retreival import InformationRetrieval

app = Flask(__name__)

app_instance = InformationRetrieval()

@app.route('/')
def index():
    return render_template('index.html', title=app_instance.title, description=app_instance.description)

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    data = request.get_json()
    query = data['query']
    if query:
        check_word = app_instance.tokenizer.tokenize(query)[-1].lower()
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
    print(query)
    docs: List[int] = app_instance.search(query)
    return jsonify({'docs': docs})

@app.route('/get_corrections', methods = ['POST'])
def get_corrections():
    data = request.get_json()
    query = data['query']
    corrected_query = app_instance.word_corrector.correct_query(query)
    return jsonify({'corrected_query': corrected_query})

if __name__ == '__main__':
    app.run(debug=True)

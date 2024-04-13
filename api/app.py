from flask import Flask, request, jsonify
from src.retreival import InformationRetrieval

app = Flask(__name__)

app_instance = InformationRetrieval()

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    data = request.get_json()
    query = data['query']
    if query:
        check_word = app_instance.tokenizer.tokenize(query)[-1].lower()
        if check_word is not None and len(check_word) > 0:
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
    ranked_docs = app_instance.search(query)
    ranks = [doc[1] for doc in ranked_docs]
    docs = [doc[0] for doc in ranked_docs]
    summaries = [doc[2] for doc in ranked_docs]
    return jsonify({'docs': docs, 'ranks': ranks, 'summaries': summaries})

@app.route('/get_corrections', methods=['POST'])
def get_corrections():
    data = request.get_json()
    query = data['query']
    corrected_query = app_instance.word_corrector.correct_query(query)
    if corrected_query == query:
        return jsonify({"corrected_query": ""})
    return jsonify({'corrected_query': corrected_query})

# if __name__ == '__main__':
#     app.run(debug=True)


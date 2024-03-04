import re
import json
from typing import List, Dict, Tuple, Optional, Any, Set
# Assuming the below imports work as intended
from inverted_index import InvertedIndex
from porter_stemmer import PorterStemmer as Stemmer
from tokenizer import Tokenizer
from utils import get_logger, timing_decorator
from processor import processor

class BooleanModel:
    def __init__(self) -> None:
        processor('../data/ResearchPapers')
        self.inv_idx = None
        with open(f'test_inv-index.json', 'r') as f:
            self.inv_idx = json.load(f)
        self.stemmer = Stemmer()
        self.tokenizer = Tokenizer()
        self.logger = get_logger("boolean_model", see_time=True, console_log=True)
        self.error_logger = get_logger("boolean_model_error", see_time=True, console_log=True)
    
    @timing_decorator
    def process_query(self, query: str) -> List[str]:
        query = re.split(r'\s', query)
        words = [self.stemmer.stem(word.lower()) for word in query if word.upper() not in ['AND', 'OR', 'NOT']]
        postings = self.get_postings(words)
        
        
        

    def get_postings(self, words: List[str]):
        postings = []
        for word in words:
            if word in self.inv_idx:
                docs = list(self.inv_idx[word].keys())
                docs = [int(doc.split('_')[1]) for doc in docs]
                #! is it necessary to sort..?
                docs.sort()
                postings.append({word: docs})
            else:
                self.error_logger.error(f"Word '{word}' not found in inverted index")
        return postings

if __name__=="__main__":
    bm = BooleanModel()
    query = "heart AND heart"
    docs = bm.process_query(query)
    print(docs)

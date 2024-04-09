from src.processing.processor import IndexProcessor 
from src.processing.word_suggestor import WordSuggestor
from src.processing.word_corrector import WordCorrector
from src.processing.tokenizer import Tokenizer
from src.models.boolean_model import BooleanModel
from src.models.extended_boolean import ExtendedBooleanModel
from src.models.vector_space_model import VectorSpaceModel
from src.utils import list_files
import re
from typing import List

class InformationRetrieval:
    def __init__(self):
        self.title = "Information Retrieval System"
        self.description = "This is a simple information retrieval system that uses the boolean model to search for documents in a collection of research papers."
        self.dict_set = None
        self.inv_idx = None
        self.pos_idx = None
        self.processor = IndexProcessor(data_dir="./data", exclude_files=["Stopword-List.txt"])
        self.load_data()
        
        self.tokenizer = Tokenizer()
        self.suggestions_cache = {}
        self.word_suggestor = WordSuggestor(self.dict_set)
        self.word_corrector = WordCorrector(self.dict_set)
        
        all_docs = list_files('./data', exclude_files=["Stopword-List.txt"])
        self.boolean_model = BooleanModel(self.inv_idx, all_docs_files=all_docs)
        self.extended_boolean_model = ExtendedBooleanModel(self.pos_idx, all_docs_files=all_docs)
        self.vsm = VectorSpaceModel(self.inv_idx)
        

    def load_data(self) -> None:
        inv_idx, pos_idx, dict_set = self.processor.process_data()
        self.inv_idx = inv_idx.index
        self.pos_idx = pos_idx.index
        self.dict_set = dict_set    

    def cache_suggestions(self, word, suggestions):
        self.suggestions_cache[word] = suggestions

    def get_cached_suggestions(self, word):
        return self.suggestions_cache.get(word, [])
    
    def search(self, query: str) -> List:
        query = self.tokenizer.remove_stop_words(query)
        query_type = self.query_type(query)
        if query_type == 'boolean':
            return self.boolean_search(query)
        elif query_type == 'proximity':
            return self.proximity_search(query)
        else:
            return self.vector_search(query)
    
    def boolean_search(self, query: str) -> List:
        return self.boolean_model.search(query)
    
    def proximity_search(self, query: str) -> List:
        return self.extended_boolean_model.search(query)
    
    def vector_search(self, query: str) -> List:
        return self.vsm.search(query)

    
    def query_type(self, query: str) -> str:
        if len(query.split()) == 1 or re.search(r'AND|OR|NOT', query):
            return 'boolean'
        elif re.search(r'/(\d*)$', query):
            return 'proximity'
        return "invalid query"

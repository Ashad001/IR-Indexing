from src.processing.processor import IndexProcessor 
from src.processing.word_suggestor import WordSuggestor
from src.processing.word_corrector import WordCorrector
from src.processing.tokenizer import Tokenizer
from src.models.boolean_model import BooleanModel
from src.models.extended_boolean import ExtendedBooleanModel
from src.models.vector_space_model import VectorSpaceModel
from src.ml_workbench.knn_classifier import KNNClassifier
from src.utils import list_files, read_summary
import re
from typing import List, Tuple

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
        
        self.knn_classifier = KNNClassifier(data_dir="./data", index_file="./docs/inv-index.json", k=3, use_tts=True)

    def load_data(self) -> None:
        """
        Load the data from the data directory and process it using the IndexProcessor
        """
        inv_idx, pos_idx, dict_set = self.processor.process_data()
        self.inv_idx = inv_idx.index
        self.pos_idx = pos_idx.index
        self.dict_set = dict_set    
        
        with open('./logs/metadata.log', 'r') as f:
            self.metadata = f.read()

    def cache_suggestions(self, word, suggestions):
        self.suggestions_cache[word] = suggestions

    def get_cached_suggestions(self, word):
        return self.suggestions_cache.get(word, [])
    
    def search(self, query: str, alpha: float = 0.05) -> List:
        query = self.tokenizer.remove_stop_words(query)
        query_type = self.query_type(query)
        if query_type == 'boolean':
            return self.boolean_search(query)
        elif query_type == 'proximity':
            return self.proximity_search(query)
        elif query_type == 'ranked':
            return self.vector_search(query, alpha)
        else:
            return []
    
    def boolean_search(self, query: str) -> List:
        """
        search for documents using the boolean model

        Args:
            query (str): user query string


        Returns:
            List[Tuple[str, float, str]]: Returns a list of documents with their scores and summaries
        """
        docs =  self.boolean_model.search(query)
        summaries = [read_summary(self.metadata, doc) for doc in docs]        
        docs = [(doc_id, round(100.0, 2), summary) for doc_id, summary in zip(docs, summaries)]        
        return docs
    
    def proximity_search(self, query: str) -> List:
        """
        search for documents using the procimity search

        Args:
            query (str): user query string


        Returns:
            List[Tuple[str, float, str]]: Returns a list of documents with their scores and summaries
        """
        docs = self.extended_boolean_model.search(query)
        summaries = [read_summary(self.metadata, doc) for doc in docs]
        docs = [(doc_id, round(100.0, 2), summary) for doc_id, summary in zip(docs, summaries)]
        return docs
    
    def vector_search(self, query: str, alpha: float) -> List[Tuple[str, float, str]]:
        """
        search for documents using the vector space model

        Args:
            query (str): user query string
            alpha (float): the alpha parameter for the vector space model


        Returns:
            List[Tuple[str, float, str]]: Returns a list of documents with their scores and summaries
        """
        docs =  self.vsm.search(query)
        summaries = [read_summary(self.metadata, doc_id) for doc_id, _ in docs]
        docs = [(doc_id, round(score, 6), summary) for (doc_id, score), summary in zip(docs, summaries) if score > alpha]
        return docs
    
    def query_type(self, query: str) -> str:
        if re.search(r'AND|OR|NOT', query):
            return 'boolean'
        elif re.search(r'/(\d*)$', query):
            return 'proximity'
        return "ranked"
    
    def get_class(self, query: str) -> str:
        return self.knn_classifier.predict(query)
    
    def get_relevant_docs(self, predicted_class: str) -> List[str]:
        return self.knn_classifier.get_relevant_class(predicted_class)
    
    def evaluate(self) -> dict:
        return self.knn_classifier.evaluate()
    
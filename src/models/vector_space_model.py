import json
import math
import os
import re
import logging
from typing import Dict, List, Tuple
from src.processing.tokenizer import Tokenizer
from src.processing.porter_stemmer import PorterStemmer
from src.logger import get_logger, log_message, CONSOLE_LOGS
from src.utils import timing_decorator
from src.processing.processor import IndexProcessor

class VectorSpaceModel:
    def __init__(self, inverted_index: Dict[str, Dict[str, int]]):
        """
        Initialize the VectorSpaceModel with the inverted index.

        Args:
            inverted_index (dict): A dictionary representing the inverted index.
            load_from_files (bool): Whether to load pre-computed TF-IDF data from files if available.
        """
        
        self.stemmer = PorterStemmer()
        self.logger = get_logger("vector_model", see_time=True, console_log=False)
        
        self.inverted_index = inverted_index
        self.documents = self._parse_inverted_index()
        self.document_ids = list(self.documents.keys())
        self.document_term_matrix, self.tfidf_matrix, self.normalized_tfidf_matrix = self.load_saved_matrices()
        self.save_to_files()
        
        
            
    def _parse_inverted_index(self) -> Dict[str, Dict[str, int]]:
        """
        Parse the inverted index into a usable format.

        Returns:
            dict: A dictionary containing documents and their respective term frequencies.
        """
        documents = {}
        for category, index in self.inverted_index.items():
            for doc_id, tf in index.items():
                doc_id_parts = doc_id.split('_')
                doc = doc_id_parts[1]
                if doc not in documents:
                    documents[doc] = {}
                documents[doc][category] = tf
        return documents

    def load_saved_matrices(self):
        """
        Load pre-computed matrices from files if available.

        Returns:
            Tuple: Document-Term Matrix, TF-IDF Matrix, Normalized TF-IDF Matrix.
        """
        if os.path.exists('./docs/document_term_matrix.json') and os.path.exists('./docs/tfidf_matrix.json') and os.path.exists('./docs/normalized_tfidf_matrix.json'):
            with open('./docs/document_term_matrix.json', 'r') as f:
                document_term_matrix = json.load(f)
            with open('./docs/tfidf_matrix.json', 'r') as f:
                tfidf_matrix = json.load(f)
            with open('./docs/normalized_tfidf_matrix.json', 'r') as f:
                normalized_tfidf_matrix = json.load(f)
            return document_term_matrix, tfidf_matrix, normalized_tfidf_matrix
        else:
            log_message('Could not load pre-computed matrices from files.', logger=self.logger, level=logging.WARNING)
            return self.generate_vector_space_model()

    def create_document_term_matrix(self) -> List[List[int]]:
        """
        Create a Document-Term Matrix.

        Returns:
            list: A matrix where rows represent documents and columns represent terms.
        """
        matrix = []
        for doc in self.document_ids:
            row = [0] * len(self.inverted_index)
            for i, term in enumerate(self.inverted_index):
                if term in self.documents[doc]:
                    row[i] = self.documents[doc][term]
            matrix.append(row)
        return matrix

    @timing_decorator
    def calculate_tf_idf(self, matrix: List[List[int]]) -> List[List[float]]:
        """
        Calculate TF-IDF Weights.

        Args:
            matrix (list): Document-Term Matrix.

        Returns:
            list: TF-IDF Matrix.
        """
        n_docs = len(matrix)
        n_terms = len(matrix[0])

        # Calculate IDF
        idf = [0] * n_terms
        for j in range(n_terms):
            df = sum(1 for i in range(n_docs) if matrix[i][j] > 0)
            idf[j] = math.log(n_docs / (df + 1))

        # Calculate TF-IDF
        tfidf_matrix = []
        for i in range(n_docs):
            tfidf_row = []
            for j in range(n_terms):
                tfidf_row.append(matrix[i][j] * idf[j])
            tfidf_matrix.append(tfidf_row)
        return tfidf_matrix

    @timing_decorator
    def normalize_vectors(self, matrix: List[List[float]]) -> List[List[float]]:
        """
        Normalize Vectors to unit length.

        Args:
            matrix (list): Matrix to be normalized.

        Returns:
            list: Normalized matrix.
        """
        normalized_matrix = []
        for row in matrix:
            norm = math.sqrt(sum(x ** 2 for x in row))
            normalized_row = [x / norm for x in row]
            normalized_matrix.append(normalized_row)
        return normalized_matrix

    @timing_decorator
    def generate_vector_space_model(self) -> Tuple[List[List[int]], List[List[float]], List[List[float]]]:
        """
        Generate Vector Space Model.

        Returns:
            tuple: A tuple containing Document-Term Matrix, TF-IDF Matrix, and Normalized TF-IDF Matrix.
        """
        # Step 2
        matrix = self.create_document_term_matrix()

        # Step 3
        tfidf_matrix = self.calculate_tf_idf(matrix)

        # Step 4
        normalized_matrix = self.normalize_vectors(tfidf_matrix)

        return matrix, tfidf_matrix, normalized_matrix

    def save_to_files(self):
        with open('./docs/document_term_matrix.json', 'w') as f:
            json.dump(self.document_term_matrix, f)
        with open('./docs/tfidf_matrix.json', 'w') as f:
            json.dump(self.tfidf_matrix, f)
        with open('./docs/normalized_matrix.json', 'w') as f:
            json.dump(self.normalized_tfidf_matrix, f)
            
        pass

    @timing_decorator
    def cosine_similarity(self, doc_id1: str, doc_id2: str) -> float:
        """
        Compute cosine similarity between two documents.

        Args:
            doc_id1 (str): Identifier of the first document.
            doc_id2 (str): Identifier of the second document.

        Returns:
            float: Cosine similarity between the two documents.
        """
        index1 = self.document_ids.index(doc_id1)
        index2 = self.document_ids.index(doc_id2)
        vector1 = self.normalized_tfidf_matrix[index1]
        vector2 = self.normalized_tfidf_matrix[index2]
        dot_product = sum(x * y for x, y in zip(vector1, vector2))
        magnitude1 = math.sqrt(sum(x ** 2 for x in vector1))
        magnitude2 = math.sqrt(sum(y ** 2 for y in vector2))
        return dot_product / (magnitude1 * magnitude2)

    def get_document_vector(self, doc_id: str) -> List[float]:
        """
        Get the vector representation of a document.

        Args:
            doc_id (str): Document identifier.

        Returns:
            list: Vector representation of the document.
        """
        index = self.document_ids.index(doc_id)
        return self.normalized_tfidf_matrix[index]
    
    @timing_decorator
    def generate_query_vector(self, query: str) -> List[float]:
        """
        Generate a query vector for a given query.

        Args:
            query (str): Query string.

        Returns:
            list: Query vector.
        """
        tokens = Tokenizer().tokenize(query)
        
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        
        query_vector = [0] * len(self.inverted_index)
        for term in stemmed_tokens:
            if term in self.inverted_index:
                index = list(self.inverted_index.keys()).index(term)
                query_vector[index] += 1
        return query_vector
    
    @timing_decorator
    def rank_documents(self, query: str) -> List[Tuple[str, float]]:
        """
        Rank documents based on the query.

        Args:
            query (str): Query string.

        Returns:
            list: List of document IDs and their respective cosine similarity scores.
        """
        query_vector = self.generate_query_vector(query)
        query_vector = [x / len(query.split()) for x in query_vector]
        query_magnitude = math.sqrt(sum(x ** 2 for x in query_vector))
        normalized_query_vector = [x / query_magnitude for x in query_vector]

        scores = []
        for doc_id in self.document_ids:
            doc_vector = self.get_document_vector(doc_id)
            score = sum(x * y for x, y in zip(normalized_query_vector, doc_vector))
            scores.append((doc_id, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)

    def search(self, query: str) -> List[str]:
        """
        Search for documents based on the query.

        Args:
            query (str): Query string.

        Returns:
            list: List of document IDs.
        """
        ranks = self.rank_documents(query)
        print(ranks)
        return [doc_id for doc_id, score in ranks if score > 0.005 ]

if __name__ == "__main__":
    iv = IndexProcessor(data_dir='./data')
    iv.process_data()

    with open('./docs/inv-index.json', 'r') as f:
        inverted_index = json.load(f)

    vsm = VectorSpaceModel(inverted_index)

    ex_1 = '1'
    ex_2 = '2'
    # Example of computing cosine similarity
    similarity = vsm.cosine_similarity(ex_1, ex_2)
    print(f"Cosine Similarity between Document {ex_1} and Document {ex_2}:", similarity)

    ranks = vsm.rank_documents("machin learn")
    
    for doc_id, score in ranks:
        print(f"Document {doc_id}: {score}")

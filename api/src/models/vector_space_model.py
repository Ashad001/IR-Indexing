import json
import math
import os
import re
import logging
import numpy as np
from typing import Dict, List, Tuple
from src.processing.tokenizer import Tokenizer
from src.processing.porter_stemmer import PorterStemmer
from src.logger import get_logger, log_message, CONSOLE_LOGS
from src.utils import time_logger

class VectorSpaceModel:
    def __init__(self, inverted_index: Dict[str, Dict[str, int]], alpha: float = 0.025):
        """
        Initialize the VectorSpaceModel with the inverted index.

        Args:
            inverted_index (dict): A dictionary representing the inverted index.
            load_from_files (bool): Whether to load pre-computed TF-IDF data from files if available.
        """
        self.stemmer = PorterStemmer()
        self.logger = get_logger("vector_model", see_time=True, console_log=False)
        self.alpha = alpha
        
        self.inverted_index = inverted_index
        self.inverted_index = self.sort_index(self.inverted_index)
        self.documents = self._parse_inverted_index()
        self.document_ids = list(self.documents.keys())
        self.document_term_matrix, self.tfidf_matrix, self.normalized_tfidf_matrix = self.load_saved_matrices()
        self.save_to_files()
        
    def sort_index(self, index):
        return {k: v for k, v in sorted(index.items(), key=lambda item: item[0], reverse=False)}
            
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
        with open("./docs/documents.json", "w") as f:
            json.dump(documents, f, indent=4)
        return documents

    def load_saved_matrices(self):
        """
        Load pre-computed matrices from files if available.

        Returns:
            Tuple: Document-Term Matrix, TF-IDF Matrix, Normalized TF-IDF Matrix.
        """
        if os.path.exists('./docs/document_term_matrix.npy') and os.path.exists('./docs/tfidf_matrix.npy') and os.path.exists('./docs/normalized_tfidf_matrix.npy'):
            document_term_matrix = np.load('./docs/document_term_matrix.npy')
            tfidf_matrix = np.load('./docs/tfidf_matrix.npy')
            normalized_tfidf_matrix = np.load('./docs/normalized_tfidf_matrix.npy')
            return document_term_matrix, tfidf_matrix, normalized_tfidf_matrix
        else:
            log_message('Could not load pre-computed matrices from files.', logger=self.logger, level=logging.WARNING)
            return self.generate_vector_space_model()

    def create_document_term_matrix(self) -> np.ndarray:
        """
        Create a Document-Term Matrix.

        Returns:
            np.ndarray: A matrix where rows represent documents and columns represent terms.
        """
        matrix = np.zeros((len(self.document_ids), len(self.inverted_index)), dtype=int)
        for i, doc in enumerate(self.document_ids):
            for j, term in enumerate(self.inverted_index):
                if term in self.documents[doc]:
                    matrix[i, j] = self.documents[doc][term]
        return matrix

    @time_logger
    def calculate_tf_idf(self, matrix: np.ndarray) -> np.ndarray:
        """
        Calculate TF-IDF Weights.

        Args:
            matrix (np.ndarray): Document-Term Matrix.

        Returns:
            np.ndarray: TF-IDF Matrix.
        """
        n_docs = matrix.shape[0]
        n_terms = matrix.shape[1]
        
        # Calculate DF & IDF
        df = np.sum(matrix > 0, axis=0)
        idf = np.where(df > 0, np.log10(n_docs / df), 0)

        # Calculate TF-IDF
        tfidf_matrix = matrix * idf
        return tfidf_matrix

    @time_logger
    def normalize_vectors(self, matrix: np.ndarray) -> np.ndarray:
        """
        Normalize Vectors to unit length.

        Args:
            matrix (np.ndarray): Matrix to be normalized.

        Returns:
            np.ndarray: Normalized matrix.
        """
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        return matrix / norms

    @time_logger
    def generate_vector_space_model(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
        np.save('./docs/document_term_matrix.npy', self.document_term_matrix)
        np.save('./docs/tfidf_matrix.npy', self.tfidf_matrix)
        np.save('./docs/normalized_tfidf_matrix.npy', self.normalized_tfidf_matrix)
            

    def get_document_vector(self, doc_id: str) -> np.ndarray:
        """
        Get the vector representation of a document.

        Args:
            doc_id (str): Document identifier.

        Returns:
            np.ndarray: Vector representation of the document.
        """
        index = self.document_ids.index(doc_id)
        return self.normalized_tfidf_matrix[index]
    
    @time_logger
    def generate_query_vector(self, query: str) -> np.ndarray:
        """
        Generate a query vector for a given query.

        Args:
            query (str): Query string.

        Returns:
            np.ndarray: Query vector.
        """
        tokens = Tokenizer().tokenize(query)
        # sort tokens 
        tokens = sorted(tokens, key=lambda x: x)
        
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        
        query_vector = np.zeros(len(self.inverted_index))
        for term in stemmed_tokens:
            if term in self.inverted_index:
                index = list(self.inverted_index.keys()).index(term)
                query_vector[index] += 1
            else:
                log_message(f"Term '{term}' not found in the inverted index.", logger=self.logger, level=logging.WARNING)
                return None
        return query_vector
    
    def generate_normalized_query_vector(self, query: str) -> np.ndarray:
        """
        Generate a query vector for a given query.

        Args:
            query (str): Query string.

        Returns:
            np.ndarray: Query vector.
        """
        query_vector = self.generate_query_vector(query)
        if query_vector is None:
            return None
        query_vector = query_vector / np.linalg.norm(query_vector)
        return query_vector
    
    @time_logger
    def rank_documents(self, query: str) -> List[Tuple[str, float]]:
        """
        Rank documents based on the query.

        Args:
            query (str): Query string.

        Returns:
            list: List of document IDs and their respective cosine similarity scores.
        """
        normalized_query_vector = self.generate_normalized_query_vector(query)
        scores = []
        for doc_id in self.document_ids:
            doc_vector = self.get_document_vector(doc_id)
            score = np.dot(normalized_query_vector, doc_vector)
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
        if ranks is None:
            return []

        return ranks

# if __name__ == "__main__":
    # iv = IndexProcessor(data_dir='./data')
    # iv.process_data()

    # with open('./docs/inv-index.json', 'r') as f:
    #     inverted_index = json.load(f)

    # vsm = VectorSpaceModel(inverted_index)

#     ex_1 = '1'
#     ex_2 = '2'
#     # Example of computing cosine similarity
#     similarity = vsm.cosine_similarity(ex_1, ex_2)
#     print(f"Cosine Similarity between Document {ex_1} and Document {ex_2}:", similarity)

#     ranks = vsm.rank_documents("machine learn")
#     for doc_id, score in ranks:
#         print(f"Document {doc_id}: {score}")

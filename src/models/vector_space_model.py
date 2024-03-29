import json
import math
from typing import Dict, List, Tuple
import os
# append path on sys
# import sys
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '../..'))

# Append the parent directory to sys.path
sys.path.append(parent_dir)

from src.processing.processor import IndexProcessor

class VectorSpaceModel:
    def __init__(self, inverted_index: Dict[str, Dict[str, int]]):
        """
        Initialize the VectorSpaceModel with the inverted index.

        Args:
            inverted_index (dict): A dictionary representing the inverted index.
        """
        self.inverted_index = inverted_index
        self.documents = self._parse_inverted_index()
        self.document_ids = list(self.documents.keys())
        print(self.document_ids)
        
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

    def cosine_similarity(self, doc_id1: str, doc_id2: str, normalized_tfidf_matrix: List[List[float]]) -> float:
        """
        Compute cosine similarity between two documents.

        Args:
            doc_id1 (str): Identifier of the first document.
            doc_id2 (str): Identifier of the second document.
            normalized_tfidf_matrix (list): Normalized TF-IDF matrix.

        Returns:
            float: Cosine similarity between the two documents.
        """
        index1 = self.document_ids.index(doc_id1)
        index2 = self.document_ids.index(doc_id2)
        vector1 = normalized_tfidf_matrix[index1]
        vector2 = normalized_tfidf_matrix[index2]
        dot_product = sum(x * y for x, y in zip(vector1, vector2))
        magnitude1 = math.sqrt(sum(x ** 2 for x in vector1))
        magnitude2 = math.sqrt(sum(y ** 2 for y in vector2))
        return dot_product / (magnitude1 * magnitude2)

if __name__ == "__main__":
    
    iv = IndexProcessor(data_dir='./data')
    iv.process_data()
    
    with open('./docs/inv-index.json', 'r') as f:
        inverted_index = json.load(f)
    
    vsm = VectorSpaceModel(inverted_index)

    document_term_matrix, tfidf_matrix, normalized_tfidf_matrix = vsm.generate_vector_space_model()

    with open('document_term_matrix.json', 'w') as f:
        json.dump(document_term_matrix, f, indent=4)
        
    with open('tfidf_matrix.json', 'w') as f:
        json.dump(tfidf_matrix, f, indent=4)
        
    with open('normalized_tfidf_matrix.json', 'w') as f:
        json.dump(normalized_tfidf_matrix, f, indent=4)

    print(vsm.document_ids)
    ex_1 = '1'
    ex_2 = '2'
    # Example of computing cosine similarity
    similarity = vsm.cosine_similarity(ex_1, ex_2, normalized_tfidf_matrix)
    print(f"Cosine Similarity between Document {ex_1} and Document {ex_2}:", similarity)

import math 
import json
from typing import List, Dict

class CosineSimilarity:
    def __init__(self, normalized_tfidf_matrix: List[List[float]]):
        self.normalized_tfidf_matrix = normalized_tfidf_matrix
        self.document_ids = ['1', '12', '15', '16', '17', '2', '22', '7', '13', '14', '21', '3', '26', '9', '8', '23', '25', '100', '101', '11', '24', '18', '99']

    def cosine_similarity(self, doc_id1: str, doc_id2: str) -> float:
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
    
    
if __name__=="__main__":
    with open('normalized_tfidf_matrix.json', 'r') as f:
        normalized_tfidf_matrix = json.load(f)
        
    cs = CosineSimilarity(normalized_tfidf_matrix)
    
    ex_1 = '1'
    ex_2 = '25'
    # Example of computing cosine similarity
    similarity = cs.cosine_similarity(ex_1, ex_2)
    print(f"Cosine Similarity between Document {ex_1} and Document {ex_2}:", similarity)

    
    
    
import json
import numpy as np
from typing import List

from src.models.vector_space_model import VectorSpaceModel
from src.processing.processor import IndexProcessor

from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

class KNNClassifier:
    def __init__(self, data_dir: str, index_file: str, k: int = 3):
        self.class_mapping = {
            "1": "Explainable Artificial Intelligence",
            "2": "Explainable Artificial Intelligence",
            "3": "Explainable Artificial Intelligence",
            "7": "Explainable Artificial Intelligence",
            "8": "Heart Failure",
            "9": "Heart Failure",
            "11": "Heart Failure",
            "12": "Time Series Forecasting",
            "13": "Time Series Forecasting",
            "14": "Time Series Forecasting",
            "15": "Time Series Forecasting",
            "16": "Time Series Forecasting",
            "17": "Transformer Model",
            "18": "Transformer Model",
            "21": "Transformer Model",
            "22": "Feature Selection",
            "23": "Feature Selection",
            "24": "Feature Selection",
            "25": "Feature Selection",
            "26": "Feature Selection",
        }

        self.vector_space_model = self._initialize_vector_space_model(data_dir, index_file)
        self.k = k
        self.classifier = self._train_classifier()

    def _initialize_vector_space_model(self, data_dir: str, index_file: str) -> VectorSpaceModel:
        iv = IndexProcessor(data_dir=data_dir)
        iv.process_data()

        with open(index_file, 'r') as f:
            inverted_index = json.load(f)

        vector_space_model = VectorSpaceModel(inverted_index)
        vector_space_model.load_saved_matrices()

        return vector_space_model

    def _train_classifier(self) -> KNeighborsClassifier:
        tfidf_matrix, document_class = self._prepare_data()
        classifier = KNeighborsClassifier(n_neighbors=self.k)
        classifier.fit(tfidf_matrix, document_class)
        return classifier

    def _prepare_data(self):
        """
        Prepares the data for training.

        Returns:
            tuple: Tuple containing TF-IDF matrix and document classes.
        """
        # self.tfidf_vectorizer = TfidfVectorizer()
        # documents = self.vector_space_model.documents
        # document_texts = [" ".join(doc.keys()) for doc in documents.values()]
        # tfidf_matrix = self.tfidf_vectorizer.fit_transform(document_texts)
        # doc_ids = documents.keys()
        # document_classes = [self.class_mapping.get(doc_id, "Unknown") for doc_id in doc_ids]
        tfidf_matrix = self.vector_space_model.normalized_tfidf_matrix
        document_classes = [self.class_mapping.get(doc_id, "Unknown") for doc_id in self.vector_space_model.document_ids]

        return tfidf_matrix, document_classes

    def predict(self, query: str) -> str:
        """
        Predicts the class label for a given query.

        Args:
            query (str): Input query.

        Returns:
            str: Predicted class label.
        """
        # query_vector = self.tfidf_vectorizer.transform([query])
        # predicted_class = self.classifier.predict(query_vector)[0]
        # return predicted_class  
        query_vector = self.vector_space_model.generate_normalized_query_vector(query)
        predicted_class = self.classifier.predict([query_vector])[0]
        return predicted_class
    
    def get_relevant_class(self, predicted_class: str) -> List:
        """
        Retrieves relevant document IDs for a predicted class label.

        Args:
            predicted_class (str): Predicted class label.

        Returns:
            List[str]: List of relevant document IDs.
        """
        docs = [key for key, value in self.class_mapping.items() if value == predicted_class]
        return docs

if __name__ == "__main__":
    knn_classifier = KNNClassifier(data_dir='./data', index_file='./docs/inv-index.json', k=5)

    query = """
    HEART FAILURE BURDEN
    Around a million people in England 
    are living with heart failure, and nearly 
    200 000 are newly diagnosed each year.4 
    Patients typically experience increasing 
    """
    predicted_class = knn_classifier.predict(query)
    print("Predicted Class:", predicted_class)
    docs = knn_classifier.get_relevant_class(predicted_class)
    print("Relevant Documents:", docs)

import json
import numpy as np
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
        self.tfidf_vectorizer = TfidfVectorizer()
        documents = self.vector_space_model.documents
        document_texts = [" ".join(doc.keys()) for doc in documents.values()]
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(document_texts)
        doc_ids = documents.keys()
        document_classes = [self.class_mapping.get(doc_id, "Unknown") for doc_id in doc_ids]

        return tfidf_matrix, document_classes

    def predict(self, query: str) -> str:
        query_vector = self.tfidf_vectorizer.transform([query])
        predicted_class = self.classifier.predict(query_vector)[0]
        return predicted_class  
    
    def get_relevant_class(self, predicted_class: str) -> list:
        docs = [key for key, value in self.class_mapping.items() if value == predicted_class]
        return docs

if __name__ == "__main__":
    knn_classifier = KNNClassifier(data_dir='./data', index_file='./docs/inv-index.json', k=5)

    query = """
    FEATURE selection has been an active research area in
    machine learning and data m ining for decades. It is an
    important and frequently used technique for data dimensionreduction by removing irrelevant and redundant information
    from a data set. It is also a knowledge discovery tool for
    providing insights on the problem through interpretations of
    the most relevant features [1]. Discussions on feature selec-
    tion usually center on two technical aspects: search strategyand evaluation criteria. Algorithms designed with different
    strategies broadly fall into three categories: ?lter, wrapper,
    """
    predicted_class = knn_classifier.predict(query)
    print("Predicted Class:", predicted_class)
    docs = knn_classifier.get_relevant_class(predicted_class)
    print("Relevant Documents:", docs)

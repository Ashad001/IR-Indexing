from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from src.models.vector_space_model import VectorSpaceModel, IndexProcessor
import json

class KNNClassifier:

    def __init__(self, data_dir: str, index_file: str, k: int = 3):
        
        self.class_mapping = {

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
            "1": "Explainable Artificial Intelligence",
            "2": "Explainable Artificial Intelligence",
            "3": "Explainable Artificial Intelligence",
            "7": "Explainable Artificial Intelligence",
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
        tfidf_matrix = self.vector_space_model.tfidf_matrix
        document_classes = []

        for doc_id in self.vector_space_model.document_ids:
            class_label = self.class_mapping.get(doc_id, "Unknown")
            document_classes.append(class_label)

        return tfidf_matrix, document_classes



    def predict(self, query: str) -> str:
        query_vector = self.vector_space_model.generate_query_vector(query)
        if query_vector is None:
            return "Unknown"
        normalized_query_vector = query_vector / np.linalg.norm(query_vector)
        print(self.classifier.predict([normalized_query_vector]))
        return self.classifier.predict([normalized_query_vector])[0]
    
    def get_relevant_class(self, predicted_class: str) -> str:
        docs = []
        for key, value in self.class_mapping.items():
            if value == predicted_class:
                docs.append(key)
        return docs

if __name__ == "__main__":
    knn_classifier = KNNClassifier(data_dir='./data', index_file='./docs/inv-index.json', k=7)

    query = "heart disease detection"
    predicted_class = knn_classifier.predict(query)
    print("Predicted Class:", predicted_class)
    docs = knn_classifier.get_relevant_class(predicted_class)
    print("Relevant Documents:", docs)

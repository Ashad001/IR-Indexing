import json
import numpy as np
from typing import List
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from src.models.vector_space_model import VectorSpaceModel
from src.processing.processor import IndexProcessor

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
        tfidf_matrix, document_classes = self._prepare_data()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(tfidf_matrix, document_classes, test_size=0.1, random_state=42)
        classifier = KNeighborsClassifier(n_neighbors=self.k)
        classifier.fit(self.X_train, self.y_train)
        return classifier

    def _prepare_data(self):
        tfidf_matrix = self.vector_space_model.normalized_tfidf_matrix
        document_classes = [self.class_mapping.get(doc_id, "Unknown") for doc_id in self.vector_space_model.document_ids]
        return tfidf_matrix, document_classes

    def predict(self, query: str) -> str:
        query_vector = self.vector_space_model.generate_normalized_query_vector(query)
        if query_vector is None:
            return "Unknown"
        predicted_class = self.classifier.predict([query_vector])[0]
        return predicted_class

    def get_relevant_class(self, predicted_class: str) -> List[str]:
        docs = [key for key, value in self.class_mapping.items() if value == predicted_class]
        return docs

    def evaluate(self) -> dict:
        y_pred = self.classifier.predict(self.X_test)
        y_true = self.y_test
        accuracy = accuracy_score(y_true, y_pred)
        report = classification_report(y_true, y_pred, output_dict=True)
        return {
            'accuracy': accuracy,
            'precision': report['weighted avg']['precision'],
            'recall': report['weighted avg']['recall'],
            'f1_score': report['weighted avg']['f1-score']
        }

if __name__ == "__main__":
    knn_classifier = KNNClassifier(data_dir='./data', index_file='./docs/inv-index.json', k=5)

    evaluation_metrics = knn_classifier.evaluate()
    print("Evaluation Metrics:")
    print("Accuracy:", evaluation_metrics['accuracy'])
    print("Precision:", evaluation_metrics['precision'])
    print("Recall:", evaluation_metrics['recall'])
    print("F1 Score:", evaluation_metrics['f1_score'])

    query = """
    and deep neural networks, in their feedforward and
    recurrent versions, and tree-based methods, such as
    random forests and boosted trees. We also consider
    ensembleandhybridmodelsbycombiningingredients
    fromdifferentalternatives.Testsforsuperiorpredictive
    ability are briefly reviewed. Finally, we discuss appli-
    cationofMLineconomicsandfinanceandprovidean
    illustrationwithhigh-frequencyfinancialdata.
    """
    predicted_class = knn_classifier.predict(query)
    print("Predicted Class:", predicted_class)
    docs = knn_classifier.get_relevant_class(predicted_class)
    print("Relevant Documents:", docs)

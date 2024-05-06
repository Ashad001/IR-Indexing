import os
import json
import pickle
import numpy as np
from typing import List
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import classification_report, accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from src.models.vector_space_model import VectorSpaceModel
from src.processing.processor import IndexProcessor


class KNNClassifier:
    def __init__(
        self,
        data_dir: str,
        index_file: str,
        k: int = 3,
        model_file: str = "./docs/knn_classifier.pkl",
        use_tts: bool = True,
    ):
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

        self.vector_space_model = self._initialize_vector_space_model(
            data_dir, index_file
        )
        self.k = k
        self.model_file = model_file
        if model_file and os.path.exists(model_file):
            with open(model_file, "rb") as f:
                self.classifier = pickle.load(f)
        else:
            if use_tts:
                self.classifier = self._train_classifier_tts()
            else:
                self.classifier = self._train_classifier_sss()
            if model_file:
                self.save_model()  
                # also save evaluation results
                with open("./docs/knn_classifier_evaluation.json", "w") as f:
                    json.dump(self.evaluate(), f, indent=4)
            

    def _initialize_vector_space_model(
        self, data_dir: str, index_file: str
    ) -> VectorSpaceModel:
        iv = IndexProcessor(data_dir=data_dir)
        iv.process_data()

        with open(index_file, "r") as f:
            inverted_index = json.load(f)

        vector_space_model = VectorSpaceModel(inverted_index)
        vector_space_model.load_saved_matrices()

        return vector_space_model

    def _train_classifier_tts(self) -> KNeighborsClassifier:
        tfidf_matrix, document_classes = self._prepare_data()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            tfidf_matrix, document_classes, test_size=0.2, random_state=42
        )
        classifier = KNeighborsClassifier(n_neighbors=self.k)
        classifier.fit(self.X_train, self.y_train)
        return classifier

    def _train_classifier_sss(self) -> KNeighborsClassifier:
        X, y = self._prepare_data()
        sss = StratifiedShuffleSplit(n_splits=2, test_size=0.25, random_state=42)
        for train_index, test_index in sss.split(X, y):
            self.X_train, self.X_test = [X[i] for i in train_index], [
                X[i] for i in test_index
            ]
            self.y_train, self.y_test = [y[i] for i in train_index], [
                y[i] for i in test_index
            ]
        classifier = KNeighborsClassifier(n_neighbors=self.k)
        classifier.fit(self.X_train, self.y_train)
        return classifier

    def _prepare_data(self):
        tfidf_matrix = self.vector_space_model.normalized_tfidf_matrix
        document_classes = [
            self.class_mapping.get(doc_id, "Unknown")
            for doc_id in self.vector_space_model.document_ids
        ]
        return tfidf_matrix, document_classes

    def predict(self, query: str) -> str:
        query_vector = self.vector_space_model.generate_normalized_query_vector(query)
        if query_vector is None:
            return "Unknown"
        predicted_class = self.classifier.predict([query_vector])[0]
        return predicted_class

    def get_relevant_class(self, predicted_class: str) -> List[str]:
        docs = [
            key for key, value in self.class_mapping.items() if value == predicted_class
        ]
        return docs

    def evaluate(self) -> dict:
        y_pred = self.classifier.predict(self.X_test)
        y_true = self.y_test
        accuracy = accuracy_score(y_true, y_pred)
        report = classification_report(
            y_true, y_pred, output_dict=True, labels=np.unique(y_pred)
        )
        return {
            "accuracy": round(accuracy, 2),
            "precision": round(report["weighted avg"]["precision"], 2),
            "recall": round(report["weighted avg"]["recall"], 2),
            "f1_score": round(report["weighted avg"]["f1-score"], 2),
        }

    def save_model(self):
        with open(self.model_file, "wb") as f:
            pickle.dump(self.classifier, f)


if __name__ == "__main__":

    # model_file = None
    model_file = "./docs/knn_classifier.pkl"
    knn_classifier = KNNClassifier(
        data_dir="./data",
        index_file="./docs/inv-index.json",
        model_file=model_file,
        k=5,
    )

    evaluation_metrics = knn_classifier.evaluate()
    print("Evaluation Metrics:")
    print("Accuracy:", evaluation_metrics["accuracy"])
    print("Precision:", evaluation_metrics["precision"])
    print("Recall:", evaluation_metrics["recall"])
    print("F1 Score:", evaluation_metrics["f1_score"])

    query = """
    Transformers have achieved superior performances
    in many tasks in natural language processing and
    computer vision, which also triggered great inter-
    est in the time series community. Among multiple
    advantages of Transformers, the ability to capture
    long-range dependencies and interactions is espe-
    cially attractive for time series modeling, leading
    to exciting progress in various time series appli-
    cations. In this paper, we systematically review
    Transformer schemes for time series modeling by
    """
    predicted_class = knn_classifier.predict(query)
    print("Predicted Class:", predicted_class)
    docs = knn_classifier.get_relevant_class(predicted_class)
    print("Relevant Documents:", docs)

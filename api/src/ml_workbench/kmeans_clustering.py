import json
from src.models.vector_space_model import VectorSpaceModel
from src.processing.processor import IndexProcessor
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.cluster import KMeans


class KMeansTextClustering:
    def __init__(self, data_dir: str, index_file: str, k: int = 3, max_k: int = 10):
        self.vector_space_model = self._initialize_vector_space_model(
            data_dir, index_file
        )
        self.k = k
        self.max_k = max_k
        self.cluster_labels = None
        self.true_labels = [3, 2, 2, 2, 0, 1, 1, 1, 3, 2, 2, 0, 3, 0, 1, 4, 1, 3, 4, 4]

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

    def cluster_documents(self):
        kmeans = KMeans(n_clusters=self.k, random_state=42, n_init=50, max_iter=1000)
        self.cluster_labels = kmeans.fit_predict(
            self.vector_space_model.normalized_tfidf_matrix
        )
        print("Clustering complete.", self.cluster_labels)

    def evaluate_clustering(self):
        """
        Evaluate clustering results using purity, silhouette score, and random index.

        Returns:
            dict: Dictionary containing evaluation metrics (purity, silhouette score, random index).
        """
        true_labels = self.true_labels
        print(self.cluster_representation(true_labels))
        cluster_dict = defaultdict(list)
        for i, label in enumerate(self.cluster_labels):
            cluster_dict[label].append(true_labels[i])

        majority_labels = []
        for cluster in cluster_dict.values():
            majority_label = max(set(cluster), key=cluster.count)
            majority_labels.extend([majority_label] * len(cluster))

        purity = sum(
            majority_label == true_label
            for majority_label, true_label in zip(majority_labels, true_labels)
        ) / len(true_labels)

        silhouette = silhouette_score(
            self.vector_space_model.normalized_tfidf_matrix, self.cluster_labels
        )
        rand_index = adjusted_rand_score(true_labels, self.cluster_labels)

        return {
            "purity": purity,
            "silhouette_score": silhouette,
            "rand_index": rand_index,
        }

    def cluster_representation(self, labels=None):
        """
        Get the representation of the clusters.

        Returns:
            dict: Dictionary containing the cluster representation.
        """
        if labels is None:
            labels = self.cluster_labels
        cluster_dict = {}
        for i, label in enumerate(labels):
            if label not in cluster_dict:
                cluster_dict[label] = []
            cluster_dict[label].append(self.vector_space_model.document_ids[i])

        return cluster_dict

    def reduce_dimentions(self):
        """
        Reduce the dimensions of the vector space model using PCA.
        """
        pca = PCA(n_components=2)
        reduced_matrix = pca.fit_transform(
            self.vector_space_model.normalized_tfidf_matrix
        )
        return reduced_matrix

    def calculate_wcss(self):
        wcss = []
        for k in range(2, self.max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=50, max_iter=1000)
            kmeans.fit(self.vector_space_model.normalized_tfidf_matrix)
            wcss.append(kmeans.inertia_)
        return wcss

    def plot_elbow(self):
        wcss = self.calculate_wcss()
        plt.plot(range(2, self.max_k + 1), wcss)
        plt.title("Elbow Method")
        plt.xlabel("Number of clusters")
        plt.ylabel("WCSS")
        plt.show()

    def plot_clusters(self):
        """
        Plot the clusters.
        """
        reduced_matrix = self.reduce_dimentions()
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(
            reduced_matrix[:, 0],
            reduced_matrix[:, 1],
            c=self.cluster_labels,
            cmap="viridis",
        )
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 2")
        plt.title("KMeans Clustering")

        # Create legend entries for each document ID
        handles = []
        labels = []
        for cluster_label in range(self.k):
            indices = np.where(self.cluster_labels == cluster_label)[0]
            cluster_docs = [self.vector_space_model.document_ids[i] for i in indices]
            handles.append(scatter)
            labels.append(cluster_docs)

        plt.legend(handles, labels, loc="best", title="Document IDs", fontsize="small")
        plt.show()


if __name__ == "__main__":
    kmeans_clustering = KMeansTextClustering(
        data_dir="./data", index_file="./docs/inv-index.json", k=5
    )
    # kmeans_clustering.plot_elbow()
    # kmeans_clustering.plot_silhouette_scores()
    kmeans_clustering.cluster_documents()
    print(kmeans_clustering.cluster_representation())
    kmeans_clustering.plot_clusters()

    # # Evaluate clustering
    evaluation_metrics = kmeans_clustering.evaluate_clustering()
    print("Evaluation Metrics:")
    print("Purity:", evaluation_metrics["purity"])
    print("Silhouette Score:", evaluation_metrics["silhouette_score"])
    print("Random Index:", evaluation_metrics["rand_index"])

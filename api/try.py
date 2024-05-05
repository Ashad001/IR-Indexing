from sklearn.metrics import silhouette_score, adjusted_rand_score
import numpy as np

def evaluate_clustering(predicted_labels, true_labels):
    """
    Evaluate clustering results using purity, silhouette score, and adjusted rand index.

    Args:
        predicted_labels (dict): Dictionary containing cluster labels for each document.
        true_labels (dict): Dictionary containing true labels for each document.

    Returns:
        dict: Dictionary containing evaluation metrics (purity, silhouette score, adjusted rand index).
    """
    pred_labels_flat = flatten_labels(predicted_labels)
    true_labels_flat = flatten_labels(true_labels)

    # Calculate silhouette score
    silhouette = silhouette_score(true_labels_flat, pred_labels_flat)

    # Calculate adjusted rand index
    rand_index = adjusted_rand_score(true_labels_flat, pred_labels_flat)

    return {'silhouette_score': silhouette, 'rand_index': rand_index}

def flatten_labels(labels_dict):
    """
    Flatten dictionary of labels into a list of labels.

    Args:
        labels_dict (dict): Dictionary containing cluster labels for each document.

    Returns:
        list: Flattened list of labels.
    """
    flattened_labels = []
    for cluster_labels in labels_dict.values():
        flattened_labels.extend(cluster_labels)
    return flattened_labels

if __name__ == "__main__":
    predicted_labels = {
        3: ['1', '7', '2', '3'],
        2: ['12', '15', '16', '17', '18', '21'],
        1: ['22', '23', '24', '26', '25'],
        0: ['13', '14'],
        4: ['9', '8', '11']
    }

    true_labels = {
        3: ['1', '7', '2', '3'],
        2: ['12', '15', '16', '13', '14'],
        0: ['17', '18', '21'],
        1: ['22', '23', '24', '26', '25'],
        4: ['9', '8', '11']
    }

    evaluation_metrics = evaluate_clustering(predicted_labels, true_labels)
    print("Evaluation Metrics:")
    print("Silhouette Score:", evaluation_metrics['silhouette_score'])
    print("Adjusted Rand Index:", evaluation_metrics['rand_index'])

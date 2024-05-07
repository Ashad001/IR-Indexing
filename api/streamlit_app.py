import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.ml_workbench.knn_classifier import KNNClassifier
from src.ml_workbench.kmeans_clustering import KMeansClustering


def main():
    st.title("Machine Learning Workbench")
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose the app mode",
        ["Home", "KNN Classifier", "KMeans Clustering"]
    )

    if app_mode == "Home":
        st.write("Welcome to the Machine Learning Workbench For Information Retrieval System. This application provides a simple interface to interact with the different machine learning models. You can choose from the following options in the sidebar to get started.")
        st.write("1. KNN Classifier: This model classifies a given query into one of the classes based on the K-Nearest Neighbors algorithm.")
        st.write("2. KMeans Clustering: This model clusters the documents into different clusters based on the KMeans algorithm.")
        
        st.header("Credits")
        st.write("This application is developed by Ashad Abdullah")
        st.image("./icons/linkedin_icon.png", width=30)
        st.markdown("<a style='color: white;' href='https://www.linkedin.com/in/ashadqureshi1/'>LinkedIn</a>", unsafe_allow_html=True)
        st.image("./icons/github_icon.png", width=30)
        st.markdown("<a style='color: white;' href='https://github.com/Ashad001'>GitHub</a>", unsafe_allow_html=True)
        
    elif app_mode == "KNN Classifier":
        st.write("KNN Classifier")
        query, tts = st.columns(2)
        with query:
            user_query = st.text_area("Please enter a query to classify:", "machine learning", height=200)
        with tts:
            tts_option = st.checkbox("Stratified Shuffle Split")
            
        if tts_option:
            knn_classifier = KNNClassifier(data_dir="./data", index_file="./docs/inv-index.json", k=5, model_file=None, use_tts=True)
        else:
            knn_classifier = KNNClassifier(data_dir="./data", index_file="./docs/inv-index.json", k=5, model_file=None, use_tts=False)
        predicted_class = knn_classifier.predict(user_query)
        relevant_docs = knn_classifier.get_relevant_class(predicted_class)
        st.write(f"<h3>Predicted class: {predicted_class}</h4>", unsafe_allow_html=True)
        if relevant_docs:
            st.write(f"<h4>Relevant documents:</h4>", unsafe_allow_html=True)
            for doc in relevant_docs:
                st.write(f"Doc: {doc}")
        else:
            st.write("No relevant documents found.")
            
        with tts:
            evaluation = knn_classifier.evaluate()
            st.write("<h4 style='color: #FFFFFF;'>Evaluation Metrics:</h4>", unsafe_allow_html=True)
            st.write(f"<p style='margin: 5px 0;'><strong>Accuracy:</strong> {evaluation['accuracy']}</p>", unsafe_allow_html=True)
            st.write(f"<p style='margin: 5px 0;'><strong>Precision:</strong> {evaluation['precision']}</p>", unsafe_allow_html=True)
            st.write(f"<p style='margin: 5px 0;'><strong>Recall:</strong> {evaluation['recall']}</p>", unsafe_allow_html=True)
            st.write(f"<p style='margin: 5px 0;'><strong>F1 Score:</strong> {evaluation['f1_score']}</p>", unsafe_allow_html=True)
            st.write("</div>", unsafe_allow_html=True)
                

    elif app_mode == "KMeans Clustering":
        
        cl_box, eval_box = st.columns(2)
        
        with cl_box:
            n_clusters = st.number_input("Please Enter Nubmer of Clusters", min_value=2, max_value=10, value=3)
        kmeans_clustering = KMeansClustering(data_dir="./data", index_file="./docs/inv-index.json", k=n_clusters)
        kmeans_clustering.cluster_documents()
        clusters = kmeans_clustering.cluster_representation()
        clusters = dict(sorted(clusters.items()))
        print(clusters)
         
        st.subheader("Clusters:")
        
        cluster_ids = list(clusters.keys())
        num_clusters = len(cluster_ids)
        num_columns = 3
        num_rows = (num_clusters + num_columns - 1) // num_columns

        for i in range(num_rows):
            row_start = i * num_columns
            row_end = min(row_start + num_columns, num_clusters)
            columns = st.columns(num_columns)

            for j, cluster_id in enumerate(cluster_ids[row_start:row_end]):
                with columns[j]:
                    st.write(f"Cluster {cluster_id}:")
                    for doc in clusters[cluster_id]:
                        st.write(f"Doc: {doc}")

            st.write("---")
            
        st.subheader("Cluster Visualization")
        fig, ax = plt.subplots()
        ax.bar(cluster_ids, [len(clusters[cluster_id]) for cluster_id in cluster_ids])
        ax.set_xlabel("Cluster ID")
        ax.set_ylabel("Number of Documents")
        st.pyplot(fig)
        
        cluster_plt = kmeans_clustering.plot_clusters()
        st.pyplot(cluster_plt)
        
        with eval_box:
            st.write("<h4 style='color: #FFFFFF;'>Evaluation Metrics:</h4>", unsafe_allow_html=True)
            evaluation = kmeans_clustering.evaluate_clustering()
            st.write(f"<p style='margin: 5px 0;'><strong>Purity: </strong> {evaluation['purity']}</p>", unsafe_allow_html=True)
            st.write(f"<p style='margin: 5px 0;'><strong>Silhouette Score: </strong> {evaluation['silhouette_score']}</p>", unsafe_allow_html=True)
            st.write(f"<p style='margin: 5px 0;'><strong>Rand Score: </strong> {evaluation['rand_index']}</p>", unsafe_allow_html=True)
        
            
if __name__ == "__main__":
    main()    
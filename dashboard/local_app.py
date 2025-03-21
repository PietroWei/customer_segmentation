import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import plotly.express as px
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.cluster import DBSCAN, AgglomerativeClustering
import os

# Function to load the pre-trained model
def load_model(model_name):
    model_path = f"../scripts/models/{model_name}_model.pkl"  # Assuming models are stored in a "models" directory
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    else:
        st.error(f"Model {model_name} not found!")
        return None

# Load data from Excel
file_path = "../data/OnlineRetail.xlsx"
df = pd.read_excel(file_path)

# Preprocess data
df = df.dropna(subset=['CustomerID'])  # Remove missing customer IDs
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

# Calculate RFM metrics
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
rfm_df = df.groupby('CustomerID').agg(
    recency=('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
    frequency=('InvoiceNo', 'nunique'),
    monetary=('TotalAmount', 'sum')
).reset_index()

# Normalize RFM values
rfm_values = rfm_df[['recency', 'frequency', 'monetary']]
rfm_values = (rfm_values - rfm_values.mean()) / rfm_values.std()

# Streamlit App
st.set_page_config(layout="wide")
st.title("Customer Segmentation & Retention Analysis")
st.write("This dashboard shows customer segments using the RFM model.")

# Sidebar for selections
st.sidebar.title("Settings")
st.sidebar.write("Choose the clustering algorithm and view the results.")

# Select clustering algorithm
algorithm = st.sidebar.selectbox("Choose Clustering Algorithm", ["K-Means", "DBSCAN", "Agglomerative"])

# Load pre-trained model based on selection
if algorithm == "K-Means":
    model = load_model('kmeans')
    st.sidebar.write("**K-Means Clustering**: Partitions data into K clusters by minimizing the variance within each cluster.")
elif algorithm == "DBSCAN":
    model = load_model('dbscan')
    st.sidebar.write("**DBSCAN**: Density-based clustering that groups together points that are closely packed.")
elif algorithm == "Agglomerative":
    model = load_model('agglomerative')
    st.sidebar.write("**Agglomerative Clustering**: Hierarchical clustering that merges clusters iteratively.")

if model is not None:
    # Use the loaded model for predictions
    rfm_df['cluster'] = model.predict(rfm_values) if hasattr(model, 'predict') else model.fit_predict(rfm_values)

    # Display processed data
    st.write("### First Few Rows of Processed Data")
    st.dataframe(rfm_df.head())

    # Display Cluster Profile
    st.write("### Cluster Profile")
    cluster_profile = rfm_df.groupby('cluster')[['recency', 'frequency', 'monetary']].mean()
    st.dataframe(cluster_profile)

    # Interactive Cluster Filter
    cluster_filter = st.sidebar.selectbox("Select Cluster", options=rfm_df['cluster'].unique())
    filtered_data = rfm_df[rfm_df['cluster'] == cluster_filter]
    st.write(f"### Cluster {cluster_filter} Profile")
    st.dataframe(filtered_data)

    # 3D Scatter Plot
    fig = px.scatter_3d(rfm_df, x='recency', y='frequency', z='monetary', color='cluster', title="Customer Segments")
    st.plotly_chart(fig)

    # Histograms of RFM Variables
    st.write("### Distribution of RFM Variables")
    col1, col2, col3 = st.columns(3)
    with col1:
        fig_recency = px.histogram(rfm_df, x='recency', title="Recency Distribution")
        st.plotly_chart(fig_recency)
    with col2:
        fig_frequency = px.histogram(rfm_df, x='frequency', title="Frequency Distribution")
        st.plotly_chart(fig_frequency)
    with col3:
        fig_monetary = px.histogram(rfm_df, x='monetary', title="Monetary Distribution")
        st.plotly_chart(fig_monetary)

    # Correlation Heatmap
    st.write("### Correlation Heatmap of RFM Variables")
    corr_matrix = rfm_df[['recency', 'frequency', 'monetary']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    st.pyplot(plt)

    # Download Button for Processed Data
    st.write("### Download Segmented Data")
    csv = rfm_df.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name="segmented_customers.csv", mime="text/csv")

    # Predict Customer Segment
    st.write("### Predict Customer Segment Based on RFM Scores")
    recency_input = st.number_input("Recency (Days)", min_value=0)
    frequency_input = st.number_input("Frequency", min_value=1)
    monetary_input = st.number_input("Monetary Amount", min_value=0)

    # Compute Button to Trigger Prediction
    if st.button("Compute Segment"):
        input_data = np.array([[recency_input, frequency_input, monetary_input]])
        
        # Normalize input data
        input_data_normalized = (input_data - rfm_values.mean().values) / rfm_values.std().values
        
        # Predict using the loaded clustering model
        if hasattr(model, 'predict'):
            cluster_pred = model.predict(input_data_normalized)
        else:
            cluster_pred = model.fit_predict(input_data_normalized)
        
        st.write(f"Predicted Cluster: {cluster_pred[0]}")
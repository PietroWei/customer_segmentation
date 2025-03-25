import pandas as pd
import numpy as np
import os
import pickle
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering

# Streamlit App Setup (Must be the first command)
st.set_page_config(layout="wide", page_title="Customer Segmentation", page_icon="📊")

# Function to load the pre-trained model
def load_model(model_name):
    model_path = f"scripts/models/{model_name}_model.pkl"  # Model directory path
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    else:
        st.error(f"Model '{model_name}' not found! Please train and save the model.")
        return None

# Load dataset
st.sidebar.header("Dataset Information")
st.sidebar.write("The dataset used in this project comes from the **Online Retail Dataset** available at the UCI Machine Learning Repository. It contains transactional data from an online retail store, including customer purchases, invoice details, and timestamps.")
file_path = "data/OnlineRetail.xlsx"
df = pd.read_excel(file_path)

# Preprocess data
df = df.dropna(subset=['CustomerID'])  # Remove missing customer IDs
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

# Compute RFM metrics
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
rfm_df = df.groupby('CustomerID').agg(
    recency=('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
    frequency=('InvoiceNo', 'nunique'),
    monetary=('TotalAmount', 'sum')
).reset_index()

# Normalize RFM values
rfm_values = (rfm_df[['recency', 'frequency', 'monetary']] - rfm_df[['recency', 'frequency', 'monetary']].mean()) \
             / rfm_df[['recency', 'frequency', 'monetary']].std()

st.title("Customer Segmentation & Retention Analysis")
st.markdown("""
    This dashboard allows interactive exploration of customer segments using **RFM analysis**.
    Choose a clustering method to segment customers based on their purchasing behavior.

    **Dataset Summary:**
    - Transactions from an online retail store
    - Contains **invoices, customer IDs, quantity, unit price, and timestamps**
    - Helps analyze purchasing behavior and customer value
""")

# Sidebar Configuration
st.sidebar.header("Settings")
st.sidebar.write("Choose a clustering algorithm to visualize the customer segments.")
algorithm = st.sidebar.selectbox(
    "Select Clustering Algorithm",
    ["K-Means", "DBSCAN", "Agglomerative Clustering"],
    help="""Select a method to understand customer segmentation."""
)

# Dynamically update the description based on the selected algorithm
if algorithm == "K-Means":
    st.sidebar.markdown("""
    **K-Means**:
    - Partitions data into K clusters by minimizing variance within each cluster.
    - Best suited for well-separated and spherical data.
    """)
elif algorithm == "DBSCAN":
    st.sidebar.markdown("""
    **DBSCAN**:
    - A density-based clustering algorithm that groups closely packed points while marking outliers.
    - Ideal for discovering clusters of arbitrary shape and handling noise.
    """)
elif algorithm == "Agglomerative Clustering":
    st.sidebar.markdown("""
    **Agglomerative Clustering**:
    - A hierarchical clustering approach that iteratively merges data points into clusters.
    - Suitable for smaller datasets and exploring hierarchical relationships.
    """)

# Load selected clustering model
model_name = algorithm.lower().replace(" ", "_").replace("-", "")
model = load_model(model_name)

if model is None:
    st.stop()  # Stops execution if the model is not found

if model is not None:
    try:
        # Apply clustering
        rfm_df['cluster'] = model.predict(rfm_values) if hasattr(model, 'predict') else model.fit_predict(rfm_values)
        
        # Display processed data
        st.subheader("Clustered Data")
        st.dataframe(rfm_df.head())
        
        # Cluster Profile Analysis
        st.subheader("Cluster Profiles")
        st.markdown("Each cluster represents a group of customers with similar purchasing behavior, categorized based on Recency, Frequency, and Monetary values.")
        cluster_profile = rfm_df.groupby('cluster')[['recency', 'frequency', 'monetary']].mean()
        st.dataframe(cluster_profile)
        
        # Cluster Selection for Detailed Analysis
        cluster_filter = st.sidebar.selectbox("Select Cluster for Details", options=rfm_df['cluster'].unique())
        st.subheader(f"Cluster {cluster_filter} Details")
        st.dataframe(rfm_df[rfm_df['cluster'] == cluster_filter])
        
        # 3D Scatter Plot
        st.subheader("Customer Segmentation Visualization")
        st.write("The following 3D scatter plot visualizes customer groups based on RFM scores. Each point represents a customer, with colors indicating different clusters.")
        fig = px.scatter_3d(rfm_df, x='recency', y='frequency', z='monetary', color='cluster', title="Customer Segments")
        st.plotly_chart(fig)
        
        # RFM Distributions
        st.subheader("Distribution of RFM Metrics")
        st.write("Understanding the distribution of Recency, Frequency, and Monetary values helps in identifying customer behavior patterns.")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(px.histogram(rfm_df, x='recency', title="Recency Distribution"))
        with col2:
            st.plotly_chart(px.histogram(rfm_df, x='frequency', title="Frequency Distribution"))
        with col3:
            st.plotly_chart(px.histogram(rfm_df, x='monetary', title="Monetary Distribution"))
        
        # Correlation Heatmap
        st.subheader("RFM Correlation Heatmap")
        st.write("The heatmap below shows the correlation between Recency, Frequency, and Monetary values, giving insights into how these factors relate.")
        corr_matrix = rfm_df[['recency', 'frequency', 'monetary']].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        st.pyplot(plt)
        
        # Download Button for Segmented Data
        st.subheader("Download Segmented Data")
        st.write("Download the customer segmentation data for further analysis or reporting.")
        csv = rfm_df.to_csv(index=False)
        st.download_button("Download CSV", csv, "segmented_customers.csv", "text/csv")
        
        # Predict Customer Segment
        st.subheader("Predict Customer Segment Based on RFM Scores")
        st.write("Enter the RFM values for a new customer to predict their segment.")
        recency_input = st.number_input("Recency (Days)", min_value=0)
        frequency_input = st.number_input("Frequency", min_value=1)
        monetary_input = st.number_input("Monetary Amount", min_value=0)
        
        if st.button("Compute Segment"):
            input_data = np.array([[recency_input, frequency_input, monetary_input]])
            input_data_normalized = (input_data - rfm_values.mean().values) / rfm_values.std().values
            cluster_pred = model.predict(input_data_normalized) if hasattr(model, 'predict') else model.fit_predict(input_data_normalized)
            st.success(f"Predicted Cluster: {cluster_pred[0]}")
    except Exception as e:
        st.error(f"An error occurred while processing the clustering: {e}")

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
import pickle
import os

# Load data from Excel and preprocess
def load_and_preprocess_data(file_path):
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

    return rfm_df, rfm_values

# Train KMeans clustering model
def train_kmeans(rfm_values, n_clusters=4):
    model = KMeans(n_clusters=n_clusters, random_state=42)
    model.fit(rfm_values)
    return model

# Train DBSCAN clustering model
def train_dbscan(rfm_values):
    model = DBSCAN(eps=0.5, min_samples=5)
    model.fit(rfm_values)
    return model

# Train Agglomerative clustering model
def train_agglomerative(rfm_values, n_clusters=4):
    model = AgglomerativeClustering(n_clusters=n_clusters)
    model.fit(rfm_values)
    return model

# Save model to disk in 'models' folder
def save_model(model, filename):
    # Define the directory to store models
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')

    # Create the 'models' folder if it doesn't exist
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    # Define the full path for the model file
    model_path = os.path.join(model_dir, filename)

    # Save the model
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

# Main function to execute the training and saving process
def main():
    file_path = "data/OnlineRetail.xlsx"
    rfm_df, rfm_values = load_and_preprocess_data(file_path)
    
    # Train and save KMeans model
    kmeans_model = train_kmeans(rfm_values)
    save_model(kmeans_model, 'kmeans_model.pkl')
    print(f"KMeans model saved as models/kmeans_model.pkl")

    # Train and save DBSCAN model
    dbscan_model = train_dbscan(rfm_values)
    save_model(dbscan_model, 'dbscan_model.pkl')
    print(f"DBSCAN model saved as models/dbscan_model.pkl")

    # Train and save Agglomerative model
    agglomerative_model = train_agglomerative(rfm_values)
    save_model(agglomerative_model, 'agglomerative_model.pkl')
    print(f"Agglomerative model saved as models/agglomerative_model.pkl")

if __name__ == "__main__":
    main()

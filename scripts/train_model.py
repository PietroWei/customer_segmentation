# Import required libraries
import pandas as pd  # For data manipulation
import numpy as np  # For numerical computations
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering  # Clustering algorithms
import pickle  # To save and load model files
import os  # For file and directory operations

# Function to load data from an Excel file and preprocess it
def load_and_preprocess_data(file_path):
    # Read the dataset from the specified Excel file
    df = pd.read_excel(file_path)

    # Remove rows with missing CustomerID values
    df = df.dropna(subset=['CustomerID'])  # Clean the data by ensuring all rows have valid customer IDs

    # Convert 'InvoiceDate' to a datetime format for easier date manipulation
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Calculate the total amount spent per transaction (Quantity * Unit Price)
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

    # Calculate RFM metrics: Recency, Frequency, and Monetary
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)  # Define a reference point for 'recency'
    rfm_df = df.groupby('CustomerID').agg(
        recency=('InvoiceDate', lambda x: (snapshot_date - x.max()).days),  # Days since last purchase
        frequency=('InvoiceNo', 'nunique'),  # Count of unique invoices (purchases)
        monetary=('TotalAmount', 'sum')  # Total amount spent by each customer
    ).reset_index()

    # Extract the RFM metrics and normalize them using Z-score standardization
    rfm_values = rfm_df[['recency', 'frequency', 'monetary']]
    rfm_values = (rfm_values - rfm_values.mean()) / rfm_values.std()

    return rfm_df, rfm_values  # Return both the processed data and the normalized RFM values

# Function to train a KMeans clustering model
def train_kmeans(rfm_values, n_clusters=4):
    # Initialize the KMeans algorithm with the specified number of clusters
    model = KMeans(n_clusters=n_clusters, random_state=42)

    # Train the model on the normalized RFM values
    model.fit(rfm_values)

    return model  # Return the trained model

# Function to train a DBSCAN clustering model
def train_dbscan(rfm_values):
    # Initialize DBSCAN with default parameters (can be customized)
    model = DBSCAN(eps=0.5, min_samples=5)

    # Train the model on the normalized RFM values
    model.fit(rfm_values)

    return model  # Return the trained model

# Function to train an Agglomerative Clustering model
def train_agglomerative(rfm_values, n_clusters=4):
    # Initialize the Agglomerative Clustering algorithm
    model = AgglomerativeClustering(n_clusters=n_clusters)

    # Train the model on the normalized RFM values
    model.fit(rfm_values)

    return model  # Return the trained model

# Function to save a trained model to disk
def save_model(model, filename):
    # Determine the directory where models will be saved
    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')

    # Create the 'models' folder if it does not already exist
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    # Define the full path for the model file
    model_path = os.path.join(model_dir, filename)

    # Save the model to the specified file using pickle
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

# Main function to execute the data preprocessing, training, and saving process
def main():
    # Specify the path to the dataset (Excel file)
    file_path = "data/OnlineRetail.xlsx"

    # Load and preprocess the dataset, obtaining both the RFM dataframe and normalized RFM values
    rfm_df, rfm_values = load_and_preprocess_data(file_path)
    
    # Train and save the KMeans clustering model
    kmeans_model = train_kmeans(rfm_values)
    save_model(kmeans_model, 'kmeans_model.pkl')  # Save the model to the 'models' folder
    print(f"KMeans model saved as models/kmeans_model.pkl")

    # Train and save the DBSCAN clustering model
    dbscan_model = train_dbscan(rfm_values)
    save_model(dbscan_model, 'dbscan_model.pkl')  # Save the model to the 'models' folder
    print(f"DBSCAN model saved as models/dbscan_model.pkl")

    # Train and save the Agglomerative Clustering model
    agglomerative_model = train_agglomerative(rfm_values)
    save_model(agglomerative_model, 'agglomerative_model.pkl')  # Save the model to the 'models' folder
    print(f"Agglomerative model saved as models/agglomerative_model.pkl")

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()  # Call the main function to execute the workflow

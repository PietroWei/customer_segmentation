import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import psycopg2
from config.config import DB_SETTINGS

def compute_rfm():
    """
    Compute RFM metrics and perform clustering analysis.

    Returns:
    DataFrame: DataFrame containing RFM metrics and cluster labels.
    """
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname=DB_SETTINGS['dbname'],
        user=DB_SETTINGS['user'],
        password=DB_SETTINGS['password'],
        host=DB_SETTINGS['host'],
        port=DB_SETTINGS['port']
    )
    
    # Extract RFM data
    df_rfm = pd.read_sql_query("""
        SELECT customer_id, 
               EXTRACT(DAY FROM (NOW() - MAX(sale_date))) AS recency,
               COUNT(DISTINCT invoice_no) AS frequency,
               SUM(total_amount) AS monetary
        FROM sales 
        GROUP BY customer_id;
    """, conn)
    
    # Normalize RFM values
    rfm_values = df_rfm[['recency', 'frequency', 'monetary']]
    rfm_values = (rfm_values - rfm_values.mean()) / rfm_values.std()
    
    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=4, random_state=42)
    df_rfm['cluster'] = kmeans.fit_predict(rfm_values)
    
    # Close database connection
    conn.close()
    
    return df_rfm

# Example usage
if __name__ == "__main__":
    rfm_data = compute_rfm()
    print(rfm_data.head())

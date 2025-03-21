import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
from config.config import DB_SETTINGS

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
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4, random_state=42)
df_rfm['cluster'] = kmeans.fit_predict(rfm_values)

# Close database connection
conn.close()

# Create Streamlit dashboard
st.title("Customer Segmentation & Retention Analysis")
st.write("This dashboard shows customer segments using the RFM model.")
fig = px.scatter_3d(df_rfm, x='recency', y='frequency', z='monetary', color='cluster', title="Customer Segments")
st.plotly_chart(fig)
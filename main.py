# Step 1: Caricamento del Dataset Online Retail in PostgreSQL
# Useremo il dataset "Online Retail" di UCI Machine Learning

import pandas as pd
import psycopg2
from config.config import DB_SETTINGS

# Caricare il dataset
df = pd.read_excel("Online Retail.xlsx")

# Pulizia e conversione dati
df = df.dropna(subset=['CustomerID'])  # Rimuovere transazioni senza ID cliente
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Connessione al database
conn = psycopg2.connect(
    dbname=DB_SETTINGS['dbname'],
    user=DB_SETTINGS['user'],
    password=DB_SETTINGS['password'],
    host=DB_SETTINGS['host'],
    port=DB_SETTINGS['port']
)
cursor = conn.cursor()

# Creazione delle tabelle
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    country VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    invoice_no VARCHAR(255),
    sale_date TIMESTAMP,
    product VARCHAR(255),
    quantity INT,
    total_amount DECIMAL(10,2)
);
""")

# Inserimento dati
for index, row in df.iterrows():
    cursor.execute("INSERT INTO customers (customer_id, country) VALUES (%s, %s) ON CONFLICT DO NOTHING", 
                   (int(row['CustomerID']), row['Country']))
    cursor.execute("INSERT INTO sales (customer_id, invoice_no, sale_date, product, quantity, total_amount) VALUES (%s, %s, %s, %s, %s, %s)",
                   (int(row['CustomerID']), row['InvoiceNo'], row['InvoiceDate'], row['Description'], int(row['Quantity']), float(row['Quantity'] * row['UnitPrice'])))

conn.commit()
cursor.close()
conn.close()

# Step 2: Estrarre dati RFM con SQL
# Corrected the SQL query syntax
rfm_query = """
SELECT
    c.customer_id,
    NOW() - MAX(s.sale_date) AS recency,
    COUNT(DISTINCT s.invoice_no) AS frequency,
    SUM(s.total_amount) AS monetary
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
GROUP BY c.customer_id;
"""

# Step 3: Analisi RFM & Clustering in Python
import numpy as np
from sklearn.cluster import KMeans
import plotly.express as px
import streamlit as st

# Connessione al database e lettura dati RFM
conn = psycopg2.connect(
    dbname=DB_SETTINGS['dbname'],
    user=DB_SETTINGS['user'],
    password=DB_SETTINGS['password'],
    host=DB_SETTINGS['host'],
    port=DB_SETTINGS['port']
)
df_rfm = pd.read_sql_query(rfm_query, conn)

# Normalizzazione e Clustering
rfm_values = df_rfm[['recency', 'frequency', 'monetary']]
rfm_values = (rfm_values - rfm_values.mean()) / rfm_values.std()
kmeans = KMeans(n_clusters=4, random_state=42)
df_rfm['cluster'] = kmeans.fit_predict(rfm_values)

# Step 4: Creazione della Dashboard
st.title("Customer Segmentation & Retention Analysis")
st.write("Questa dashboard mostra i segmenti clienti usando il modello RFM.")
fig = px.scatter_3d(df_rfm, x='recency', y='frequency', z='monetary', color='cluster', title="Customer Segments")
st.plotly_chart(fig)

conn.close()

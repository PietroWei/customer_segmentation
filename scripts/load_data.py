import pandas as pd
import psycopg2

def load_customer_data(file_path):
    """
    Load customer data from an Excel file and insert it into PostgreSQL database.

    Parameters:
    file_path (str): The path to the Excel file.

    Returns:
    None
    """
    # Load data from Excel file
    df = pd.read_excel(file_path)
    
    # Clean and preprocess data
    df = df.dropna(subset=['CustomerID'])  # Remove transactions without CustomerID
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Connect to PostgreSQL database
    conn = psycopg2.connect("dbname=yourdb user=youruser password=yourpass host=localhost")
    cursor = conn.cursor()
    
    # Create tables if they don't exist
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
    
    # Insert data into tables
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO customers (customer_id, country) VALUES (%s, %s) ON CONFLICT DO NOTHING", 
                       (int(row['CustomerID']), row['Country']))
        cursor.execute("INSERT INTO sales (customer_id, invoice_no, sale_date, product, quantity, total_amount) VALUES (%s, %s, %s, %s, %s, %s)",
                       (int(row['CustomerID']), row['InvoiceNo'], row['InvoiceDate'], row['Description'], int(row['Quantity']), float(row['Quantity'] * row['UnitPrice'])))
    
    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
if __name__ == "__main__":
    load_customer_data("/workspaces/customer_segmentation/data/Online Retail.xlsx")

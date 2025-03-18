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
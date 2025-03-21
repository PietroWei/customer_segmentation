import os

# Database connection settings
DB_SETTINGS = {
    'dbname': os.getenv('DB_NAME', 'customer_db'),
    'user': os.getenv('DB_USER', 'PietroWei'),
    'password': os.getenv('DB_PASSWORD', 'Gionniwei98@'),
    'host': os.getenv('DB_HOST', 'db'),
    'port': int(os.getenv('DB_PORT', 5432))
}

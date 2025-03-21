import os

# Database connection settings
DB_SETTINGS = {
    'dbname': os.getenv('DB_NAME', 'yourdb'),
    'user': os.getenv('DB_USER', 'youruser'),
    'password': os.getenv('DB_PASSWORD', 'yourpass'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432))
}

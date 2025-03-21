#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until psql -h "$DB_HOST" -U "$DB_USER" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - executing commands"

# Run the SQL script to create tables
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -f /workspaces/customer_segmentation/sql/create_tables.sql

# Run the Python script to load data
python /workspaces/customer_segmentation/scripts/load_data.py
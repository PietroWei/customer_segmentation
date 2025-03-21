FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install PostgreSQL development libraries
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make the init script executable
RUN chmod +x /app/init_db.sh

# Expose the port for Streamlit
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
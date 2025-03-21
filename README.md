# Customer Segmentation & Retention Analysis

## 📌 Overview
This project analyzes customer purchasing behavior using the **Online Retail Dataset (UCI Machine Learning)**. We implement **RFM analysis (Recency, Frequency, Monetary)** and use **K-Means clustering** to segment customers. The results are displayed in an interactive **Streamlit dashboard**.

## 🏗 Project Structure
```
customer-segmentation/
│── data/                   # Raw & processed data (optional, add .gitignore)
│   ├── online_retail.xlsx  # Dataset (if not too large)
│── sql/                    # SQL scripts for database setup & queries
│   ├── create_tables.sql   # SQL script to create database tables
│   ├── rfm_query.sql       # SQL query to extract RFM metrics
│── scripts/                # Python scripts for ETL & analysis
│   ├── load_data.py        # Load dataset into PostgreSQL
│   ├── rfm_analysis.py     # Compute RFM metrics & clustering
│── dashboard/              # Streamlit app & visualization
│   ├── app.py              # Main Streamlit app
│── config/                 # Configuration files
│   ├── config.py           # Database connection settings
│── notebooks/              # Jupyter notebooks (optional)
│   ├── rfm_analysis.ipynb  # Exploratory data analysis
│── requirements.txt        # Dependencies
│── README.md               # Project documentation
│── .gitignore              # Ignore large files (data, cache, etc.)
```

## 🚀 Technologies Used
- **SQL:** PostgreSQL for database management
- **Python Libraries:** Pandas, NumPy, scikit-learn, psycopg2, Plotly, Streamlit
- **Dashboard:** Interactive visualization with Streamlit

## 📂 Dataset
The dataset is publicly available at [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/online+retail).

## 🔧 Setup Instructions

### Using Docker Compose

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/customer-segmentation.git
   cd customer-segmentation
   ```

2. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. Access the Streamlit dashboard at `http://localhost:8501`.

### Without Docker

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/customer-segmentation.git
   cd customer-segmentation
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL database:
   - Create a PostgreSQL database (e.g., `customer_db`)
   - Update connection details in `config/config.py`
   - Run the SQL script to create tables:
     ```bash
     psql -U username -d customer_db -f sql/create_tables.sql
     ```

4. Load the dataset into PostgreSQL:
   ```bash
   python scripts/load_data.py
   ```

5. Run the clustering analysis:
   ```bash
   python scripts/rfm_analysis.py
   ```

6. Start the Streamlit dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

## 📊 Key Features
- **Automated RFM scoring** for customer behavior analysis
- **K-Means clustering** for customer segmentation
- **Interactive dashboard** to explore insights

## 📬 Contact
For questions, reach out to **Pietro Gazzi** via [LinkedIn](https://www.linkedin.com/in/pietro-gazzi/) or email at `pietrogazzi01@gmail.com`.


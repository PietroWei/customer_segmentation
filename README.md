# Customer Segmentation & Retention Analysis

## 📌 Overview
This project analyzes customer purchasing behavior using the **Online Retail Dataset (UCI Machine Learning)**. We implement **RFM analysis (Recency, Frequency, Monetary)** and use various clustering algorithms (**K-Means clustering**, **DBScan** and **Agglomerative Clustering**) to segment customers. The results are displayed in an interactive **Streamlit dashboard**.

**Deployed at:** [Customer Segmentation App](https://customersegmentation-pg.streamlit.app/)

### **Consideration of 4 Clusters**
In this project, **4 clusters** were initially chosen based on common marketing segmentation strategies using the RFM (Recency, Frequency, Monetary) model:

1. **Champions**: Recent, frequent, and high spenders.
2. **Loyal Customers**: Frequent, moderate spenders.
3. **Potential Loyalists**: Recent, moderate spenders.
4. **At-Risk Customers**: Infrequent, low spenders.

However, the number of clusters can be optimized using various methods: 

- **Elbow Method** to find the optimal number of clusters by evaluating within-cluster sum of squares.
-  **Silhouette Score** to determine the best number of clusters based on cluster separation.
-  **Gap Statistics** for comparing clustering against random data.
-  **Davies-Bouldin Index** to measure cluster similarity.

**Alternative Clustering Methods**:

-  **K-Means**: A widely-used method that partitions the data into a predefined number of clusters (e.g., 4).
-  **DBScan**: A density-based clustering algorithm that doesn't require a predefined number of clusters and is good for discovering clusters of arbitrary shape.
-  **Agglomerative Clustering**: A hierarchical clustering algorithm that builds a tree of clusters, providing a visual representation to help determine the number of clusters.

The clustering results are stored and used in a Streamlit dashboard for visualization and analysis.

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


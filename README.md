# Library Management Data Warehouse and Data Mining System

> **“Design a Library Management Data Warehouse and Data Mining System for Book Circulation Analysis, Reader Classification, Reader Clustering, Borrowing Pattern Discovery, and Text Mining”**

A complete, beginner-friendly, and fully functional academic final-year project developed with **Python (Flask)**, **MySQL** (with automated zero-config fallback), **Scikit-Learn**, **NLTK**, **Bootstrap 5**, and **Chart.js**.

---

## 1. Project Overview & Objective

The primary objective of this system is to transform raw library transactional records into actionable business intelligence and data mining models. It features a complete end-to-end data lifecycle:
1. **Operational Layer (OLTP):** Full CRUD for Readers, Books Catalogue, and Borrowing Transactions.
2. **ETL Synchronization Pipeline:** Extracts operational data, cleans missing fields, computes derived metrics (borrowing duration, overdue fines), and loads the data into a star-schema warehouse.
3. **Data Warehouse (OLAP):** High-performance dimensional model with a central `fact_borrowing` table and `dim_reader`, `dim_book`, and `dim_date` dimension tables.
4. **Circulation Analytics:** Dynamic KPI cards and 7 real-time Chart.js visualisations with multi-attribute filtering (Year, Department, Category, Membership).
5. **Data Mining & Machine Learning:**
   - **Reader Classification:** Decision Tree Classifier ($k$-fold evaluation, Confusion Matrix, live predictor widget).
   - **Reader Clustering:** $K$-Means clustering ($k=3$) with 2D interactive scatter plot and behavioral profiling.
   - **Borrowing Pattern Discovery:** Association Rule Mining via the Apriori algorithm with interactive Support/Confidence sliders.
   - **Text Mining & NLP:** NLTK preprocessing, TF-IDF term scoring, and semantic cosine similarity book search.
6. **Reports & Data Export:** Automated summary generation with CSV export for all analysis modules.

---

## 2. Technology Stack

- **Backend Framework:** Python 3.10+ / Flask 3.1
- **Database Engine:** MySQL 8.x / 5.7 (with automatic SQLite fallback for zero-config offline runs)
- **Data Science & ML:** `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`
- **Text Mining & NLP:** `nltk`, `scikit-learn` (`TfidfVectorizer`, Cosine Similarity)
- **Frontend Architecture:** HTML5, CSS3, JavaScript (ES6), Bootstrap 5, Bootstrap Icons, Chart.js

---

## 3. System Architecture & Data Flow

```
[ Library Transaction Data (OLTP) ]
                 │
                 ▼
[ Data Cleaning & ETL Pipeline (Extract -> Transform -> Load) ]
                 │
                 ▼
[ Dimensional Data Warehouse (Star Schema: Fact + Dimensions) ]
                 │
                 ▼
[ Data Mining & Analytical Engine ]
 ├── Circulation Analytics (Time series, category breakdown)
 ├── Reader Classification (Decision Tree model)
 ├── Reader Clustering (K-Means k=3 algorithm)
 ├── Borrowing Pattern Discovery (Apriori association rules)
 └── Text Mining & NLP (TF-IDF keyword extraction & search)
                 │
                 ▼
[ Web Dashboard & Executive Reports (Chart.js + CSV Export) ]
```

---

## 4. Star Schema Architecture

The Data Warehouse follows Ralph Kimball's dimensional modeling methodology:

```
        +-----------------------------+
        |         dim_reader          |
        +-----------------------------+
        | PK: reader_key              |
        |     reader_id (Natural Key) |
        |     reader_name             |
        |     age, gender             |
        |     department              |
        |     membership_type         |
        +--------------+--------------+
                       |
                       | 1:N
                       v
+----------------------+----------------------+
|                    fact_borrowing           |
+---------------------------------------------+
| PK: borrowing_id                            |
| FK: reader_key -----------------------------+
| FK: book_key   -----------------------------+--------+
| FK: date_key   -----------------------------+----+   |
|     transaction_id                          |    |   |
|     borrow_count (Additive Measure)         |    |   |
|     return_count (Additive Measure)         |    |   |
|     fine_amount ($ Measure)                 |    |   |
|     borrowing_duration (Days Measure)       |    |   |
|     status                                  |    |   |
+---------------------------------------------+    |   |
                       ^                           |   |
                       | 1:N                       |   |
        +--------------+--------------+            |   |
        |          dim_date           |            |   |
        +-----------------------------+            |   |
        | PK: date_key (YYYYMMDD)     |<-----------+   |
        |     full_date               |                |
        |     day, month, quarter     |                |
        |     year, month_name        |                |
        |     day_of_week             |                |
        +-----------------------------+                |
                                                       |
        +-----------------------------+                |
        |          dim_book           |                |
        +-----------------------------+                |
        | PK: book_key                |<---------------+
        |     book_id (Natural Key)   |
        |     title, author           |
        |     category, publisher     |
        |     language                |
        +-----------------------------+
```

---

## 5. Project Modules

### Module 1: Library Data Management (OLTP)
- **Readers Management:** Manage student, faculty, and researcher profiles (Reader ID, Name, Age, Gender, Department, Membership Type, Registration Date).
- **Books Catalogue:** Catalog titles, authors, categories, publishers, publication year, language, and book abstracts.
- **Borrowing Records:** Issue books, track due dates, compute overdue fines, and record returns.

### Module 2: Star-Schema Data Warehouse & ETL
- **ETL Synchronization:** Automated Extract $\rightarrow$ Transform $\rightarrow$ Load trigger.
- **Data Cleaning:** Removes duplicate entries, handles NULL dates, standardizes department/category casings, and computes metrics (`borrowing_duration`, `fine_amount`).
- **Warehouse Explorer:** Interactive visual diagram of the Star Schema with dimension & fact table browsers.

### Module 3: Book Circulation Analytics
- **Interactive KPI Cards:** Total Readers, Total Books, Total Borrows, Returned Books, Pending Returns, Overdue Fines.
- **7 Live Chart.js Visualisations:**
  1. Monthly Borrowing Trends (Area/Line chart)
  2. Most Borrowed Books (Horizontal Bar chart)
  3. Most Popular Book Categories (Doughnut chart)
  4. Borrowing by Department (Bar chart)
  5. Borrowing by Membership Type (Polar Area chart)
  6. Returned vs. Pending Books (Pie chart)
  7. Average Borrowing Duration by Category (Bar chart)
- **Dynamic Multi-Filters:** Live filtering by Year, Department, Category, and Membership.

### Module 4: Reader Classification & Clustering
- **A. Reader Classification:** Classifies readers into *Low Borrower* (1–3), *Medium Borrower* (4–7), and *High Borrower* (8+). Trains a **Decision Tree Classifier** with full evaluation metrics (Accuracy, Confusion Matrix, Precision, Recall, F1-Score) and a real-time single-reader prediction widget.
- **B. Reader Clustering:** Applies **$K$-Means Clustering** ($k=3$) on standardized features (`total_books_borrowed`, `avg_borrowing_duration`, `total_fine`, `late_returns`). Identifies segments: *Low Activity Readers*, *Regular Readers*, and *Highly Active Readers* with an interactive 2D scatter plot.

### Module 5: Borrowing Patterns & Text Mining
- **A. Apriori Association Rules:** Discovers co-borrowing affinities across book titles and categories. Supports configurable Minimum Support ($0.04 - 0.40$) and Minimum Confidence ($0.20 - 0.90$) sliders, reporting Support (%), Confidence (%), and Lift.
- **B. Text Mining & NLP:** Tokenization, lowercasing, punctuation stripping, and stop-word removal. Generates top 20 word frequency distributions, TF-IDF term weights, a keyword cloud, and an interactive **Semantic Cosine Similarity Book Search Engine**.

### Module 6: Reports & Export
- Generates downloadable CSV reports and print-optimized summaries for Circulation, Reader Mining, Association Patterns, and Text Mining.

---

## 6. Installation & Setup Guide

### Step 1: Clone or Navigate to Project Directory
```bash
cd "d:/projects/DWDM assignment project"
```

### Step 2: Create and Activate Python Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Configuration (MySQL or Zero-Config Offline)
The application connects to **MySQL** by default if available. If MySQL is not running or credentials differ, it **automatically runs seamlessly via SQLite** with zero errors.

To configure your local MySQL database:
1. Open XAMPP / MySQL Workbench / Terminal and start MySQL service (`localhost:3306`).
2. Run the provided SQL script:
   ```bash
   mysql -u root -p < database/database.sql
   ```
3. Or edit connection settings in `config.py` / `.env`:
   - `MYSQL_HOST = 'localhost'`
   - `MYSQL_PORT = 3306`
   - `MYSQL_USER = 'root'`
   - `MYSQL_PASSWORD = ''`
   - `MYSQL_DB = 'library_dw_dm'`

### Step 5: Start the Flask Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 7. Sample Login Credentials

- **Username:** `admin`
- **Password:** `admin123`

---

## 8. Step-by-Step Demonstration Flow (For Viva / Project Defense)

1. **Login:** Enter `admin` / `admin123` on the login screen.
2. **Dashboard:** Highlight KPI cards, monthly trends, and popular categories.
3. **Operational Records:** 
   - Navigate to **Readers** $\rightarrow$ show student/faculty records, search by department, or add a reader.
   - Navigate to **Books Catalogue** $\rightarrow$ show titles and abstracts.
   - Navigate to **Borrowing Records** $\rightarrow$ demonstrate issuing a book and returning a book with fine calculation.
4. **ETL Pipeline:** Open **ETL Pipeline** and click **"Run ETL Pipeline"** $\rightarrow$ explain the 3 stages (Extract $\rightarrow$ Transform $\rightarrow$ Load) and show the updated row counts and execution log.
5. **Data Warehouse:** Open **Star Schema & DW** $\rightarrow$ explain the central `fact_borrowing` and the 3 dimension tables (`dim_reader`, `dim_book`, `dim_date`).
6. **Circulation Analysis:** Open **Circulation Analytics** $\rightarrow$ interact with the Year, Department, and Category filters to demonstrate reactive chart updates.
7. **Reader Classification:** Open **Reader Classification** $\rightarrow$ explain Decision Tree accuracy, confusion matrix, and enter values into the **Live Predictor** form to classify a test reader.
8. **Reader Clustering:** Open **Reader Clustering** $\rightarrow$ review the $K$-Means scatter plot, explain the 3 clusters (*Low Activity*, *Regular*, *High Activity*), and test $k=4$.
9. **Borrowing Patterns:** Open **Borrowing Patterns** $\rightarrow$ show Apriori association rules, explain Support, Confidence, and Lift. Adjust the sliders to show dynamic rule pruning.
10. **Text Mining:** Open **Text Mining** $\rightarrow$ show the keyword cloud and word frequency chart. Type `machine learning python` into the semantic search box to show TF-IDF cosine similarity results.
11. **Reports:** Open **Reports & Export** $\rightarrow$ switch between tabs and click **"Export CSV"** to download analytical datasets.

---

## 9. Data Mining Algorithms Reference (Viva Q&A)

### 1. Decision Tree Classification
- **Concept:** Supervised classification model that partitions reader data using feature thresholds (`age`, `borrow_count`, `avg_duration`, `total_fine`, `late_returns`).
- **Splitting Criterion:** Gini Impurity $I_G(p) = 1 - \sum_{i=1}^{J} p_i^2$.

### 2. K-Means Clustering
- **Concept:** Unsupervised clustering algorithm that partitions $n$ readers into $k$ distinct clusters by minimizing within-cluster variance.
- **Objective Function:** $J = \sum_{j=1}^{k} \sum_{i \in S_j} ||x_i - \mu_j||^2$.
- **Standardization:** Utilizes `StandardScaler` ($\mu=0, \sigma=1$) to prevent features with larger scales from dominating cluster centroids.

### 3. Apriori Association Rule Mining
- **Concept:** Discovers co-occurrence affinities in transaction baskets.
- **Support:** $P(A \cup B) = \frac{\text{Count}(A \cup B)}{\text{Total Transactions}}$
- **Confidence:** $P(B|A) = \frac{\text{Support}(A \cup B)}{\text{Support}(A)}$
- **Lift:** $\frac{\text{Confidence}(A \rightarrow B)}{\text{Support}(B)}$. A Lift $> 1$ indicates that items $A$ and $B$ are borrowed together significantly more often than expected by chance.

### 4. TF-IDF Text Mining
- **Term Frequency (TF):** Relative frequency of term $t$ in book description $d$: $\text{TF}(t, d) = \frac{f_{t, d}}{\sum_{t'} f_{t', d}}$.
- **Inverse Document Frequency (IDF):** Measure of term rarity across all books: $\text{IDF}(t, D) = \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$.
- **Cosine Similarity:** $\text{Similarity}(q, d) = \frac{\vec{q} \cdot \vec{d}}{||\vec{q}|| \, ||\vec{d}||}$.

---

## 10. Automated Test Suite

To verify the entire project end-to-end, execute:
```bash
python test_system.py
```
This tests:
- Database connection & schema tables
- ETL pipeline extraction & loading
- Decision Tree reader classifier & prediction
- K-Means reader clustering ($k=3$)
- Apriori frequent itemset & association rule mining
- Text mining & TF-IDF search
- All 17 Flask routes, APIs, and CSV download endpoints (HTTP 200)

---

## License & Academic Usage
Developed for Academic Final-Year Project Demonstration. Suitable for coursework in **Data Warehousing & Data Mining (DWDM)**, **Business Intelligence (BI)**, and **Database Management Systems (DBMS)**.

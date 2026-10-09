import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from werkzeug.security import generate_password_hash
from database.db import Database
from config import Config
from data.sample_data import SAMPLE_READERS, SAMPLE_BOOKS, SAMPLE_TRANSACTIONS

def init_db(seed_sample_data=True):
    """
    Initializes database tables for both MySQL and SQLite.
    Inserts admin user and seeds sample records if tables are empty.
    """
    db_type = Database.get_db_type()
    print(f"[Schema] Initializing database using engine: {db_type.upper()}")

    # Table creation statements compatible across SQLite & MySQL
    if db_type == 'sqlite':
        tables_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Administrator',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS readers (
            reader_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            department TEXT NOT NULL,
            membership_type TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS books (
            book_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            publisher TEXT NOT NULL,
            publication_year INTEGER NOT NULL,
            language TEXT NOT NULL DEFAULT 'English',
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS borrowing_transactions (
            transaction_id TEXT PRIMARY KEY,
            reader_id TEXT NOT NULL,
            book_id TEXT NOT NULL,
            borrow_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            fine REAL NOT NULL DEFAULT 0.0,
            status TEXT NOT NULL DEFAULT 'Borrowed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (reader_id) REFERENCES readers(reader_id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS dim_reader (
            reader_key INTEGER PRIMARY KEY AUTOINCREMENT,
            reader_id TEXT UNIQUE NOT NULL,
            reader_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            department TEXT NOT NULL,
            membership_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS dim_book (
            book_key INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            publisher TEXT NOT NULL,
            language TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS dim_date (
            date_key INTEGER PRIMARY KEY,
            full_date TEXT UNIQUE NOT NULL,
            day INTEGER NOT NULL,
            month INTEGER NOT NULL,
            month_name TEXT NOT NULL,
            quarter INTEGER NOT NULL,
            year INTEGER NOT NULL,
            day_of_week TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS fact_borrowing (
            borrowing_id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE NOT NULL,
            reader_key INTEGER NOT NULL,
            book_key INTEGER NOT NULL,
            date_key INTEGER NOT NULL,
            borrow_count INTEGER NOT NULL DEFAULT 1,
            return_count INTEGER NOT NULL DEFAULT 0,
            fine_amount REAL NOT NULL DEFAULT 0.0,
            borrowing_duration INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (reader_key) REFERENCES dim_reader(reader_key),
            FOREIGN KEY (book_key) REFERENCES dim_book(book_key),
            FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
        );

        CREATE TABLE IF NOT EXISTS etl_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source_records_count INTEGER NOT NULL,
            cleaned_records_count INTEGER NOT NULL,
            warehouse_fact_count INTEGER NOT NULL,
            status TEXT NOT NULL,
            execution_duration_sec REAL NOT NULL,
            details TEXT
        );
        """
        Database.execute_script(tables_sql)
    else:
        # For MySQL, read and execute database.sql
        sql_file = os.path.join(os.path.dirname(__file__), 'database.sql')
        if os.path.exists(sql_file):
            with open(sql_file, 'r', encoding='utf-8') as f:
                Database.execute_script(f.read())

    # Create Default Admin User
    admin_user = Database.query("SELECT * FROM users WHERE username = %s", (Config.ADMIN_USERNAME,), fetchone=True)
    if not admin_user:
        hashed = generate_password_hash(Config.ADMIN_PASSWORD)
        Database.query(
            "INSERT INTO users (username, password_hash, full_name, role) VALUES (%s, %s, %s, %s)",
            (Config.ADMIN_USERNAME, hashed, "Library Administrator", "Administrator"),
            commit=True
        )
        print(f"[Schema] Default admin user created (Username: {Config.ADMIN_USERNAME})")

    # Seed Sample Data if readers table is empty
    reader_count = Database.query("SELECT COUNT(*) as cnt FROM readers", fetchone=True)
    count = reader_count['cnt'] if reader_count else 0
    if count == 0 and seed_sample_data:
        print("[Schema] Seeding realistic sample dataset...")
        
        # Readers
        for r in SAMPLE_READERS:
            Database.query(
                "INSERT INTO readers (reader_id, name, age, gender, department, membership_type, registration_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (r['reader_id'], r['name'], r['age'], r['gender'], r['department'], r['membership_type'], r['registration_date']),
                commit=True
            )
        
        # Books
        for b in SAMPLE_BOOKS:
            Database.query(
                "INSERT INTO books (book_id, title, author, category, publisher, publication_year, language, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (b['book_id'], b['title'], b['author'], b['category'], b['publisher'], b['publication_year'], b['language'], b['description']),
                commit=True
            )

        # Transactions
        for t in SAMPLE_TRANSACTIONS:
            Database.query(
                "INSERT INTO borrowing_transactions (transaction_id, reader_id, book_id, borrow_date, due_date, return_date, fine, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (t['transaction_id'], t['reader_id'], t['book_id'], t['borrow_date'], t['due_date'], t['return_date'], t['fine'], t['status']),
                commit=True
            )

        print(f"[Schema] Seeded {len(SAMPLE_READERS)} readers, {len(SAMPLE_BOOKS)} books, and {len(SAMPLE_TRANSACTIONS)} borrowing transactions.")

    # Auto-populate Data Warehouse if fact table is empty
    try:
        fact_count = Database.query("SELECT COUNT(*) as cnt FROM fact_borrowing", fetchone=True)
        if not fact_count or fact_count['cnt'] == 0:
            print("[Schema] Initializing Star Schema Data Warehouse via ETL...")
            from etl.etl_pipeline import ETLPipeline
            ETLPipeline.run_etl()
    except Exception as e:
        print(f"[Schema] Note on ETL auto-initialization: {e}")

if __name__ == '__main__':
    init_db()

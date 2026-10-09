import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.sample_data import SAMPLE_READERS, SAMPLE_BOOKS, SAMPLE_TRANSACTIONS

def export_csvs():
    data_dir = os.path.dirname(__file__)
    
    df_readers = pd.DataFrame(SAMPLE_READERS)
    df_readers.to_csv(os.path.join(data_dir, 'sample_readers.csv'), index=False)
    
    df_books = pd.DataFrame(SAMPLE_BOOKS)
    df_books.to_csv(os.path.join(data_dir, 'sample_books.csv'), index=False)
    
    df_transactions = pd.DataFrame(SAMPLE_TRANSACTIONS)
    df_transactions.to_csv(os.path.join(data_dir, 'sample_borrowing.csv'), index=False)
    
    print(f"[CSV Export] Created sample_readers.csv ({len(df_readers)} rows), sample_books.csv ({len(df_books)} rows), and sample_borrowing.csv ({len(df_transactions)} rows).")

if __name__ == '__main__':
    export_csvs()

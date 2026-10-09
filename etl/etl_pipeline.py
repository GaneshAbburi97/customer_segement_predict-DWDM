import os
import sys
import time
from datetime import datetime, date
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db import Database

class ETLPipeline:
    @staticmethod
    def run_etl():
        """
        Executes the complete Extract, Transform, Load (ETL) pipeline:
        Extracts from OLTP tables (readers, books, borrowing_transactions),
        Cleans and transforms data,
        Loads into OLAP Star Schema (dim_reader, dim_book, dim_date, fact_borrowing),
        and records execution metadata into etl_log.
        """
        start_time = time.time()
        logs = []
        errors = []

        try:
            # -------------------------------------------------------------
            # STEP 1: EXTRACT
            # -------------------------------------------------------------
            logs.append("Starting ETL Pipeline execution...")
            raw_readers = Database.query("SELECT * FROM readers")
            raw_books = Database.query("SELECT * FROM books")
            raw_transactions = Database.query("SELECT * FROM borrowing_transactions")

            source_count = len(raw_readers) + len(raw_books) + len(raw_transactions)
            logs.append(f"[Extract] Extracted {len(raw_readers)} readers, {len(raw_books)} books, {len(raw_transactions)} transactions (Total: {source_count} source records).")

            if not raw_transactions:
                return {
                    "status": "WARNING",
                    "message": "No transaction records found to process.",
                    "source_count": source_count,
                    "cleaned_count": 0,
                    "fact_count": 0,
                    "duration_sec": round(time.time() - start_time, 3),
                    "logs": logs
                }

            # -------------------------------------------------------------
            # STEP 2: TRANSFORM
            # -------------------------------------------------------------
            logs.append("[Transform] Cleaning and transforming data...")

            # Clean Readers
            cleaned_readers = []
            for r in raw_readers:
                cleaned_readers.append({
                    "reader_id": str(r["reader_id"]).strip(),
                    "reader_name": str(r["name"]).strip(),
                    "age": int(r["age"]) if r["age"] is not None else 20,
                    "gender": str(r["gender"]).strip().capitalize(),
                    "department": str(r["department"]).strip(),
                    "membership_type": str(r["membership_type"]).strip()
                })

            # Clean Books
            cleaned_books = []
            for b in raw_books:
                cleaned_books.append({
                    "book_id": str(b["book_id"]).strip(),
                    "title": str(b["title"]).strip(),
                    "author": str(b["author"]).strip(),
                    "category": str(b["category"]).strip().title(),
                    "publisher": str(b["publisher"]).strip(),
                    "language": str(b.get("language") or "English").strip()
                })

            # Clean & Transform Transactions & Generate Calendar Dates
            cleaned_transactions = []
            unique_dates = set()
            today = date.today()

            for t in raw_transactions:
                # Parse Dates
                try:
                    if isinstance(t["borrow_date"], (datetime, date)):
                        b_date = t["borrow_date"] if isinstance(t["borrow_date"], date) else t["borrow_date"].date()
                    else:
                        b_date = datetime.strptime(str(t["borrow_date"]).split()[0], "%Y-%m-%d").date()
                except Exception:
                    b_date = today

                unique_dates.add(b_date)

                r_date = None
                if t["return_date"]:
                    try:
                        if isinstance(t["return_date"], (datetime, date)):
                            r_date = t["return_date"] if isinstance(t["return_date"], date) else t["return_date"].date()
                        else:
                            r_date = datetime.strptime(str(t["return_date"]).split()[0], "%Y-%m-%d").date()
                        unique_dates.add(r_date)
                    except Exception:
                        r_date = None

                due_d = None
                if t["due_date"]:
                    try:
                        if isinstance(t["due_date"], (datetime, date)):
                            due_d = t["due_date"] if isinstance(t["due_date"], date) else t["due_date"].date()
                        else:
                            due_d = datetime.strptime(str(t["due_date"]).split()[0], "%Y-%m-%d").date()
                    except Exception:
                        due_d = b_date

                # Derived metrics: borrowing_duration
                if r_date:
                    duration = max(0, (r_date - b_date).days)
                else:
                    duration = max(0, (today - b_date).days)

                # Fine Calculation
                fine = float(t.get("fine") or 0.0)
                status = str(t.get("status") or "Borrowed").strip()

                if r_date and due_d and r_date > due_d and fine == 0.0:
                    fine = float((r_date - due_d).days * 1.0)
                elif not r_date and due_d and today > due_d and fine == 0.0:
                    fine = float((today - due_d).days * 1.0)
                    status = "Overdue"

                return_count = 1 if status.lower() == "returned" else 0
                date_key = int(b_date.strftime("%Y%m%d"))

                cleaned_transactions.append({
                    "transaction_id": str(t["transaction_id"]).strip(),
                    "reader_id": str(t["reader_id"]).strip(),
                    "book_id": str(t["book_id"]).strip(),
                    "date_key": date_key,
                    "borrow_count": 1,
                    "return_count": return_count,
                    "fine_amount": fine,
                    "borrowing_duration": duration,
                    "status": status
                })

            cleaned_count = len(cleaned_readers) + len(cleaned_books) + len(cleaned_transactions)
            logs.append(f"[Transform] Cleaned {cleaned_count} total records across reader, book, and transaction dimensions.")

            # -------------------------------------------------------------
            # STEP 3: LOAD INTO WAREHOUSE STAR SCHEMA
            # -------------------------------------------------------------
            logs.append("[Load] Populating Dimension Tables (dim_reader, dim_book, dim_date)...")

            # Load dim_reader
            for r in cleaned_readers:
                existing = Database.query("SELECT reader_key FROM dim_reader WHERE reader_id = %s", (r["reader_id"],), fetchone=True)
                if existing:
                    Database.query(
                        """UPDATE dim_reader SET reader_name=%s, age=%s, gender=%s, department=%s, membership_type=%s 
                           WHERE reader_id=%s""",
                        (r["reader_name"], r["age"], r["gender"], r["department"], r["membership_type"], r["reader_id"]),
                        commit=True
                    )
                else:
                    Database.query(
                        """INSERT INTO dim_reader (reader_id, reader_name, age, gender, department, membership_type) 
                           VALUES (%s, %s, %s, %s, %s, %s)""",
                        (r["reader_id"], r["reader_name"], r["age"], r["gender"], r["department"], r["membership_type"]),
                        commit=True
                    )

            # Load dim_book
            for b in cleaned_books:
                existing = Database.query("SELECT book_key FROM dim_book WHERE book_id = %s", (b["book_id"],), fetchone=True)
                if existing:
                    Database.query(
                        """UPDATE dim_book SET title=%s, author=%s, category=%s, publisher=%s, language=%s 
                           WHERE book_id=%s""",
                        (b["title"], b["author"], b["category"], b["publisher"], b["language"], b["book_id"]),
                        commit=True
                    )
                else:
                    Database.query(
                        """INSERT INTO dim_book (book_id, title, author, category, publisher, language) 
                           VALUES (%s, %s, %s, %s, %s, %s)""",
                        (b["book_id"], b["title"], b["author"], b["category"], b["publisher"], b["language"]),
                        commit=True
                    )

            # Load dim_date
            for d in unique_dates:
                d_key = int(d.strftime("%Y%m%d"))
                existing = Database.query("SELECT date_key FROM dim_date WHERE date_key = %s", (d_key,), fetchone=True)
                if not existing:
                    Database.query(
                        """INSERT INTO dim_date (date_key, full_date, day, month, month_name, quarter, year, day_of_week) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            d_key,
                            d.strftime("%Y-%m-%d"),
                            d.day,
                            d.month,
                            d.strftime("%B"),
                            (d.month - 1) // 3 + 1,
                            d.year,
                            d.strftime("%A")
                        ),
                        commit=True
                    )

            # Build Surrogate Key Lookups
            reader_map = {row["reader_id"]: row["reader_key"] for row in Database.query("SELECT reader_key, reader_id FROM dim_reader")}
            book_map = {row["book_id"]: row["book_key"] for row in Database.query("SELECT book_key, book_id FROM dim_book")}

            logs.append("[Load] Populating Fact Table (fact_borrowing)...")

            # Load fact_borrowing
            loaded_fact_count = 0
            for t in cleaned_transactions:
                r_key = reader_map.get(t["reader_id"])
                b_key = book_map.get(t["book_id"])
                d_key = t["date_key"]

                if r_key is None or b_key is None:
                    continue

                existing = Database.query("SELECT borrowing_id FROM fact_borrowing WHERE transaction_id = %s", (t["transaction_id"],), fetchone=True)
                if existing:
                    Database.query(
                        """UPDATE fact_borrowing SET reader_key=%s, book_key=%s, date_key=%s, 
                           borrow_count=%s, return_count=%s, fine_amount=%s, borrowing_duration=%s, status=%s 
                           WHERE transaction_id=%s""",
                        (r_key, b_key, d_key, t["borrow_count"], t["return_count"], t["fine_amount"], t["borrowing_duration"], t["status"], t["transaction_id"]),
                        commit=True
                    )
                else:
                    Database.query(
                        """INSERT INTO fact_borrowing (transaction_id, reader_key, book_key, date_key, borrow_count, return_count, fine_amount, borrowing_duration, status) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (t["transaction_id"], r_key, b_key, d_key, t["borrow_count"], t["return_count"], t["fine_amount"], t["borrowing_duration"], t["status"]),
                        commit=True
                    )
                loaded_fact_count += 1

            duration_sec = round(time.time() - start_time, 3)
            logs.append(f"[Load] Successfully loaded {loaded_fact_count} records into fact_borrowing in {duration_sec} seconds.")

            # Record in etl_log
            status_str = "SUCCESS"
            details_str = "\n".join(logs)
            Database.query(
                """INSERT INTO etl_log (source_records_count, cleaned_records_count, warehouse_fact_count, status, execution_duration_sec, details) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (source_count, cleaned_count, loaded_fact_count, status_str, duration_sec, details_str),
                commit=True
            )

            return {
                "status": status_str,
                "message": "ETL pipeline completed successfully.",
                "source_count": source_count,
                "cleaned_count": cleaned_count,
                "fact_count": loaded_fact_count,
                "duration_sec": duration_sec,
                "logs": logs
            }

        except Exception as e:
            duration_sec = round(time.time() - start_time, 3)
            error_msg = f"ETL Pipeline Error: {str(e)}"
            logs.append(error_msg)
            print(f"[ETL Error] {error_msg}")
            
            try:
                Database.query(
                    """INSERT INTO etl_log (source_records_count, cleaned_records_count, warehouse_fact_count, status, execution_duration_sec, details) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (0, 0, 0, "FAILED", duration_sec, "\n".join(logs)),
                    commit=True
                )
            except Exception:
                pass

            return {
                "status": "FAILED",
                "message": error_msg,
                "source_count": 0,
                "cleaned_count": 0,
                "fact_count": 0,
                "duration_sec": duration_sec,
                "logs": logs
            }

if __name__ == "__main__":
    result = ETLPipeline.run_etl()
    print(result)

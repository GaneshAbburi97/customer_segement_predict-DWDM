from flask import Blueprint, render_template
from routes.auth import login_required
from database.db import Database

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    # 1. Total Readers
    reader_res = Database.query("SELECT COUNT(*) AS total_readers FROM readers", fetchone=True)
    total_readers = reader_res['total_readers'] if reader_res else 0

    # 2. Total Books
    book_res = Database.query("SELECT COUNT(*) AS total_books FROM books", fetchone=True)
    total_books = book_res['total_books'] if book_res else 0

    # 3. Total Borrowings
    borrow_res = Database.query("SELECT COUNT(*) AS total_borrowings FROM borrowing_transactions", fetchone=True)
    total_borrowings = borrow_res['total_borrowings'] if borrow_res else 0

    # 4. Active / Returned Borrowings
    status_res = Database.query("""
        SELECT 
            SUM(CASE WHEN status = 'Returned' THEN 1 ELSE 0 END) AS returned_count,
            SUM(CASE WHEN status != 'Returned' THEN 1 ELSE 0 END) AS active_count,
            COALESCE(SUM(fine), 0.0) AS total_fines
        FROM borrowing_transactions
    """, fetchone=True)
    returned_count = status_res['returned_count'] or 0
    active_count = status_res['active_count'] or 0
    total_fines = round(float(status_res['total_fines'] or 0.0), 2)

    # 5. Most Popular Category
    pop_cat_res = Database.query("""
        SELECT b.category, COUNT(*) as cnt 
        FROM borrowing_transactions t
        JOIN books b ON t.book_id = b.book_id
        GROUP BY b.category 
        ORDER BY cnt DESC 
        LIMIT 1
    """, fetchone=True)
    popular_category = pop_cat_res['category'] if pop_cat_res else "N/A"

    # 6. Most Borrowed Book
    pop_book_res = Database.query("""
        SELECT b.title, COUNT(*) as cnt 
        FROM borrowing_transactions t
        JOIN books b ON t.book_id = b.book_id
        GROUP BY b.book_id, b.title 
        ORDER BY cnt DESC 
        LIMIT 1
    """, fetchone=True)
    most_borrowed_book = pop_book_res['title'] if pop_book_res else "N/A"

    # 7. Recent Transactions (Top 7)
    recent_transactions = Database.query("""
        SELECT 
            t.transaction_id,
            r.name AS reader_name,
            b.title AS book_title,
            b.category,
            t.borrow_date,
            t.due_date,
            t.status,
            t.fine
        FROM borrowing_transactions t
        JOIN readers r ON t.reader_id = r.reader_id
        JOIN books b ON t.book_id = b.book_id
        ORDER BY t.borrow_date DESC
        LIMIT 7
    """)

    # 8. Category Distribution for Mini Chart
    cat_dist = Database.query("""
        SELECT b.category, COUNT(*) as cnt
        FROM borrowing_transactions t
        JOIN books b ON t.book_id = b.book_id
        GROUP BY b.category
        ORDER BY cnt DESC
        LIMIT 6
    """)

    # 9. Monthly Trends for Mini Chart
    monthly_trend = Database.query("""
        SELECT SUBSTR(borrow_date, 1, 7) AS ym, COUNT(*) AS cnt
        FROM borrowing_transactions
        GROUP BY ym
        ORDER BY ym ASC
    """)

    # 10. Data Warehouse Status
    wh_fact = Database.query("SELECT COUNT(*) as cnt FROM fact_borrowing", fetchone=True)
    warehouse_fact_count = wh_fact['cnt'] if wh_fact else 0

    return render_template(
        'dashboard.html',
        total_readers=total_readers,
        total_books=total_books,
        total_borrowings=total_borrowings,
        returned_count=returned_count,
        active_count=active_count,
        total_fines=total_fines,
        popular_category=popular_category,
        most_borrowed_book=most_borrowed_book,
        recent_transactions=recent_transactions,
        cat_dist=cat_dist,
        monthly_trend=monthly_trend,
        warehouse_fact_count=warehouse_fact_count,
        db_type=Database.get_db_type().upper()
    )

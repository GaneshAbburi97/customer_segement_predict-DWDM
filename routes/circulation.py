from flask import Blueprint, render_template, request, jsonify
from routes.auth import login_required
from database.db import Database

circulation_bp = Blueprint('circulation', __name__)

def fetch_circulation_metrics(year=None, department=None, category=None, membership=None):
    """
    Queries star schema (fact_borrowing + dimensions) with dynamic filter criteria.
    """
    where_clauses = ["1=1"]
    params = []

    if year and year != 'All':
        where_clauses.append("d.year = %s")
        params.append(int(year))

    if department and department != 'All':
        where_clauses.append("r.department = %s")
        params.append(department)

    if category and category != 'All':
        where_clauses.append("b.category = %s")
        params.append(category)

    if membership and membership != 'All':
        where_clauses.append("r.membership_type = %s")
        params.append(membership)

    where_sql = " AND ".join(where_clauses)

    # 1. KPI Aggregates
    kpi_sql = f"""
    SELECT 
        COUNT(DISTINCT r.reader_key) AS total_readers,
        COUNT(DISTINCT b.book_key) AS total_books,
        COALESCE(SUM(f.borrow_count), 0) AS total_borrowings,
        COALESCE(SUM(f.return_count), 0) AS returned_count,
        COALESCE(SUM(CASE WHEN f.status != 'Returned' THEN 1 ELSE 0 END), 0) AS pending_count,
        COALESCE(SUM(f.fine_amount), 0.0) AS total_fines,
        COALESCE(AVG(f.borrowing_duration), 0.0) AS avg_duration
    FROM fact_borrowing f
    JOIN dim_reader r ON f.reader_key = r.reader_key
    JOIN dim_book b ON f.book_key = b.book_key
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE {where_sql}
    """
    kpis = Database.query(kpi_sql, params, fetchone=True) or {}

    # 2. Monthly Trend (Line Chart)
    monthly_sql = f"""
    SELECT 
        d.year,
        d.month,
        d.month_name,
        COUNT(f.borrowing_id) AS borrow_count
    FROM fact_borrowing f
    JOIN dim_reader r ON f.reader_key = r.reader_key
    JOIN dim_book b ON f.book_key = b.book_key
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE {where_sql}
    GROUP BY d.year, d.month, d.month_name
    ORDER BY d.year ASC, d.month ASC
    """
    monthly_rows = Database.query(monthly_sql, params)
    monthly_labels = [f"{r['month_name'][:3]} {r['year']}" for r in monthly_rows]
    monthly_data = [r['borrow_count'] for r in monthly_rows]

    # 3. Top Borrowed Books (Bar Chart)
    books_sql = f"""
    SELECT 
        b.title,
        COUNT(f.borrowing_id) AS borrow_count
    FROM fact_borrowing f
    JOIN dim_reader r ON f.reader_key = r.reader_key
    JOIN dim_book b ON f.book_key = b.book_key
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE {where_sql}
    GROUP BY b.book_key, b.title
    ORDER BY borrow_count DESC
    LIMIT 7
    """
    books_rows = Database.query(books_sql, params)
    top_books_labels = [r['title'][:25] + ('...' if len(r['title']) > 25 else '') for r in books_rows]
    top_books_data = [r['borrow_count'] for r in books_rows]

    # 4. Popular Categories (Doughnut Chart)
    cat_sql = f"""
    SELECT 
        b.category,
        COUNT(f.borrowing_id) AS borrow_count
    FROM fact_borrowing f
    JOIN dim_reader r ON f.reader_key = r.reader_key
    JOIN dim_book b ON f.book_key = b.book_key
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE {where_sql}
    GROUP BY b.category
    ORDER BY borrow_count DESC
    """
    cat_rows = Database.query(cat_sql, params)
    cat_labels = [r['category'] for r in cat_rows]
    cat_data = [r['borrow_count'] for r in cat_rows]

    # 5. Borrowing by Department (Bar Chart)
    dept_sql = f"""
    SELECT 
        r.department,
        COUNT(f.borrowing_id) AS borrow_count
    FROM fact_borrowing f
    JOIN dim_reader r ON f.reader_key = r.reader_key
    JOIN dim_book b ON f.book_key = b.book_key
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE {where_sql}
    GROUP BY r.department
    ORDER BY borrow_count DESC
    """
    dept_rows = Database.query(dept_sql, params)
    dept_labels = [r['department'] for r in dept_rows]
    dept_data = [r['borrow_count'] for r in dept_rows]

    # 6. Borrowing by Membership Type (Polar Area / Pie Chart)
    mem_sql = f"""
    SELECT 
        r.membership_type,
        COUNT(f.borrowing_id) AS borrow_count
    FROM fact_borrowing f
    JOIN dim_reader r ON f.reader_key = r.reader_key
    JOIN dim_book b ON f.book_key = b.book_key
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE {where_sql}
    GROUP BY r.membership_type
    ORDER BY borrow_count DESC
    """
    mem_rows = Database.query(mem_sql, params)
    mem_labels = [r['membership_type'] for r in mem_rows]
    mem_data = [r['borrow_count'] for r in mem_rows]

    # 7. Returned vs Pending Books (Doughnut Chart)
    status_counts = {
        "Returned": int(kpis.get('returned_count') or 0),
        "Pending / Borrowed": int(kpis.get('pending_count') or 0)
    }

    # 8. Avg Duration by Category (Bar Chart)
    dur_sql = f"""
    SELECT 
        b.category,
        ROUND(AVG(f.borrowing_duration), 1) AS avg_duration
    FROM fact_borrowing f
    JOIN dim_reader r ON f.reader_key = r.reader_key
    JOIN dim_book b ON f.book_key = b.book_key
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE {where_sql}
    GROUP BY b.category
    ORDER BY avg_duration DESC
    """
    dur_rows = Database.query(dur_sql, params)
    dur_labels = [r['category'] for r in dur_rows]
    dur_data = [float(r['avg_duration']) for r in dur_rows]

    return {
        "kpis": {
            "total_readers": kpis.get('total_readers') or 0,
            "total_books": kpis.get('total_books') or 0,
            "total_borrowings": kpis.get('total_borrowings') or 0,
            "returned_count": kpis.get('returned_count') or 0,
            "pending_count": kpis.get('pending_count') or 0,
            "total_fines": round(float(kpis.get('total_fines') or 0.0), 2),
            "avg_duration": round(float(kpis.get('avg_duration') or 0.0), 1)
        },
        "monthly_trend": {"labels": monthly_labels, "data": monthly_data},
        "top_books": {"labels": top_books_labels, "data": top_books_data},
        "categories": {"labels": cat_labels, "data": cat_data},
        "departments": {"labels": dept_labels, "data": dept_data},
        "memberships": {"labels": mem_labels, "data": mem_data},
        "status_distribution": {"labels": list(status_counts.keys()), "data": list(status_counts.values())},
        "duration_by_category": {"labels": dur_labels, "data": dur_data}
    }

@circulation_bp.route('/circulation')
@login_required
def index():
    # Filter dropdown options
    years = [str(r['year']) for r in Database.query("SELECT DISTINCT year FROM dim_date ORDER BY year DESC") if r['year']]
    departments = [r['department'] for r in Database.query("SELECT DISTINCT department FROM dim_reader ORDER BY department") if r['department']]
    categories = [r['category'] for r in Database.query("SELECT DISTINCT category FROM dim_book ORDER BY category") if r['category']]
    memberships = [r['membership_type'] for r in Database.query("SELECT DISTINCT membership_type FROM dim_reader ORDER BY membership_type") if r['membership_type']]

    # Initial data payload
    data = fetch_circulation_metrics()

    return render_template(
        'circulation.html',
        years=years,
        departments=departments,
        categories=categories,
        memberships=memberships,
        initial_data=data
    )

@circulation_bp.route('/api/circulation-data')
@login_required
def get_circulation_data():
    year = request.args.get('year')
    department = request.args.get('department')
    category = request.args.get('category')
    membership = request.args.get('membership')

    data = fetch_circulation_metrics(year, department, category, membership)
    return jsonify(data)

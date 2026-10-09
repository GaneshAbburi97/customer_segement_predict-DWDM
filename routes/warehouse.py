from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from routes.auth import login_required
from database.db import Database
from etl.etl_pipeline import ETLPipeline

warehouse_bp = Blueprint('warehouse', __name__)

@warehouse_bp.route('/warehouse')
@login_required
def index():
    # Fetch Counts
    dim_reader_cnt = Database.query("SELECT COUNT(*) AS cnt FROM dim_reader", fetchone=True)['cnt'] or 0
    dim_book_cnt = Database.query("SELECT COUNT(*) AS cnt FROM dim_book", fetchone=True)['cnt'] or 0
    dim_date_cnt = Database.query("SELECT COUNT(*) AS cnt FROM dim_date", fetchone=True)['cnt'] or 0
    fact_cnt = Database.query("SELECT COUNT(*) AS cnt FROM fact_borrowing", fetchone=True)['cnt'] or 0

    # Fetch Sample Fact Records joined with dimensions
    sample_facts = Database.query("""
        SELECT 
            f.borrowing_id,
            f.transaction_id,
            r.reader_name,
            r.department,
            b.title AS book_title,
            b.category,
            d.full_date AS borrow_date,
            f.borrow_count,
            f.return_count,
            f.fine_amount,
            f.borrowing_duration,
            f.status
        FROM fact_borrowing f
        JOIN dim_reader r ON f.reader_key = r.reader_key
        JOIN dim_book b ON f.book_key = b.book_key
        JOIN dim_date d ON f.date_key = d.date_key
        ORDER BY f.borrowing_id DESC
        LIMIT 10
    """)

    # Fetch Dimension Samples
    dim_readers = Database.query("SELECT * FROM dim_reader ORDER BY reader_key ASC LIMIT 8")
    dim_books = Database.query("SELECT * FROM dim_book ORDER BY book_key ASC LIMIT 8")
    dim_dates = Database.query("SELECT * FROM dim_date ORDER BY date_key DESC LIMIT 8")

    return render_template(
        'warehouse.html',
        dim_reader_cnt=dim_reader_cnt,
        dim_book_cnt=dim_book_cnt,
        dim_date_cnt=dim_date_cnt,
        fact_cnt=fact_cnt,
        sample_facts=sample_facts,
        dim_readers=dim_readers,
        dim_books=dim_books,
        dim_dates=dim_dates
    )

@warehouse_bp.route('/etl')
@login_required
def etl_view():
    # Source counts
    op_readers = Database.query("SELECT COUNT(*) AS cnt FROM readers", fetchone=True)['cnt'] or 0
    op_books = Database.query("SELECT COUNT(*) AS cnt FROM books", fetchone=True)['cnt'] or 0
    op_tx = Database.query("SELECT COUNT(*) AS cnt FROM borrowing_transactions", fetchone=True)['cnt'] or 0
    total_source = op_readers + op_books + op_tx

    # Warehouse count
    wh_fact_count = Database.query("SELECT COUNT(*) AS cnt FROM fact_borrowing", fetchone=True)['cnt'] or 0

    # ETL Execution History
    logs = Database.query("SELECT * FROM etl_log ORDER BY run_timestamp DESC LIMIT 10")
    last_log = logs[0] if logs else None

    return render_template(
        'etl.html',
        op_readers=op_readers,
        op_books=op_books,
        op_tx=op_tx,
        total_source=total_source,
        wh_fact_count=wh_fact_count,
        logs=logs,
        last_log=last_log
    )

@warehouse_bp.route('/etl/run', methods=['POST'])
@login_required
def run_etl():
    """
    Triggers the ETL Pipeline and returns JSON response for AJAX or redirects with flash message.
    """
    result = ETLPipeline.run_etl()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return jsonify(result)

    if result['status'] == 'SUCCESS':
        flash(f"ETL Execution Successful! {result['fact_count']} fact records synchronized into Data Warehouse in {result['duration_sec']}s.", 'success')
    else:
        flash(f"ETL Finished with status: {result['status']}. Message: {result['message']}", 'warning')

    return redirect(url_for('warehouse.etl_view'))

from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, date, timedelta
from routes.auth import login_required
from database.db import Database

borrowing_bp = Blueprint('borrowing', __name__)

@borrowing_bp.route('/borrowing', methods=['GET'])
@login_required
def index():
    search = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '').strip()

    sql = """
    SELECT 
        t.transaction_id,
        t.reader_id,
        r.name AS reader_name,
        r.department,
        t.book_id,
        b.title AS book_title,
        b.category,
        t.borrow_date,
        t.due_date,
        t.return_date,
        t.fine,
        t.status
    FROM borrowing_transactions t
    JOIN readers r ON t.reader_id = r.reader_id
    JOIN books b ON t.book_id = b.book_id
    WHERE 1=1
    """
    params = []

    if search:
        sql += " AND (t.transaction_id LIKE %s OR r.name LIKE %s OR b.title LIKE %s OR t.reader_id LIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param, search_param])

    if status_filter:
        sql += " AND t.status = %s"
        params.append(status_filter)

    sql += " ORDER BY t.borrow_date DESC"
    transactions = Database.query(sql, params)

    # Readers & Books lists for Issue Book modal
    readers = Database.query("SELECT reader_id, name, department FROM readers ORDER BY name")
    books = Database.query("SELECT book_id, title, category FROM books ORDER BY title")

    # Generate next suggested transaction ID
    last_tx = Database.query("SELECT transaction_id FROM borrowing_transactions ORDER BY transaction_id DESC LIMIT 1", fetchone=True)
    if last_tx and str(last_tx['transaction_id']).startswith('T'):
        try:
            num = int(str(last_tx['transaction_id'])[1:]) + 1
            next_tx_id = f"T{num}"
        except Exception:
            next_tx_id = "T1200"
    else:
        next_tx_id = "T1001"

    default_borrow_date = str(date.today())
    default_due_date = str(date.today() + timedelta(days=14))

    return render_template(
        'borrowing.html',
        transactions=transactions,
        readers=readers,
        books=books,
        next_tx_id=next_tx_id,
        default_borrow_date=default_borrow_date,
        default_due_date=default_due_date,
        selected_search=search,
        selected_status=status_filter
    )

@borrowing_bp.route('/borrowing/add', methods=['POST'])
@login_required
def add():
    transaction_id = request.form.get('transaction_id', '').strip()
    reader_id = request.form.get('reader_id', '').strip()
    book_id = request.form.get('book_id', '').strip()
    borrow_date = request.form.get('borrow_date') or str(date.today())
    due_date = request.form.get('due_date') or str(date.today() + timedelta(days=14))
    fine = float(request.form.get('fine') or 0.0)
    status = request.form.get('status', 'Borrowed')

    if not transaction_id or not reader_id or not book_id:
        flash('Transaction ID, Reader, and Book are required.', 'danger')
        return redirect(url_for('borrowing.index'))

    existing = Database.query("SELECT transaction_id FROM borrowing_transactions WHERE transaction_id = %s", (transaction_id,), fetchone=True)
    if existing:
        flash(f'Transaction ID {transaction_id} already exists.', 'danger')
        return redirect(url_for('borrowing.index'))

    try:
        Database.query(
            """INSERT INTO borrowing_transactions (transaction_id, reader_id, book_id, borrow_date, due_date, fine, status) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (transaction_id, reader_id, book_id, borrow_date, due_date, fine, status),
            commit=True
        )
        flash(f'Book issued successfully under Transaction ID {transaction_id}!', 'success')
    except Exception as e:
        flash(f'Error issuing book: {str(e)}', 'danger')

    return redirect(url_for('borrowing.index'))

@borrowing_bp.route('/borrowing/return/<transaction_id>', methods=['POST'])
@login_required
def return_book(transaction_id):
    today = str(date.today())
    # Fetch due date to compute fine if overdue
    tx = Database.query("SELECT * FROM borrowing_transactions WHERE transaction_id = %s", (transaction_id,), fetchone=True)
    if not tx:
        flash('Transaction not found.', 'danger')
        return redirect(url_for('borrowing.index'))

    due_str = str(tx['due_date']).split()[0]
    fine = 0.0
    try:
        due_d = datetime.strptime(due_str, '%Y-%m-%d').date()
        if date.today() > due_d:
            overdue_days = (date.today() - due_d).days
            fine = float(overdue_days * 1.0)
    except Exception:
        fine = 0.0

    try:
        Database.query(
            """UPDATE borrowing_transactions SET return_date = %s, fine = %s, status = 'Returned' 
               WHERE transaction_id = %s""",
            (today, fine, transaction_id),
            commit=True
        )
        if fine > 0:
            flash(f'Book returned on {today}. Late fine of ${fine:.2f} recorded.', 'warning')
        else:
            flash(f'Book returned successfully on {today} with zero fines!', 'success')
    except Exception as e:
        flash(f'Error processing book return: {str(e)}', 'danger')

    return redirect(url_for('borrowing.index'))

@borrowing_bp.route('/borrowing/delete/<transaction_id>', methods=['POST'])
@login_required
def delete(transaction_id):
    try:
        Database.query("DELETE FROM borrowing_transactions WHERE transaction_id = %s", (transaction_id,), commit=True)
        flash(f'Transaction {transaction_id} deleted successfully.', 'info')
    except Exception as e:
        flash(f'Error deleting transaction: {str(e)}', 'danger')
    return redirect(url_for('borrowing.index'))

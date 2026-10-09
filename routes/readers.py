from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import date
from routes.auth import login_required
from database.db import Database

readers_bp = Blueprint('readers', __name__)

@readers_bp.route('/readers', methods=['GET'])
@login_required
def index():
    search = request.args.get('search', '').strip()
    dept = request.args.get('department', '').strip()
    membership = request.args.get('membership', '').strip()

    sql = "SELECT * FROM readers WHERE 1=1"
    params = []

    if search:
        sql += " AND (reader_id LIKE %s OR name LIKE %s OR department LIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])

    if dept:
        sql += " AND department = %s"
        params.append(dept)

    if membership:
        sql += " AND membership_type = %s"
        params.append(membership)

    sql += " ORDER BY reader_id ASC"
    readers = Database.query(sql, params)

    # Get distinct departments & memberships for filter dropdowns
    dept_rows = Database.query("SELECT DISTINCT department FROM readers ORDER BY department")
    departments = [r['department'] for r in dept_rows if r['department']]

    mem_rows = Database.query("SELECT DISTINCT membership_type FROM readers ORDER BY membership_type")
    memberships = [r['membership_type'] for r in mem_rows if r['membership_type']]

    return render_template(
        'readers.html',
        readers=readers,
        departments=departments,
        memberships=memberships,
        selected_search=search,
        selected_dept=dept,
        selected_membership=membership
    )

@readers_bp.route('/readers/add', methods=['POST'])
@login_required
def add():
    reader_id = request.form.get('reader_id', '').strip()
    name = request.form.get('name', '').strip()
    age = request.form.get('age', 20)
    gender = request.form.get('gender', 'Male')
    department = request.form.get('department', '').strip()
    membership_type = request.form.get('membership_type', 'Student')
    registration_date = request.form.get('registration_date') or str(date.today())

    if not reader_id or not name or not department:
        flash('Reader ID, Name, and Department are required fields.', 'danger')
        return redirect(url_for('readers.index'))

    existing = Database.query("SELECT reader_id FROM readers WHERE reader_id = %s", (reader_id,), fetchone=True)
    if existing:
        flash(f'Reader ID {reader_id} already exists. Please choose a unique ID.', 'danger')
        return redirect(url_for('readers.index'))

    try:
        Database.query(
            """INSERT INTO readers (reader_id, name, age, gender, department, membership_type, registration_date) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (reader_id, name, int(age), gender, department, membership_type, registration_date),
            commit=True
        )
        flash(f'Reader {name} ({reader_id}) added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding reader: {str(e)}', 'danger')

    return redirect(url_for('readers.index'))

@readers_bp.route('/readers/edit/<reader_id>', methods=['POST'])
@login_required
def edit(reader_id):
    name = request.form.get('name', '').strip()
    age = request.form.get('age', 20)
    gender = request.form.get('gender', 'Male')
    department = request.form.get('department', '').strip()
    membership_type = request.form.get('membership_type', 'Student')
    registration_date = request.form.get('registration_date')

    try:
        Database.query(
            """UPDATE readers SET name=%s, age=%s, gender=%s, department=%s, membership_type=%s, registration_date=%s 
               WHERE reader_id=%s""",
            (name, int(age), gender, department, membership_type, registration_date, reader_id),
            commit=True
        )
        flash(f'Reader {reader_id} updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating reader: {str(e)}', 'danger')

    return redirect(url_for('readers.index'))

@readers_bp.route('/readers/delete/<reader_id>', methods=['POST'])
@login_required
def delete(reader_id):
    try:
        Database.query("DELETE FROM readers WHERE reader_id = %s", (reader_id,), commit=True)
        flash(f'Reader {reader_id} deleted successfully.', 'info')
    except Exception as e:
        flash(f'Error deleting reader: {str(e)}', 'danger')
    return redirect(url_for('readers.index'))

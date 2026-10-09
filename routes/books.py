from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required
from database.db import Database

books_bp = Blueprint('books', __name__)

@books_bp.route('/books', methods=['GET'])
@login_required
def index():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    language = request.args.get('language', '').strip()

    sql = "SELECT * FROM books WHERE 1=1"
    params = []

    if search:
        sql += " AND (book_id LIKE %s OR title LIKE %s OR author LIKE %s OR publisher LIKE %s)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param, search_param])

    if category:
        sql += " AND category = %s"
        params.append(category)

    if language:
        sql += " AND language = %s"
        params.append(language)

    sql += " ORDER BY book_id ASC"
    books = Database.query(sql, params)

    cat_rows = Database.query("SELECT DISTINCT category FROM books ORDER BY category")
    categories = [r['category'] for r in cat_rows if r['category']]

    lang_rows = Database.query("SELECT DISTINCT language FROM books ORDER BY language")
    languages = [r['language'] for r in lang_rows if r['language']]

    return render_template(
        'books.html',
        books=books,
        categories=categories,
        languages=languages,
        selected_search=search,
        selected_category=category,
        selected_language=language
    )

@books_bp.route('/books/add', methods=['POST'])
@login_required
def add():
    book_id = request.form.get('book_id', '').strip()
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    category = request.form.get('category', '').strip()
    publisher = request.form.get('publisher', '').strip()
    publication_year = request.form.get('publication_year', 2024)
    language = request.form.get('language', 'English').strip()
    description = request.form.get('description', '').strip()

    if not book_id or not title or not author or not category:
        flash('Book ID, Title, Author, and Category are required.', 'danger')
        return redirect(url_for('books.index'))

    existing = Database.query("SELECT book_id FROM books WHERE book_id = %s", (book_id,), fetchone=True)
    if existing:
        flash(f'Book ID {book_id} already exists. Please use a unique ID.', 'danger')
        return redirect(url_for('books.index'))

    try:
        Database.query(
            """INSERT INTO books (book_id, title, author, category, publisher, publication_year, language, description) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (book_id, title, author, category, publisher, int(publication_year), language, description),
            commit=True
        )
        flash(f'Book "{title}" ({book_id}) added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding book: {str(e)}', 'danger')

    return redirect(url_for('books.index'))

@books_bp.route('/books/edit/<book_id>', methods=['POST'])
@login_required
def edit(book_id):
    title = request.form.get('title', '').strip()
    author = request.form.get('author', '').strip()
    category = request.form.get('category', '').strip()
    publisher = request.form.get('publisher', '').strip()
    publication_year = request.form.get('publication_year', 2024)
    language = request.form.get('language', 'English').strip()
    description = request.form.get('description', '').strip()

    try:
        Database.query(
            """UPDATE books SET title=%s, author=%s, category=%s, publisher=%s, publication_year=%s, language=%s, description=%s 
               WHERE book_id=%s""",
            (title, author, category, publisher, int(publication_year), language, description, book_id),
            commit=True
        )
        flash(f'Book {book_id} updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating book: {str(e)}', 'danger')

    return redirect(url_for('books.index'))

@books_bp.route('/books/delete/<book_id>', methods=['POST'])
@login_required
def delete(book_id):
    try:
        Database.query("DELETE FROM books WHERE book_id = %s", (book_id,), commit=True)
        flash(f'Book {book_id} deleted successfully.', 'info')
    except Exception as e:
        flash(f'Error deleting book: {str(e)}', 'danger')
    return redirect(url_for('books.index'))

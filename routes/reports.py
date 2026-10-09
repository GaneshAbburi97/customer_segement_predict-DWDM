import csv
import io
from flask import Blueprint, render_template, request, Response
from routes.auth import login_required
from database.db import Database
from mining.classification import ReaderClassifier
from mining.clustering import ReaderClusterer
from mining.association_rules import AprioriMiner
from mining.text_mining import TextMiner

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
@login_required
def index():
    active_tab = request.args.get('tab', 'circulation')
    
    # 1. Circulation Data
    circ_summary = Database.query("""
        SELECT 
            COUNT(DISTINCT r.reader_key) AS total_readers,
            COUNT(DISTINCT b.book_key) AS total_books,
            COUNT(f.borrowing_id) AS total_borrowings,
            SUM(f.return_count) AS returned_count,
            SUM(CASE WHEN f.status != 'Returned' THEN 1 ELSE 0 END) AS pending_count,
            COALESCE(SUM(f.fine_amount), 0.0) AS total_fines,
            COALESCE(AVG(f.borrowing_duration), 0.0) AS avg_duration
        FROM fact_borrowing f
        JOIN dim_reader r ON f.reader_key = r.reader_key
        JOIN dim_book b ON f.book_key = b.book_key
    """, fetchone=True) or {}

    popular_books = Database.query("""
        SELECT b.title, b.category, b.author, COUNT(f.borrowing_id) as borrows
        FROM fact_borrowing f
        JOIN dim_book b ON f.book_key = b.book_key
        GROUP BY b.book_key, b.title, b.category, b.author
        ORDER BY borrows DESC
        LIMIT 10
    """)

    # 2. Classification & Clustering
    classification_res = ReaderClassifier.train_and_evaluate()
    clustering_res = ReaderClusterer.run_kmeans(k=3)

    # 3. Association Patterns
    pattern_res = AprioriMiner.mine_patterns(min_support=0.08, min_confidence=0.40, target_type="books")

    # 4. Text Mining
    freq_data = TextMiner.analyze_word_frequencies(top_n=20)
    tfidf_data = TextMiner.calculate_tfidf(top_n_terms=20)

    return render_template(
        'reports.html',
        active_tab=active_tab,
        circ_summary=circ_summary,
        popular_books=popular_books,
        classification_res=classification_res,
        clustering_res=clustering_res,
        pattern_res=pattern_res,
        freq_data=freq_data,
        tfidf_data=tfidf_data
    )

@reports_bp.route('/reports/export/<report_type>')
@login_required
def export_csv(report_type):
    output = io.StringIO()
    writer = csv.writer(output)

    if report_type == 'circulation':
        writer.writerow(['Book Title', 'Category', 'Author', 'Total Borrowings'])
        rows = Database.query("""
            SELECT b.title, b.category, b.author, COUNT(f.borrowing_id) as borrows
            FROM fact_borrowing f
            JOIN dim_book b ON f.book_key = b.book_key
            GROUP BY b.book_key, b.title, b.category, b.author
            ORDER BY borrows DESC
        """)
        for r in rows:
            writer.writerow([r['title'], r['category'], r['author'], r['borrows']])
        filename = 'circulation_report.csv'

    elif report_type == 'readers':
        writer.writerow(['Reader ID', 'Name', 'Department', 'Membership', 'Total Borrows', 'Avg Duration (Days)', 'Total Fine ($)', 'Classification', 'Cluster'])
        class_res = ReaderClassifier.train_and_evaluate()
        clust_res = ReaderClusterer.run_kmeans(k=3)
        
        clust_map = {r['reader_id']: r['cluster_name'] for r in clust_res.get('readers', [])}
        for r in class_res.get('readers', []):
            writer.writerow([
                r['reader_id'],
                r['reader_name'],
                r['department'],
                r['membership_type'],
                r['borrow_count'],
                round(r['avg_duration'], 1),
                round(r['total_fine'], 2),
                r.get('predicted_category', r.get('category')),
                clust_map.get(r['reader_id'], 'Unassigned')
            ])
        filename = 'reader_analysis_report.csv'

    elif report_type == 'patterns':
        writer.writerow(['Antecedent (If Borrowed)', 'Consequent (Also Borrowed)', 'Support (%)', 'Confidence (%)', 'Lift Score'])
        pat_res = AprioriMiner.mine_patterns(min_support=0.08, min_confidence=0.40)
        for rule in pat_res.get('rules', []):
            writer.writerow([
                rule['antecedent_str'],
                rule['consequent_str'],
                rule['support_pct'],
                rule['confidence_pct'],
                rule['lift']
            ])
        filename = 'borrowing_patterns_report.csv'

    elif report_type == 'text_mining':
        writer.writerow(['Term / Keyword', 'Corpus TF-IDF Score'])
        tfidf_res = TextMiner.calculate_tfidf(top_n_terms=50)
        for term in tfidf_res.get('top_tfidf_terms', []):
            writer.writerow([term['term'], term['tfidf_score']])
        filename = 'text_mining_report.csv'

    else:
        writer.writerow(['Invalid Report Type'])
        filename = 'report.csv'

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )

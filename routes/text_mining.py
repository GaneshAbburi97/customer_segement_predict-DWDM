from flask import Blueprint, render_template, request, jsonify
from routes.auth import login_required
from mining.text_mining import TextMiner

text_mining_bp = Blueprint('text_mining', __name__)

@text_mining_bp.route('/text-mining')
@login_required
def index():
    query = request.args.get('q', '').strip()
    
    # 1. Word Frequencies
    freq_data = TextMiner.analyze_word_frequencies(top_n=20)

    # 2. TF-IDF Matrix Scores
    tfidf_data = TextMiner.calculate_tfidf(top_n_terms=20)

    # 3. Search Results if query entered
    search_results = []
    if query:
        search_results = TextMiner.search_books_by_keyword(query)

    return render_template(
        'text_mining.html',
        freq_data=freq_data,
        tfidf_data=tfidf_data,
        search_results=search_results,
        query=query
    )

@text_mining_bp.route('/api/text-search')
@login_required
def search_api():
    query = request.args.get('q', '').strip()
    results = TextMiner.search_books_by_keyword(query)
    return jsonify({"query": query, "count": len(results), "results": results})

from flask import Blueprint, render_template, request, jsonify, flash
from routes.auth import login_required
from mining.classification import ReaderClassifier
from mining.clustering import ReaderClusterer
from mining.association_rules import AprioriMiner

mining_bp = Blueprint('mining', __name__)

# =============================================================================
# 1. READER CLASSIFICATION (DECISION TREE & RULE-BASED)
# =============================================================================
@mining_bp.route('/classification')
@login_required
def classification_view():
    results = ReaderClassifier.train_and_evaluate()
    return render_template('classification.html', results=results)

@mining_bp.route('/classification/predict', methods=['POST'])
@login_required
def predict_reader():
    try:
        age = float(request.form.get('age', 22))
        borrow_count = float(request.form.get('borrow_count', 5))
        avg_duration = float(request.form.get('avg_duration', 14))
        total_fine = float(request.form.get('total_fine', 0.0))
        late_returns = float(request.form.get('late_returns', 0))

        prediction_result = ReaderClassifier.predict_custom(age, borrow_count, avg_duration, total_fine, late_returns)
        return jsonify({"status": "SUCCESS", "result": prediction_result})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)})


# =============================================================================
# 2. READER CLUSTERING (K-MEANS)
# =============================================================================
@mining_bp.route('/clustering')
@login_required
def clustering_view():
    k = int(request.args.get('k', 3))
    results = ReaderClusterer.run_kmeans(k=k)
    return render_template('clustering.html', results=results, current_k=k)

@mining_bp.route('/clustering/run', methods=['POST'])
@login_required
def run_clustering_api():
    k = int(request.form.get('k', 3))
    results = ReaderClusterer.run_kmeans(k=k)
    return jsonify(results)


# =============================================================================
# 3. BORROWING PATTERNS (APRIORI ASSOCIATION RULES)
# =============================================================================
@mining_bp.route('/patterns')
@login_required
def patterns_view():
    min_support = float(request.args.get('min_support', 0.08))
    min_confidence = float(request.args.get('min_confidence', 0.40))
    target_type = request.args.get('target_type', 'books')

    results = AprioriMiner.mine_patterns(min_support=min_support, min_confidence=min_confidence, target_type=target_type)
    return render_template(
        'patterns.html',
        results=results,
        min_support=min_support,
        min_confidence=min_confidence,
        target_type=target_type
    )

@mining_bp.route('/patterns/mine', methods=['POST'])
@login_required
def mine_patterns_api():
    min_support = float(request.form.get('min_support', 0.08))
    min_confidence = float(request.form.get('min_confidence', 0.40))
    target_type = request.form.get('target_type', 'books')

    results = AprioriMiner.mine_patterns(min_support=min_support, min_confidence=min_confidence, target_type=target_type)
    return jsonify(results)

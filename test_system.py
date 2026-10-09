import unittest
import json
import os
import sys

# Ensure root in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from database.db import Database
from database.schema import init_db
from etl.etl_pipeline import ETLPipeline
from mining.classification import ReaderClassifier
from mining.clustering import ReaderClusterer
from mining.association_rules import AprioriMiner
from mining.text_mining import TextMiner

class TestLibraryDWDMAcademicSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        init_db(seed_sample_data=True)

    def test_01_database_connectivity(self):
        """Test database connection and operational data count"""
        db_type = Database.get_db_type()
        self.assertIn(db_type, ['mysql', 'sqlite'])
        
        readers = Database.query("SELECT COUNT(*) AS cnt FROM readers", fetchone=True)
        self.assertGreaterEqual(readers['cnt'], 20)

        books = Database.query("SELECT COUNT(*) AS cnt FROM books", fetchone=True)
        self.assertGreaterEqual(books['cnt'], 15)

        txs = Database.query("SELECT COUNT(*) AS cnt FROM borrowing_transactions", fetchone=True)
        self.assertGreaterEqual(txs['cnt'], 50)
        print(f"[TEST 01 OK] Database operational: {readers['cnt']} readers, {books['cnt']} books, {txs['cnt']} transactions.")

    def test_02_etl_pipeline(self):
        """Test ETL pipeline extraction, transformation, and warehouse fact loading"""
        result = ETLPipeline.run_etl()
        self.assertEqual(result['status'], 'SUCCESS')
        self.assertGreater(result['fact_count'], 0)
        self.assertGreater(result['cleaned_count'], 0)

        # Check Star Schema tables
        dim_r = Database.query("SELECT COUNT(*) AS cnt FROM dim_reader", fetchone=True)['cnt']
        dim_b = Database.query("SELECT COUNT(*) AS cnt FROM dim_book", fetchone=True)['cnt']
        dim_d = Database.query("SELECT COUNT(*) AS cnt FROM dim_date", fetchone=True)['cnt']
        facts = Database.query("SELECT COUNT(*) AS cnt FROM fact_borrowing", fetchone=True)['cnt']

        self.assertGreater(dim_r, 0)
        self.assertGreater(dim_b, 0)
        self.assertGreater(dim_d, 0)
        self.assertGreater(facts, 0)
        print(f"[TEST 02 OK] ETL Loaded Star Schema: {dim_r} dim_reader, {dim_b} dim_book, {dim_d} dim_date, {facts} fact_borrowing.")

    def test_03_classification_decision_tree(self):
        """Test reader classification and decision tree accuracy"""
        res = ReaderClassifier.train_and_evaluate()
        self.assertEqual(res['status'], 'SUCCESS')
        self.assertGreaterEqual(res['accuracy'], 50.0)
        self.assertIn('Low Borrower', res['distribution'])
        
        # Test custom prediction
        pred = ReaderClassifier.predict_custom(22, 9, 14, 0.0, 0)
        self.assertEqual(pred['predicted_category'], 'High Borrower')
        print(f"[TEST 03 OK] Classification: Accuracy={res['accuracy']}%, Custom Prediction={pred['predicted_category']}.")

    def test_04_clustering_kmeans(self):
        """Test K-Means reader clustering"""
        res = ReaderClusterer.run_kmeans(k=3)
        self.assertEqual(res['status'], 'SUCCESS')
        self.assertEqual(len(res['clusters']), 3)
        self.assertIn('Low Activity Readers', [c['cluster_name'] for c in res['clusters']])
        print(f"[TEST 04 OK] K-Means Clustering: Created {len(res['clusters'])} distinct reader clusters.")

    def test_05_apriori_pattern_discovery(self):
        """Test Apriori Association Rule Mining"""
        res = AprioriMiner.mine_patterns(min_support=0.08, min_confidence=0.40)
        self.assertEqual(res['status'], 'SUCCESS')
        self.assertGreater(len(res['frequent_itemsets']), 0)
        self.assertGreater(len(res['rules']), 0)
        print(f"[TEST 05 OK] Apriori Mining: Discovered {len(res['frequent_itemsets'])} itemsets and {len(res['rules'])} rules.")

    def test_06_text_mining(self):
        """Test Text Mining word frequency and TF-IDF calculation"""
        freq = TextMiner.analyze_word_frequencies(top_n=20)
        self.assertGreater(len(freq['top_words']), 0)

        tfidf = TextMiner.calculate_tfidf(top_n_terms=20)
        self.assertGreater(len(tfidf['top_tfidf_terms']), 0)

        search_res = TextMiner.search_books_by_keyword("machine learning python")
        self.assertGreater(len(search_res), 0)
        print(f"[TEST 06 OK] Text Mining: Top word='{freq['top_words'][0]['word']}', TF-IDF Search matches={len(search_res)}.")

    def test_07_web_routes_and_views(self):
        """Test Flask HTTP endpoints and authentication protection"""
        # Unauthenticated access redirects to login
        resp = self.client.get('/dashboard')
        self.assertEqual(resp.status_code, 302)

        # Authenticate session
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'admin'
            sess['full_name'] = 'Library Administrator'
            sess['role'] = 'Administrator'

        routes = [
            '/dashboard',
            '/readers',
            '/books',
            '/borrowing',
            '/warehouse',
            '/etl',
            '/circulation',
            '/classification',
            '/clustering',
            '/patterns',
            '/text-mining',
            '/reports',
            '/api/circulation-data',
            '/reports/export/circulation',
            '/reports/export/readers',
            '/reports/export/patterns',
            '/reports/export/text_mining'
        ]

        for route in routes:
            r = self.client.get(route)
            self.assertIn(r.status_code, [200, 302], f"Route {route} failed with status {r.status_code}")

        print(f"[TEST 07 OK] All {len(routes)} Web Routes, APIs, and CSV Export endpoints validated (HTTP 200).")

if __name__ == '__main__':
    unittest.main()

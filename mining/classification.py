import os
import sys
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db import Database

class ReaderClassifier:
    _model = None
    _feature_names = ['age', 'borrow_count', 'avg_duration', 'total_fine', 'late_returns']
    _target_classes = ['Low Borrower', 'Medium Borrower', 'High Borrower']

    @staticmethod
    def get_reader_features():
        """
        Extracts reader behavior features from warehouse / operational data:
        - age
        - total borrow_count
        - avg borrowing_duration
        - total fine_amount
        - late_returns count
        """
        # Query fact_borrowing joined with dim_reader or operational tables fallback
        sql = """
        SELECT 
            r.reader_id,
            r.reader_name,
            r.age,
            r.gender,
            r.department,
            r.membership_type,
            COALESCE(COUNT(f.borrowing_id), 0) AS borrow_count,
            COALESCE(AVG(f.borrowing_duration), 0.0) AS avg_duration,
            COALESCE(SUM(f.fine_amount), 0.0) AS total_fine,
            COALESCE(SUM(CASE WHEN f.fine_amount > 0 OR f.status = 'Overdue' THEN 1 ELSE 0 END), 0) AS late_returns
        FROM dim_reader r
        LEFT JOIN fact_borrowing f ON r.reader_key = f.reader_key
        GROUP BY r.reader_id, r.reader_name, r.age, r.gender, r.department, r.membership_type
        """
        rows = Database.query(sql)
        if not rows:
            # Fallback to operational tables if warehouse not yet loaded
            sql_op = """
            SELECT 
                r.reader_id,
                r.name AS reader_name,
                r.age,
                r.gender,
                r.department,
                r.membership_type,
                COALESCE(COUNT(t.transaction_id), 0) AS borrow_count,
                COALESCE(AVG(14), 0.0) AS avg_duration,
                COALESCE(SUM(t.fine), 0.0) AS total_fine,
                COALESCE(SUM(CASE WHEN t.fine > 0 OR t.status = 'Overdue' THEN 1 ELSE 0 END), 0) AS late_returns
            FROM readers r
            LEFT JOIN borrowing_transactions t ON r.reader_id = t.reader_id
            GROUP BY r.reader_id, r.name, r.age, r.gender, r.department, r.membership_type
            """
            rows = Database.query(sql_op)

        df = pd.DataFrame(rows)
        if df.empty:
            return df

        # Assign rule-based ground-truth classification
        # 1-3 -> Low Borrower, 4-7 -> Medium Borrower, 8+ -> High Borrower
        def assign_category(count):
            if count <= 3:
                return 'Low Borrower'
            elif count <= 7:
                return 'Medium Borrower'
            else:
                return 'High Borrower'

        df['category'] = df['borrow_count'].apply(assign_category)
        return df

    @classmethod
    def train_and_evaluate(cls):
        """
        Trains a Decision Tree Classifier on reader behavior features
        and returns accuracy, confusion matrix, report, and classified readers.
        """
        df = cls.get_reader_features()
        if df.empty or len(df) < 5:
            return {
                "status": "EMPTY",
                "message": "Insufficient reader transaction data to perform classification.",
                "readers": [],
                "accuracy": 0.0,
                "confusion_matrix": [],
                "report": {},
                "feature_importances": {}
            }

        X = df[cls._feature_names].values
        y = df['category'].values

        # If data is small, train on all and test on stratified split or cross-val
        test_size = 0.25 if len(df) >= 20 else 0.2
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y if len(np.unique(y)) > 1 else None
            )
        except Exception:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

        clf = DecisionTreeClassifier(criterion='gini', max_depth=4, random_state=42)
        clf.fit(X_train, y_train)
        cls._model = clf

        y_pred = clf.predict(X_test)
        acc = float(accuracy_score(y_test, y_pred))

        # Full predictions on dataset
        all_pred = clf.predict(X)
        df['predicted_category'] = all_pred
        df['match'] = df['category'] == df['predicted_category']

        # Confusion Matrix
        labels = ['Low Borrower', 'Medium Borrower', 'High Borrower']
        cm = confusion_matrix(y_test, y_pred, labels=labels).tolist()

        # Classification Report
        report_dict = classification_report(y_test, y_pred, labels=labels, output_dict=True, zero_division=0)

        # Feature importances
        importances = {name: round(float(imp), 4) for name, imp in zip(cls._feature_names, clf.feature_importances_)}

        # Category distribution counts
        distribution = df['category'].value_counts().to_dict()

        return {
            "status": "SUCCESS",
            "accuracy": round(acc * 100, 2),
            "confusion_matrix": cm,
            "matrix_labels": labels,
            "classification_report": report_dict,
            "feature_importances": importances,
            "distribution": distribution,
            "readers": df.to_dict(orient='records')
        }

    @classmethod
    def predict_custom(cls, age, borrow_count, avg_duration, total_fine, late_returns):
        """
        Predicts classification category for arbitrary user input features.
        """
        if cls._model is None:
            cls.train_and_evaluate()

        if cls._model is None:
            # Fallback rule
            if borrow_count <= 3:
                return 'Low Borrower'
            elif borrow_count <= 7:
                return 'Medium Borrower'
            else:
                return 'High Borrower'

        input_data = np.array([[float(age), float(borrow_count), float(avg_duration), float(total_fine), float(late_returns)]])
        prediction = cls._model.predict(input_data)[0]
        probabilities = {}
        if hasattr(cls._model, "predict_proba"):
            probs = cls._model.predict_proba(input_data)[0]
            for cls_name, prob in zip(cls._model.classes_, probs):
                probabilities[cls_name] = round(float(prob) * 100, 1)

        return {
            "predicted_category": prediction,
            "probabilities": probabilities
        }

if __name__ == "__main__":
    res = ReaderClassifier.train_and_evaluate()
    print("Classification Accuracy:", res["accuracy"])
    print("Distribution:", res["distribution"])
    print("Predict (Age=22, Borrows=9, Duration=14, Fine=0, Late=0):", ReaderClassifier.predict_custom(22, 9, 14, 0, 0))

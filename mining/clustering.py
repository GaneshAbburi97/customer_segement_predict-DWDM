import os
import sys
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db import Database

class ReaderClusterer:
    @staticmethod
    def get_clustering_data():
        """
        Retrieves aggregated behavioral metrics for all readers.
        """
        sql = """
        SELECT 
            r.reader_id,
            r.reader_name,
            r.age,
            r.gender,
            r.department,
            r.membership_type,
            COALESCE(COUNT(f.borrowing_id), 0) AS total_books_borrowed,
            COALESCE(AVG(f.borrowing_duration), 0.0) AS avg_borrowing_duration,
            COALESCE(SUM(f.fine_amount), 0.0) AS total_fine,
            COALESCE(SUM(CASE WHEN f.fine_amount > 0 OR f.status = 'Overdue' THEN 1 ELSE 0 END), 0) AS late_returns
        FROM dim_reader r
        LEFT JOIN fact_borrowing f ON r.reader_key = f.reader_key
        GROUP BY r.reader_id, r.reader_name, r.age, r.gender, r.department, r.membership_type
        """
        rows = Database.query(sql)
        if not rows:
            # Fallback to operational tables
            sql_op = """
            SELECT 
                r.reader_id,
                r.name AS reader_name,
                r.age,
                r.gender,
                r.department,
                r.membership_type,
                COALESCE(COUNT(t.transaction_id), 0) AS total_books_borrowed,
                COALESCE(AVG(14), 0.0) AS avg_borrowing_duration,
                COALESCE(SUM(t.fine), 0.0) AS total_fine,
                COALESCE(SUM(CASE WHEN t.fine > 0 OR t.status = 'Overdue' THEN 1 ELSE 0 END), 0) AS late_returns
            FROM readers r
            LEFT JOIN borrowing_transactions t ON r.reader_id = t.reader_id
            GROUP BY r.reader_id, r.name, r.age, r.gender, r.department, r.membership_type
            """
            rows = Database.query(sql_op)

        return pd.DataFrame(rows)

    @classmethod
    def run_kmeans(cls, k=3):
        """
        Runs K-Means Clustering on reader profiles using standardized features.
        Returns cluster assignments, profiles, centroids, and scatter plot points.
        """
        df = cls.get_clustering_data()
        if df.empty or len(df) < k:
            return {
                "status": "EMPTY",
                "message": "Insufficient reader data to form clusters.",
                "k": k,
                "clusters": [],
                "readers": [],
                "scatter_data": []
            }

        feature_cols = ['total_books_borrowed', 'avg_borrowing_duration', 'total_fine', 'late_returns']
        X = df[feature_cols].values

        # Feature Standardization
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # K-Means Model
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        df['cluster_id'] = labels

        # Rank clusters by average borrow count to assign intuitive, meaningful names
        cluster_means = df.groupby('cluster_id')['total_books_borrowed'].mean().sort_values()
        sorted_cluster_ids = cluster_means.index.tolist()

        cluster_names = {}
        if k == 3:
            cluster_names[sorted_cluster_ids[0]] = "Low Activity Readers"
            cluster_names[sorted_cluster_ids[1]] = "Regular Readers"
            cluster_names[sorted_cluster_ids[2]] = "Highly Active Readers"
        else:
            for idx, c_id in enumerate(sorted_cluster_ids):
                cluster_names[c_id] = f"Reader Cluster {idx + 1}"

        df['cluster_name'] = df['cluster_id'].map(cluster_names)

        # 2D Dimension Reduction for Scatter Plot Visualization (using PCA)
        pca = PCA(n_components=2, random_state=42)
        coords = pca.fit_transform(X_scaled)
        df['pca_x'] = np.round(coords[:, 0], 3)
        df['pca_y'] = np.round(coords[:, 1], 3)

        # Cluster Summaries
        cluster_summary = []
        for c_id in sorted_cluster_ids:
            c_df = df[df['cluster_id'] == c_id]
            name = cluster_names[c_id]
            cluster_summary.append({
                "cluster_id": int(c_id),
                "cluster_name": name,
                "reader_count": int(len(c_df)),
                "avg_borrowing_count": round(float(c_df['total_books_borrowed'].mean()), 2),
                "avg_duration": round(float(c_df['avg_borrowing_duration'].mean()), 2),
                "avg_fine": round(float(c_df['total_fine'].mean()), 2),
                "avg_late_returns": round(float(c_df['late_returns'].mean()), 2),
                "top_department": c_df['department'].mode()[0] if not c_df.empty else "N/A"
            })

        # Format scatter data for Chart.js
        scatter_by_cluster = {}
        for c_id, name in cluster_names.items():
            c_df = df[df['cluster_id'] == c_id]
            points = []
            for _, r in c_df.iterrows():
                points.append({
                    "x": round(float(r['total_books_borrowed']), 2),
                    "y": round(float(r['avg_borrowing_duration']), 2),
                    "reader_id": r['reader_id'],
                    "reader_name": r['reader_name'],
                    "fine": float(r['total_fine']),
                    "department": r['department']
                })
            scatter_by_cluster[name] = points

        return {
            "status": "SUCCESS",
            "k": k,
            "clusters": cluster_summary,
            "scatter_by_cluster": scatter_by_cluster,
            "readers": df.to_dict(orient='records')
        }

if __name__ == "__main__":
    result = ReaderClusterer.run_kmeans(k=3)
    print("Cluster Summary:")
    for c in result["clusters"]:
        print(f" - {c['cluster_name']}: {c['reader_count']} readers | Avg Borrows: {c['avg_borrowing_count']}")

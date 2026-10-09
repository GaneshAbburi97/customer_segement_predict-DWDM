import os
import sys
import re
import string
from collections import Counter
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db import Database

# Built-in academic stop words for zero external network download dependency
DEFAULT_STOP_WORDS = set([
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'aren\'t', 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'can\'t', 'cannot',
    'could', 'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down', 'during', 'each',
    'few', 'for', 'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t', 'have', 'haven\'t', 'having', 'he', 'he\'d',
    'he\'ll', 'he\'s', 'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'how\'s', 'i',
    'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it', 'it\'s', 'its', 'itself', 'let\'s',
    'me', 'more', 'most', 'mustn\'t', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or',
    'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shan\'t', 'she', 'she\'d', 'she\'ll',
    'she\'s', 'should', 'shouldn\'t', 'so', 'some', 'such', 'than', 'that', 'that\'s', 'the', 'their', 'theirs',
    'them', 'themselves', 'then', 'there', 'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re', 'they\'ve',
    'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll',
    'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'when', 'when\'s', 'where', 'where\'s', 'which',
    'while', 'who', 'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t', 'you', 'you\'d',
    'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours', 'yourself', 'yourselves', 'also', 'covering', 'handbook', 'textbook',
    'guide', 'essential', 'principles', 'core', 'introduction', 'step', 'practical', 'modern', 'using'
])

class TextMiner:
    @staticmethod
    def preprocess_text(text):
        """
        Tokenizes text, strips punctuation, converts to lowercase, and filters out stop words.
        """
        if not text:
            return []
        
        # Lowercase
        text = text.lower()
        # Remove punctuation and special characters
        text = re.sub(r'[' + re.escape(string.punctuation) + r'0-9]', ' ', text)
        # Tokenize by whitespace
        tokens = text.split()
        # Remove stop words and short tokens (len < 3)
        cleaned_tokens = [t for t in tokens if t not in DEFAULT_STOP_WORDS and len(t) >= 3]
        return cleaned_tokens

    @classmethod
    def get_books_corpus(cls):
        """
        Fetches all books with their titles, categories, and descriptions.
        """
        rows = Database.query("SELECT book_id, title, author, category, description FROM books")
        if not rows:
            return []
        
        corpus = []
        for r in rows:
            combined_text = f"{r['title']} {r['category']} {r.get('description') or ''}"
            tokens = cls.preprocess_text(combined_text)
            corpus.append({
                "book_id": r["book_id"],
                "title": r["title"],
                "author": r["author"],
                "category": r["category"],
                "description": r.get("description") or "",
                "combined_text": combined_text,
                "cleaned_text": " ".join(tokens),
                "tokens": tokens
            })
        return corpus

    @classmethod
    def analyze_word_frequencies(cls, top_n=20):
        """
        Calculates most frequent words across all book titles and descriptions.
        """
        corpus = cls.get_books_corpus()
        if not corpus:
            return {"top_words": [], "word_cloud_data": []}

        all_tokens = []
        for doc in corpus:
            all_tokens.extend(doc["tokens"])

        counts = Counter(all_tokens)
        top_words = counts.most_common(top_n)

        formatted_top = [{"word": word.capitalize(), "count": count} for word, count in top_words]
        
        # For Word Cloud visualization
        word_cloud = [{"text": word.capitalize(), "size": min(48, max(14, count * 5))} for word, count in counts.most_common(40)]

        return {
            "total_words": len(all_tokens),
            "unique_words": len(counts),
            "top_words": formatted_top,
            "word_cloud_data": word_cloud
        }

    @classmethod
    def calculate_tfidf(cls, top_n_terms=20):
        """
        Calculates TF-IDF (Term Frequency-Inverse Document Frequency) matrices and top ranking terms.
        """
        corpus = cls.get_books_corpus()
        if not corpus or len(corpus) < 2:
            return {"top_tfidf_terms": [], "book_tfidf_profiles": []}

        docs_text = [doc["cleaned_text"] for doc in corpus]
        
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(docs_text)
        feature_names = vectorizer.get_feature_names_out()

        # Mean TF-IDF score per term across all documents
        mean_tfidf = np.array(tfidf_matrix.mean(axis=0)).flatten()
        top_indices = mean_tfidf.argsort()[::-1][:top_n_terms]

        top_tfidf_terms = []
        for idx in top_indices:
            top_tfidf_terms.append({
                "term": feature_names[idx].capitalize(),
                "tfidf_score": round(float(mean_tfidf[idx]), 4)
            })

        # Top TF-IDF terms per book
        book_profiles = []
        for i, doc in enumerate(corpus):
            row_vector = tfidf_matrix[i].toarray().flatten()
            top_book_indices = row_vector.argsort()[::-1][:5]
            top_terms_for_book = [
                {"term": feature_names[idx].capitalize(), "score": round(float(row_vector[idx]), 3)}
                for idx in top_book_indices if row_vector[idx] > 0
            ]
            book_profiles.append({
                "book_id": doc["book_id"],
                "title": doc["title"],
                "category": doc["category"],
                "top_keywords": top_terms_for_book
            })

        return {
            "top_tfidf_terms": top_tfidf_terms,
            "book_tfidf_profiles": book_profiles
        }

    @classmethod
    def search_books_by_keyword(cls, query_str):
        """
        Uses TF-IDF Vectorizer and Cosine Similarity to find books most relevant to the user's query.
        """
        if not query_str or not query_str.strip():
            return []

        corpus = cls.get_books_corpus()
        if not corpus:
            return []

        docs_text = [doc["cleaned_text"] for doc in corpus]
        cleaned_query = " ".join(cls.preprocess_text(query_str))
        if not cleaned_query:
            cleaned_query = query_str.lower()

        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform(docs_text)
            query_vector = vectorizer.transform([cleaned_query])
            similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

            results = []
            for i, sim in enumerate(similarities):
                if sim > 0:
                    results.append({
                        "book_id": corpus[i]["book_id"],
                        "title": corpus[i]["title"],
                        "author": corpus[i]["author"],
                        "category": corpus[i]["category"],
                        "description": corpus[i]["description"],
                        "similarity_score": round(float(sim) * 100, 1)
                    })

            results.sort(key=lambda x: x["similarity_score"], reverse=True)
            return results
        except Exception:
            # Substring fallback
            results = []
            q_lower = query_str.lower()
            for doc in corpus:
                if q_lower in doc["combined_text"].lower():
                    results.append({
                        "book_id": doc["book_id"],
                        "title": doc["title"],
                        "author": doc["author"],
                        "category": doc["category"],
                        "description": doc["description"],
                        "similarity_score": 85.0
                    })
            return results

if __name__ == "__main__":
    freq = TextMiner.analyze_word_frequencies()
    print("Top Word Frequencies:", freq["top_words"][:5])
    tfidf = TextMiner.calculate_tfidf()
    print("Top TF-IDF Terms:", tfidf["top_tfidf_terms"][:5])
    search_res = TextMiner.search_books_by_keyword("machine learning python")
    print(f"Search Results for 'machine learning python': Found {len(search_res)} matches.")

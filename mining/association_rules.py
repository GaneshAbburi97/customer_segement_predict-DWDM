import os
import sys
from itertools import combinations
from collections import defaultdict
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db import Database

class AprioriMiner:
    @staticmethod
    def get_transactions_basket():
        """
        Groups borrowed books by reader (or borrowing session/date) to create transaction baskets.
        Returns both book title baskets and category baskets.
        """
        # Query fact_borrowing or borrowing_transactions
        sql = """
        SELECT 
            r.reader_id,
            b.title AS book_title,
            b.category AS book_category,
            f.date_key
        FROM fact_borrowing f
        JOIN dim_reader r ON f.reader_key = r.reader_key
        JOIN dim_book b ON f.book_key = b.book_key
        ORDER BY r.reader_id, f.date_key
        """
        rows = Database.query(sql)
        if not rows:
            # Fallback
            sql_op = """
            SELECT 
                t.reader_id,
                b.title AS book_title,
                b.category AS book_category,
                t.borrow_date AS date_key
            FROM borrowing_transactions t
            JOIN books b ON t.book_id = b.book_id
            ORDER BY t.reader_id, t.borrow_date
            """
            rows = Database.query(sql_op)

        if not rows:
            return [], []

        # Basket by Reader Profile (all books borrowed by a reader across sessions)
        reader_baskets = defaultdict(set)
        reader_cat_baskets = defaultdict(set)

        for r in rows:
            reader_baskets[r["reader_id"]].add(r["book_title"])
            reader_cat_baskets[r["reader_id"]].add(r["book_category"])

        book_baskets = [list(items) for items in reader_baskets.values() if len(items) >= 1]
        category_baskets = [list(items) for items in reader_cat_baskets.values() if len(items) >= 1]

        return book_baskets, category_baskets

    @staticmethod
    def run_apriori(baskets, min_support=0.08, min_confidence=0.40, max_len=3):
        """
        Pure Apriori Algorithm Implementation:
        1. Generates 1-itemsets and prunes by min_support.
        2. Generates k-itemsets candidates, counts frequencies, prunes.
        3. Derives Association Rules (A -> B) and calculates Support, Confidence, and Lift.
        """
        total_transactions = len(baskets)
        if total_transactions == 0:
            return {"frequent_itemsets": [], "rules": []}

        # Step 1: Count 1-itemsets
        item_counts = defaultdict(int)
        for basket in baskets:
            for item in set(basket):
                item_counts[frozenset([item])] += 1

        # Prune 1-itemsets
        min_count = max(1, int(min_support * total_transactions))
        frequent_itemsets = {}
        
        current_l = {itemset: count for itemset, count in item_counts.items() if count >= min_count}
        k = 1

        while current_l and k <= max_len:
            frequent_itemsets.update(current_l)
            k += 1

            # Generate candidate (k)-itemsets from current_l
            items_in_prev = list(set().union(*current_l.keys()))
            candidate_counts = defaultdict(int)

            for combo in combinations(items_in_prev, k):
                candidate_set = frozenset(combo)
                # Check subset frequency (Apriori principle)
                valid = True
                for sub in combinations(combo, k - 1):
                    if frozenset(sub) not in current_l:
                        valid = False
                        break
                if not valid:
                    continue

                for basket in baskets:
                    if candidate_set.issubset(basket):
                        candidate_counts[candidate_set] += 1

            current_l = {itemset: count for itemset, count in candidate_counts.items() if count >= min_count}

        # Format Frequent Itemsets Output
        frequent_list = []
        for itemset, count in frequent_itemsets.items():
            supp = count / total_transactions
            frequent_list.append({
                "itemset": list(itemset),
                "itemset_str": " + ".join(sorted(itemset)),
                "size": len(itemset),
                "support_count": count,
                "support": round(supp, 4),
                "support_pct": round(supp * 100, 1)
            })

        frequent_list.sort(key=lambda x: (x["size"], x["support"]), reverse=True)

        # Step 2: Generate Association Rules (Antecedent -> Consequent)
        rules = []
        for itemset, count in frequent_itemsets.items():
            if len(itemset) < 2:
                continue

            itemset_support = count / total_transactions
            items = list(itemset)

            # Generate all non-empty subsets as antecedents
            for r in range(1, len(items)):
                for antecedent_tuple in combinations(items, r):
                    antecedent = frozenset(antecedent_tuple)
                    consequent = itemset.difference(antecedent)

                    if not consequent:
                        continue

                    antecedent_count = frequent_itemsets.get(antecedent, 0)
                    consequent_count = frequent_itemsets.get(consequent, 0)

                    if antecedent_count == 0 or consequent_count == 0:
                        continue

                    antecedent_support = antecedent_count / total_transactions
                    consequent_support = consequent_count / total_transactions

                    confidence = itemset_support / antecedent_support
                    lift = confidence / consequent_support if consequent_support > 0 else 0

                    if confidence >= min_confidence:
                        rules.append({
                            "antecedent": list(antecedent),
                            "consequent": list(consequent),
                            "antecedent_str": ", ".join(sorted(antecedent)),
                            "consequent_str": ", ".join(sorted(consequent)),
                            "rule_str": f"{', '.join(sorted(antecedent))} -> {', '.join(sorted(consequent))}",
                            "support": round(itemset_support, 4),
                            "support_pct": round(itemset_support * 100, 1),
                            "confidence": round(confidence, 4),
                            "confidence_pct": round(confidence * 100, 1),
                            "lift": round(lift, 3)
                        })

        rules.sort(key=lambda x: (x["lift"], x["confidence"]), reverse=True)

        return {
            "total_transactions": total_transactions,
            "min_support": min_support,
            "min_confidence": min_confidence,
            "frequent_itemsets": frequent_list,
            "rules": rules
        }

    @classmethod
    def mine_patterns(cls, min_support=0.08, min_confidence=0.40, target_type="books"):
        """
        Mines frequent itemsets and association rules for either books or categories.
        """
        book_baskets, category_baskets = cls.get_transactions_basket()
        baskets = book_baskets if target_type == "books" else category_baskets
        
        if not baskets:
            return {
                "status": "EMPTY",
                "message": "No transaction baskets available.",
                "frequent_itemsets": [],
                "rules": [],
                "target_type": target_type
            }

        mining_results = cls.run_apriori(baskets, min_support=min_support, min_confidence=min_confidence)
        mining_results["status"] = "SUCCESS"
        mining_results["target_type"] = target_type
        return mining_results

if __name__ == "__main__":
    res = AprioriMiner.mine_patterns(min_support=0.08, min_confidence=0.40, target_type="books")
    print(f"Apriori Results: Found {len(res['frequent_itemsets'])} frequent itemsets and {len(res['rules'])} rules.")
    for r in res['rules'][:5]:
        print(f" * Rule: {r['rule_str']} | Supp: {r['support_pct']}% | Conf: {r['confidence_pct']}% | Lift: {r['lift']}")

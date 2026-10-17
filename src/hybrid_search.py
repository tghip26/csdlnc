"""
Module: hybrid_search.py
Mục đích: Triển khai động cơ tìm kiếm lai (Hybrid Search Engine) kết hợp:
1. Sparse Lexical Search (Okapi BM25 Probabilistic Relevance Framework)
2. Dense Semantic Search (HNSW / Cosine Similarity)
3. Thuật toán hợp nhất thứ hạng (Ranking Fusion: Reciprocal Rank Fusion RRF & Linear Combination)
4. Bộ chỉ số đo lường chuẩn Information Retrieval (NDCG@K, MRR@K, Recall@K)
"""

import re
import math
import collections
import numpy as np

def tokenize(text):
    """Tách từ đơn giản và chuẩn hóa chữ thường"""
    return re.findall(r"\b\w+\b", text.lower())

class BM25Index:
    """Chỉ mục ngược và thuật toán xếp hạng Okapi BM25 (Robertson & Zaragoza 2009)"""
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.doc_len = []
        self.avg_doc_len = 0.0
        self.doc_count = 0
        self.inverted_index = collections.defaultdict(list) # term -> list of (doc_id, tf)
        self.idf = {}
        
    def fit(self, corpus_texts):
        self.doc_count = len(corpus_texts)
        total_len = 0
        df = collections.defaultdict(int)
        
        for doc_id, text in enumerate(corpus_texts):
            tokens = tokenize(text)
            length = len(tokens)
            self.doc_len.append(length)
            total_len += length
            
            tf_map = collections.Counter(tokens)
            for term, count in tf_map.items():
                self.inverted_index[term].append((doc_id, count))
                df[term] += 1
                
        self.avg_doc_len = total_len / max(1, self.doc_count)
        
        # Tính chỉ số nghịch đảo IDF
        for term, freq in df.items():
            # Công thức chuẩn BM25 IDF: ln((N - n + 0.5) / (n + 0.5) + 1)
            self.idf[term] = math.log((self.doc_count - freq + 0.5) / (freq + 0.5) + 1.0)

    def search(self, query_text, top_k=10):
        query_terms = tokenize(query_text)
        scores = collections.defaultdict(float)
        
        for term in query_terms:
            if term not in self.inverted_index:
                continue
            idf_val = self.idf[term]
            for doc_id, tf in self.inverted_index[term]:
                doc_len_d = self.doc_len[doc_id]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len_d / self.avg_doc_len))
                scores[doc_id] += idf_val * (numerator / denominator)
                
        if not scores:
            return np.array([], dtype=int), np.array([])
            
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        doc_ids = np.array([x[0] for x in ranked], dtype=int)
        score_vals = np.array([x[1] for x in ranked], dtype=np.float32)
        return doc_ids, score_vals


class HybridSearchEngine:
    """
    Động cơ tìm kiếm lai kết hợp Dense và Sparse với hai chiến lược hợp nhất:
    1. RRF (Reciprocal Rank Fusion - Cormack et al. 2009)
    2. Linear Normalized Combination (Bruch et al. 2023)
    """
    def __init__(self, bm25_index, vector_index, rrf_k=60):
        self.bm25_index = bm25_index
        self.vector_index = vector_index
        self.rrf_k = rrf_k

    def search_rrf(self, query_text, query_vector, top_k=10, candidate_k=50):
        # Lấy danh sách ứng viên từ cả hai nhánh
        bm25_ids, bm25_scores = self.bm25_index.search(query_text, top_k=candidate_k)
        vec_ids, vec_scores = self.vector_index.search(query_vector, top_k=candidate_k)
        
        rrf_scores = collections.defaultdict(float)
        
        # Hợp nhất nhánh BM25
        for rank, doc_id in enumerate(bm25_ids):
            rrf_scores[doc_id] += 1.0 / (self.rrf_k + (rank + 1))
            
        # Hợp nhất nhánh Vector
        for rank, doc_id in enumerate(vec_ids):
            rrf_scores[doc_id] += 1.0 / (self.rrf_k + (rank + 1))
            
        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        final_ids = np.array([x[0] for x in sorted_docs], dtype=int)
        final_scores = np.array([x[1] for x in sorted_docs], dtype=np.float32)
        return final_ids, final_scores

    def search_linear(self, query_text, query_vector, alpha=0.5, top_k=10, candidate_k=50):
        """
        Kết hợp tuyến tính có chuẩn hóa Min-Max:
        Score = alpha * Dense_norm + (1 - alpha) * BM25_norm
        """
        bm25_ids, bm25_scores = self.bm25_index.search(query_text, top_k=candidate_k)
        vec_ids, vec_scores = self.vector_index.search(query_vector, top_k=candidate_k)
        
        # Chuẩn hóa Min-Max cho BM25
        norm_bm25 = {}
        if len(bm25_scores) > 0:
            min_b, max_b = np.min(bm25_scores), np.max(bm25_scores)
            range_b = max_b - min_b if max_b > min_b else 1.0
            for doc_id, sc in zip(bm25_ids, bm25_scores):
                norm_bm25[doc_id] = (sc - min_b) / range_b
                
        # Chuẩn hóa Min-Max cho Vector
        norm_vec = {}
        if len(vec_scores) > 0:
            min_v, max_v = np.min(vec_scores), np.max(vec_scores)
            range_v = max_v - min_v if max_v > min_v else 1.0
            for doc_id, sc in zip(vec_ids, vec_scores):
                norm_vec[doc_id] = (sc - min_v) / range_v
                
        # Tập hợp tất cả ứng viên
        all_candidates = set(norm_bm25.keys()).union(set(norm_vec.keys()))
        combined = []
        for doc_id in all_candidates:
            s_bm25 = norm_bm25.get(doc_id, 0.0)
            s_vec = norm_vec.get(doc_id, 0.0)
            final_score = alpha * s_vec + (1.0 - alpha) * s_bm25
            combined.append((doc_id, final_score))
            
        combined.sort(key=lambda x: x[1], reverse=True)
        top_res = combined[:top_k]
        final_ids = np.array([x[0] for x in top_res], dtype=int)
        final_scores = np.array([x[1] for x in top_res], dtype=np.float32)
        return final_ids, final_scores


# === CÁC HÀM TÍNH TOÁN CHỈ SỐ ĐỐI CHUẨN THÔNG TIN (IR EVALUATION METRICS) ===

def compute_recall_at_k(retrieved_ids, ground_truth_set, k=10):
    """Tỉ lệ tài liệu liên quan được thu hồi trong Top-K"""
    if len(ground_truth_set) == 0:
        return 0.0
    top_k_retrieved = set(retrieved_ids[:k])
    intersect = top_k_retrieved.intersection(ground_truth_set)
    return len(intersect) / float(len(ground_truth_set))

def compute_mrr_at_k(retrieved_ids, ground_truth_set, k=10):
    """Mean Reciprocal Rank trong Top-K"""
    for rank, doc_id in enumerate(retrieved_ids[:k]):
        if doc_id in ground_truth_set:
            return 1.0 / (rank + 1)
    return 0.0

def compute_ndcg_at_k(retrieved_ids, ground_truth_rel_dict, k=10):
    """Normalized Discounted Cumulative Gain tại vị trí K"""
    dcg = 0.0
    for rank, doc_id in enumerate(retrieved_ids[:k]):
        rel = ground_truth_rel_dict.get(doc_id, 0.0)
        dcg += (2.0**rel - 1.0) / math.log2(rank + 2)
        
    # Tính IDCG lý tưởng
    ideal_rels = sorted(ground_truth_rel_dict.values(), reverse=True)[:k]
    idcg = 0.0
    for rank, rel in enumerate(ideal_rels):
        idcg += (2.0**rel - 1.0) / math.log2(rank + 2)
        
    if idcg == 0.0:
        return 0.0
    return dcg / idcg

"""
Module: filter_pushdown.py
Mục đích: Đề xuất và thực nghiệm các chiến lược Tìm kiếm Vector có điều kiện lọc (Filtered Vector Search):
1. Pre-filtering (Tiền lọc bằng chỉ mục quan hệ trước khi quét vector)
2. Post-filtering (Hậu lọc sau khi lấy Top-K từ chỉ mục vector)
3. Single-Stage Iterative Predicate-Aware Traversal (Đề xuất: Duyệt đồ thị nhận biết vị từ kiểu ACORN / Gupta et al. 2024)
4. Cost-Based Query Optimizer (Bộ tối ưu hóa chi phí tự động chọn kế hoạch thực thi dựa trên Selectivity)
"""

import time
import heapq
import numpy as np

class FilterEvaluator:
    """Đánh giá điều kiện lọc trên metadata của tài liệu"""
    @staticmethod
    def match(doc, filter_spec):
        if not filter_spec:
            return True
        for key, val in filter_spec.items():
            if key == "category" and val != "all":
                if doc.get("category") != val:
                    return False
            elif key == "min_year":
                if doc.get("year", 0) < val:
                    return False
            elif key == "access_level" and val != "all":
                if doc.get("access_level") != val:
                    return False
        return True


class FilteredSearchFramework:
    def __init__(self, documents, vectors, hnsw_index):
        self.documents = documents
        self.vectors = vectors
        self.hnsw_index = hnsw_index
        self.doc_count = len(documents)

    def pre_filtering_search(self, query_vec, filter_spec, top_k=10):
        """
        Chiến lược 1: Pre-filtering
        - Bước 1: Quét và lọc các bản ghi thỏa mãn điều kiện metadata.
        - Bước 2: Quét tuần tự tính khoảng cách vector trên tập ứng viên đã lọc.
        """
        start = time.time()
        # Bước 1: Lọc metadata
        valid_indices = []
        for idx, doc in enumerate(self.documents):
            if FilterEvaluator.match(doc, filter_spec):
                valid_indices.append(idx)
                
        if len(valid_indices) == 0:
            return np.array([]), np.array([]), time.time() - start
            
        # Bước 2: Quét vector trên tập thỏa mãn
        cand_indices = np.array(valid_indices, dtype=int)
        cand_vecs = self.vectors[cand_indices]
        q_norm = query_vec / (np.linalg.norm(query_vec) + 1e-9)
        sims = np.dot(cand_vecs, q_norm)
        
        k = min(top_k, len(valid_indices))
        top_cand = np.argpartition(sims, -k)[-k:]
        sorted_cand = top_cand[np.argsort(-sims[top_cand])]
        latency = time.time() - start
        return cand_indices[sorted_cand], sims[sorted_cand], latency

    def post_filtering_search(self, query_vec, filter_spec, top_k=10, oversample_factor=10):
        """
        Chiến lược 2: Post-filtering
        - Bước 1: Lấy Top-(K * factor) từ chỉ mục HNSW không có điều kiện lọc.
        - Bước 2: Loại bỏ các ứng viên không thỏa điều kiện cho đến khi đủ K.
        """
        start = time.time()
        fetch_k = top_k * oversample_factor
        cand_ids, cand_sims = self.hnsw_index.search(query_vec, top_k=fetch_k, ef=fetch_k * 2)
        
        filtered_ids = []
        filtered_sims = []
        for doc_id, sim in zip(cand_ids, cand_sims):
            doc = self.documents[doc_id]
            if FilterEvaluator.match(doc, filter_spec):
                filtered_ids.append(doc_id)
                filtered_sims.append(sim)
                if len(filtered_ids) >= top_k:
                    break
                    
        latency = time.time() - start
        return np.array(filtered_ids, dtype=int), np.array(filtered_sims, dtype=np.float32), latency

    def iterative_ingraph_filtering(self, query_vec, filter_spec, top_k=10, max_budget=200):
        """
        Chiến lược 3 (Đề xuất): Single-Stage Predicate-Aware Graph Traversal
        - Duyệt trực tiếp trên đồ thị HNSW.
        - Tiếp tục bước nhảy qua các node không thỏa vị từ (để duy trì đường liên thông),
          nhưng chỉ ghi nhận vào kết quả Top-K nếu node thỏa mãn vị từ.
        """
        start = time.time()
        q_norm = query_vec / (np.linalg.norm(query_vec) + 1e-9)
        
        if self.hnsw_index.enter_point is None:
            return np.array([]), np.array([]), time.time() - start
            
        curr_obj = self.hnsw_index.enter_point
        # Định tuyến nhanh từ các tầng cao xuống tầng đáy 0
        for lc in range(self.hnsw_index.max_level, 0, -1):
            curr_node = self.hnsw_index.nodes[curr_obj]
            if lc < len(curr_node.friends):
                best_d = 1.0 - np.dot(q_norm, self.vectors[curr_obj])
                for nb in curr_node.friends[lc]:
                    d = 1.0 - np.dot(q_norm, self.vectors[nb])
                    if d < best_d:
                        best_d = d
                        curr_obj = nb
                        
        # Tầng đáy 0: Duyệt có kiểm tra vị từ
        visited = {curr_obj}
        v_queue = [] # Min-heap: (dist, doc_id)
        result_heap = [] # Max-heap lưu trữ (-sim, doc_id) cho Top-K thỏa vị từ
        
        curr_d = 1.0 - np.dot(q_norm, self.vectors[curr_obj])
        heapq.heappush(v_queue, (curr_d, curr_obj))
        
        steps = 0
        while len(v_queue) > 0 and steps < max_budget:
            steps += 1
            d_curr, u_id = heapq.heappop(v_queue)
            sim_u = 1.0 - d_curr
            
            # Kiểm tra vị từ
            doc = self.documents[u_id]
            if FilterEvaluator.match(doc, filter_spec):
                if len(result_heap) < top_k:
                    heapq.heappush(result_heap, (-sim_u, u_id))
                else:
                    if sim_u > -result_heap[0][0]:
                        heapq.heapreplace(result_heap, (-sim_u, u_id))
                        
            # Mở rộng láng giềng
            node = self.hnsw_index.nodes[u_id]
            if 0 < len(node.friends):
                for nb in node.friends[0]:
                    if nb not in visited:
                        visited.add(nb)
                        d_nb = 1.0 - np.dot(q_norm, self.vectors[nb])
                        heapq.heappush(v_queue, (d_nb, nb))
                        
        sorted_res = sorted([(-neg_s, d_id) for neg_s, d_id in result_heap], reverse=True)
        res_ids = np.array([d_id for _, d_id in sorted_res], dtype=int)
        res_sims = np.array([sim for sim, _ in sorted_res], dtype=np.float32)
        latency = time.time() - start
        return res_ids, res_sims, latency

    def adaptive_optimizer_search(self, query_vec, filter_spec, top_k=10, sample_size=200):
        """
        Chiến lược 4: Cost-Based Adaptive Optimizer
        - Ước lượng độ chọn lọc Selectivity sigma trên mẫu thống kê.
        - Nếu sigma < 2%: Chọn Pre-filtering.
        - Nếu 2% <= sigma <= 25%: Chọn Đề xuất Iterative In-Graph Filtering.
        - Nếu sigma > 25%: Chọn Post-filtering với oversampling thích ứng.
        """
        # Ước tính độ chọn lọc sigma qua mẫu ngẫu nhiên (Sample Scan)
        sample_indices = np.random.choice(self.doc_count, size=sample_size, replace=False)
        match_count = sum(1 for idx in sample_indices if FilterEvaluator.match(self.documents[idx], filter_spec))
        est_selectivity = match_count / float(sample_size)
        
        if est_selectivity < 0.02:
            plan = "Pre-filtering (Scan on tiny subset)"
            ids, sims, lat = self.pre_filtering_search(query_vec, filter_spec, top_k)
        elif est_selectivity <= 0.25:
            plan = "In-Graph Iterative Filtering (ACORN-style)"
            ids, sims, lat = self.iterative_ingraph_filtering(query_vec, filter_spec, top_k)
        else:
            plan = "Post-filtering (HNSW Over-sampling)"
            oversample = max(2, int(2.0 / (est_selectivity + 1e-4)))
            ids, sims, lat = self.post_filtering_search(query_vec, filter_spec, top_k, oversample_factor=oversample)
            
        return ids, sims, lat, plan, est_selectivity

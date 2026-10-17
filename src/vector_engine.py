"""
Module: vector_engine.py
Mục đích: Triển khai và đối chuẩn các cấu trúc chỉ mục Vector:
1. Exact Flat Scan (Brute-force baseline - Chuẩn đối sánh chính xác tuyệt đối 100% Recall)
2. Inverted File Index (IVF-Flat cơ bản)
3. Hierarchical Navigable Small World (HNSW graph-based index tối ưu hóa)
"""

import sys
import time
import heapq
import numpy as np

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class FlatIndex:
    """Chỉ mục quét tuần tự chính xác (Exact Flat Scan)"""
    def __init__(self, dim, metric="cosine"):
        self.dim = dim
        self.metric = metric
        self.vectors = None
        
    def fit(self, vectors):
        start = time.time()
        self.vectors = vectors.astype(np.float32)
        if self.metric == "cosine":
            norms = np.linalg.norm(self.vectors, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            self.vectors = self.vectors / norms
        build_time = time.time() - start
        return build_time

    def search(self, query, top_k=10):
        if self.metric == "cosine":
            q_norm = query / (np.linalg.norm(query) + 1e-9)
            sims = np.dot(self.vectors, q_norm)
            k = min(top_k, len(sims))
            top_idx = np.argpartition(sims, -k)[-k:]
            sorted_idx = top_idx[np.argsort(-sims[top_idx])]
            return sorted_idx, sims[sorted_idx]
        else:
            diff = self.vectors - query
            dists = np.sum(diff * diff, axis=1)
            k = min(top_k, len(dists))
            top_idx = np.argpartition(dists, k)[:k]
            sorted_idx = top_idx[np.argsort(dists[top_idx])]
            return sorted_idx, dists[sorted_idx]


class IVFIndex:
    """Chỉ mục phân cụm danh sách đảo (Inverted File Index - IVF)"""
    def __init__(self, dim, nlist=32, nprobe=4, metric="cosine"):
        self.dim = dim
        self.nlist = nlist
        self.nprobe = nprobe
        self.metric = metric
        self.centroids = None
        self.inv_lists = {i: [] for i in range(nlist)}
        self.vectors = None

    def fit(self, vectors):
        start = time.time()
        self.vectors = vectors.astype(np.float32)
        n = len(vectors)
        actual_nlist = min(self.nlist, max(2, n // 20))
        self.nlist = actual_nlist
        self.inv_lists = {i: [] for i in range(self.nlist)}
        
        np.random.seed(42)
        init_indices = np.random.choice(n, size=self.nlist, replace=False)
        self.centroids = self.vectors[init_indices].copy()
        
        # 3 vòng lặp K-Means tối ưu
        for _ in range(3):
            sims = np.dot(self.vectors, self.centroids.T)
            labels = np.argmax(sims, axis=1)
            for c in range(self.nlist):
                members = self.vectors[labels == c]
                if len(members) > 0:
                    mean_vec = np.mean(members, axis=0)
                    self.centroids[c] = mean_vec / (np.linalg.norm(mean_vec) + 1e-9)
                    
        sims = np.dot(self.vectors, self.centroids.T)
        labels = np.argmax(sims, axis=1)
        for i, lbl in enumerate(labels):
            self.inv_lists[lbl].append(i)
            
        build_time = time.time() - start
        return build_time

    def search(self, query, top_k=10):
        q_norm = query / (np.linalg.norm(query) + 1e-9)
        c_sims = np.dot(self.centroids, q_norm)
        actual_probe = min(self.nprobe, self.nlist)
        probe_centroids = np.argpartition(c_sims, -actual_probe)[-actual_probe:]
        
        candidates = []
        for c in probe_centroids:
            candidates.extend(self.inv_lists[c])
            
        if len(candidates) == 0:
            return np.array([], dtype=int), np.array([])
            
        cand_indices = np.array(candidates, dtype=int)
        cand_vectors = self.vectors[cand_indices]
        sims = np.dot(cand_vectors, q_norm)
        
        k = min(top_k, len(candidates))
        top_cand = np.argpartition(sims, -k)[-k:]
        sorted_cand = top_cand[np.argsort(-sims[top_cand])]
        return cand_indices[sorted_cand], sims[sorted_cand]


class HNSWNode:
    __slots__ = ['id', 'level', 'friends']
    def __init__(self, doc_id, level):
        self.id = doc_id
        self.level = level
        self.friends = [[] for _ in range(level + 1)]


class HNSWIndex:
    """
    Chỉ mục đồ thị phân tầng (Hierarchical Navigable Small World - HNSW)
    Tối ưu hóa bộ nhớ và tốc độ duyệt
    """
    def __init__(self, dim, M=12, ef_construction=32, ef_search=24, mL=None):
        self.dim = dim
        self.M = M
        self.max_M0 = 2 * M
        self.ef_construction = ef_construction
        self.ef_search = ef_search
        self.mL = mL if mL is not None else 1.0 / np.log(M)
        self.nodes = {}
        self.enter_point = None
        self.max_level = -1
        self.vectors = None

    def _get_random_level(self):
        r = np.random.uniform(1e-9, 1.0)
        return int(-np.log(r) * self.mL)

    def fit(self, vectors):
        start = time.time()
        self.vectors = vectors.astype(np.float32)
        norms = np.linalg.norm(self.vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.vectors = self.vectors / norms
        
        np.random.seed(42)
        n = len(vectors)
        for i in range(n):
            self.insert(i)
            
        build_time = time.time() - start
        return build_time

    def insert(self, doc_id):
        vec_q = self.vectors[doc_id]
        level = self._get_random_level()
        node = HNSWNode(doc_id, level)
        self.nodes[doc_id] = node

        if self.enter_point is None:
            self.enter_point = doc_id
            self.max_level = level
            return

        curr_obj = self.enter_point
        curr_dist = 1.0 - np.dot(vec_q, self.vectors[curr_obj])

        # Giai đoạn 1: Greedy search từ max_level xuống level + 1
        for lc in range(self.max_level, level, -1):
            changed = True
            while changed:
                changed = False
                curr_node = self.nodes[curr_obj]
                if lc < len(curr_node.friends) and len(curr_node.friends[lc]) > 0:
                    nbs = curr_node.friends[lc]
                    nb_vecs = self.vectors[nbs]
                    dists = 1.0 - np.dot(nb_vecs, vec_q)
                    min_idx = np.argmin(dists)
                    if dists[min_idx] < curr_dist:
                        curr_dist = dists[min_idx]
                        curr_obj = nbs[min_idx]
                        changed = True

        # Giai đoạn 2: Tại các tầng lc <= level
        ep = [curr_obj]
        top_level_loop = min(self.max_level, level)
        for lc in range(top_level_loop, -1, -1):
            candidates = self._search_layer(vec_q, ep, self.ef_construction, lc)
            m_max = self.max_M0 if lc == 0 else self.M
            selected_neighbors = [c_id for _, c_id in sorted(candidates)[:self.M]]
            
            node.friends[lc] = selected_neighbors
            for neighbor_id in selected_neighbors:
                nb_node = self.nodes[neighbor_id]
                if lc < len(nb_node.friends):
                    nb_node.friends[lc].append(doc_id)
                    if len(nb_node.friends[lc]) > m_max:
                        # Thu gọn danh sách láng giềng
                        nbs = nb_node.friends[lc]
                        nb_vecs = self.vectors[nbs]
                        dists = 1.0 - np.dot(nb_vecs, self.vectors[neighbor_id])
                        best_indices = np.argsort(dists)[:m_max]
                        nb_node.friends[lc] = [nbs[k] for k in best_indices]
                        
            ep = [c_id for _, c_id in candidates]

        if level > self.max_level:
            self.max_level = level
            self.enter_point = doc_id

    def _search_layer(self, vec_q, ep_list, ef, lc):
        visited = set(ep_list)
        v_queue = []
        w_set = []

        for ep in ep_list:
            d = 1.0 - np.dot(vec_q, self.vectors[ep])
            heapq.heappush(v_queue, (d, ep))
            heapq.heappush(w_set, (-d, ep))

        while len(v_queue) > 0:
            d_curr, c_curr = heapq.heappop(v_queue)
            furthest_d = -w_set[0][0]
            if d_curr > furthest_d:
                break

            curr_node = self.nodes[c_curr]
            if lc < len(curr_node.friends) and len(curr_node.friends[lc]) > 0:
                unvisited_nbs = [nb for nb in curr_node.friends[lc] if nb not in visited]
                if len(unvisited_nbs) > 0:
                    for nb in unvisited_nbs:
                        visited.add(nb)
                    nb_vecs = self.vectors[unvisited_nbs]
                    nb_dists = 1.0 - np.dot(nb_vecs, vec_q)
                    for d_nb, nb in zip(nb_dists, unvisited_nbs):
                        furthest_d = -w_set[0][0]
                        if d_nb < furthest_d or len(w_set) < ef:
                            heapq.heappush(v_queue, (d_nb, nb))
                            heapq.heappush(w_set, (-d_nb, nb))
                            if len(w_set) > ef:
                                heapq.heappop(w_set)

        results = [(-neg_d, c_id) for neg_d, c_id in w_set]
        results.sort()
        return results

    def search(self, query, top_k=10, ef=None):
        if self.enter_point is None:
            return np.array([], dtype=int), np.array([])
            
        ef_val = ef if ef is not None else max(self.ef_search, top_k)
        q_norm = query / (np.linalg.norm(query) + 1e-9)
        
        curr_obj = self.enter_point
        curr_dist = 1.0 - np.dot(q_norm, self.vectors[curr_obj])

        for lc in range(self.max_level, 0, -1):
            changed = True
            while changed:
                changed = False
                curr_node = self.nodes[curr_obj]
                if lc < len(curr_node.friends) and len(curr_node.friends[lc]) > 0:
                    nbs = curr_node.friends[lc]
                    nb_vecs = self.vectors[nbs]
                    dists = 1.0 - np.dot(nb_vecs, q_norm)
                    min_idx = np.argmin(dists)
                    if dists[min_idx] < curr_dist:
                        curr_dist = dists[min_idx]
                        curr_obj = nbs[min_idx]
                        changed = True

        candidates = self._search_layer(q_norm, [curr_obj], ef_val, 0)
        top_candidates = candidates[:top_k]
        
        ids = np.array([c_id for _, c_id in top_candidates], dtype=int)
        sims = np.array([1.0 - d for d, _ in top_candidates], dtype=np.float32)
        return ids, sims

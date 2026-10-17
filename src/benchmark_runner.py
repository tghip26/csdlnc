"""
Script: benchmark_runner.py
Mục đích: Chạy toàn bộ chu trình thực nghiệm tự động đo kiểm hiệu năng CSDL:
1. Đo lường Kế hoạch Thực thi (EXPLAIN QUERY PLAN) và Thời gian chạy ở Trạng thái cơ sở (Stage 0).
2. Đo lường sau khi thêm Chỉ mục đơn (Stage 1).
3. Đo lường sau khi thêm Chỉ mục phức hợp & Covering Index (Stage 2 & Stage 3).
4. Đo lường Tác động của Phân vùng Bảng và Loại trừ Phân vùng (Partition Pruning).
5. Xuất báo cáo số liệu so sánh định lượng phục vụ Bài báo khoa học và Báo cáo môn học.
"""

import os
import sys
import json
import time
import sqlite3

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.append(os.path.dirname(__file__))
from query_workload import QUERIES
from index_tuner import IndexTuner
from partitioning_engine import PartitioningEngine

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "ecommerce_real.db")
OUT_JSON = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "tuning_results.json")
os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)

def measure_query(conn, sql, repeats=3):
    cursor = conn.cursor()
    # 1. Lấy Execution Plan
    cursor.execute("EXPLAIN QUERY PLAN " + sql)
    plan_rows = cursor.fetchall()
    plan_str = " | ".join([f"{p[3]}" for p in plan_rows])

    # 2. Đo thời gian thực thi trung bình
    latencies = []
    for _ in range(repeats):
        t0 = time.time()
        cursor.execute(sql)
        cursor.fetchall()
        latencies.append((time.time() - t0) * 1000.0) # ms
        
    avg_lat = sum(latencies) / len(latencies)
    return avg_lat, plan_str

def run_benchmark():
    if not os.path.exists(DB_PATH):
        print(f"[-] Không tìm thấy file CSDL tại {DB_PATH}. Hãy chạy download_and_prepare_data.py trước.", flush=True)
        return

    print("="*85, flush=True)
    print("CHƯƠNG TRÌNH THỰC NGHIỆM ĐO KIỂM & TINH CHỈNH HIỆU NĂNG CƠ SỞ DỮ LIỆU THỰC TẾ", flush=True)
    print("="*85, flush=True)

    tuner = IndexTuner(DB_PATH)
    partitioner = PartitioningEngine(DB_PATH)

    results = {
        "queries": {},
        "partitioning": {}
    }

    # =========================================================================
    # GIAI ĐOẠN 1: ĐO LƯỜNG TRẠNG THÁI CƠ SỞ CHƯA CÓ CHỈ MỤC (STAGE 0: UNINDEXED)
    # =========================================================================
    print("\n[*] 1. Đang đo lường Trạng thái Cơ sở (Stage 0: Unindexed Baseline)...", flush=True)
    tuner.drop_all_custom_indexes()
    conn = sqlite3.connect(DB_PATH)
    
    stage0_metrics = {}
    for q_id, q_data in QUERIES.items():
        lat, plan = measure_query(conn, q_data["sql"], repeats=2)
        stage0_metrics[q_id] = {"latency_ms": lat, "plan": plan}
        print(f"    * {q_id}: {lat:>8.2f} ms | Plan: {plan[:65]}...", flush=True)
    conn.close()

    # =========================================================================
    # GIAI ĐOẠN 2: ĐO LƯỜNG VỚI CHỈ MỤC ĐƠN TRÊN KHÓA NGOẠI (STAGE 1: SINGLE-COLUMN)
    # =========================================================================
    print("\n[*] 2. Đang áp dụng Chỉ mục đơn (Stage 1: Single-Column B-Trees)...", flush=True)
    tuner.apply_stage_1_single_column()
    conn = sqlite3.connect(DB_PATH)
    
    stage1_metrics = {}
    for q_id, q_data in QUERIES.items():
        lat, plan = measure_query(conn, q_data["sql"], repeats=3)
        stage1_metrics[q_id] = {"latency_ms": lat, "plan": plan}
        print(f"    * {q_id}: {lat:>8.2f} ms | Plan: {plan[:65]}...", flush=True)
    conn.close()

    # =========================================================================
    # GIAI ĐOẠN 3: ĐO LƯỜNG VỚI COMPOSITE & COVERING INDEXES (STAGE 3: ADVANCED TUNED)
    # =========================================================================
    print("\n[*] 3. Đang áp dụng Chỉ mục Phức hợp & Covering Indexes (Stage 3: Advanced Tuned)...", flush=True)
    tuner.apply_stage_3_partial_and_covering()
    conn = sqlite3.connect(DB_PATH)
    
    stage3_metrics = {}
    for q_id, q_data in QUERIES.items():
        lat, plan = measure_query(conn, q_data["sql"], repeats=3)
        stage3_metrics[q_id] = {"latency_ms": lat, "plan": plan}
        print(f"    * {q_id}: {lat:>8.2f} ms | Plan: {plan[:65]}...", flush=True)
    conn.close()

    # =========================================================================
    # GIAI ĐOẠN 4: ĐO LƯỜNG THỰC NGHIỆM PHÂN VÙNG BẢNG & PARTITION PRUNING
    # =========================================================================
    print("\n[*] 4. Đang thiết lập và đối chuẩn Phân vùng Bảng (Table Partitioning)...", flush=True)
    part_counts = partitioner.setup_partitioned_orders()
    print(f"    [+] Đã phân vùng bảng orders: 2016 ({part_counts['2016']:,d} dòng) | 2017 ({part_counts['2017']:,d} dòng) | 2018 ({part_counts['2018']:,d} dòng)", flush=True)
    part_res = partitioner.benchmark_partition_pruning()
    results["partitioning"] = part_res
    print(f"    [+] Bảng không phân vùng: {part_res['unpartitioned_latency_ms']:.2f} ms", flush=True)
    print(f"    [+] Phân vùng có Pruning: {part_res['partitioned_latency_ms']:.2f} ms (Nhanh hơn {part_res['speedup_percentage']:.1f}%)", flush=True)

    # =========================================================================
    # TỔNG HỢP VÀ IN BẢNG BÁO CÁO ĐỐI SÁNH
    # =========================================================================
    print("\n" + "="*95, flush=True)
    print("BẢNG TỔNG HỢP SO SÁNH HIỆU NĂNG TRUY VẤN TRƯỚC VÀ SAU KHI TINH CHỈNH:", flush=True)
    print("="*95, flush=True)
    print(f"{'Mã':<4} | {'Truy vấn':<32} | {'Chưa Index (ms)':<16} | {'Single Index (ms)':<18} | {'Covering Index (ms)':<20} | {'Tốc độ tăng'}", flush=True)
    print("-" * 105, flush=True)

    for q_id, q_data in QUERIES.items():
        t0 = stage0_metrics[q_id]["latency_ms"]
        t1 = stage1_metrics[q_id]["latency_ms"]
        t3 = stage3_metrics[q_id]["latency_ms"]
        speedup = t0 / t3 if t3 > 0 else 1.0
        
        results["queries"][q_id] = {
            "title": q_data["title"],
            "stage0_unindexed_ms": t0,
            "stage0_plan": stage0_metrics[q_id]["plan"],
            "stage1_single_ms": t1,
            "stage1_plan": stage1_metrics[q_id]["plan"],
            "stage3_advanced_ms": t3,
            "stage3_plan": stage3_metrics[q_id]["plan"],
            "speedup_factor": speedup
        }
        
        print(f"{q_id:<4} | {q_data['title'][:32]:<32} | {t0:<16.2f} | {t1:<18.2f} | {t3:<20.2f} | {speedup:>6.1f}x", flush=True)

    print("="*95, flush=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[+] Đã lưu toàn bộ số liệu đo đạc thực nghiệm chi tiết vào: {OUT_JSON}", flush=True)

if __name__ == "__main__":
    run_benchmark()

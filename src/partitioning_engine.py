"""
Module: partitioning_engine.py
Mục đích: Thiết lập và đánh giá kỹ thuật Phân vùng Bảng (Table Partitioning)
và Loại trừ Phân vùng (Partition Pruning) trên bảng đơn hàng lớn (orders).
"""

import time
import sqlite3

class PartitioningEngine:
    def __init__(self, db_path):
        self.db_path = db_path

    def setup_partitioned_orders(self):
        """
        Tạo cấu trúc phân vùng theo dải năm (Range Partitioning by Year):
        - orders_2016 (Các đơn hàng năm 2016)
        - orders_2017 (Các đơn hàng năm 2017)
        - orders_2018 (Các đơn hàng năm 2018)
        - View v_orders_partitioned hợp nhất qua UNION ALL
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tạo các bảng phân vùng
        cursor.execute("DROP TABLE IF EXISTS orders_2016;")
        cursor.execute("DROP TABLE IF EXISTS orders_2017;")
        cursor.execute("DROP TABLE IF EXISTS orders_2018;")
        cursor.execute("DROP VIEW IF EXISTS v_orders_partitioned;")

        schema_sql = """
        CREATE TABLE {tbl} (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            order_status TEXT,
            order_purchase_timestamp TEXT,
            order_approved_at TEXT,
            order_delivered_carrier_date TEXT,
            order_delivered_customer_date TEXT,
            order_estimated_delivery_date TEXT
        );
        """
        cursor.execute(schema_sql.format(tbl="orders_2016"))
        cursor.execute(schema_sql.format(tbl="orders_2017"))
        cursor.execute(schema_sql.format(tbl="orders_2018"))

        # Phân bổ dữ liệu thực tế vào từng phân vùng
        cursor.execute("INSERT INTO orders_2016 SELECT * FROM orders WHERE order_purchase_timestamp < '2017-01-01';")
        cursor.execute("INSERT INTO orders_2017 SELECT * FROM orders WHERE order_purchase_timestamp >= '2017-01-01' AND order_purchase_timestamp < '2018-01-01';")
        cursor.execute("INSERT INTO orders_2018 SELECT * FROM orders WHERE order_purchase_timestamp >= '2018-01-01';")

        # Tạo chỉ mục cục bộ trên từng phân vùng (Local Partitioned Indexes)
        cursor.execute("CREATE INDEX idx_orders2016_ts ON orders_2016(order_purchase_timestamp);")
        cursor.execute("CREATE INDEX idx_orders2017_ts ON orders_2017(order_purchase_timestamp);")
        cursor.execute("CREATE INDEX idx_orders2018_ts ON orders_2018(order_purchase_timestamp);")

        # Tạo View phân vùng với ràng buộc kiểm tra
        cursor.execute("""
        CREATE VIEW v_orders_partitioned AS
            SELECT * FROM orders_2016 WHERE order_purchase_timestamp < '2017-01-01'
            UNION ALL
            SELECT * FROM orders_2017 WHERE order_purchase_timestamp >= '2017-01-01' AND order_purchase_timestamp < '2018-01-01'
            UNION ALL
            SELECT * FROM orders_2018 WHERE order_purchase_timestamp >= '2018-01-01';
        """)

        conn.commit()
        
        # Thống kê số lượng dòng trong từng phân vùng
        cursor.execute("SELECT COUNT(*) FROM orders_2016;")
        c2016 = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM orders_2017;")
        c2017 = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM orders_2018;")
        c2018 = cursor.fetchone()[0]
        conn.close()

        return {"2016": c2016, "2017": c2017, "2018": c2018}

    def benchmark_partition_pruning(self):
        """
        Đo đạc và đối chứng:
        - Quét trên Bảng không phân vùng (Non-partitioned orders table)
        - Quét trên Phân vùng được cắt tỉa (Pruned Partition: Chỉ quét orders_2017, bỏ qua 2016 và 2018)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        date_start = "2017-06-01 00:00:00"
        date_end = "2017-08-31 23:59:59"

        # 1. Truy vấn trên bảng không phân vùng (Đo lường kế hoạch và thời gian)
        sql_unpartitioned = f"""
        SELECT COUNT(order_id), AVG(julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp))
        FROM orders
        WHERE order_purchase_timestamp BETWEEN '{date_start}' AND '{date_end}';
        """
        cursor.execute("EXPLAIN QUERY PLAN " + sql_unpartitioned)
        plan_unpartitioned = cursor.fetchall()

        times_unpart = []
        for _ in range(5):
            t0 = time.time()
            cursor.execute(sql_unpartitioned)
            cursor.fetchall()
            times_unpart.append((time.time() - t0) * 1000.0)
        avg_unpart = sum(times_unpart) / len(times_unpart)

        # 2. Truy vấn trực tiếp vào phân vùng mục tiêu (Pruned Partition Scan)
        sql_partitioned = f"""
        SELECT COUNT(order_id), AVG(julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp))
        FROM orders_2017
        WHERE order_purchase_timestamp BETWEEN '{date_start}' AND '{date_end}';
        """
        cursor.execute("EXPLAIN QUERY PLAN " + sql_partitioned)
        plan_partitioned = cursor.fetchall()

        times_part = []
        for _ in range(5):
            t0 = time.time()
            cursor.execute(sql_partitioned)
            cursor.fetchall()
            times_part.append((time.time() - t0) * 1000.0)
        avg_part = sum(times_part) / len(times_part)

        conn.close()

        speedup = ((avg_unpart - avg_part) / avg_unpart) * 100.0 if avg_unpart > 0 else 0.0

        return {
            "unpartitioned_latency_ms": avg_unpart,
            "partitioned_latency_ms": avg_part,
            "speedup_percentage": speedup,
            "unpartitioned_plan": [str(p) for p in plan_unpartitioned],
            "partitioned_plan": [str(p) for p in plan_partitioned]
        }

"""
Module: index_tuner.py
Mục đích: Quản lý các tầng tinh chỉnh chỉ mục vật lý (Physical Index Tuning Stages):
- Stage 0: Unindexed Baseline (Chỉ có khóa chính mặc định, quét toàn bảng SCAN TABLE).
- Stage 1: Single-Column B-Trees (Chỉ mục đơn trên các khóa ngoại và cột lọc vị từ).
- Stage 2: Composite B-Trees (Chỉ mục đa cột tối ưu theo thứ tự lọc và kết nối).
- Stage 3: Partial & Covering Indexes (Chỉ mục có điều kiện WHERE và Covering Index cho Index-Only Scan).
"""

import sqlite3

class IndexTuner:
    def __init__(self, db_path):
        self.db_path = db_path

    def _execute_sql(self, sql_commands):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for cmd in sql_commands:
            cmd = cmd.strip()
            if cmd:
                cursor.execute(cmd)
        conn.commit()
        # Chạy ANALYZE để bộ tối ưu hóa CBO cập nhật thống kê sqlite_stat1
        cursor.execute("ANALYZE;")
        conn.commit()
        conn.close()

    def drop_all_custom_indexes(self):
        """Xóa toàn bộ các chỉ mục tùy chỉnh, đưa CSDL về trạng thái cơ sở (Stage 0)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'index' AND name NOT LIKE 'sqlite_autoindex%';")
        indexes = cursor.fetchall()
        for (idx_name,) in indexes:
            cursor.execute(f"DROP INDEX IF EXISTS {idx_name};")
        conn.commit()
        cursor.execute("ANALYZE;")
        conn.commit()
        conn.close()

    def apply_stage_1_single_column(self):
        """Stage 1: Tạo các chỉ mục đơn (Single-Column B-Tree) trên các khóa ngoại và cột lọc"""
        self.drop_all_custom_indexes()
        sql = [
            "CREATE INDEX idx_orders_customer ON orders(customer_id);",
            "CREATE INDEX idx_orders_status ON orders(order_status);",
            "CREATE INDEX idx_orders_ts ON orders(order_purchase_timestamp);",
            "CREATE INDEX idx_items_product ON order_items(product_id);",
            "CREATE INDEX idx_items_seller ON order_items(seller_id);",
            "CREATE INDEX idx_reviews_order ON order_reviews(order_id);",
            "CREATE INDEX idx_payments_order ON order_payments(order_id);"
        ]
        self._execute_sql(sql)

    def apply_stage_2_composite(self):
        """Stage 2: Thêm các chỉ mục phức hợp (Composite B-Tree Indexes) đa thuộc tính"""
        self.apply_stage_1_single_column()
        sql = [
            # Tối ưu cho Q1 và Q2: lọc trạng thái + thời gian
            "CREATE INDEX idx_orders_status_ts ON orders(order_status, order_purchase_timestamp, customer_id);",
            # Tối ưu cho kết nối items + products
            "CREATE INDEX idx_items_order_prod ON order_items(order_id, product_id, price);",
            # Tối ưu cho Q3: lọc review_score và kết nối order_id
            "CREATE INDEX idx_reviews_score_order ON order_reviews(review_score, order_id);"
        ]
        self._execute_sql(sql)

    def apply_stage_3_partial_and_covering(self):
        """Stage 3: Áp dụng Partial Indexing và Covering Indexing tối ưu cao cấp"""
        self.apply_stage_2_composite()
        sql = [
            # Partial Index: Chỉ lập chỉ mục các đơn hàng 'delivered' (chiếm 97% dữ liệu)
            "CREATE INDEX idx_partial_orders_delivered ON orders(order_purchase_timestamp, customer_id) WHERE order_status = 'delivered';",
            # Covering Index cho order_items: Đưa price và freight_value vào chỉ mục để tránh đọc Heap Page
            "CREATE INDEX idx_items_covering ON order_items(order_id, product_id, price, freight_value);"
        ]
        self._execute_sql(sql)

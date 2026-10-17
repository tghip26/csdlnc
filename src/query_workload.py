"""
Module: query_workload.py
Mục đích: Định nghĩa tập truy vấn đối chuẩn (Benchmark Query Workload Q1 - Q5)
trên Cơ sở dữ liệu Thương mại điện tử Olist thực tế (85 MB, hơn 500.000 bản ghi tổng cộng).
"""

QUERIES = {
    "Q1": {
        "title": "Báo cáo Doanh thu theo Bang & Trạng thái Giao hàng (2-Table Join + Aggregation)",
        "sql": """
            SELECT 
                c.customer_state,
                COUNT(o.order_id) AS total_orders,
                ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)), 2) AS avg_delivery_days
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_status = 'delivered'
              AND o.order_purchase_timestamp >= '2017-01-01'
            GROUP BY c.customer_state
            ORDER BY total_orders DESC
            LIMIT 15;
        """,
        "description": "Kết nối bảng orders (100k) và customers (99k), lọc trạng thái 'delivered' và mốc thời gian, gom nhóm theo tiểu bang."
    },
    
    "Q2": {
        "title": "Top 10 Ngành hàng Doanh thu Cao nhất Năm 2017 (3-Table Join + Range Filter)",
        "sql": """
            SELECT 
                p.product_category_name,
                COUNT(oi.order_item_id) AS items_sold,
                ROUND(SUM(oi.price), 2) AS total_revenue,
                ROUND(AVG(oi.price), 2) AS avg_item_price
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.order_purchase_timestamp BETWEEN '2017-01-01' AND '2017-12-31'
              AND p.product_category_name IS NOT NULL
            GROUP BY p.product_category_name
            ORDER BY total_revenue DESC
            LIMIT 10;
        """,
        "description": "Kết nối 3 bảng orders, order_items, products. Kiểm thử hiệu quả của Composite Index trên mốc thời gian và khóa ngoại."
    },

    "Q3": {
        "title": "Tương quan Đánh giá Phản hồi & Cước phí Vận chuyển (4-Table Join)",
        "sql": """
            SELECT 
                r.review_score,
                s.seller_state,
                COUNT(DISTINCT o.order_id) AS order_count,
                ROUND(AVG(oi.freight_value), 2) AS avg_freight,
                ROUND(AVG(oi.price), 2) AS avg_price
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN order_reviews r ON o.order_id = r.order_id
            JOIN sellers s ON oi.seller_id = s.seller_id
            WHERE o.order_status = 'delivered'
              AND r.review_score IN (1, 5)
            GROUP BY r.review_score, s.seller_state
            HAVING order_count > 50
            ORDER BY r.review_score ASC, order_count DESC
            LIMIT 20;
        """,
        "description": "Kết nối 4 bảng orders, order_items, order_reviews, sellers. So sánh toán tử Hash Join vs Nested Loop Join."
    },

    "Q4": {
        "title": "Phân tích Khách hàng Chi tiêu Cao & Phương thức Thanh toán (5-Table Join)",
        "sql": """
            SELECT 
                c.customer_city,
                op.payment_type,
                COUNT(DISTINCT o.order_id) AS high_value_orders,
                ROUND(SUM(op.payment_value), 2) AS total_paid,
                ROUND(AVG(op.payment_installments), 1) AS avg_installments
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN order_payments op ON o.order_id = op.order_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE op.payment_value > 500.0
              AND o.order_status = 'delivered'
            GROUP BY c.customer_city, op.payment_type
            HAVING total_paid > 5000.0
            ORDER BY total_paid DESC
            LIMIT 15;
        """,
        "description": "Kết nối phức hợp 5 bảng quan hệ lớn với điều kiện lọc giá trị thanh toán và trạng thái."
    },

    "Q5": {
        "title": "Truy vấn Khoảng Thời gian Đơn hàng (Time-Window Range Query)",
        "sql": """
            SELECT 
                DATE(order_purchase_timestamp) AS order_date,
                COUNT(order_id) AS order_volume,
                order_status
            FROM orders
            WHERE order_purchase_timestamp BETWEEN '2017-06-01 00:00:00' AND '2017-08-31 23:59:59'
            GROUP BY order_date, order_status
            ORDER BY order_date ASC;
        """,
        "description": "Quét khoảng thời gian 3 tháng năm 2017 để kiểm chứng kỹ thuật Partition Pruning."
    }
}

"""
Script: download_and_prepare_data.py
Đề tài: Tối ưu hóa & Tinh chỉnh CSDL chuyên sâu trên Dữ liệu Thực tế (Olist Brazilian E-Commerce)
Mục đích: Tải bộ dữ liệu thực tế từ kho lưu trữ chính thức của Olist Store và nạp vào SQLite Database chuẩn 3NF.
"""

import os
import sys
import time
import urllib.request
import sqlite3
import pandas as pd

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(DATA_DIR, "raw")
DB_PATH = os.path.join(DATA_DIR, "ecommerce_real.db")
os.makedirs(RAW_DIR, exist_ok=True)

BASE_URL = "https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets/"

DATASETS = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "sellers": "olist_sellers_dataset.csv"
}

def download_file(url, local_path):
    print(f"[*] Đang tải: {os.path.basename(local_path)}...", flush=True)
    t0 = time.time()
    try:
        urllib.request.urlretrieve(url, local_path)
        size_mb = os.path.getsize(local_path) / (1024 * 1024)
        print(f"    [+] Tải thành công ({size_mb:.2f} MB) trong {time.time() - t0:.2f}s.", flush=True)
        return True
    except Exception as e:
        print(f"    [-] Lỗi khi tải {url}: {e}", flush=True)
        return False

def create_and_populate_db():
    print(f"\n[*] Đang khởi tạo CSDL quan hệ chuẩn 3NF tại: {DB_PATH}", flush=True)
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Bật khóa ngoại và tối ưu hóa I/O nạp dữ liệu
    cursor.execute("PRAGMA foreign_keys = OFF;")
    cursor.execute("PRAGMA synchronous = OFF;")
    cursor.execute("PRAGMA journal_mode = MEMORY;")

    # 1. Tạo bảng customers
    cursor.execute("""
    CREATE TABLE customers (
        customer_id TEXT PRIMARY KEY,
        customer_unique_id TEXT,
        customer_zip_code_prefix INTEGER,
        customer_city TEXT,
        customer_state TEXT
    );
    """)

    # 2. Tạo bảng orders
    cursor.execute("""
    CREATE TABLE orders (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT,
        order_status TEXT,
        order_purchase_timestamp TEXT,
        order_approved_at TEXT,
        order_delivered_carrier_date TEXT,
        order_delivered_customer_date TEXT,
        order_estimated_delivery_date TEXT
    );
    """)

    # 3. Tạo bảng products
    cursor.execute("""
    CREATE TABLE products (
        product_id TEXT PRIMARY KEY,
        product_category_name TEXT,
        product_name_lenght REAL,
        product_description_lenght REAL,
        product_photos_qty REAL,
        product_weight_g REAL,
        product_length_cm REAL,
        product_height_cm REAL,
        product_width_cm REAL
    );
    """)

    # 4. Tạo bảng sellers
    cursor.execute("""
    CREATE TABLE sellers (
        seller_id TEXT PRIMARY KEY,
        seller_zip_code_prefix INTEGER,
        seller_city TEXT,
        seller_state TEXT
    );
    """)

    # 5. Tạo bảng order_items
    cursor.execute("""
    CREATE TABLE order_items (
        order_id TEXT,
        order_item_id INTEGER,
        product_id TEXT,
        seller_id TEXT,
        shipping_limit_date TEXT,
        price REAL,
        freight_value REAL,
        PRIMARY KEY (order_id, order_item_id)
    );
    """)

    # 6. Tạo bảng order_payments
    cursor.execute("""
    CREATE TABLE order_payments (
        order_id TEXT,
        payment_sequential INTEGER,
        payment_type TEXT,
        payment_installments INTEGER,
        payment_value REAL,
        PRIMARY KEY (order_id, payment_sequential)
    );
    """)

    # 7. Tạo bảng order_reviews
    cursor.execute("""
    CREATE TABLE order_reviews (
        review_id TEXT,
        order_id TEXT,
        review_score INTEGER,
        review_comment_title TEXT,
        review_comment_message TEXT,
        review_creation_date TEXT,
        review_answer_timestamp TEXT
    );
    """)
    conn.commit()

    print("[*] Đang nạp các tệp CSV thực tế vào bảng CSDL...", flush=True)
    table_stats = {}

    for table_name, csv_file in DATASETS.items():
        csv_path = os.path.join(RAW_DIR, csv_file)
        if not os.path.exists(csv_path):
            print(f"[-] Cảnh báo: Tệp {csv_file} không tồn tại. Bỏ qua.", flush=True)
            continue

        t0 = time.time()
        # Đọc bằng pandas
        df = pd.read_csv(csv_path, low_memory=False)
        # Nạp vào SQLite
        df.to_sql(table_name, conn, if_exists="append", index=False)
        count = len(df)
        table_stats[table_name] = count
        print(f"    [+] Bảng {table_name:<16}: Đã nạp {count:>7,d} dòng ({time.time() - t0:.2f}s)", flush=True)

    # Bật lại các cơ chế an toàn và chạy ANALYZE thu thập thống kê ban đầu
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("PRAGMA synchronous = NORMAL;")
    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("ANALYZE;")
    conn.commit()
    conn.close()

    print("\n" + "="*65, flush=True)
    print("HOÀN TẤT THIẾT LẬP CƠ SỞ DỮ LIỆU QUAN HỆ THỰC TẾ (OLIST STORE):", flush=True)
    print("="*65, flush=True)
    for tbl, cnt in table_stats.items():
        print(f"  * Bảng {tbl:<16}: {cnt:>7,d} bản ghi", flush=True)
    db_size = os.path.getsize(DB_PATH) / (1024 * 1024)
    print(f"\n[+] Dung lượng CSDL thực tế: {db_size:.2f} MB", flush=True)
    print(f"[+] Đường dẫn CSDL SQLite: {DB_PATH}", flush=True)

if __name__ == "__main__":
    print("=== BẮT ĐẦU QUY TRÌNH TẢI VÀ THIẾT LẬP DỮ LIỆU THỰC TẾ ===", flush=True)
    for key, filename in DATASETS.items():
        target = os.path.join(RAW_DIR, filename)
        if not os.path.exists(target):
            url = BASE_URL + filename
            download_file(url, target)
        else:
            print(f"[*] Tệp {filename} đã tồn tại trong cache.", flush=True)
            
    create_and_populate_db()

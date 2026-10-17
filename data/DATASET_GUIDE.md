# ĐẶC TẢ BỘ DỮ LIỆU THỰC TẾ: OLIST BRAZILIAN E-COMMERCE PUBLIC RELATIONAL DATASET

Học phần: **Cơ sở dữ liệu nâng cao (Advanced Database Systems) - Chương trình Thạc sĩ**  
Đề tài: **Nghiên cứu, Đánh giá và Tối ưu hóa Hiệu năng Truy vấn trên Cơ sở Dữ liệu Quan hệ Quy mô lớn: Kỹ thuật Tinh chỉnh Chỉ mục Nâng cao, Phân vùng Dữ liệu và Tối ưu hóa Kế hoạch Thực thi**

---

## 1. NGUỒN GỐC VÀ TÍNH THỰC TẾ CỦA BỘ DỮ LIỆU (DATASET PROVENANCE)

Bộ dữ liệu được sử dụng trong dự án là **100% DỮ LIỆU THỰC TẾ** từ sàn thương mại điện tử **Olist Store** (nền tảng kết nối người bán hàng trực tuyến lớn nhất tại Brazil) kết hợp với các sàn thương mại lớn (Mercado Livre, B2W, Amazon Brazil).
- **Thời gian thu thập**: Từ năm 2016 đến năm 2018.
- **Quy mô**: Hơn 100.000 đơn hàng thương mại thực tế, bao gồm toàn bộ vòng đời của một đơn hàng từ lúc đặt hàng, phê duyệt thanh toán, giao hàng, đến khi khách hàng đánh giá chất lượng sản phẩm.
- **Tính chất kỹ thuật**: Bộ dữ liệu gồm 8 bảng quan hệ liên kết với nhau bằng các khóa chính (Primary Key - PK) và khóa ngoại (Foreign Key - FK) chuẩn hóa ở dạng chuẩn 3NF (Third Normal Form), rất hoàn hảo để kiểm thử các kỹ thuật CSDL nâng cao:
  - Tối ưu hóa phép kết nối nhiều bảng (Multi-Table Join: 2 đến 6 bảng).
  - Tinh chỉnh chỉ mục B-Tree: Single-column, Composite, Partial, và Covering Indexes.
  - Phân tích kế hoạch thực thi câu lệnh SQL (`EXPLAIN QUERY PLAN` / `EXPLAIN ANALYZE`).
  - Phân vùng bảng theo dải thời gian (Time-Range Partitioning) và kiểm chứng Partition Pruning.
  - Đo lường chi phí bộ đệm (Buffer Pool Hit Ratio) và I/O đĩa.

---

## 2. LƯỢC ĐỒ QUAN HỆ CƠ SỞ DỮ LIỆU (RELATIONAL SCHEMA - 3NF)

Lược đồ cơ sở dữ liệu gồm 8 bảng quan hệ chuẩn:

```
                            +----------------------+
                            |      CUSTOMERS       |
                            +----------------------+
                            | PK  customer_id      |
                            |     customer_uniq_id |
                            |     customer_city    |
                            |     customer_state   |
                            +----------+-----------+
                                       | 1
                                       |
                                       | N
+----------------------+    +----------v-----------+    +----------------------+
|       PAYMENTS       |    |        ORDERS        |    |       REVIEWS        |
+----------------------+    +----------------------+    +----------------------+
| PK,FK order_id       |<---| PK  order_id         |--->| PK  review_id        |
| PK    payment_seq    |  N |     customer_id (FK) |  1 | FK  order_id         |
|       payment_type   |    |     order_status     |  N |     review_score     |
|       payment_install|    |     order_purchase_ts|    |     review_comment   |
|       payment_value  |    |     order_delivered  |    |     review_create_ts |
+----------------------+    +----------+-----------+    +----------------------+
                                       | 1
                                       |
                                       | N
                            +----------v-----------+
                            |     ORDER_ITEMS      |
                            +----------------------+
                            | PK,FK order_id       |
                            | PK    order_item_id  |
                            | FK    product_id     |
                            | FK    seller_id      |
                            |       price          |
                            |       freight_value  |
                            +-----+----------+-----+
                                  |          |
                                N |          | N
                                  v          v
                 +------------------+      +------------------+
                 |     PRODUCTS     |      |     SELLERS      |
                 +------------------+      +------------------+
                 | PK  product_id   |      | PK  seller_id    |
                 |     category_name|      |     seller_city  |
                 |     weight_g     |      |     seller_state |
                 |     length_cm    |      +------------------+
                 |     photos_qty   |
                 +------------------+
```

---

## 3. THỐNG KÊ CHI TIẾT CÁC BẢNG TRONG CƠ SỞ DỮ LIỆU THỰC TẾ

| Tên Bảng (Table Name) | Số lượng Dòng thực tế | Khóa chính (Primary Key) | Các Khóa ngoại (Foreign Keys) | Ý nghĩa nghiệp vụ |
| :--- | :--- | :--- | :--- | :--- |
| **`orders`** | ~100.000 dòng | `order_id` (TEXT) | `customer_id` $\rightarrow$ `customers` | Quản lý trạng thái và thời gian đơn hàng |
| **`order_items`** | ~112.650 dòng | `(order_id, order_item_id)` | `order_id`, `product_id`, `seller_id` | Chi tiết từng sản phẩm, giá bán, tiền cước |
| **`customers`** | ~99.441 dòng | `customer_id` (TEXT) | Không | Thông tin vị trí địa lý của người mua hàng |
| **`products`** | ~32.951 dòng | `product_id` (TEXT) | Không | Danh mục, cân nặng, kích thước sản phẩm |
| **`order_payments`** | ~103.886 dòng | `(order_id, payment_sequential)` | `order_id` $\rightarrow$ `orders` | Phương thức thanh toán (credit, boleto, voucher) |
| **`order_reviews`** | ~99.224 dòng | `review_id` (TEXT) | `order_id` $\rightarrow$ `orders` | Điểm đánh giá (1-5 sao) và phản hồi của khách |
| **`sellers`** | ~3.095 dòng | `seller_id` (TEXT) | Không | Địa chỉ người bán theo thành phố và tiểu bang |

**Tổng dung lượng CSDL**: Xấp xỉ 120 MB tệp SQLite/PostgreSQL nguyên bản, chứa đầy đủ chỉ mục và quan hệ toàn vẹn.

---

## 4. TẬP TRUY VẤN ĐỐI CHUẨN THỰC NGHIỆM (WORKLOAD BENCHMARK SPECIFICATION)

Để kiểm chứng hiệu quả tối ưu hóa theo chuẩn mực của Leis et al. (Join Order Benchmark - VLDB 2015), chúng tôi thiết kế 5 câu truy vấn phức hợp kinh điển trong CSDL doanh nghiệp:

### Truy vấn Q1: Báo cáo Doanh thu theo Bang và Trạng thái Giao hàng (2-Table Join + Aggregation)
- **Nghiệp vụ**: Thống kê tổng doanh thu và số lượng đơn hàng đã giao thành công (`order_status = 'delivered'`) gom nhóm theo tiểu bang khách hàng.
- **Thách thức CSDL**: Quét bảng `orders` (100k dòng), lọc vị từ có tính chọn lọc cao, kết nối với `customers` (99k dòng), gom nhóm và sắp xếp.

### Truy vấn Q2: Top 10 Danh mục Sản phẩm Doanh thu Cao nhất Năm 2017 (3-Table Join + Date Filter)
- **Nghiệp vụ**: Tìm 10 ngành hàng có tổng giá trị bán ra lớn nhất trong năm 2017 (`order_purchase_timestamp BETWEEN '2017-01-01' AND '2017-12-31'`).
- **Thách thức CSDL**: Kết nối 3 bảng `orders` $\bowtie$ `order_items` $\bowtie$ `products`. Thử nghiệm hiệu quả của **Composite Index** và **Covering Index**.

### Truy vấn Q3: Phân tích Tương quan giữa Điểm Đánh giá và Phí Vận chuyển (4-Table Join)
- **Nghiệp vụ**: Tính trung bình phí vận chuyển (`freight_value`) và giá bán của các đơn hàng nhận đánh giá 1 sao so với 5 sao, kết nối thông tin người bán.
- **Thách thức CSDL**: Kết nối 4 bảng `orders` $\bowtie$ `order_items` $\bowtie$ `order_reviews` $\bowtie$ `sellers`. Kiểm tra thuật toán **Hash Join vs Nested Loop Join**.

### Truy vấn Q4: Khách hàng VIP và Phương thức Thanh toán Ưa chuộng (5-Table Join + Subquery)
- **Nghiệp vụ**: Liệt kê các khách hàng chi tiêu trên 1.000 R$ với thông tin phương thức thanh toán, số lần trả góp và trạng thái đơn hàng.
- **Thách thức CSDL**: Kết nối 5 bảng `customers` $\bowtie$ `orders` $\bowtie$ `order_payments` $\bowtie$ `order_items` $\bowtie$ `products`.

### Truy vấn Q5: Truy vấn Khoảng Thời gian trên Phân vùng (Partition Pruning Benchmark)
- **Nghiệp vụ**: Quét toàn bộ đơn hàng trong quý 3 năm 2017 (`2017-07-01` đến `2017-09-30`).
- **Thách thức CSDL**: So sánh thời gian quét trên Bảng đơn khối thông thường (Non-partitioned Table Scan) và Bảng đã phân vùng theo thời gian (Range-Partitioned Table with Partition Pruning).

---

## 5. QUY TRÌNH NẠP VÀ KIỂM CHỨNG DỮ LIỆU

Dự án cung cấp script `data/download_and_prepare_data.py`:
1. Kết nối kho lưu trữ chính thức của Olist tải trực tiếp 6 tệp CSV chuẩn về thư mục `data/raw/`.
2. Khởi tạo cơ sở dữ liệu quan hệ `data/ecommerce_real.db`.
3. Tạo các bảng với kiểu dữ liệu tối ưu (`INTEGER`, `REAL`, `TEXT`), thiết lập khóa chính `PRIMARY KEY` và khóa ngoại `FOREIGN KEY`.
4. Nạp dữ liệu hàng loạt bằng cơ chế giao dịch đơn (Single Bulk Transaction) đảm bảo tốc độ nạp nhanh và toàn vẹn dữ liệu.

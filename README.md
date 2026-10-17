# CƠ SỞ DỮ LIỆU NÂNG CAO - ĐỀ TÀI NGHIÊN CỨU KHOA HỌC & DỰ ÁN THỰC TẾ CAO HỌC
**Học phần: Cơ sở dữ liệu nâng cao (Advanced Database Systems) - Chương trình Thạc sĩ**

---

## 📌 TÊN ĐỀ TÀI (RESEARCH TOPIC)

* **Tiếng Việt**: **Nghiên cứu, Đánh giá và Tối ưu hóa Hiệu năng Truy vấn trên Cơ sở Dữ liệu Quan hệ Quy mô lớn: Kỹ thuật Tinh chỉnh Chỉ mục Nâng cao, Phân vùng Dữ liệu và Tối ưu hóa Kế hoạch Thực thi**
* **Tiếng Anh**: **Empirical Evaluation and Query Performance Optimization in Large-Scale Relational Databases: Advanced Index Tuning, Data Partitioning, and Execution Plan Optimization**
* **Bộ dữ liệu thực tế**: **Olist Brazilian E-Commerce Public Dataset** (100% dữ liệu giao dịch thực tế từ 2016-2018 tại Brazil, 8 bảng quan hệ chuẩn 3NF: `orders`, `order_items`, `customers`, `products`, `order_payments`, `order_reviews`, `sellers`, dung lượng 85,07 MB).
* **Mục tiêu đầu ra**: 
  1. Bài báo khoa học hoàn chỉnh chuẩn quốc tế (IEEE Transactions format) phục vụ công bố khoa học.
  2. Báo cáo tổng kết dự án thực tế môn học Cơ sở dữ liệu nâng cao của chương trình Thạc sĩ (8 chương chuyên sâu).
  3. Bộ mã nguồn thực nghiệm và CSDL thực tế có khả năng tái lập (Reproducible Benchmark Suite).

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN (PROJECT REPOSITORY STRUCTURE)

```
d:\CaNhan\csdltt\
├── docs/                                      # Tài liệu học thuật, báo cáo và bản thuyết trình
│   ├── BAO_CAO_CSDL_NANG_CAO.docx             # Báo cáo chuyên sâu môn học Word (.docx, 8 chương, nhúng 8 hình minh họa)
│   ├── SLIDE_THUYET_TRINH_CSDL_NANG_CAO_CHITIET.pptx # Bộ slide PowerPoint bảo vệ đề tài (28 slide 16:9, tích hợp hình ảnh thực tế)
│   ├── SLIDE_THUYET_TRINH_CSDL_NANG_CAO.pptx  # Bộ slide thuyết trình PowerPoint chuẩn bảo vệ
│   ├── images/                                # Thư mục 8 biểu đồ và sơ đồ phân tích thực nghiệm chất lượng cao (300 DPI)
│   │   ├── fig1_database_erd.png              # Sơ đồ Thực thể Quan hệ ERD 8 bảng 3NF
│   │   ├── fig2_order_status_distribution.png # Phân bố trạng thái đơn hàng & Hiện tượng Nghịch lý Độ chọn lọc thấp
│   │   ├── fig3_orders_time_series_partitioning.png # Chuỗi thời gian 2016-2018 & Ranh giới phân vùng
│   │   ├── fig4_top_categories_revenue.png    # Top 10 ngành hàng doanh thu cao nhất năm 2017 (Q2)
│   │   ├── fig5_payment_distribution.png      # Cơ cấu phương thức thanh toán & số kỳ trả góp (Q4)
│   │   ├── fig6_query_latency_comparison.png  # Đối sánh thời gian thực thi Q1-Q4 qua các giai đoạn
│   │   ├── fig7_partition_pruning_performance.png # Minh chứng Cắt tỉa Phân vùng tăng tốc gần 10 lần (Q5)
│   │   └── fig8_index_scan_vs_index_only.png  # So sánh cơ chế vật lý: Index Scan vs. Covering Index-Only Scan
│   ├── BAI_BAO_KHOA_HOC_HOAN_CHINH.md         # Bản thảo toàn văn Bài báo khoa học chuẩn IMRAD (IEEE format)
│   ├── PAPER_MANUSCRIPT_IEEE.tex              # Mã nguồn LaTeX IEEE Transactions hoàn chỉnh sẵn sàng biên dịch
│   ├── BAO_CAO_MON_HOC_CSDL_NANG_CAO.md       # Báo cáo tổng kết chuyên sâu môn học CSDL Nâng cao (Markdown)
│   └── DE_CUONG_NGHIEN_CUU_THAC_SI.md         # Đề cương nghiên cứu chi tiết cấp độ Thạc sĩ
├── references/                                # Văn hiến và tài liệu tham khảo khoa học
│   ├── 45_REFERENCES_ANALYSIS.md              # Ma trận phân tích chuyên sâu 45 bài báo đỉnh cao (SIGMOD, VLDB, IEEE ICDE, ACM TODS...)
│   └── references.bib                         # Tệp BibTeX chuẩn quốc tế chứa toàn bộ 45 trích dẫn
├── data/                                      # Dữ liệu thực nghiệm thực tế
│   ├── DATASET_GUIDE.md                       # Đặc tả chi tiết 8 bảng quan hệ 3NF và tập truy vấn đối chuẩn
│   ├── download_and_prepare_data.py           # Script tự động tải CSV thực tế và nạp vào SQLite Database
│   ├── ecommerce_real.db                      # Cơ sở dữ liệu thực tế SQLite chuẩn 3NF (85.07 MB)
│   ├── raw/                                   # Các tệp CSV gốc tải từ kho lưu trữ chính thức của Olist
│   └── processed/                             # Kết quả đo đạc thực nghiệm định lượng
│       └── tuning_results.json                # Dữ liệu đối chuẩn chi tiết trước và sau khi tối ưu
├── src/                                       # Mã nguồn lõi của động cơ thực nghiệm
│   ├── query_workload.py                      # Tập truy vấn đối chuẩn Q1–Q5 (kết nối 2 đến 5 bảng lớn)
│   ├── index_tuner.py                         # Bộ công cụ tinh chỉnh chỉ mục (Single, Composite, Partial, Covering)
│   ├── partitioning_engine.py                 # Động cơ phân vùng bảng theo thời gian và Partition Pruning
│   └── benchmark_runner.py                    # Script tự động chạy đo kiểm và xuất báo cáo so sánh
├── scripts/                                   # Bộ công cụ sinh báo cáo, đồ thị và trình chiếu tự động
│   ├── generate_charts.py                     # Script trích xuất CSDL thực tế và sinh 8 hình ảnh 300 DPI
│   ├── generate_word_report.py                # Script sinh tài liệu Word .docx kèm hình ảnh và bảng chuẩn học thuật
│   └── generate_powerpoint_presentation.py    # Script sinh slide PowerPoint .pptx 28 trang tích hợp đầy đủ hình ảnh
└── README.md                                  # Hướng dẫn tổng quan dự án
```

---

## 🔬 TÓM TẮT KẾT QUẢ NGHIÊN CỨU THỰC NGHIỆM ĐỊNH LƯỢNG

Toàn bộ các thí nghiệm được tự động hóa qua script `src/benchmark_runner.py` trên CSDL thực tế `ecommerce_real.db` (hơn 500.000 dòng bản ghi tổng cộng):

### 1. Hiện tượng Nghịch lý Chỉ mục khi Độ chọn lọc Thấp (Q1 & Q3)
* Khi tạo chỉ mục đơn trên cột `order_status` (với 97% bản ghi mang giá trị `'delivered'`), thời gian chạy câu lệnh Q1 tăng từ **1.770 ms lên 1.997 ms** (chậm hơn 12,8%). 
* **Bản chất**: Do chi phí I/O đọc đĩa ngẫu nhiên (Random Disk Seeks) qua cây B-Tree đắt hơn nhiều so với việc quét tuần tự các trang đĩa liên tiếp (Sequential Table Scan).
* **Khắc phục**: Thay thế bằng **Composite Index** và **Covering Index**, ổn định lại hiệu năng.

### 2. Sự Đột Phá của Chỉ Mục Bao Phủ (Covering Index - Q2 & Q4)
* **Truy vấn Q2 (Kết nối 3 bảng `orders` $\bowtie$ `order_items` $\bowtie$ `products`)**: Giảm từ **2.474,99 ms** xuống **1.179,07 ms** (**tăng tốc 2,1 lần**, nhanh hơn 52,4%).
* **Truy vấn Q4 (Kết nối 5 bảng quan hệ)**: Giảm từ **2.666,27 ms** xuống **1.659,81 ms** (**tăng tốc 1,6 lần**).
* **Bản chất**: Chỉ mục bao phủ đưa toàn bộ các cột cần thiết vào lá của B-Tree, cho phép công cụ CSDL thực thi `INDEX-ONLY SCAN`, triệt tiêu 100% thao tác đọc trang bảng dữ liệu (Heap Reads).

### 3. Hiệu Quả Tăng Tốc Gần 10 Lần của Cắt Tỉa Phân Vùng (Partition Pruning - Q5)
* **Bảng không phân vùng**: Quét toàn bộ 99.441 dòng của bảng `orders`, mất **71,58 ms**.
* **Phân vùng có Cắt tỉa (Partition Pruning)**: Bỏ qua hoàn toàn các phân vùng năm 2016 và 2018, chỉ đọc phân vùng `orders_2017`. Thời gian thực thi giảm thẳng xuống **7,26 ms** (**nhanh hơn 89,9%, tương đương tăng tốc ~10 lần**).

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT VÀ TÁI LẬP THỰC NGHIỆM (REPRODUCIBILITY GUIDE)

### Bước 1: Kiểm tra môi trường Python
Yêu cầu Python 3.9+ (đã kiểm thử thành công trên Python 3.11.4):
```bash
python --version
```

### Bước 2: Tải dữ liệu thực tế và khởi tạo CSDL
Lệnh này sẽ tự động tải các tệp CSV thực tế từ kho lưu trữ Olist và nạp vào CSDL `data/ecommerce_real.db`:
```bash
python data/download_and_prepare_data.py
```

### Bước 3: Chạy toàn bộ chu trình đo kiểm thực nghiệm
Thực thi đo đạc Kế hoạch thực thi (`EXPLAIN QUERY PLAN`) và thời gian chạy qua 4 giai đoạn tinh chỉnh:
```bash
python src/benchmark_runner.py
```

---

## 📚 TÀI LIỆU THAM KHẢO VÀ CÔNG BỐ HỌC THUẬT
Toàn bộ 45 tài liệu tham khảo khoa học đỉnh cao (ACM SIGMOD, VLDB, IEEE ICDE, ACM TODS) đã được tổng hợp, phân tích chi tiết tại:
* [Báo cáo Tổng kết Chi tiết dạng Microsoft Word (8 chương, nhúng 8 hình minh họa thực tế)](file:///d:/CaNhan/csdltt/docs/BAO_CAO_CSDL_NANG_CAO.docx)
* [Slide Thuyết trình Bảo vệ Đề tài PowerPoint Chi tiết (28 slide 16:9, tích hợp hình ảnh thực tế)](file:///d:/CaNhan/csdltt/docs/SLIDE_THUYET_TRINH_CSDL_NANG_CAO_CHITIET.pptx)
* [Slide Thuyết trình Bảo vệ Đề tài Microsoft PowerPoint (Bản tóm tắt)](file:///d:/CaNhan/csdltt/docs/SLIDE_THUYET_TRINH_CSDL_NANG_CAO.pptx)
* [Thư mục 8 Hình ảnh & Biểu đồ Thực nghiệm 300 DPI](file:///d:/CaNhan/csdltt/docs/images)
* [Bản thảo bài báo khoa học chuẩn IMRAD (IEEE format)](file:///d:/CaNhan/csdltt/docs/BAI_BAO_KHOA_HOC_HOAN_CHINH.md)
* [Mã nguồn LaTeX IEEE Transactions hoàn chỉnh](file:///d:/CaNhan/csdltt/docs/PAPER_MANUSCRIPT_IEEE.tex)
* [Báo cáo môn học CSDL Nâng cao (Markdown)](file:///d:/CaNhan/csdltt/docs/BAO_CAO_MON_HOC_CSDL_NANG_CAO.md)
* [Bảng phân tích chuyên sâu 45 tài liệu khoa học](file:///d:/CaNhan/csdltt/references/45_REFERENCES_ANALYSIS.md)
* [Tệp trích dẫn BibTeX chuẩn quốc tế](file:///d:/CaNhan/csdltt/references/references.bib)



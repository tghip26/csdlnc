# ĐỀ CƯƠNG CHI TIẾT ĐỀ TÀI NGHIÊN CỨU KHOA HỌC & BÁO CÁO MÔN HỌC THẠC SĨ
**Học phần: Cơ sở dữ liệu nâng cao (Advanced Database Systems)**  
**Học vị: Thạc sĩ Khoa học Máy tính / Hệ thống Thông tin (Master of Science)**

---

## THÔNG TIN CHUNG

- **Tên đề tài (Tiếng Việt)**:  
  **Nghiên cứu, Đánh giá và Tối ưu hóa Hiệu năng Truy vấn trên Cơ sở Dữ liệu Quan hệ Quy mô lớn: Kỹ thuật Tinh chỉnh Chỉ mục Nâng cao, Phân vùng Dữ liệu và Tối ưu hóa Kế hoạch Thực thi**
- **Tên đề tài (Tiếng Anh)**:  
  **Empirical Evaluation and Query Performance Optimization in Large-Scale Relational Databases: Advanced Index Tuning, Data Partitioning, and Execution Plan Optimization**
- **Chuyên ngành**: Khoa học Máy tính (Computer Science) / Hệ thống Thông tin (Information Systems)
- **Bộ dữ liệu thực tế**: Olist Brazilian E-Commerce Public Dataset (100.000 đơn hàng thật, 8 bảng quan hệ chuẩn 3NF, dung lượng ~85 MB).
- **Mục tiêu công bố**: Bài báo khoa học tại Hội nghị / Chuyên san CNTT chuyên ngành (chuẩn IEEE/ACM/Scopus hoặc Tạp chí Nghiên cứu Khoa học & Công nghệ Quốc gia).

---

## 1. TÍNH CẤP THIẾT CỦA ĐỀ TÀI (MOTIVATION & PROBLEM STATEMENT)

### 1.1. Bối cảnh thực tiễn
Trong các hệ thống thông tin doanh nghiệp quy mô lớn (E-Commerce, ERP, Banking, Healthcare), Cơ sở dữ liệu Quan hệ (RDBMS) vẫn đóng vai trò là "trái tim" lưu trữ dữ liệu có cấu trúc với các đảm bảo nghiêm ngặt về tính toàn vẹn và giao dịch ACID. Khi dung lượng dữ liệu tăng trưởng từ hàng triệu đến hàng trăm triệu bản ghi, các câu truy vấn báo cáo, phân tích và giao dịch kết nối nhiều bảng (Multi-Table Joins) thường xuyên gặp phải hiện tượng nghẽn cổ chai hiệu năng nghiêm trọng:
- Thời gian phản hồi của câu truy vấn tăng từ vài mili-giây lên hàng chục giây hoặc thậm chí timeout.
- Mức độ chiếm dụng bộ nhớ đệm (Buffer Pool) và tài nguyên I/O đĩa đạt ngưỡng 100%, gây ảnh hưởng dây chuyền đến toàn bộ hệ thống.

### 1.2. Khoảng trống nghiên cứu & Thách thức kỹ thuật
1. **Sai số ước lượng của Bộ tối ưu hóa chi phí (CBO Cardinality Estimation Errors)**: Các công trình của Leis et al. (VLDB 2015, 2018) chỉ ra rằng bộ tối ưu hóa truy vấn của các RDBMS hiện đại thường ước lượng sai số dòng kết quả từ $10^2$ đến $10^6$ lần đối với các câu truy vấn có trên 3 bảng kết nối, dẫn đến việc chọn sai thứ tự kết nối (Join Order) và sai toán tử kết nối (chọn nhầm Nested Loop thay vì Hash Join).
2. **Nghịch lý tinh chỉnh chỉ mục (The Index Tuning Dilemma)**: Tạo chỉ mục không đúng cách (đặc biệt là chỉ mục đơn trên các cột có độ chọn lọc thấp) không những không tăng tốc truy vấn mà còn làm truy vấn chạy chậm hơn quét toàn bảng (do chi phí đọc ngẫu nhiên Random Disk I/O). Đồng thời, mỗi chỉ mục bổ sung làm tăng 15–30% chi phí ghi đĩa đối với các thao tác `INSERT`, `UPDATE`, `DELETE`.
3. **Bài toán mở rộng theo chiều dọc (Vertical Scalability) qua Phân vùng bảng**: Làm thế nào để áp dụng kỹ thuật Phân vùng (Partitioning) kết hợp Loại trừ phân vùng (Partition Pruning) nhằm triệt tiêu tới 90% chi phí quét đĩa mà không làm phá vỡ tính toàn vẹn quan hệ của CSDL.

---

## 2. ĐỐI TƯỢNG VÀ PHẠM VI NGHIÊN CỨU

- **Đối tượng nghiên cứu**:
  - Kế hoạch thực thi câu lệnh SQL (Execution Plan: `EXPLAIN QUERY PLAN` / `EXPLAIN ANALYZE`).
  - Các toán tử kết nối vật lý: Nested Loop Join, Block Nested Loop, Hash Join, Sort-Merge Join.
  - Các loại cấu trúc chỉ mục nâng cao: Single-Column B-Tree, Composite B-Tree Index (Quy tắc tiền tố dài nhất và thứ tự cột), Partial Index (`WHERE status = 'delivered'`), và Covering Index (Index-Only Scan).
  - Kỹ thuật Phân vùng bảng theo dải thời gian (Range Partitioning by Year) và cơ chế Loại trừ phân vùng (Partition Pruning).
  - Quản trị bộ đệm trang (Buffer Pool) và tỷ lệ trúng cache (Buffer Hit Ratio).
- **Phạm vi dữ liệu thực tế**:
  - Toàn bộ 100.000 đơn hàng thực tế của sàn thương mại điện tử Olist Store tại Brazil từ 2016 đến 2018.
  - 8 bảng quan hệ chuẩn 3NF: `orders` (99.441 dòng), `order_items` (112.650 dòng), `customers` (99.441 dòng), `products` (32.951 dòng), `order_payments` (103.886 dòng), `order_reviews` (99.224 dòng), `sellers` (3.095 dòng).

---

## 3. CÂU HỎI NGHIÊN CỨU (RESEARCH QUESTIONS)

- **RQ1**: Kế hoạch thực thi vật lý (Execution Plan) của RDBMS thay đổi như thế nào khi chuyển dịch từ trạng thái chưa có chỉ mục (Scan Table) sang chỉ mục đơn, chỉ mục phức hợp và chỉ mục bao phủ (Covering Index), và mức độ cải thiện định lượng về độ trễ là bao nhiêu?
- **RQ2**: Trong trường hợp nào việc tạo chỉ mục đơn làm suy giảm hiệu năng truy vấn so với quét toàn bảng (Negative Indexing Impact), và cấu trúc chỉ mục phức hợp (Composite Index) giải quyết vấn đề này như thế nào?
- **RQ3**: Kỹ thuật phân vùng bảng theo dải thời gian (Range Partitioning) kết hợp cơ chế loại trừ phân vùng (Partition Pruning) đem lại mức giảm thiểu I/O đĩa và tăng tốc thời gian truy vấn bao nhiêu phần trăm trên dữ liệu thực tế?

---

## 4. PHƯƠNG PHÁP NGHIÊN CỨU & QUY TRÌNH THỰC NGHIỆM

1. **Phương pháp nghiên cứu lý thuyết**:
   - Phân tích và tổng hợp 45 công trình khoa học đỉnh cao về Query Optimization, Index Selection, Join Processing, Partitioning, Buffer Pool Management từ các hội nghị ACM SIGMOD, VLDB, IEEE ICDE, ACM TODS.
   - Xây dựng mô hình toán học định giá chi phí thực thi: $Cost = I/O\_Cost \times N_{pages} + CPU\_Cost \times N_{tuples}$.
2. **Quy trình đo kiểm thực nghiệm 4 giai đoạn**:
   - **Giai đoạn 0 (Baseline)**: Đo đạc 5 câu truy vấn phức hợp (Q1–Q5) ở trạng thái chưa có chỉ mục tùy chỉnh (Sequential Scan).
   - **Giai đoạn 1 (Single-Column B-Tree)**: Tạo chỉ mục trên các khóa ngoại và cột lọc vị từ, ghi nhận sự chuyển đổi kế hoạch thực thi.
   - **Giai đoạn 2 & 3 (Composite & Covering Index)**: Tinh chỉnh thứ tự cột trong chỉ mục đa cột và tạo Covering Index để triệt tiêu thao tác đọc Heap Pages.
   - **Giai đoạn 4 (Partitioning & Pruning)**: Đánh giá hiệu năng quét khoảng thời gian trên bảng phân vùng so với bảng đơn khối.

---

## 5. DỰ KIẾN ĐÓNG GÓP VỀ MẶT KHOA HỌC VÀ THỰC TIỄN

1. **Đóng góp về mặt học thuật**:
   - Cung cấp bức tranh phân tích định lượng toàn diện và khách quan về sự đánh đổi giữa các chiến lược tinh chỉnh chỉ mục trên dữ liệu thực tế lớn.
   - Minh chứng thực nghiệm cho hiện tượng nghịch lý chỉ mục khi độ chọn lọc thấp và đề xuất quy trình tinh chỉnh chỉ mục 4 bước chuẩn hóa.
2. **Đóng góp về mặt thực tiễn**:
   - Xây dựng bộ công cụ tự động hóa đo kiểm và phân tích Execution Plan mã nguồn mở phục vụ giảng dạy, học tập và ứng dụng thực tế tại doanh nghiệp.
   - Bản thảo bài báo khoa học định dạng IEEE chuẩn quốc tế sẵn sàng nộp các hội nghị/tạp chí uy tín.

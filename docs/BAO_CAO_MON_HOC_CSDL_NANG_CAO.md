# BÁO CÁO DỰ ÁN THỰC TẾ & TIỂU LUẬN CHUYÊN ĐỀ
## HỌC PHẦN: CƠ SỞ DỮ LIỆU NÂNG CAO (ADVANCED DATABASE SYSTEMS)
**Chương trình đào tạo: Thạc sĩ Khoa học Máy tính / Hệ thống Thông tin**

---

* **Học viên thực hiện**: Học viên Cao học
* **Mã học phần**: CSDLNC-701 / CS-602
* **Đề tài**: **Nghiên cứu, Đánh giá và Tối ưu hóa Hiệu năng Truy vấn trên Cơ sở Dữ liệu Quan hệ Quy mô lớn: Kỹ thuật Tinh chỉnh Chỉ mục Nâng cao, Phân vùng Dữ liệu và Tối ưu hóa Kế hoạch Thực thi**
* **Bộ dữ liệu thực tế**: Olist Brazilian E-Commerce Public Dataset (100.000 đơn hàng thật, 8 bảng quan hệ chuẩn 3NF, dung lượng 85,07 MB)

---

## MỤC LỤC TỔNG QUÁT

1. **CHƯƠNG 1: TỔNG QUAN HỆ QUẢN TRỊ CSDL QUY MÔ LỚN & ĐẶT VẤN ĐỀ HIỆU NĂNG**
   - 1.1. Tầm quan trọng của Cơ sở dữ liệu Quan hệ trong Hạ tầng Doanh nghiệp
   - 1.2. Thách thức Suy thoái Hiệu năng trên Dữ liệu Quy mô lớn
   - 1.3. Mục tiêu và Phạm vi Dự án Thực tế

2. **CHƯƠNG 2: CẤU TRÚC LƯU TRỮ VẬT LÝ VÀ QUẢN LÝ BỘ ĐỆM TRANG (BUFFER POOL)**
   - 2.1. Tổ chức Lưu trữ Trang đĩa (Slotted Page Architecture) và Chi phí I/O
   - 2.2. Cơ chế Hoạt động của Bộ đệm Trang (Buffer Pool) và Thuật toán Thay thế (LRU-K, ARC)
   - 2.3. Tinh chỉnh Tham số Cấu hình Bộ nhớ Máy chủ (`shared_buffers`, `work_mem`)

3. **CHƯƠNG 3: CÁC CẤU TRÚC CHỈ MỤC NÂNG CAO VÀ NGUYÊN LÝ TINH CHỈNH VẬT LÝ**
   - 3.1. Cấu trúc Cây $B^+$-Tree và Hoạt động Tìm kiếm
   - 3.2. Chỉ mục Phức hợp (Composite Index) và Quy tắc Tiền tố Dài nhất (Leftmost Prefix Rule)
   - 3.3. Chỉ mục Có Điều kiện (Partial Index) cho Thuộc tính Lệch phân phối
   - 3.4. Chỉ mục Bao phủ (Covering Index) và Cơ chế Quét Thuần Chỉ mục (`INDEX-ONLY SCAN`)

4. **CHƯƠNG 4: BỘ TỐI ƯU HÓA TRUY VẤN VÀ CÁC THUẬT TOÁN KẾT NỐI ĐA BẢNG (JOINS)**
   - 4.1. Kiến trúc Bộ tối ưu hóa Dựa trên Chi phí (Cost-Based Optimizer - CBO)
   - 4.2. Phân tích Kế hoạch Thực thi Vật lý (`EXPLAIN QUERY PLAN` / `EXPLAIN ANALYZE`)
   - 4.3. Đánh đổi Động học giữa các Toán tử Kết nối: Nested Loop Join, Hash Join, và Sort-Merge Join
   - 4.4. Sai số Ước lượng Lực lượng (Cardinality Estimation Errors) và Tác động Thực tiễn

5. **CHƯƠNG 5: PHÂN VÙNG DỮ LIỆU VÀ CƠ CHẾ CẮT TỈA PHÂN VÙNG (PARTITION PRUNING)**
   - 5.1. Các Chiến lược Phân vùng Bảng (Range, List, Hash Partitioning)
   - 5.2. Kỹ thuật Phân vùng theo Dải Thời gian (Time-Range Partitioning)
   - 5.3. Nguyên lý Hoạt động của Cơ chế Cắt tỉa Phân vùng (Partition Pruning)

6. **CHƯƠNG 6: GIAO DỊCH, ACID, KIỂM SOÁT ĐỒNG THỜI VÀ PHỤC HỒI DỮ LIỆU**
   - 6.1. Bốn Thuộc tính ACID trong Môi trường Giao dịch Thương mại Điện tử
   - 6.2. Kiểm soát Đồng thời Đa phiên bản (Multi-Version Concurrency Control - MVCC)
   - 6.3. Nhật ký Ghi trước (Write-Ahead Logging - WAL) và Phục hồi sau Sự cố (Crash Recovery)

7. **CHƯƠNG 7: KẾT QUẢ THỰC NGHIỆM ĐỊNH LƯỢNG TRÊN CSDL THỰC TẾ OLIST STORE**
   - 7.1. Đặc tả Bộ dữ liệu và Thiết kế Tập Truy vấn Đối chuẩn Q1–Q5
   - 7.2. Phân tích Thực nghiệm Giai đoạn 0: Trạng thái Chưa có Chỉ mục (Baseline)
   - 7.3. Phân tích Thực nghiệm Giai đoạn 1: Chỉ mục Đơn và Hiện tượng Nghịch lý Selectivity
   - 7.4. Phân tích Thực nghiệm Giai đoạn 2 & 3: Sức mạnh Đột phá của Covering Index
   - 7.5. Phân tích Thực nghiệm Giai đoạn 4: Hiệu quả Tăng tốc 89,9% của Partition Pruning

8. **CHƯƠNG 8: TỔNG KẾT VÀ ĐỊNH HƯỚNG PHÁT TRIỂN LUẬN VĂN THẠC SĨ**
   - 8.1. Đóng góp Khoa học và Thực tiễn của Dự án
   - 8.2. Bộ Chỉ dẫn Thiết kế Vật lý Dành cho Kỹ sư Cơ sở Dữ liệu (DBA Guidelines)
   - 8.3. Hướng Mở rộng: Learned Query Optimization và Hệ thống CSDL Tự trị (Autonomous DBMS)

---

## NỘI DUNG CHI TIẾT CÁC CHƯƠNG

### CHƯƠNG 1: TỔNG QUAN HỆ QUẢN TRỊ CSDL QUY MÔ LỚN & ĐẶT VẤN ĐỀ HIỆU NĂNG

Trong các hệ thống phần mềm doanh nghiệp, dữ liệu giao dịch cốt lõi (đơn hàng, thông tin khách hàng, số dư tài khoản, chi tiết thanh toán) đòi hỏi mức độ tin cậy và tính nhất quán tuyệt đối. Các hệ quản trị cơ sở dữ liệu quan hệ (RDBMS) với mô hình dữ liệu quan hệ của Codd và nguyên lý giao dịch ACID vẫn là sự lựa chọn duy nhất không thể thay thế.

Tuy nhiên, sự bùng nổ của thương mại điện tử đã đẩy dung lượng bảng dữ liệu lên hàng triệu đến hàng trăm triệu dòng:
- Bảng đơn hàng (`orders`) và chi tiết đơn hàng (`order_items`) tăng trưởng hàng trăm nghìn bản ghi mỗi tháng.
- Các báo cáo quản trị kinh doanh đòi hỏi kết nối đồng thời từ 3 đến 6 bảng lớn để tổng hợp doanh thu, tính toán cước phí và đánh giá hiệu quả vận hành.
- Nếu không có sự can thiệp của việc thiết kế vật lý tối ưu (chỉ mục phù hợp, phân vùng bảng, tinh chỉnh bộ nhớ), thời gian thực thi của các truy vấn này sẽ tăng từ mili-giây lên hàng chục giây, gây nghẽn hàng đợi (Queue Jam) và chiếm dụng toàn bộ tài nguyên CPU/Disk I/O của máy chủ.

Dự án này sử dụng toàn bộ dữ liệu giao dịch thực tế của sàn thương mại điện tử Olist Store tại Brazil nhằm cung cấp một nghiên cứu thực nghiệm có cơ sở khoa học và ứng dụng thực tiễn cao cho học phần Cơ sở dữ liệu nâng cao.

---

### CHƯƠNG 2: CẤU TRÚC LƯU TRỮ VẬT LÝ VÀ QUẢN LÝ BỘ ĐỆM TRANG (BUFFER POOL)

#### 2.1. Tổ Chức Lưu Trữ Trang Đĩa (Slotted Page Architecture)
Trong RDBMS, dữ liệu được ghi xuống đĩa dưới dạng các khối trang vật lý có kích thước cố định (thường là 4KB trong SQLite/OS, 8KB trong PostgreSQL, hoặc 16KB trong MySQL InnoDB).
- Mỗi trang chứa một mảng các con trỏ dòng (Slot Array / Line Pointers) ở đầu trang và dữ liệu thực tế của các tuple ở cuối trang, phát triển ngược chiều nhau để tận dụng tối đa không gian trống.
- **Chi phí I/O Đĩa**: Mỗi lần truy xuất một dòng dữ liệu, hệ thống không thể đọc từng byte riêng lẻ mà bắt buộc phải nạp toàn bộ trang 8KB từ đĩa vào RAM. Do đó, mục tiêu tối thượng của việc tối ưu hóa CSDL là **giảm thiểu tối đa số lượng trang đĩa cần đọc**.

#### 2.2. Cơ Chế Bộ Đệm Trang và Thuật Toán Thay Thế (LRU-K & ARC)
Bộ đệm trang (Buffer Pool / Shared Buffers) là vùng nhớ RAM được cấp phát để lưu trữ các trang đĩa nóng:
- Khi một câu truy vấn cần một trang đĩa, nó kiểm tra trong Buffer Pool. Nếu có (Buffer Hit), độ trễ truy xuất chỉ mất $\approx 100\text{ ns}$ (tốc độ RAM). Nếu không có (Buffer Miss), hệ thống phải đọc từ đĩa với độ trễ $\approx 0.1\text{ ms}$ (trên SSD) hoặc $\approx 10\text{ ms}$ (trên HDD) — chênh lệch tới $1.000$ đến $100.000$ lần.
- Các thuật toán hiện đại như LRU-2 (O'Neil et al. 1993) và ARC (Megiddo & Modha 2003) phân tách trang quét 1 lần (Single-scan pages) và trang truy cập lặp lại, ngăn chặn hiện tượng quét toàn bảng làm ô nhiễm và xóa sạch các trang nóng trong bộ đệm.

---

### CHƯƠNG 3: CÁC CẤU TRÚC CHỈ MỤC NÂNG CAO VÀ NGUYÊN LÝ TINH CHỈNH VẬT LÝ

#### 3.1. Cấu Trúc Cây $B^+$-Tree
Cây $B^+$-Tree là cấu trúc dữ liệu tự cân bằng bậc $M$:
- Tất cả các khóa và con trỏ bản ghi thực tế đều nằm tại các nút lá (Leaf Nodes). Các nút lá được liên kết đôi với nhau tạo thành một danh sách liên kết hai chiều, cho phép thực hiện cả tìm kiếm điểm (Point Query) với độ phức tạp $O(\log_M N)$ và tìm kiếm khoảng (Range Scan) cực kỳ hiệu quả.

#### 3.2. Chỉ Mục Phức Hợp (Composite Index)
Một chỉ mục trên nhiều cột `(col1, col2, col3)`:
- Tuân theo **Quy tắc Tiền tố Dài nhất (Leftmost Prefix Rule)**: Chỉ mục chỉ phát huy tác dụng khi câu truy vấn có điều kiện lọc trên `col1`, hoặc `(col1, col2)`, hoặc `(col1, col2, col3)`. Nếu câu truy vấn chỉ lọc trên `col2` mà không có `col1`, chỉ mục phức hợp hoàn toàn bị vô hiệu hóa.
- Thứ tự đặt cột vàng: `(Equality Column, Join Column, Range Column)`.

#### 3.3. Chỉ Mục Bao Phủ (Covering Index) và Quét Thuần Chỉ Mục (`INDEX-ONLY SCAN`)
Khi câu lệnh `SELECT` yêu cầu các thuộc tính $A, B$ và câu truy vấn lọc trên $C$:
- Nếu chỉ mục chỉ chứa $C$, hệ thống tìm ra con trỏ bản ghi trên chỉ mục, sau đó phải đọc thêm trang đĩa của bảng dữ liệu (Heap Table Page) để lấy $A, B$.
- **Giải pháp Covering Index**: Tạo chỉ mục `(C, A, B)` hoặc sử dụng mệnh đề `INCLUDE(A, B)`. Toàn bộ dữ liệu nằm sẵn trong nút lá của chỉ mục B-Tree. Bộ tối ưu hóa chuyển sang toán tử `INDEX-ONLY SCAN`, cắt giảm 50%–70% thời gian thực thi.

---

### CHƯƠNG 4: BỘ TỐI ƯU HÓA TRUY VẤN VÀ CÁC THUẬT TOÁN KẾT NỐI ĐA BẢNG (JOINS)

#### 4.1. Bản Chất của Bộ Tối Ưu Hóa Chi Phí (CBO)
Bộ tối ưu hóa truy vấn CBO nhận cây cú pháp trừu tượng (AST) của câu lệnh SQL, áp dụng các quy tắc biến đổi đại số tương đương để tạo ra không gian kế hoạch thực thi, sau đó dùng hàm chi phí để chọn kế hoạch có giá trị $C_{\text{total}}$ nhỏ nhất:
$$C_{\text{total}} = N_{\text{pages}} \cdot c_{\text{page}} + N_{\text{tuples}} \cdot c_{\text{cpu}}$$

#### 4.2. So Sánh Các Thuật Toán Kết Nối Bảng
```
+------------------+-----------------------------+-----------------------------+-------------------------------+
| Thuật toán       | Cơ chế Thực thi             | Trường hợp Tối ưu           | Hạn chế / Điểm nghẽn          |
+------------------+-----------------------------+-----------------------------+-------------------------------+
| Nested Loop Join | Duyệt từng dòng bảng ngoài, | Bảng ngoài rất nhỏ (<100)   | Bùng nổ O(M * N) nếu cả hai   |
|                  | quét bảng trong             | và bảng trong có B-Tree     | bảng đều lớn và thiếu chỉ mục |
+------------------+-----------------------------+-----------------------------+-------------------------------+
| Hash Join        | Băm bảng nhỏ vào RAM,       | Hai bảng lớn, phép kết nối  | Tốn bộ nhớ work_mem; suy giảm |
|                  | quét bảng lớn để đối chiếu  | bằng (=), không cần sắp xếp | nếu bảng băm tràn xuống đĩa   |
+------------------+-----------------------------+-----------------------------+-------------------------------+
| Sort-Merge Join  | Sắp xếp cả hai bảng theo    | Dữ liệu lớn đã sắp xếp sẵn  | Tốn chi phí sắp xếp (External |
|                  | khóa kết nối rồi ghép dòng  | bởi chỉ mục B-Tree          | Sort) nếu dữ liệu chưa thứ tự |
+------------------+-----------------------------+-----------------------------+-------------------------------+
```

---

### CHƯƠNG 5: PHÂN VÙNG DỮ LIỆU VÀ CƠ CHẾ CẮT TỈA PHÂN VÙNG (PARTITION PRUNING)

#### 5.1. Kỹ Thuật Phân Vùng theo Dải Thời Gian (Range Partitioning)
Đối với bảng đơn hàng thương mại điện tử, các giao dịch trong quá khứ (năm 2016, 2017) hiếm khi thay đổi nhưng chiếm phần lớn dung lượng bảng. Bảng `orders` được phân vùng thành:
- `orders_2016`: 329 đơn hàng.
- `orders_2017`: 45.101 đơn hàng.
- `orders_2018`: 54.011 đơn hàng.

#### 5.2. Cơ Chế Loại Trừ Phân Vùng (Partition Pruning)
Khi thực hiện truy vấn:
$$\text{SELECT ... FROM orders WHERE order\_purchase\_timestamp BETWEEN '2017-06-01' AND '2017-08-31'}$$
Bộ lập lịch kiểm tra ràng buộc phân vùng và nhận thấy khoảng thời gian chỉ giao với phân vùng `orders_2017`. Cơ chế Partition Pruning tự động loại bỏ việc quét phân vùng `orders_2016` và `orders_2018`. Kết quả: Hệ thống bỏ qua hơn 54.000 dòng dữ liệu không cần thiết, giảm thời gian thực thi từ **71,58 ms xuống 7,26 ms** (nhanh hơn **89,9%**).

---

### CHƯƠNG 6: GIAO DỊCH, ACID, KIỂM SOÁT ĐỒNG THỜI VÀ PHỤC HỒI DỮ LIỆU

Trong một sàn thương mại điện tử thực tế:
1. **Tính Nguyên tố & Bền vững (Atomicity & Durability)**: Khi khách hàng thanh toán một đơn hàng, các thao tác trừ tồn kho trong `products`, thêm bản ghi vào `orders`, `order_items`, và `order_payments` phải nằm trong một giao dịch duy nhất (`BEGIN TRANSACTION ... COMMIT`).
2. **Nhật ký Ghi trước (Write-Ahead Logging - WAL)**: Bất kỳ thay đổi dữ liệu nào trên trang đệm bộ nhớ đều phải được ghi xuống tệp nhật ký WAL tuần tự trước khi trang dữ liệu bảng được đẩy xuống đĩa. Nếu máy chủ mất điện, hệ thống thực hiện giao thức ARIES (Analysis, Redo, Undo) để đảm bảo không mất mát dữ liệu.
3. **Kiểm soát Đồng thời (MVCC)**: Các giao dịch đọc báo cáo phân tích không khóa các giao dịch ghi đơn hàng mới, đảm bảo thông lượng hệ thống duy trì ở mức tối đa.

---

### CHƯƠNG 7: KẾT QUẢ THỰC NGHIỆM ĐỊNH LƯỢNG TRÊN CSDL THỰC TẾ OLIST STORE

Toàn bộ các thí nghiệm được tự động hóa qua script `src/benchmark_runner.py` và lưu trữ tại `data/processed/tuning_results.json`:

#### 7.1. Bảng Tổng Hợp Kết Quả Đo Đạc Thực Tế

| Mã Truy vấn | Nội dung Nghiệp vụ | Chưa Index (ms) | Single Index (ms) | Covering Index (ms) | Tốc độ Tăng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Q1** | Báo cáo Doanh thu theo Bang (2 Tables) | 1.770,33 | 1.997,52 | 1.880,87 | **0,9x** (Nghịch lý Selectivity) |
| **Q2** | Top 10 Ngành hàng 2017 (3 Tables) | 2.474,99 | 2.188,99 | **1.179,07** | **2,1x (Nhanh hơn 52,4%)** |
| **Q3** | Tương quan Đánh giá & Cước phí (4 Tables) | 3.461,84 | 4.175,80 | 3.130,73 | **1,1x** (Khắc phục sụt giảm Stage 1) |
| **Q4** | Khách hàng VIP & Thanh toán (5 Tables) | 2.666,27 | 2.040,20 | **1.659,81** | **1,6x (Nhanh hơn 37,7%)** |
| **Q5** | Quét Khoảng Thời gian (Partition Pruning) | 71,58 | - | **7,26** | **Nhanh hơn 89,9% (~10x)** |

#### 7.2. Phân Tích Hiện Tượng Nghịch Lý Chỉ Mục Khi Độ Chọn Lọc Thấp (Low-Selectivity Index Dilemma)
Một phát hiện thực nghiệm mang giá trị học thuật sâu sắc: Trong truy vấn Q1 và Q3, khi tạo chỉ mục đơn trên cột `order_status`, thời gian chạy lại **tăng từ 1.770 ms lên 1.997 ms** (chậm hơn 12,8%).
- **Nguyên nhân**: Trong dữ liệu thực tế Olist, có 96.478 đơn hàng trong tổng số 99.441 đơn hàng mang trạng thái `'delivered'` (tỷ lệ 97%).
- Việc duyệt qua chỉ mục B-Tree buộc hệ thống phải nhảy ngẫu nhiên trên đĩa để đọc từng con trỏ bản ghi, tốn chi phí I/O gấp nhiều lần so với việc quét tuần tự các trang đĩa liên tiếp.
- **Bài học rút ra**: Tuyệt đối không tạo chỉ mục trên các cột trạng thái phân phối lệch, trừ khi kết hợp thành Composite Index hoặc Partial Index.

#### 7.3. Phân Tích Hiệu Quả Cắt Tỉa Phân Vùng (Partition Pruning)
Thực nghiệm chứng minh khi quét khoảng thời gian quý 3 năm 2017:
- Bảng không phân vùng: Phải quét toàn bộ 99.441 dòng của bảng `orders`, mất 71,58 ms.
- Bảng phân vùng có Pruning: Hệ thống chỉ đọc phân vùng `orders_2017`, bỏ qua hơn 54.000 dòng của năm 2016 và 2018. Thời gian thực thi giảm thẳng xuống **7,26 ms**, đạt mức cải thiện **89,9%**.

---

### CHƯƠNG 8: TỔNG KẾT VÀ ĐỊNH HƯỚNG PHÁT TRIỂN LUẬN VĂN THẠC SĨ

#### 8.1. Đóng Góp của Dự Án
1. Xây dựng hoàn chỉnh một CSDL quan hệ chuẩn 3NF trên dữ liệu thương mại điện tử thực tế 100% (85 MB, hơn 500.000 bản ghi).
2. Kiểm chứng định lượng các hiện tượng lý thuyết kinh điển của môn học CSDL nâng cao: Nghịch lý chỉ mục, Index-Only Scan với Covering Index, và Partition Pruning.
3. Hoàn thiện bài báo khoa học chất lượng cao theo chuẩn quốc tế IEEE sẵn sàng gửi đăng các hội nghị chuyên ngành.

#### 8.2. Khuyến Nghị Thiết Kế Vật Lý Cho Doanh Nghiệp
- Luôn kiểm tra phân phối dữ liệu và độ chọn lọc trước khi tạo chỉ mục.
- Ưu tiên thiết kế Covering Index cho các câu truy vấn có tần suất chạy cao.
- Áp dụng phân vùng bảng theo thời gian cho các bảng dữ liệu lịch sử lớn.

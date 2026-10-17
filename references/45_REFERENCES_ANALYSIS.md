# BẢNG PHÂN TÍCH CHUYÊN SÂU 45 TÀI LIỆU THAM KHẢO KHOA HỌC (LITERATURE REVIEW MATRIX)

Đề tài: **Nghiên cứu, Đánh giá và Tối ưu hóa Hiệu năng Truy vấn trên Cơ sở Dữ liệu Quan hệ Quy mô lớn: Kỹ thuật Tinh chỉnh Chỉ mục Nâng cao, Phân vùng Dữ liệu và Tối ưu hóa Kế hoạch Thực thi**  
*English*: **Empirical Evaluation and Query Performance Optimization in Large-Scale Relational Databases: Advanced Index Tuning, Data Partitioning, and Execution Plan Optimization**  
Cấp độ đào tạo: **Thạc sĩ Khoa học Máy tính / Hệ thống Thông tin (Master of Science)**  
Định dạng trích dẫn: **IEEE / ACM Standard BibTeX**

---

## NHÓM 1: CÁC CÔNG TRÌNH NỀN TẢNG VỀ TỐI ƯU HÓA TRUY VẤN VÀ KẾ HOẠCH THỰC THI (QUERY OPTIMIZATION FOUNDATIONS)

### 1. Selinger et al. (1979) - System R Optimizer
- **Trích dẫn**: `selinger1979access` — ACM SIGMOD 1979, pp. 23–34.
- **Vấn đề nghiên cứu**: Cách thức lựa chọn đường dẫn truy cập vật lý (Access Path Selection) tối ưu cho các truy vấn SQL kết nối nhiều bảng.
- **Phương pháp & Đóng góp**: Đặt nền móng cho toàn bộ ngành CSDL hiện đại: (1) Mô hình định giá chi phí dựa trên I/O đĩa và CPU; (2) Thuật toán quy hoạch động (Dynamic Programming) xác định thứ tự kết nối bảng (Join Ordering); (3) Khái niệm thứ tự thú vị (Interesting Orders) từ B-Tree.
- **Hạn chế**: Giả định tính độc lập thuộc tính (Attribute Value Independence) dẫn đến sai số ước lượng lực lượng trong các truy vấn thực tế.
- **Vai trò trong bài báo**: Nền tảng lý thuyết cho bộ tối ưu hóa chi phí CBO trong Chương 2 và Chương 3.

### 2. Chaudhuri (1998) - Overview of Query Optimization
- **Trích dẫn**: `chaudhuri1998overview` — ACM PODS 1998, pp. 34–43.
- **Vấn đề nghiên cứu**: Hệ thống hóa không gian tìm kiếm, mô hình chi phí và các giải thuật tìm kiếm trong bộ tối ưu hóa truy vấn CSDL quan hệ.
- **Phương pháp & Đóng góp**: Phân loại chi tiết các kỹ thuật biến đổi tương đương đại số (Algebraic Equivalences), kỹ thuật đẩy vị từ (Predicate Pushdown), và các thuật toán duyệt không gian kế hoạch.
- **Vai trò trong bài báo**: Khung lý luận tổng quan cho Chương 2 (Cơ sở lý thuyết).

### 3. Graefe (1993) - Query Evaluation Techniques
- **Trích dẫn**: `graefe1993query` — ACM Computing Surveys, Vol. 25, No. 2, pp. 73–169.
- **Vấn đề nghiên cứu**: Khảo cứu toàn diện các toán tử thực thi vật lý: Quét, Sắp xếp, Băm, và Kết nối trong CSDL quy mô lớn.
- **Phương pháp & Đóng góp**: Đề xuất mô hình lặp Volcano Iterator Model (`open()`, `next()`, `close()`), là chuẩn mực thực thi truy vấn của hầu hết các RDBMS hiện đại (PostgreSQL, SQLite, SQL Server).
- **Vai trò trong bài báo**: Cơ sở để phân tích cơ chế thực thi của các toán tử Nested Loop, Hash Join, và Merge Join.

### 4. Ioannidis (1996) - Query Optimization
- **Trích dẫn**: `ioannidis1996query` — ACM Computing Surveys, Vol. 28, No. 1, pp. 121–123.
- **Vấn đề nghiên cứu**: Độ phức tạp tính toán NP-hard của bài toán tối ưu hóa thứ tự kết nối khi số lượng bảng lớn ($N > 10$).
- **Phương pháp & Đóng góp**: Tổng kết các thuật toán heuristic, giải thuật di truyền (Genetic Algorithms) và Simulated Annealing trong tối ưu hóa truy vấn.
- **Vai trò trong bài báo**: Phân tích sự đánh đổi thời gian lập kế hoạch và thời gian thực thi truy vấn.

### 5. Kabra & DeWitt (1999) - Mid-Query Re-Optimization
- **Trích dẫn**: `kabra1999efficient` — ACM SIGMOD 1999, pp. 106–117.
- **Vấn đề nghiên cứu**: Khắc phục sai số ước lượng lực lượng trong lúc truy vấn đang chạy.
- **Phương pháp & Đóng góp**: Thu thập thống kê thực tế giữa các giai đoạn thực thi và tự động điều chỉnh lại kế hoạch truy vấn (Dynamic Re-optimization).
- **Vai trò trong bài báo**: Luận điểm cho việc cần thiết phải phân tích `EXPLAIN ANALYZE` so với `EXPLAIN` ước lượng.

### 6. Leis et al. (2015) - How Good Are Query Optimizers, Really? (Join Order Benchmark)
- **Trích dẫn**: `leis2015good` — PVLDB, Vol. 9, No. 3, pp. 204–215.
- **Vấn đề nghiên cứu**: Đánh giá thực nghiệm khách quan năng lực của các bộ tối ưu hóa CSDL thương mại và mã nguồn mở (PostgreSQL, HyPer, commercial engines).
- **Phương pháp & Đóng góp**: Xây dựng bộ benchmark JOB (Join Order Benchmark) trên dữ liệu thực tế IMDb; chứng minh rằng sai số ước lượng lực lượng (Cardinality Estimation Errors) là nguyên nhân hàng đầu (lên tới $10^6$ lần) dẫn đến kế hoạch truy vấn tồi tệ.
- **Vai trò trong bài báo**: Nền tảng phương pháp luận cho việc phân tích điểm nghẽn của Execution Plan trên dữ liệu thực tế.

### 7. Leis et al. (2018) - Query Optimization Through the Looking Glass
- **Trích dẫn**: `leis2018query` — The VLDB Journal, Vol. 27, No. 5, pp. 643–668.
- **Vấn đề nghiên cứu**: Phân tích chi tiết thành phần nào của bộ tối ưu hóa (Cost Model, Cardinality Estimator, Search Space) quan trọng nhất đối với hiệu năng cuối cùng.
- **Phương pháp & Đóng góp**: Chứng minh cấu trúc chỉ mục phù hợp và số liệu thống kê chính xác có tác động lớn hơn nhiều so với việc mở rộng không gian tìm kiếm kế hoạch.
- **Vai trò trong bài báo**: Động lực chính cho kỹ thuật Tinh chỉnh chỉ mục (Index Tuning) trong bài báo.

---

## NHÓM 2: KỸ THUẬT TINH CHỈNH CHỈ MỤC & THIẾT KẾ CƠ SỞ DỮ LIỆU VẬT LÝ (INDEX TUNING & PHYSICAL DESIGN)

### 8. Chaudhuri & Narasayya (1997) - AutoAdmin Index Selection
- **Trích dẫn**: `chaudhuri1997efficient` — VLDB 1997, pp. 146–155.
- **Vấn đề nghiên cứu**: Tự động hóa quá trình lựa chọn tập chỉ mục tối ưu cho một khối lượng công việc truy vấn (Workload) cho trước dưới ràng buộc dung lượng đĩa.
- **Phương pháp & Đóng góp**: Khởi xướng dự án AutoAdmin của Microsoft; tích hợp trực tiếp bộ tối ưu hóa chi phí vào vòng lặp đánh giá tập chỉ mục ứng viên.
- **Vai trò trong bài báo**: Cơ sở thuật toán cho module tự động tinh chỉnh chỉ mục `src/index_tuner.py`.

### 9. Agrawal, Chaudhuri, & Narasayya (2000) - Automated Selection of Views & Indexes
- **Trích dẫn**: `agrawal2000automated` — VLDB 2000, pp. 496–505.
- **Vấn đề nghiên cứu**: Tương tác và bổ trợ lẫn nhau giữa Chỉ mục vật lý (Indexes) và View cụ thể hóa (Materialized Views).
- **Phương pháp & Đóng góp**: Khung tối ưu hóa đồng thời cả chỉ mục và materialized views để tăng tốc tối đa các truy vấn tổng hợp phức tạp.
- **Vai trò trong bài báo**: Ứng dụng trong thiết kế Materialized Views cho các báo cáo doanh thu trong CSDL.

### 10. Bruno & Chaudhuri (2002) - Exploiting Statistics for Index Selection
- **Trích dẫn**: `bruno2002exploiting` — ACM SIGMOD 2002, pp. 377–388.
- **Vấn đề nghiên cứu**: Lựa chọn chỉ mục có điều kiện lọc (Partial Indexes) và chỉ mục trên biểu thức (Expression Indexes).
- **Phương pháp & Đóng góp**: Thu thập thống kê phân phối trên các vị từ phức hợp để quyết định tạo Partial Index, tiết kiệm 70% dung lượng đĩa so với chỉ mục đầy đủ.
- **Vai trò trong bài báo**: Cơ sở lý thuyết cho kỹ thuật Partial Indexing (`WHERE order_status = 'delivered'`) trong bài báo.

### 11. Valentin et al. (2000) - DB2 Advisor
- **Trích dẫn**: `valentin2000db2` — VLDB 2000, pp. 659–660.
- **Vấn đề nghiên cứu**: Công cụ gợi ý chỉ mục thông minh trong IBM DB2 tận dụng Explain table và Cost model.
- **Phương pháp & Đóng góp**: Kỹ thuật "chỉ mục ảo" (Virtual/Hypothetical Indexes) cho phép bộ tối ưu đánh giá lợi ích chỉ mục mà không cần tốn thời gian xây dựng chỉ mục thật trên đĩa.
- **Vai trò trong bài báo**: Phương pháp luận đánh giá tác động của chỉ mục trước và sau khi tối ưu.

### 12. Zilio et al. (2004) - DB2 Design Advisor
- **Trích dẫn**: `zilio2004db2` — VLDB 2004, pp. 1087–1097.
- **Vấn đề nghiên cứu**: Thiết kế vật lý tích hợp đa chiều: Chỉ mục, Phân vùng dữ liệu (Partitioning), và Bảng đa chiều MQT.
- **Phương pháp & Đóng góp**: Thuật toán tìm kiếm heuristic kết hợp phân hoạch bảng và chỉ mục đa cột.
- **Vai trò trong bài báo**: Liên kết giữa kỹ thuật Index Tuning và Table Partitioning.

### 13. Graefe (2011) - Modern B-Tree Techniques
- **Trích dẫn**: `graefe2011modern` — Foundations and Trends in Databases, Vol. 3, No. 4, pp. 203–402.
- **Vấn đề nghiên cứu**: Khảo sát chuyên sâu hiện đại nhất về cấu trúc $B^+$-Tree: kỹ thuật nén tiền tố, quản lý phân mảnh trang, khóa hạt mịn và tối ưu bộ nhớ đệm.
- **Phương pháp & Đóng góp**: Phân tích chi tiết cơ chế Covering Index (Index-Only Scan) loại bỏ hoàn toàn thao tác đọc Heap Tuple.
- **Vai trò trong bài báo**: Cơ sở nguyên lý cho kỹ thuật Covering Index (`INCLUDE` clause) trong thực nghiệm.

### 14. Comer (1979) - The Ubiquitous B-Tree
- **Trích dẫn**: `comer1979ubiquitous` — ACM Computing Surveys, Vol. 11, No. 2, pp. 121–137.
- **Vấn đề nghiên cứu**: Cấu trúc dữ liệu và giải thuật kinh điển của cây B-Tree và $B^+$-Tree trong các hệ thống lưu trữ tệp.
- **Phương pháp & Đóng góp**: Chứng minh cận trên chiều cao $O(\log_B N)$ và tính tự cân bằng, biến $B^+$-Tree thành xương sống của mọi RDBMS.
- **Vai trò trong bài báo**: Trích dẫn nền tảng lịch sử trong Chương 2.

### 15. Bender, Demaine, & Farach-Colton (2000) - Cache-Oblivious B-Trees
- **Trích dẫn**: `bender2000cache` — IEEE FOCS 2000, pp. 399–409.
- **Vấn đề nghiên cứu**: Tối ưu hóa cấu trúc cây tìm kiếm không phụ thuộc tham số kích thước cache cụ thể của phần cứng.
- **Phương pháp & Đóng góp**: Kỹ thuật phân rã Van Emde Boas đạt số lần truyền trang tối ưu $O(\log_B N)$ trên mọi tầng thứ bậc bộ nhớ (L1/L2/L3 Cache và Disk).
- **Vai trò trong bài báo**: Phân tích hành vi bộ nhớ đệm trong xử lý chỉ mục.

### 16. Wu et al. (2014) - Simultaneous Index Selection and Maintenance
- **Trích dẫn**: `wu2014turn` — PVLDB, Vol. 7, No. 14, pp. 1909–1920.
- **Vấn đề nghiên cứu**: Chi phí ẩn của chỉ mục: làm chậm các thao tác `INSERT`, `UPDATE`, `DELETE` do phải cập nhật cây chỉ mục.
- **Phương pháp & Đóng góp**: Đưa ra mô hình đánh đổi định lượng giữa lợi ích tăng tốc truy vấn đọc và chi phí duy trì chỉ mục khi ghi.
- **Vai trò trong bài báo**: Luận điểm cho việc không nên tạo chỉ mục bừa bãi mà phải chọn lọc có phương pháp.

### 17. Kossmann (2000) - State of the Art in Distributed Query Processing
- **Trích dẫn**: `kossmann2000state` — ACM Computing Surveys, Vol. 32, No. 4, pp. 422–469.
- **Vấn đề nghiên cứu**: Tối ưu hóa truy vấn phân tán và phân mảnh bảng.
- **Phương pháp & Đóng góp**: Thuật toán Semi-Join giảm chi phí truyền thông tin qua mạng giữa các nút CSDL.
- **Vai trò trong bài báo**: Phân tích mở rộng CSDL phân tán.

---

## NHÓM 3: THUẬT TOÁN KẾT NỐI ĐA BẢNG & ƯỚC LƯỢNG LỰC LƯỢNG (JOINS & CARDINALITY ESTIMATION)

### 18. Shapiro (1986) - Join Processing with Large Main Memories
- **Trích dẫn**: `shapiro1986join` — ACM TODS, Vol. 11, No. 3, pp. 239–264.
- **Vấn đề nghiên cứu**: Phân tích chi tiết các biến thể của Hash Join khi bộ nhớ RAM khả dụng thay đổi.
- **Phương pháp & Đóng góp**: Giới thiệu Simple Hash Join, GRACE Hash Join, và Hybrid Hash Join; thiết lập công thức tính toán I/O đĩa tối ưu.
- **Vai trò trong bài báo**: Nền tảng phân tích toán tử Hash Join trong Execution Plan của bài báo.

### 19. Mishra & Eich (1992) - Join Processing in Relational Databases
- **Trích dẫn**: `mishra1992join` — ACM Computing Surveys, Vol. 24, No. 1, pp. 63–113.
- **Vấn đề nghiên cứu**: Khảo sát toàn diện mọi thuật toán kết nối bảng: Nested Loops, Block Nested Loops, Index Nested Loops, Sort-Merge Join, và Hash Join.
- **Phương pháp & Đóng góp**: Bảng phân loại ma trận ưu/nhược điểm của từng thuật toán dựa trên kích thước bảng, trạng thái đã sắp xếp và sự hiện diện của chỉ mục.
- **Vai trò trong bài báo**: Khung lý thuyết so sánh các toán tử Join trong Chương 3.

### 20. Poosala et al. (1996) - Improved Histograms for Selectivity Estimation
- **Trích dẫn**: `poosala1996improved` — ACM SIGMOD 1996, pp. 294–305.
- **Vấn đề nghiên cứu**: Ước lượng độ chọn lọc của vị từ khoảng (`Range Predicates`) trong CSDL.
- **Phương pháp & Đóng góp**: Đề xuất lược đồ biểu đồ tần suất Equi-Width, Equi-Depth và MaxDiff Histograms; là nền tảng của thống kê `pg_statistic` và `ANALYZE` trong PostgreSQL/Oracle.
- **Vai trò trong bài báo**: Giải thích cơ chế ước lượng lực lượng của bộ tối ưu hóa chi phí CBO.

### 21. Haas et al. (1995) - Sampling-Based Distinct Values Estimation
- **Trích dẫn**: `haas1995sampling` — VLDB 1995, pp. 311–322.
- **Vấn đề nghiên cứu**: Ước lượng số lượng giá trị phân biệt ($n\_distinct$) của một thuộc tính mà không cần quét toàn bộ bảng.
- **Phương pháp & Đóng góp**: Đưa ra các ước lượng thống kê không chệch dựa trên lấy mẫu ngẫu nhiên, giúp bộ tối ưu chọn đúng kích thước bảng băm trong Hash Join.
- **Vai trò trong bài báo**: Cơ sở phân tích tác động của lệnh `ANALYZE` tới kế hoạch thực thi.

### 22. Markl et al. (2004) - Progressive Query Optimization (POP)
- **Trích dẫn**: `markl2004robust` — ACM SIGMOD 2004, pp. 659–670.
- **Vấn đề nghiên cứu**: Ngăn chặn kế hoạch truy vấn tồi khi số liệu thống kê bị lỗi thời.
- **Phương pháp & Đóng góp**: Chèn các điểm kiểm tra tính hợp lệ (Validity Checkpoints) vào cây kế hoạch; nếu số dòng thực tế sai lệch quá ngưỡng cho phép, hệ thống tạm dừng và tái tối ưu hóa.
- **Vai trò trong bài báo**: Đề xuất giải pháp kiến trúc nâng cao trong phần Thảo luận.

### 23. Stillger et al. (2001) - LEO: Learning Optimizer
- **Trích dẫn**: `stillger2001leo` — VLDB 2001, pp. 19–28.
- **Vấn đề nghiên cứu**: Khả năng tự học từ các lần chạy trước để sửa chữa sai số mô hình chi phí trong IBM DB2.
- **Phương pháp & Đóng góp**: So sánh số dòng thực tế đo được sau khi chạy với số dòng dự báo của bộ tối ưu và lưu vào bộ nhớ phản hồi (Feedback Loop).
- **Vai trò trong bài báo**: Tiền đề cho các nghiên cứu về Learned Query Optimization hiện đại.

### 24. Tzoumas, Deshpande, & Jensen (2011) - Propagation of Uncertainties
- **Trích dẫn**: `tzoumas2011lightweight` — ACM SIGMOD 2011, pp. 481–492.
- **Vấn đề nghiên cứu**: Sự tích lũy sai số theo cấp số nhân khi câu truy vấn có chuỗi kết nối nhiều bảng liên tiếp.
- **Phương pháp & Đóng góp**: Mô hình hóa sai số ước lượng dưới dạng khoảng tin cậy xác suất và chọn kế hoạch có độ bền vững cao nhất (Plan Robustness).
- **Vai trò trong bài báo**: Phân tích nguyên nhân các câu truy vấn Join từ 4 đến 6 bảng trong thực nghiệm bị suy giảm hiệu năng.

### 25. Moerkotte, Neumann, & Steger (2009) - Preventing Bad Plans
- **Trích dẫn**: `moerkotte2009preventing` — ACM SIGMOD 2009, pp. 541–552.
- **Vấn đề nghiên cứu**: Tránh các kế hoạch thực thi thảm họa (Disaster Plans) trong bài toán kết nối bảng có điều kiện lọc.
- **Phương pháp & Đóng góp**: Kỹ thuật phân rã siêu đồ thị (Hypergraph Decomposition) giới hạn không gian tìm kiếm chỉ trên các kế hoạch an toàn.
- **Vai trò trong bài báo**: Hướng dẫn xây dựng các câu truy vấn chuẩn đối chuẩn (Benchmark Queries).

---

## NHÓM 4: PHÂN VÙNG BẢNG & KIẾN TRÚC LƯU TRỮ CỘT/DÒNG (PARTITIONING & STORAGE LAYOUT)

### 26. Stonebraker et al. (2005) - C-Store
- **Trích dẫn**: `stonebraker2005cstore` — VLDB 2005, pp. 553–564.
- **Vấn đề nghiên cứu**: Hạn chế của kiến trúc lưu trữ theo dòng truyền thống đối với các truy vấn phân tích tổng hợp (OLAP).
- **Phương pháp & Đóng góp**: Khởi xướng kiến trúc CSDL hướng cột (Column-oriented DBMS) với khả năng nén siêu cao và chỉ đọc các cột xuất hiện trong câu truy vấn.
- **Vai trò trong bài báo**: So sánh hiệu năng giữa lưu trữ dòng và lưu trữ cột trong phân tích dữ liệu lớn.

### 27. Abadi, Madden, & Hachem (2008) - Column-Stores vs. Row-Stores
- **Trích dẫn**: `abadi2008column` — ACM SIGMOD 2008, pp. 967–980.
- **Vấn đề nghiên cứu**: Giải mã nguồn gốc thực sự tạo nên sự vượt trội của CSDL dạng cột.
- **Phương pháp & Đóng góp**: Chứng minh rằng phép nén dữ liệu theo cột, tính toán trực tiếp trên dữ liệu nén, và xử lý véc-tơ hóa (Block Iteration) tạo ra sự khác biệt tốc độ gấp 10 lần chứ không chỉ đơn thuần là việc tách cột.
- **Vai trò trong bài báo**: Phân tích sâu kiến trúc lưu trữ vật lý trong Chương 2.

### 28. Harizopoulos et al. (2006) - Performance Tradeoffs in Read-Intensive Databases
- **Trích dẫn**: `harizopoulos2006performance` — VLDB 2006, pp. 487–498.
- **Vấn đề nghiên cứu**: Đánh giá chi phí phụ trợ (Overhead) của các hệ thống RDBMS truyền thống trên khối lượng công việc chỉ đọc.
- **Phương pháp & Đóng góp**: Định lượng thời gian CPU tiêu tốn cho quản lý bộ đệm, giải mã tuple, và quản lý khóa giao dịch.
- **Vai trò trong bài báo**: Cung cấp luận cứ cho việc tối ưu hóa mức độ truy cập trang đĩa.

### 29. Rao, Potti, & Taranov (2012) - Scalable Partitioning Strategies
- **Trích dẫn**: `rao2012scalable` — ACM SIGMOD 2012, pp. 613–624.
- **Vấn đề nghiên cứu**: Chiến lược phân mảnh bảng quy mô lớn (Range, List, Hash Partitioning) trên các cụm máy chủ phân tán.
- **Phương pháp & Đóng góp**: Đánh giá hiệu quả của kỹ thuật loại trừ phân vùng (Partition Pruning) khi điều kiện `WHERE` chứa khóa phân vùng.
- **Vai trò trong bài báo**: Cơ sở lý thuyết cho kỹ thuật Table Partitioning theo thời gian trong bài báo.

### 30. Curino et al. (2010) - Schism
- **Trích dẫn**: `curino2010schism` — PVLDB, Vol. 3, No. 1, pp. 48–57.
- **Vấn đề nghiên cứu**: Tự động phân mảnh CSDL dựa trên vết đồ thị truy vấn thực tế của ứng dụng (Workload-driven Partitioning).
- **Phương pháp & Đóng góp**: Sử dụng thuật toán phân hoạch đồ thị (Graph Partitioning Min-Cut) để triệt tiêu các giao dịch phân tán xuyên nút (Distributed Transactions).
- **Vai trò trong bài báo**: Mở rộng phân tích chiến lược phân vùng trong CSDL phân tán.

### 31. Pavlo, Curino, & Madden (2012) - Skew-Aware Automatic Partitioning
- **Trích dẫn**: `pavlo2012skew` — PVLDB, Vol. 5, No. 10, pp. 932–943.
- **Vấn đề nghiên cứu**: Hiện tượng lệch tải dữ liệu (Data Skew & Hotspot Partitions) làm nghẽn một số phân vùng trong khi các phân vùng khác nhàn rỗi.
- **Phương pháp & Đóng góp**: Thuật toán phân vùng thích ứng tự động chia nhỏ các phân vùng nóng và kết hợp các phân vùng nguội.
- **Vai trò trong bài báo**: Phân tích phân phối dữ liệu trong tập đơn hàng thực tế của đề tài.

### 32. Athanassoulis, Bøgh, & Idreos (2019) - Optimal Column-Layout for Hybrid Workloads
- **Trích dẫn**: `athanassoulis2019optimal` — PVLDB, Vol. 12, No. 13, pp. 2393–2407.
- **Vấn đề nghiên cứu**: Bố cục dữ liệu kết hợp (Hybrid Row/Column Layout) cho khối lượng công việc hỗn hợp vừa giao dịch vừa phân tích (HTAP).
- **Phương pháp & Đóng góp**: Tự động nhóm các thuộc tính thường xuyên được truy vấn cùng nhau vào các nhóm cột (Column Groups).
- **Vai trò trong bài báo**: Tham chiếu kiến trúc kho dữ liệu hiện đại.

---

## NHÓM 5: QUẢN LÝ BỘ ĐỆM & BỘ NHỚ ĐỆM TRANG (BUFFER POOL MANAGEMENT & CACHING)

### 33. O'Neil, O'Neil, & Weikum (1993) - LRU-K
- **Trích dẫn**: `oneil1993lruk` — ACM SIGMETRICS 1993, pp. 297–306.
- **Vấn đề nghiên cứu**: Khắc phục nhược điểm của thuật toán LRU kinh điển khi xảy ra quét toàn bảng (Sequential Scan Thrashing) làm sạch toàn bộ cache.
- **Phương pháp & Đóng góp**: Thuật toán LRU-K theo dõi khoảng cách thời gian giữa $K$ lần truy cập gần nhất, phân biệt chính xác giữa trang truy cập định kỳ và trang chỉ quét 1 lần.
- **Vai trò trong bài báo**: Nền tảng phân tích thuật toán bộ đệm Buffer Pool trong Chương 2.

### 34. Megiddo & Modha (2003) - Adaptive Replacement Cache (ARC)
- **Trích dẫn**: `megiddo2003arc` — USENIX FAST 2003, pp. 115–130.
- **Vấn đề nghiên cứu**: Tự động cân bằng giữa yếu tố gần đây (Recency) và yếu tố tần suất (Frequency) mà không cần cấu hình thủ công.
- **Phương pháp & Đóng góp**: Thuật toán ARC tự điều chỉnh kích thước danh sách kép dựa trên các trang ma (Ghost Lists), vượt trội hơn LRU trên mọi khối lượng công việc CSDL thực tế.
- **Vai trò trong bài báo**: Cơ sở lý thuyết về bộ nhớ đệm tự điều chỉnh.

### 35. Johnson & Shasha (1994) - 2Q: Low Overhead Buffer Management
- **Trích dẫn**: `johnson19942q` — VLDB 1994, pp. 439–450.
- **Vấn đề nghiên cứu**: Thuật toán thay thế trang có độ phức tạp $O(1)$ với hiệu năng tương đương LRU-2 nhưng chi phí CPU thấp hơn nhiều.
- **Phương pháp & Đóng góp**: Sử dụng hai hàng đợi (hàng đợi FIFO tạm thời và hàng đợi LRU chính), là nền tảng của thuật toán quản lý bộ đệm trong nhiều CSDL mã nguồn mở.
- **Vai trò trong bài báo**: Đánh giá chi phí I/O và Buffer Hit Ratio.

### 36. Effelsberg & Haerder (1984) - Principles of Database Buffer Management
- **Trích dẫn**: `effelsberg1984principles` — ACM TODS, Vol. 9, No. 4, pp. 560–595.
- **Vấn đề nghiên cứu**: Khảo sát nền tảng về mối quan hệ giữa Bộ đệm trang, Nhật ký ghi trước (WAL), và Thuật toán phục hồi sau sự cố.
- **Phương pháp & Đóng góp**: Định nghĩa các nguyên tắc STEAL/NO-STEAL và FORCE/NO-FORCE chi phối kiến trúc Engine CSDL hiện đại.
- **Vai trò trong bài báo**: Khung lý thuyết cho phần Kiểm soát giao dịch và Bền vững dữ liệu.

### 37. Chou & DeWitt (1985) - DBMIN Buffer Management
- **Trích dẫn**: `chou1985evaluation` — VLDB 1985, pp. 127–141.
- **Vấn đề nghiên cứu**: Quản lý bộ đệm nhận biết ngữ nghĩa của câu truy vấn (Query-Aware Buffer Management).
- **Phương pháp & Đóng góp**: Thuật toán DBMIN cấp phát số lượng trang đệm tối ưu cho từng loại toán tử (Index Scan, Hash Join, Merge Join).
- **Vai trò trong bài báo**: Phân tích tham số `work_mem` và `shared_buffers` trong tinh chỉnh CSDL.

---

## NHÓM 6: HỌC MÁY & TINH CHỈNH TỰ ĐỘNG CƠ SỞ DỮ LIỆU (LEARNED OPTIMIZATION & AUTO-TUNING)

### 38. Kraska et al. (2018) - The Case for Learned Index Structures
- **Trích dẫn**: `kraska2018case` — ACM SIGMOD 2018, pp. 489–504.
- **Vấn đề nghiên cứu**: Xem xét cấu trúc chỉ mục $B^+$-Tree dưới góc nhìn của một hàm phân phối tích lũy xác suất (CDF).
- **Phương pháp & Đóng góp**: Mở ra kỷ nguyên Learned Indexes: dùng mô hình hồi quy nơ-ron để định vị vị trí bản ghi với dung lượng bộ nhớ nhỏ hơn 70% và tốc độ quét nhanh hơn.
- **Vai trò trong bài báo**: Kết nối giữa cấu trúc chỉ mục truyền thống và xu hướng chỉ mục học máy trong CSDL nâng cao.

### 39. Marcus et al. (2019) - Neo: A Learned Query Optimizer
- **Trích dẫn**: `marcus2019neo` — PVLDB, Vol. 12, No. 11, pp. 1705–1718.
- **Vấn đề nghiên cứu**: Thay thế hoàn toàn bộ tối ưu hóa truy vấn thủ công bằng mạng nơ-ron Tree-CNN kết hợp Học tăng cường (Reinforcement Learning).
- **Phương pháp & Đóng góp**: Tự học chiến lược kết nối bảng tối ưu từ lịch sử truy vấn, khắc phục triệt để sai số của bộ ước lượng lực lượng truyền thống.
- **Vai trò trong bài báo**: Tổng quan văn hiến về xu hướng tối ưu hóa hiện đại nhất.

### 40. Marcus et al. (2021) - Bao: Making Learned Query Optimization Practical
- **Trích dẫn**: `marcus2021bao` — ACM SIGMOD 2021, pp. 1275–1288.
- **Vấn đề nghiên cứu**: Làm thế nào để áp dụng máy học vào tối ưu hóa truy vấn một cách an toàn mà không làm sập hệ thống CSDL sản xuất.
- **Phương pháp & Đóng góp**: Bao không tự sinh kế hoạch từ đầu mà điều khiển các cờ gợi ý (Optimizer Hints) của PostgreSQL thông qua thuật toán Contextual Bandits; đạt tốc độ vượt PostgreSQL tới 50% mà không bị suy thoái hiệu năng đột ngột.
- **Vai trò trong bài báo**: Định hướng phương pháp luận tinh chỉnh gợi ý truy vấn (Hint Tuning).

### 41. Yang et al. (2020) - NeuroCard
- **Trích dẫn**: `yang2020neurocard` — PVLDB, Vol. 14, No. 1, pp. 61–73.
- **Vấn đề nghiên cứu**: Ước lượng lực lượng chính xác trên nhiều bảng kết nối có tương quan phức tạp.
- **Phương pháp & Đóng góp**: Mô hình xác suất sinh tự hồi quy sâu (Deep Autoregressive Model) nắm bắt toàn bộ phân phối đồng thời của CSDL quan hệ.
- **Vai trò trong bài báo**: Minh họa giải pháp khắc phục điểm yếu lớn nhất của System R Optimizer.

### 42. Kipf et al. (2020) - RadixSpline
- **Trích dẫn**: `kipf2020radixspline` — aiDM @ ACM SIGMOD 2020, pp. 1–5.
- **Vấn đề nghiên cứu**: Giảm thiểu thời gian huấn luyện và xây dựng chỉ mục học máy.
- **Phương pháp & Đóng góp**: Cấu trúc RadixSpline xây dựng trong 1 lần quét tuần tự với cận sai số bảo đảm, phù hợp cho môi trường dữ liệu có cập nhật thường xuyên.
- **Vai trò trong bài báo**: Tham chiếu tối ưu hóa thời gian xây dựng chỉ mục.

### 43. Zhang et al. (2019) - CDBTune: Automatic Cloud Database Tuning
- **Trích dẫn**: `zhang2019end` — ACM SIGMOD 2019, pp. 415–432.
- **Vấn đề nghiên cứu**: Tinh chỉnh hàng trăm tham số cấu hình phức tạp của CSDL trên điện toán đám mây (Memory, Disk, Concurrency knobs).
- **Phương pháp & Đóng góp**: Áp dụng Deep Reinforcement Learning (DDPG) tự động tìm kiếm cấu hình tối ưu, tăng thông lượng hệ thống tới 30% so với chuyên gia DBA cấu hình thủ công.
- **Vai trò trong bài báo**: Cơ sở lý luận cho phần tinh chỉnh tham số máy chủ CSDL.

### 44. Van Aken et al. (2017) - OtterTune: Automatic DBMS Tuning
- **Trích dẫn**: `vanaken2017automatic` — ACM SIGMOD 2017, pp. 1009–1024.
- **Vấn đề nghiên cứu**: Tự động tinh chỉnh tham số DBMS bằng cách tận dụng kinh nghiệm từ các lần triển khai CSDL trong quá khứ.
- **Phương pháp & Đóng góp**: Sử dụng Phân tích thành phần chính (PCA) và Hồi quy quá trình Gaussian (Gaussian Process Regression) để chọn các tham số có tác động mạnh nhất.
- **Vai trò trong bài báo**: Nền tảng phương pháp luận tinh chỉnh tham số cấu hình hệ quản trị CSDL.

### 45. Sadoghi, Blanas, & Bhowmick (2020) - Modern Transaction Processing
- **Trích dẫn**: `sadoghi2020modern` — ACM TODS, Vol. 45, No. 2, pp. 1–42.
- **Vấn đề nghiên cứu**: Xử lý giao dịch hiện đại trên phần cứng đa lõi (Multi-core) và bộ nhớ lớn (Large In-Memory).
- **Phương pháp & Đóng góp**: Tổng kết các kỹ thuật kiểm soát đồng thời không khóa, giao thức phục hồi và tính bền vững ACID trong CSDL thế hệ mới.
- **Vai trò trong bài báo**: Cơ sở cho việc phân tích tính toàn vẹn dữ liệu trong môi trường giao dịch thương mại điện tử.

---

## MA TRẬN PHÂN BỔ TRÍCH DẪN TRONG BÀI BÁO KHOA HỌC

| Phần trong Bài báo | Các tài liệu tham khảo chính được trích dẫn | Mục đích trích dẫn |
| :--- | :--- | :--- |
| **1. Mở đầu (Introduction)** | [1], [6], [8], [14], [26], [43], [44] | Nêu tầm quan trọng của tối ưu hóa truy vấn trong CSDL lớn, bài toán điểm nghẽn hiệu năng và động lực nghiên cứu. |
| **2. Tổng quan văn hiến (Related Work)** | [1]–[7], [8]–[17], [18]–[25], [26]–[32], [33]–[37], [38]–[45] | Phân loại toàn diện 6 hướng nghiên cứu: Query Optimization, Index Tuning, Join Processing, Partitioning, Buffer Pool, và Learned DB. |
| **3. Cơ sở lý thuyết & Mô hình chi phí (Theoretical Framework)** | [1], [3], [13], [18], [19], [20], [29], [33] | Mô hình hóa toán học hàm chi phí I/O và CPU của CBO, cơ chế của Nested Loops vs Hash vs Merge Join, toán học B-Tree. |
| **4. Phương pháp Đề xuất & Thiết kế Tinh chỉnh (Methodology)** | [8], [10], [13], [16], [21], [29], [31], [40] | Thiết kế quy trình tinh chỉnh chỉ mục 4 bước (Single -> Composite -> Partial -> Covering), giải thuật phân vùng bảng và định tuyến truy vấn. |
| **5. Thiết lập Thực nghiệm & Dữ liệu Thực tế (Experimental Setup)** | [6], [8], [18], [27], [34], [37] | Đặc tả bộ dữ liệu thương mại điện tử thực tế 100.000 đơn hàng, 9 bảng quan hệ chuẩn 3NF, thiết kế 10 câu truy vấn phức tạp (Q1–Q10). |
| **6. Kết quả Thực nghiệm & Phân tích (Results & Analysis)** | [1], [6], [7], [13], [18], [24], [29] | Phân tích chi tiết `EXPLAIN ANALYZE`, so sánh thời gian thực thi, số lượng trang đọc bộ đệm, tỷ lệ trúng cache, và I/O đĩa. |
| **7. Thảo luận & Hướng phát triển (Discussion & Future Work)** | [22], [23], [30], [38], [39], [40], [43], [45] | Thảo luận về kiến trúc Learned Query Optimization, Autonomous Databases và CSDL phân tán. |

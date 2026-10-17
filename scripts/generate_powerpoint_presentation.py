"""
Script: generate_powerpoint_presentation.py
Mục đích: Tự động khởi tạo tệp trình chiếu Microsoft PowerPoint (.pptx) chuẩn mực,
sang trọng (Widescreen 16:9, bảng biểu số liệu thực tế, 22 slides chi tiết)
cho buổi bảo vệ đồ án / tiểu luận môn học Cơ sở dữ liệu nâng cao cấp độ Thạc sĩ.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "SLIDE_THUYET_TRINH_CSDL_NANG_CAO.pptx")
IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "images")

# Palette màu sắc học thuật cao cấp
COLOR_NAVY = RGBColor(24, 43, 73)      # #182B49 - Nền chính tiêu đề & header
COLOR_CYAN = RGBColor(0, 168, 204)     # #00A8CC - Màu điểm nhấn công nghệ
COLOR_GOLD = RGBColor(230, 149, 0)     # #E69500 - Điểm nhấn thành tựu / metrics
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_DARK = RGBColor(33, 37, 41)      # #212529 - Văn bản chính
COLOR_MUTED = RGBColor(108, 117, 125)  # #6C757D - Chú thích
COLOR_CARD_BG = RGBColor(245, 247, 250)
COLOR_CARD_BORDER = RGBColor(220, 226, 235)

def add_header(slide, title_text, category_text="CƠ SỞ DỮ LIỆU NÂNG CAO - BÁO CÁO CAO HỌC"):
    # Header bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_NAVY
    top_bar.line.color.rgb = COLOR_NAVY
    
    # Category tag
    p_cat = top_bar.text_frame.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = "Arial"
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_CYAN
    p_cat.space_after = Pt(2)
    
    # Title text
    p_title = top_bar.text_frame.add_paragraph()
    p_title.text = title_text
    p_title.font.name = "Arial"
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE

def add_card(slide, left, top, width, height, title="", bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    
    if title:
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        p.space_after = Pt(6)
    return card

def add_image_slide(prs, title_text, category_text, img_filename, max_width_in=11.7, max_height_in=5.7):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    add_header(slide, title_text, category_text)
    img_path = os.path.join(IMG_DIR, img_filename)
    if os.path.exists(img_path):
        from PIL import Image
        with Image.open(img_path) as im:
            orig_w, orig_h = im.size
        aspect = orig_w / orig_h
        target_h = max_height_in
        target_w = target_h * aspect
        if target_w > max_width_in:
            target_w = max_width_in
            target_h = target_w / aspect
        left_in = (13.333 - target_w) / 2
        top_in = 1.35 + (max_height_in - target_h) / 2
        slide.shapes.add_picture(img_path, Inches(left_in), Inches(top_in), width=Inches(target_w), height=Inches(target_h))
    return slide


def build_presentation():
    print(f"[*] Đang khởi tạo bản trình chiếu PowerPoint tại: {OUTPUT_PATH}", flush=True)
    prs = Presentation()
    # Tỉ lệ màn hình rộng 16:9 (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TRANG TIÊU ĐỀ (TITLE SLIDE)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.color.rgb = COLOR_NAVY

    tf1 = bg1.text_frame
    tf1.word_wrap = True
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf1.paragraphs[0]
    p.text = "BÁO CÁO DỰ ÁN THỰC TẾ & BÀI BÁO KHOA HỌC"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "NGHIÊN CỨU, ĐÁNH GIÁ VÀ TỐI ƯU HÓA HIỆU NĂNG TRUY VẤN\nTRÊN CƠ SỞ DỮ LIỆU QUAN HỆ QUY MÔ LỚN"
    p.font.name = "Arial"
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(8)

    p = tf1.add_paragraph()
    p.text = "Kỹ thuật Tinh chỉnh Chỉ mục Nâng cao, Phân vùng Dữ liệu và Tối ưu hóa Kế hoạch Thực thi\n(Thực nghiệm trên Dữ liệu Thực tế Olist Store 100.000 Đơn hàng)"
    p.font.name = "Arial"
    p.font.size = Pt(15)
    p.font.italic = True
    p.font.color.rgb = COLOR_GOLD
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(24)

    p = tf1.add_paragraph()
    p.text = "Học phần: Cơ sở dữ liệu nâng cao  |  Chương trình Thạc sĩ CNTT  |  Năm 2026"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: BỐI CẢNH & ĐỘNG LỰC NGHIÊN CỨU
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. Bối cảnh Doanh nghiệp & Điểm nghẽn Hiệu năng CSDL")
    
    card1 = add_card(slide2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Thách thức Dữ liệu Lớn trong RDBMS")
    tf = card1.text_frame
    p = tf.add_paragraph()
    p.text = "• Bùng nổ Giao dịch E-Commerce:\n  Dữ liệu đơn hàng, thanh toán, đánh giá tăng trưởng liên tục lên hàng trăm nghìn - hàng triệu bản ghi chuẩn 3NF.\n\n" \
             "• Báo cáo Quản trị Phức hợp:\n  Đòi hỏi phép kết nối đồng thời từ 3 đến 6 bảng lớn với các điều kiện lọc thời gian và tính toán doanh thu.\n\n" \
             "• Suy thoái Hiệu năng Nghiêm trọng:\n  Truy vấn chậm từ vài ms lên 10-30s khi thiếu thiết kế vật lý, làm nghẽn toàn bộ tài nguyên I/O đĩa và CPU."
    p.font.size = Pt(12.5)
    p.font.color.rgb = COLOR_DARK

    card2 = add_card(slide2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "3 Khoảng trống Kỹ thuật Cốt lõi")
    tf = card2.text_frame
    p = tf.add_paragraph()
    p.text = "1. Sai số Ước lượng Lực lượng (Leis et al. VLDB):\n  Bộ tối ưu hóa CBO ước lượng sai số dòng lên tới 10^4 - 10^6 lần, chọn nhầm toán tử Join tồi tệ.\n\n" \
             "2. Nghịch lý Tinh chỉnh Chỉ mục (Selectivity Trap):\n  Tạo chỉ mục đơn trên cột có độ chọn lọc thấp (ví dụ: status='delivered' chiếm 97%) làm chậm hơn quét tuần tự.\n\n" \
             "3. Quét Bảng Đơn khối Cồng kềnh:\n  Quét lãng phí hàng chục nghìn trang dữ liệu lịch sử không liên quan thay vì áp dụng Partition Pruning."
    p.font.size = Pt(12.5)
    p.font.color.rgb = COLOR_DARK

    # =========================================================================
    # SLIDE 3: MỤC TIÊU & CÂU HỎI NGHIÊN CỨU (RQ1 - RQ3)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Mục tiêu Khoa học & 3 Câu hỏi Nghiên cứu (RQs)")

    box_w = Inches(3.6)
    box_h = Inches(5.4)

    c1 = add_card(slide3, Inches(0.8), Inches(1.5), box_w, box_h, "RQ1: Kế hoạch Thực thi", bg_color=COLOR_WHITE)
    tf1 = c1.text_frame
    p1 = tf1.add_paragraph()
    p1.text = "Kế hoạch thực thi vật lý (Execution Plan) thay đổi như thế nào khi chuyển dịch qua 4 giai đoạn tinh chỉnh:\n\n" \
              "• SCAN TABLE (Quét toàn bảng)\n" \
              "• SEARCH USING INDEX (Chỉ mục đơn)\n" \
              "• COMPOSITE INDEX (Đa thuộc tính)\n" \
              "• INDEX-ONLY SCAN (Chỉ mục bao phủ)\n\n" \
              "Mức độ cải thiện độ trễ định lượng là bao nhiêu lần?"
    p1.font.size = Pt(12)
    p1.font.color.rgb = COLOR_DARK

    c2 = add_card(slide3, Inches(4.8), Inches(1.5), box_w, box_h, "RQ2: Nghịch lý Chỉ mục", bg_color=COLOR_WHITE)
    tf2 = c2.text_frame
    p2 = tf2.add_paragraph()
    p2.text = "Trong điều kiện nào việc tạo chỉ mục đơn làm suy giảm hiệu năng truy vấn so với quét toàn bộ bảng?\n\n" \
              "• Bản chất chi phí I/O đọc ngẫu nhiên (Random Disk Seeks) qua cây B-Tree.\n" \
              "• Ngưỡng độ chọn lọc vị từ (Selectivity Threshold > 20%).\n" \
              "• Giải pháp khắc phục bằng Composite & Partial Indexing."
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_DARK

    c3 = add_card(slide3, Inches(8.8), Inches(1.5), box_w, box_h, "RQ3: Cắt tỉa Phân vùng", bg_color=COLOR_WHITE)
    tf3 = c3.text_frame
    p3 = tf3.add_paragraph()
    p3.text = "Kỹ thuật phân vùng bảng theo dải thời gian (Range Partitioning) kết hợp Loại trừ phân vùng (Partition Pruning) đem lại hiệu quả gì?\n\n" \
              "• Mức độ cắt giảm số trang đĩa quét.\n" \
              "• Đánh giá thời gian truy vấn trên dữ liệu thực tế 100.000 đơn hàng.\n" \
              "• Hệ số tăng tốc thực tế so với bảng đơn khối."
    p3.font.size = Pt(12)
    p3.font.color.rgb = COLOR_DARK

    # =========================================================================
    # SLIDE 4: KHẢO SÁT 45 CÔNG TRÌNH KHOA HỌC ĐỈNH CAO
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. Ma trận Tổng quan 45 Tài liệu Tham khảo Khoa học")

    c = add_card(slide4, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.4), "Hệ thống hóa 45 Công trình Khoa học Hạng A* (ACM SIGMOD, VLDB, IEEE TKDE, ACM TODS)")
    tf = c.text_frame
    p = tf.add_paragraph()
    p.text = "1. Nhóm Tối ưu hóa Truy vấn Kinh điển (Selinger 1979, Chaudhuri 1998, Graefe 1993, Leis et al. 2015, 2018):\n" \
             "   Mô hình chi phí System R, giải thuật quy hoạch động Join Order, mô hình lặp Volcano, và bộ benchmark JOB trên dữ liệu thực tế.\n\n" \
             "2. Nhóm Tinh chỉnh Chỉ mục & Thiết kế Vật lý (Chaudhuri & Narasayya 1997, Agrawal 2000, Bruno 2002, Graefe 2011, Comer 1979):\n" \
             "   Công cụ AutoAdmin, DB2 Design Advisor, Partial Indexing và cơ chế Covering Index (INDEX-ONLY SCAN).\n\n" \
             "3. Nhóm Thuật toán Kết nối & Histogram (Shapiro 1986, Mishra 1992, Poosala 1996, Haas 1995, Markl 2004, Stillger 2001):\n" \
             "   Mô hình chi phí Hash Join, Sort-Merge Join, biểu đồ tần suất Equi-Depth, và bộ tối ưu hóa tự học LEO.\n\n" \
             "4. Nhóm Phân vùng Bảng & Lưu trữ Cột/Dòng (Stonebraker 2005, Abadi 2008, Rao 2012, Curino 2010, Pavlo 2012):\n" \
             "   Kiến trúc C-Store, kỹ thuật nén cột, phân mảnh Workload-driven Schism, và cơ chế Partition Pruning.\n\n" \
             "5. Nhóm Quản trị Bộ đệm & Cache (O'Neil 1993, Megiddo & Modha 2003, Johnson 1994, Effelsberg 1984, Chou 1985):\n" \
             "   Thuật toán thay thế trang LRU-K, Adaptive Replacement Cache (ARC), và nguyên tắc đệm truy vấn DBMIN.\n\n" \
             "6. Nhóm Học máy & Tinh chỉnh CSDL Tự động (Kraska 2018, Marcus 2019 Neo, 2021 Bao, Yang 2020, Zhang 2019 CDBTune):\n" \
             "   Chỉ mục học máy Learned B-Tree, điều khiển cờ gợi ý Optimizer Hints bằng Reinforcement Learning, và tự động tinh chỉnh cấu hình."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_DARK

    # =========================================================================
    # SLIDE 5: LƯU TRỮ VẬT LÝ & QUẢN LÝ BỘ ĐỆM TRANG (BUFFER POOL)
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. Cấu trúc Lưu trữ Vật lý & Quản lý Bộ đệm (Buffer Pool)")

    c1 = add_card(slide5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Cấu trúc Slotted Page & Chi phí I/O")
    tf = c1.text_frame
    p = tf.add_paragraph()
    p.text = "• Đơn vị Truy xuất Khối đĩa (Pages):\n  CSDL quản lý đĩa theo trang 4KB - 8KB cố định. Mọi phép đọc ghi đều nạp nguyên trang đĩa.\n\n" \
             "• Chi phí Truy xuất Đĩa:\n" \
             "  - Đọc tuần tự (Sequential I/O): c_seq = 1.0 (nhanh nhờ cơ chế Read-Ahead).\n" \
             "  - Đọc ngẫu nhiên (Random I/O): c_rand = 4.0 (rất đắt đỏ do phải nhảy trục cơ học hoặc địa chỉ nhớ).\n\n" \
             "• Mục tiêu Tối ưu hóa:\n  Giảm thiểu tối đa số lượng trang đĩa cần nạp vào bộ đệm RAM."
    p.font.size = Pt(12.5)

    c2 = add_card(slide5, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Cơ chế Bộ đệm Trang & Tinh chỉnh Cấu hình")
    tf = card2.text_frame
    p = c2.text_frame.add_paragraph()
    p.text = "• Phân cấp Độ trễ Bộ nhớ:\n" \
             "  - Buffer Hit (RAM): ~100 ns\n" \
             "  - Buffer Miss (NVMe SSD): ~100,000 ns (chậm hơn 1.000 lần)\n" \
             "  - Buffer Miss (HDD): ~10,000,000 ns (chậm hơn 100.000 lần)\n\n" \
             "• Thuật toán Thay thế Trang Tiên tiến:\n  LRU-K và ARC phân tách trang quét tạm thời và trang truy cập thường xuyên, ngăn ô nhiễm bộ đệm.\n\n" \
             "• Tham số Cấu hình Then chốt:\n  shared_buffers (vùng đệm chung), work_mem (bộ nhớ băm và sắp xếp), random_page_cost."
    p.font.size = Pt(12.5)

    # =========================================================================
    # SLIDE 6: CHỈ MỤC PHỨC HỢP & QUY TẮC TIỀN TỐ DÀI NHẤT
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Cây B+Tree & Quy tắc Tiền tố Dài nhất trong Composite Index")

    c1 = add_card(slide6, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Đặc tính Cây B+Tree")
    tf = c1.text_frame
    p = tf.add_paragraph()
    p.text = "• Cấu trúc Tự Cân bằng Bậc M:\n  Mọi nút lá đều ở cùng một độ sâu; chiều cao cây luôn bảo đảm O(log_M N), thường chỉ 3 - 4 tầng cho hàng triệu dòng.\n\n" \
             "• Nút Lá Liên kết Đôi (Doubly-Linked Leaves):\n  Cho phép duyệt tuần tự cực nhanh trong các truy vấn quét khoảng (Range Queries) mà không cần quay lui lên nút gốc.\n\n" \
             "• Tối ưu Hóa I/O Khối:\n  Kích thước mỗi nút cây B+Tree được thiết kế vừa vặn với kích thước một trang đĩa vật lý."
    p.font.size = Pt(12.5)

    c2 = add_card(slide6, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Quy tắc Tiền tố Dài nhất (Leftmost Prefix Rule)")
    tf = c2.text_frame
    p = tf.add_paragraph()
    p.text = "• Nguyên lý Hoạt động của Composite Index:\n  Một chỉ mục trên (Col1, Col2, Col3) sắp xếp ưu tiên tuyệt đối theo Col1, sau đó mới đến Col2, rồi Col3.\n\n" \
             "• Khi nào Chỉ mục có Tác dụng?\n  - Lọc trên (Col1): CÓ DÙNG INDEX\n  - Lọc trên (Col1, Col2): CÓ DÙNG INDEX\n  - Lọc chỉ trên (Col2, Col3): VÔ HIỆU HÓA (Full Scan)!\n\n" \
             "• Thứ tự Vàng khi Thiết kế Composite Index:\n  (Cột lọc Đẳng thức = , Cột Kết nối JOIN, Cột lọc Khoảng Range < >)"
    p.font.size = Pt(12.5)

    # =========================================================================
    # SLIDE 7: KỸ THUẬT ĐỘT PHÁ: COVERING INDEX & INDEX-ONLY SCAN
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. Đột phá Hiệu năng: Covering Index & INDEX-ONLY SCAN")

    c1 = add_card(slide7, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Cơ chế Chỉ mục Thông thường (2 Bước Đọc)")
    tf = c1.text_frame
    p = tf.add_paragraph()
    p.text = "1. Bước 1: Duyệt cây B+Tree tìm khóa tìm kiếm, lấy được con trỏ dòng (RowID / Tuple Pointer).\n\n" \
             "2. Bước 2 (Điểm nghẽn): Đọc Trang Bảng Dữ liệu (Heap Table Fetch) từ đĩa để lấy các cột còn lại trong mệnh đề SELECT.\n\n" \
             "Hậu quả: Nếu có 10.000 dòng thỏa mãn, hệ thống phải thực hiện 10.000 phép đọc đĩa ngẫu nhiên (Random Heap Fetches), làm chậm toàn bộ truy vấn!"
    p.font.size = Pt(12.5)

    c2 = add_card(slide7, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Cơ chế Covering Index (1 Bước Đọc Duy nhất)")
    tf = c2.text_frame
    p = tf.add_paragraph()
    p.text = "• Khái niệm Chỉ mục Bao phủ (Covering Index):\n  Bao gồm toàn bộ các cột xuất hiện trong câu lệnh SELECT vào lá của cây chỉ mục (Composite hoặc INCLUDE clause).\n\n" \
             "• Kích hoạt Toán tử INDEX-ONLY SCAN:\n  Bộ tối ưu hóa CBO nhận diện toàn bộ dữ liệu cần lấy đã nằm sẵn trong lá B-Tree.\n\n" \
             "• Lợi ích Vượt trội:\n  Triệt tiêu 100% thao tác đọc Heap Pages trên đĩa, tăng tốc độ truy vấn từ 40% đến 60%!"
    p.font.size = Pt(12.5)

    add_image_slide(prs, "6B. Bản chất Vật lý: B+Tree Index Scan vs. Covering Index-Only Scan", "CẤU TRÚC VẬT LÝ VÀ BỘ NHỚ", "fig8_index_scan_vs_index_only.png")


    # =========================================================================
    # SLIDE 8: CÁC THUẬT TOÁN KẾT NỐI ĐA BẢNG (JOINS)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "7. Động học các Toán tử Kết nối Đa Bảng (Joins)")

    bw = Inches(3.6)
    bh = Inches(5.4)

    c1 = add_card(slide8, Inches(0.8), Inches(1.5), bw, bh, "Nested Loop Join", bg_color=COLOR_WHITE)
    tf1 = c1.text_frame
    p1 = tf1.add_paragraph()
    p1.text = "• Cơ chế:\n  Duyệt từng dòng bảng ngoài, tìm kiếm dòng tương ứng trong bảng trong.\n\n" \
              "• Khi nào Tối ưu?\n  Bảng ngoài rất nhỏ (<100 dòng) và bảng trong có chỉ mục B-Tree (Index Nested Loop).\n\n" \
              "• Nguy cơ Thảm họa:\n  Chi phí O(M * N) bùng nổ nếu hai bảng đều lớn và thiếu chỉ mục."
    p1.font.size = Pt(12)

    c2 = add_card(slide8, Inches(4.8), Inches(1.5), bw, bh, "Hash Join", bg_color=COLOR_WHITE)
    tf2 = c2.text_frame
    p2 = tf2.add_paragraph()
    p2.text = "• Cơ chế:\n  - Build: Băm bảng nhỏ vào RAM (work_mem).\n  - Probe: Quét bảng lớn đối chiếu khóa băm.\n\n" \
              "• Khi nào Tối ưu?\n  Hai bảng đều lớn, phép kết nối bằng (=), không có thứ tự sắp xếp sẵn.\n\n" \
              "• Điểm nghẽn:\n  Tốn RAM; nếu bảng băm vượt work_mem phải tràn xuống đĩa (Grace Hash Join)."
    p2.font.size = Pt(12)

    c3 = add_card(slide8, Inches(8.8), Inches(1.5), bw, bh, "Sort-Merge Join", bg_color=COLOR_WHITE)
    tf3 = c3.text_frame
    p3 = tf3.add_paragraph()
    p3.text = "• Cơ chế:\n  Sắp xếp cả hai bảng theo thuộc tính kết nối, sau đó duyệt đồng thời 2 con trỏ tuần tự.\n\n" \
              "• Khi nào Tối ưu?\n  Dữ liệu lớn đã được chỉ mục B-Tree sắp xếp sẵn theo thứ tự kết nối.\n\n" \
              "• Điểm nghẽn:\n  Chi phí External Sort rất đắt đỏ nếu dữ liệu ban đầu chưa được sắp xếp."
    p3.font.size = Pt(12)

    # =========================================================================
    # SLIDE 9: PHÂN VÙNG BẢNG & CẮT TỈA PHÂN VÙNG (PARTITION PRUNING)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "8. Kỹ thuật Phân vùng Bảng & Cắt tỉa (Partition Pruning)")

    c1 = add_card(slide9, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Kiến trúc Phân vùng Dải Thời gian (Range)")
    tf = c1.text_frame
    p = tf.add_paragraph()
    p.text = "• Phân tách Bảng Lớn thành các Phân vùng Con:\n  Bảng orders (100.000 dòng) được phân vùng theo năm:\n  - orders_2016: 329 đơn hàng\n  - orders_2017: 45.101 đơn hàng\n  - orders_2018: 54.011 đơn hàng\n\n" \
             "• Ràng buộc Kiểm tra (Check Constraints):\n  Mỗi phân vùng có ràng buộc ngày tháng nghiêm ngặt và chỉ mục cục bộ (Local B-Tree Index)."
    p.font.size = Pt(12.5)

    c2 = add_card(slide9, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Nguyên lý Cắt tỉa Phân vùng (Partition Pruning)")
    tf = c2.text_frame
    p = tf.add_paragraph()
    p.text = "• Loại trừ Phân vùng Tự động:\n  Khi câu truy vấn lọc dữ liệu quý 3 năm 2017 (2017-06-01 đến 2017-08-31):\n\n" \
             "• Kế hoạch Thực thi Thông minh:\n  Bộ tối ưu hóa đối chiếu ràng buộc phân vùng và LOẠI BỎ HOÀN TOÀN việc quét phân vùng 2016 và 2018!\n\n" \
             "• Hiệu quả Thực tế:\n  Tiết kiệm hơn 54.000 dòng quét đĩa, giảm 89,9% thời gian truy vấn (từ 71,58 ms xuống 7,26 ms, nhanh gần 10 lần)!"
    p.font.size = Pt(12.5)

    add_image_slide(prs, "8B. Chuỗi Thời gian Đơn hàng Thực tế & Chiến lược Phân vùng Bảng", "PHÂN VÙNG DỮ LIỆU THỰC TẾ", "fig3_orders_time_series_partitioning.png")


    # =========================================================================
    # SLIDE 10: QUẢN TRỊ GIAO DỊCH, ACID, MVCC & WAL
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "9. Quản trị Giao dịch, ACID, MVCC và Phục hồi WAL")

    c1 = add_card(slide10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Bảo đảm Tính toàn vẹn ACID")
    tf = c1.text_frame
    p = tf.add_paragraph()
    p.text = "• Atomicity (Nguyên tố):\n  Thao tác đặt hàng, trừ kho và thanh toán nằm trong 1 Transaction duy nhất; commit hoàn toàn hoặc rollback toàn bộ.\n\n" \
             "• Consistency (Nhất quán):\n  Các ràng buộc toàn vẹn khóa chính, khóa ngoại (FK) giữa orders, items, customers luôn hợp lệ.\n\n" \
             "• Isolation (Cô lập):\n  Ngăn ngừa các hiện tượng đọc bẩn (Dirty Read), đọc không lặp lại (Non-repeatable Read)."
    p.font.size = Pt(12.5)

    c2 = add_card(slide10, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Cơ chế MVCC & Nhật ký WAL")
    tf = c2.text_frame
    p = tf.add_paragraph()
    p.text = "• MVCC (Multi-Version Concurrency Control):\n  Tạo các bản sao phiên bản của dòng dữ liệu. Các câu truy vấn đọc báo cáo không bao giờ khóa các thao tác ghi đơn hàng mới!\n\n" \
             "• Write-Ahead Logging (WAL):\n  Mọi sửa đổi dữ liệu trang đệm đều được ghi tuần tự vào tệp WAL trên đĩa trước khi ghi xuống bảng dữ liệu.\n\n" \
             "• Giao thức Phục hồi ARIES:\n  Bảo đảm khôi phục 100% dữ liệu nguyên vẹn sau khi gặp sự cố mất điện đột ngột."
    p.font.size = Pt(12.5)

    # =========================================================================
    # SLIDE 11: ĐẶC TẢ BỘ DỮ LIỆU THỰC TẾ OLIST STORE (100.000 ĐƠN HÀNG)
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "10. Đặc tả Bộ Dữ liệu Thực tế Olist Store (Brazil E-Commerce)")

    c = add_card(slide11, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.4), "Hệ thống 8 Bảng Quan hệ Chuẩn 3NF (Tổng dung lượng 85,07 MB, >500.000 dòng)")
    tf = c.text_frame
    p = tf.add_paragraph()
    p.text = "• Bảng orders (99.441 bản ghi): Quản lý vòng đời đơn hàng, thời gian đặt, duyệt, giao hàng, trạng thái.\n" \
             "• Bảng order_items (112.650 bản ghi): Chi tiết từng sản phẩm, giá bán, cước vận chuyển, người bán.\n" \
             "• Bảng customers (99.441 bản ghi): Thông tin người mua hàng, thành phố, tiểu bang tại Brazil.\n" \
             "• Bảng products (32.951 bản ghi): Danh mục ngành hàng, kích thước, khối lượng sản phẩm.\n" \
             "• Bảng order_payments (103.886 bản ghi): Phương thức thanh toán (thẻ, trả góp, boleto), giá trị.\n" \
             "• Bảng order_reviews (99.224 bản ghi): Đánh giá của khách hàng (điểm 1 - 5 sao), phản hồi.\n" \
             "• Bảng sellers (3.095 bản ghi): Thông tin người bán theo địa bàn địa lý.\n\n" \
             "Tính Thực tế Tuyệt đối: Dữ liệu giao dịch thật của sàn thương mại điện tử lớn nhất Brazil, " \
             "chứa đầy đủ các quan hệ 1-N, N-N phức tạp, hoàn hảo cho bài toán tối ưu hóa CSDL nâng cao."
    p.font.size = Pt(12)

    add_image_slide(prs, "10B. Sơ đồ Quan hệ Thực thể ERD (8 Bảng Chuẩn 3NF, 100k Đơn hàng)", "LƯỢC ĐỒ CƠ SỞ DỮ LIỆU THỰC TẾ", "fig1_database_erd.png")

    # =========================================================================
    # SLIDE 12: THIẾT KẾ TẬP TRUY VẤN ĐỐI CHUẨN Q1 - Q5
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "11. Thiết kế Tập Truy vấn Đối chuẩn Thực nghiệm Q1 - Q5")

    c = add_card(slide12, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.4), "Workload Benchmark Mô phỏng Hoạt động Phân tích Kinh doanh Đa chiều")
    tf = c.text_frame
    p = tf.add_paragraph()
    p.text = "• Truy vấn Q1: Báo cáo Doanh thu theo Bang & Trạng thái Giao hàng (2-Table Join + Aggregation)\n" \
             "  orders (100k) JOIN customers (99k), lọc order_status = 'delivered', tính số đơn và ngày giao trung bình theo bang.\n\n" \
             "• Truy vấn Q2: Top 10 Ngành hàng Doanh thu Cao nhất Năm 2017 (3-Table Join + Range Filter)\n" \
             "  orders JOIN order_items JOIN products, lọc khoảng thời gian cả năm 2017, gom nhóm theo ngành hàng. (Kiểm thử Covering Index).\n\n" \
             "• Truy vấn Q3: Tương quan Điểm Đánh giá & Cước phí Vận chuyển (4-Table Join)\n" \
             "  orders JOIN order_items JOIN order_reviews JOIN sellers, phân tích so sánh đơn hàng 1 sao và 5 sao theo từng bang người bán.\n\n" \
             "• Truy vấn Q4: Phân tích Khách hàng VIP & Phương thức Thanh toán (5-Table Join)\n" \
             "  customers JOIN orders JOIN order_payments JOIN order_items JOIN products, lọc payment_value > 500 R$.\n\n" \
             "• Truy vấn Q5: Quét Khoảng Thời gian Đơn hàng (Time-Window Range Scan)\n" \
             "  Quét dữ liệu quý 3 năm 2017 để đo kiểm và đối chứng cơ chế Cắt tỉa phân vùng (Partition Pruning)."
    p.font.size = Pt(12)

    add_image_slide(prs, "11B. Dữ liệu Thực tế: Phương thức Thanh toán & Kỳ hạn Trả góp (Q4)", "PHÂN TÍCH NGHIỆP VỤ THỰC TẾ", "fig5_payment_distribution.png")

    # =========================================================================
    # SLIDE 13: QUY TRÌNH TINH CHỈNH VẬT LÝ 4 GIAI ĐOẠN
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    add_header(slide13, "12. Quy trình Tinh chỉnh Vật lý 4 Giai đoạn Chuẩn hóa")

    bw = Inches(2.7)
    bh = Inches(5.4)

    s0 = add_card(slide13, Inches(0.8), Inches(1.5), bw, bh, "Giai đoạn 0\nBaseline", bg_color=COLOR_WHITE)
    tf = s0.text_frame
    p = tf.add_paragraph()
    p.text = "• Trạng thái Cơ sở Chưa có Chỉ mục.\n• Chỉ có khóa chính PK mặc định.\n• Mọi phép kết nối và vị từ đều phải SCAN TABLE toàn bộ bảng."
    p.font.size = Pt(11)

    s1 = add_card(slide13, Inches(3.8), Inches(1.5), bw, bh, "Giai đoạn 1\nSingle B-Tree", bg_color=COLOR_WHITE)
    tf = s1.text_frame
    p = tf.add_paragraph()
    p.text = "• Tạo chỉ mục đơn trên các khóa ngoại (FK) và cột lọc.\n• idx_orders_status\n• idx_orders_ts\n• idx_items_product\n• Chuyển sang SEARCH TABLE."
    p.font.size = Pt(11)

    s2 = add_card(slide13, Inches(6.8), Inches(1.5), bw, bh, "Giai đoạn 2 & 3\nCovering Index", bg_color=COLOR_WHITE)
    tf = s2.text_frame
    p = tf.add_paragraph()
    p.text = "• Tạo chỉ mục phức hợp theo tiền tố dài nhất.\n• Tạo Covering Index đưa toàn bộ cột SELECT vào lá B-Tree.\n• Kích hoạt toán tử INDEX-ONLY SCAN."
    p.font.size = Pt(11)

    s3 = add_card(slide13, Inches(9.8), Inches(1.5), bw, bh, "Giai đoạn 4\nPartitioning", bg_color=COLOR_WHITE)
    tf = s3.text_frame
    p = tf.add_paragraph()
    p.text = "• Phân vùng bảng theo dải thời gian năm.\n• Ràng buộc kiểm tra Check Constraints.\n• Kích hoạt Partition Pruning bỏ qua phân vùng lịch sử."
    p.font.size = Pt(11)

    # =========================================================================
    # SLIDE 14: KẾT QUẢ ĐỐI CHUẨN ĐỊNH LƯỢNG TRUY VẤN Q1 - Q5
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    add_header(slide14, "13. Bảng Kết quả Đo đạc Định lượng Toàn diện (Q1 - Q5)")

    # Bảng slide PowerPoint
    rows, cols = 6, 5
    table_shape = slide14.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(1.0)
    table.columns[1].width = Inches(4.5)
    table.columns[2].width = Inches(2.0)
    table.columns[3].width = Inches(2.2)
    table.columns[4].width = Inches(2.0)

    t_headers = ["Mã", "Tên Truy vấn Nghiệp vụ", "Chưa Index (ms)", "Covering Index (ms)", "Hệ số Tăng tốc"]
    for idx, th in enumerate(t_headers):
        cell = table.cell(0, idx)
        cell.text = th
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(11)
                run.font.color.rgb = COLOR_WHITE

    t_data = [
        ["Q1", "Báo cáo Doanh thu theo Bang (2 Tables)", "1.770,33 ms", "1.880,87 ms", "0,9x - 1,0x (Nghịch lý)"],
        ["Q2", "Top 10 Ngành hàng 2017 (3 Tables)", "2.474,99 ms", "1.179,07 ms", "2,1x (Nhanh hơn 52,4%)"],
        ["Q3", "Tương quan Đánh giá & Cước phí (4 Tables)", "3.461,84 ms", "3.130,73 ms", "1,1x (Hồi phục từ S1)"],
        ["Q4", "Khách hàng VIP & Thanh toán (5 Tables)", "2.666,27 ms", "1.659,81 ms", "1,6x (Nhanh hơn 37,7%)"],
        ["Q5", "Quét Khoảng Thời gian (Partition Pruning)", "71,58 ms", "7,26 ms", "10x (Nhanh hơn 89,9%)"]
    ]

    for r_idx, r_data in enumerate(t_data, start=1):
        for c_idx, val in enumerate(r_data):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            bg_c = RGBColor(242, 245, 248) if r_idx % 2 == 1 else COLOR_WHITE
            cell.fill.fore_color.rgb = bg_c
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER if c_idx in [0, 2, 3, 4] else PP_ALIGN.LEFT
                for run in p.runs:
                    run.font.size = Pt(11)
                    run.font.color.rgb = COLOR_DARK
                    if c_idx == 4 and "2,1x" in val:
                        run.font.bold = True
                        run.font.color.rgb = COLOR_GOLD
                    elif c_idx == 4 and "10x" in val:
                        run.font.bold = True
                        run.font.color.rgb = COLOR_CYAN

    add_image_slide(prs, "13B. Biểu đồ Đối sánh Thời gian Thực thi (Latency) Q1 - Q4", "KẾT QUẢ THỰC NGHIỆM ĐỊNH LƯỢNG", "fig6_query_latency_comparison.png")


    # =========================================================================
    # SLIDE 15: PHÂN TÍCH SÂU Q2: SỰ BỨT PHÁ CỦA COVERING INDEX
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    add_header(slide15, "14. Phân tích Chuyên sâu Q2: Bứt phá 2,1x nhờ Covering Index")

    c1 = add_card(slide15, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Trước Tối ưu: SCAN TABLE (2.474,99 ms)")
    tf = c1.text_frame
    p = tf.add_paragraph()
    p.text = "• Kế hoạch Thực thi Stage 0:\n  SCAN oi | BLOOM FILTER ON o | BLOOM FILTER ON p\n\n" \
             "• Hành vi Vật lý:\n  Công cụ CSDL phải quét tuần tự toàn bộ 112.650 bản ghi của bảng order_items trên đĩa.\n\n" \
             "• Điểm nghẽn I/O:\n  Hàng nghìn trang đĩa vật lý bị nạp vào bộ nhớ, tiêu tốn 2.474,99 ms thời gian CPU và đĩa."
    p.font.size = Pt(12.5)

    c2 = add_card(slide15, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Sau Tối ưu: INDEX-ONLY SCAN (1.179,07 ms)")
    tf = c2.text_frame
    p = tf.add_paragraph()
    p.text = "• Giải pháp Tinh chỉnh Stage 3:\n  Tạo chỉ mục bao phủ:\n  CREATE INDEX idx_items_covering ON order_items(order_id, product_id, price, freight_value);\n\n" \
             "• Kế hoạch Thực thi Tối ưu:\n  SEARCH o USING INDEX idx_orders_ts | SEARCH oi USING INDEX idx_items_covering (order_id=?)\n\n" \
             "• Kết quả:\n  Triệt tiêu 100% việc đọc trang bảng order_items, thời gian giảm xuống 1.179,07 ms (Nhanh gấp 2,1 lần)!"
    p.font.size = Pt(12.5)

    add_image_slide(prs, "14B. Kết quả Nghiệp vụ Q2: Top 10 Ngành hàng Doanh thu Cao nhất 2017", "KẾT QUẢ THỰC NGHIỆM ĐỊNH LƯỢNG", "fig4_top_categories_revenue.png")


    # =========================================================================
    # SLIDE 16: PHÂN TÍCH SÂU Q1 & Q3: NGHỊCH LÝ CHỈ MỤC ĐỘ CHỌN LỌC THẤP
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    add_header(slide16, "15. Phân tích Chuyên sâu Q1 & Q3: Nghịch lý Độ Chọn lọc Thấp")

    c1 = add_card(slide16, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Hiện tượng Suy giảm Hiệu năng ở Stage 1")
    tf = c1.text_frame
    p = tf.add_paragraph()
    p.text = "• Khi tạo chỉ mục đơn idx_orders_status ON orders(order_status):\n" \
             "  - Q1: Chậm từ 1.770,33 ms lên 1.997,52 ms (+12,8%)\n" \
             "  - Q3: Chậm từ 3.461,84 ms lên 4.175,80 ms (+20,6%)\n\n" \
             "• Câu hỏi Đặt ra:\n  Tại sao có thêm chỉ mục B-Tree mà truy vấn lại chạy chậm hơn quét toàn bảng (Full Table Scan)?"
    p.font.size = Pt(12.5)

    c2 = add_card(slide16, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Bản chất Học thuật & Khắc phục")
    tf = c2.text_frame
    p = tf.add_paragraph()
    p.text = "• Bản chất Thống kê Dữ liệu Thực tế:\n  Có tới 96.478 trong tổng số 99.441 đơn hàng mang trạng thái 'delivered' (Độ chọn lọc Selectivity = 97,02%)!\n\n" \
             "• Căn nguyên I/O:\n  Duyệt chỉ mục B-Tree buộc hệ thống thực hiện >96.000 phép đọc đĩa ngẫu nhiên (Random Disk Seeks). Quét tuần tự nhanh hơn vì đọc các khối trang liên tiếp (Graefe 2011).\n\n" \
             "• Giải pháp Khắc phục:\n  Chuyển sang Composite Index hoặc Partial Index, phục hồi lại thời gian tối ưu."
    p.font.size = Pt(12.5)

    add_image_slide(prs, "15B. Minh chứng Dữ liệu: Phân bố Trạng thái Đơn hàng (97,02% Delivered)", "NGHỊCH LÝ CHỈ MỤC & ĐỘ CHỌN LỌC", "fig2_order_status_distribution.png")


    # =========================================================================
    # SLIDE 17: PHÂN TÍCH SÂU Q5: TĂNG TỐC 10 LẦN NHỜ PARTITION PRUNING
    # =========================================================================
    slide17 = prs.slides.add_slide(blank_layout)
    add_header(slide17, "16. Phân tích Chuyên sâu Q5: Tăng tốc 10x nhờ Partition Pruning")

    c1 = add_card(slide17, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Bảng Không Phân vùng: 71,58 ms")
    tf = c1.text_frame
    p = tf.add_paragraph()
    p.text = "• Câu truy vấn quét dữ liệu Quý 3/2017:\n  WHERE order_purchase_timestamp BETWEEN '2017-06-01' AND '2017-08-31'\n\n" \
             "• Hành vi của Bảng Đơn khối:\n  Hệ thống buộc phải quét tuần tự toàn bộ 99.441 dòng của bảng orders, nạp hàng nghìn trang đĩa chứa cả các đơn hàng năm 2016 và 2018 không liên quan."
    p.font.size = Pt(12.5)

    c2 = add_card(slide17, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Phân vùng có Cắt tỉa: 7,26 ms (Nhanh hơn 89,9%)")
    tf = c2.text_frame
    p = tf.add_paragraph()
    p.text = "• Cơ chế Cắt tỉa Phân vùng (Partition Pruning):\n  Bộ tối ưu hóa đối chiếu ràng buộc kiểm tra của các phân vùng:\n  - Bỏ qua phân vùng orders_2016 (329 dòng)\n  - Bỏ qua phân vùng orders_2018 (54.011 dòng)\n\n" \
             "• Kết quả:\n  Chỉ quét duy nhất phân vùng orders_2017. Thời gian giảm thẳng từ 71,58 ms xuống 7,26 ms, tăng tốc gần 10 lần!"
    p.font.size = Pt(12.5)

    add_image_slide(prs, "16B. Minh chứng Thực nghiệm Q5: Cắt tỉa Phân vùng Tăng tốc Gần 10 Lần", "KẾT QUẢ THỰC NGHIỆM ĐỊNH LƯỢNG", "fig7_partition_pruning_performance.png")


    # =========================================================================
    # SLIDE 18: BỘ CHỈ DẪN THIẾT KẾ VẬT LÝ DÀNH CHO KỸ SƯ CSDL (DBA GUIDELINES)
    # =========================================================================
    slide18 = prs.slides.add_slide(blank_layout)
    add_header(slide18, "17. Bộ Chỉ dẫn Thiết kế Vật lý Thực tiễn cho Doanh nghiệp")

    c = add_card(slide18, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.4), "4 Quy tắc Vàng Đúc kết từ Thực nghiệm Dữ liệu Lớn")
    tf = c.text_frame
    p = tf.add_paragraph()
    p.text = "1. Quy tắc Ngưỡng Chọn lọc (Selectivity Rule):\n" \
             "   Tuyệt đối không tạo chỉ mục đơn trên các thuộc tính có độ chọn lọc thấp (tỷ lệ thỏa mãn > 20%), trừ khi dùng trong Composite Index hoặc Partial Index.\n\n" \
             "2. Thiết kế Covering Index cho các Truy vấn Trọng yếu (Critical Path Queries):\n" \
             "   Đưa toàn bộ danh sách các cột cần hiển thị trong SELECT vào chỉ mục để kích hoạt INDEX-ONLY SCAN, loại bỏ 100% chi phí đọc Heap đĩa.\n\n" \
             "3. Thu thập Số liệu Thống kê Định kỳ (ANALYZE / Statistics):\n" \
             "   Số liệu phân phối histogram và số giá trị phân biệt (n_distinct) chính xác là điều kiện tiên quyết để CBO không chọn nhầm kế hoạch tồi.\n\n" \
             "4. Áp dụng Phân vùng Bảng theo Thời gian (Time-Range Partitioning):\n" \
             "   Đối với các bảng đơn hàng và giao dịch chuỗi thời gian, phân vùng kết hợp Partition Pruning là giải pháp tối thượng để duy trì hiệu năng ổn định."
    p.font.size = Pt(13)

    # =========================================================================
    # SLIDE 19: ĐÓNG GÓP KHOA HỌC & ĐỊNH HƯỚNG PHÁT TRIỂN LUẬN VĂN
    # =========================================================================
    slide19 = prs.slides.add_slide(blank_layout)
    add_header(slide19, "18. Đóng góp Khoa học & Hướng Mở rộng Luận văn Thạc sĩ")

    c1 = add_card(slide19, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "Đóng góp của Dự án")
    tf = c1.text_frame
    p = tf.add_paragraph()
    p.text = "• Bộ Dữ liệu Thực tế & Lược đồ 3NF:\n  Xây dựng CSDL quan hệ thực tế chuẩn hóa từ sàn thương mại Olist Store (85 MB, 100k đơn hàng).\n\n" \
             "• Kiểm chứng Lý thuyết bằng Thực nghiệm:\n  Minh chứng định lượng hiện tượng nghịch lý chỉ mục, cơ chế Index-Only Scan và Partition Pruning.\n\n" \
             "• Bản thảo Bài báo IEEE Chuẩn mực:\n  Hoàn thiện bản thảo khoa học IMRAD và mã nguồn LaTeX sẵn sàng nộp các hội nghị chuyên ngành."
    p.font.size = Pt(12.5)

    c2 = add_card(slide19, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Hướng Phát triển Luận văn Thạc sĩ")
    tf = c2.text_frame
    p = tf.add_paragraph()
    p.text = "• Learned Query Optimization (Bao & Neo):\n  Ứng dụng mạng nơ-ron Tree-CNN và Reinforcement Learning tự động học các cờ gợi ý (Optimizer Hints) thích ứng với khối lượng công việc động.\n\n" \
             "• CSDL Lai HTAP (Hybrid Transactional/Analytical):\n  Đánh giá hiệu năng đồng thời giữa xử lý giao dịch OLTP và phân tích OLAP trên kiến trúc cột hiện đại (DuckDB/ClickHouse)."
    p.font.size = Pt(12.5)

    # =========================================================================
    # SLIDE 20: KẾT LUẬN & HỎI ĐÁP (Q&A)
    # =========================================================================
    slide20 = prs.slides.add_slide(blank_layout)
    bg20 = slide20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg20.fill.solid()
    bg20.fill.fore_color.rgb = COLOR_NAVY
    bg20.line.color.rgb = COLOR_NAVY

    tf20 = bg20.text_frame
    tf20.word_wrap = True
    tf20.vertical_anchor = MSO_ANCHOR.MIDDLE

    p = tf20.paragraphs[0]
    p.text = "XIN TRÂN TRỌNG CẢM ƠN THẦY CÔ VÀ HỘI ĐỒNG!"
    p.font.name = "Arial"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(16)

    p = tf20.add_paragraph()
    p.text = "Kính mong nhận được sự nhận xét và đóng góp ý kiến của Thầy Cô!"
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.color.rgb = COLOR_CYAN
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(24)

    p = tf20.add_paragraph()
    p.text = "Học phần: Cơ sở dữ liệu nâng cao  |  Chương trình Thạc sĩ CNTT"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_GOLD
    p.alignment = PP_ALIGN.CENTER

    saved_path = OUTPUT_PATH
    try:
        prs.save(OUTPUT_PATH)
    except PermissionError:
        saved_path = os.path.join(OUTPUT_DIR, "SLIDE_THUYET_TRINH_CSDL_NANG_CAO_CHITIET.pptx")
        prs.save(saved_path)
        print(f"[!] Lưu ý: Tệp {OUTPUT_PATH} đang được mở trong ứng dụng khác (WPS/PowerPoint).")
        print(f"[*] Đã lưu bản slide chi tiết có hình ảnh tại: {saved_path}")

    file_size_kb = os.path.getsize(saved_path) / 1024
    print(f"[+] Đã tạo thành công bản trình chiếu PowerPoint ({file_size_kb:.2f} KB) tại:\n    {saved_path}", flush=True)


if __name__ == "__main__":
    build_presentation()

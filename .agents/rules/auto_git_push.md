# Quy tắc Tự động Đồng bộ Git (Auto Git Push Rule)

## BẮT BUỘC (MANDATORY REQUIREMENT)
Sau mỗi lần chỉnh sửa, tạo mới hoặc cập nhật bất kỳ tệp tin nào (mã nguồn, tài liệu, báo cáo, dữ liệu, cấu hình...) trong workspace `d:\CaNhan\csdltt`:
1. Luôn tự động kiểm tra trạng thái thay đổi (`git status`).
2. Tự động thêm toàn bộ thay đổi vào staging (`git add .`).
3. Tự động tạo commit với thông điệp rõ ràng, chuẩn Conventional Commits (`git commit -m "..."`).
4. Tự động đẩy ngay lập tức lên kho lưu trữ GitHub chính thức: `git push origin main` (Kho lưu trữ: `https://github.com/tghip26/csdlnc.git`).
5. Không bao giờ để trạng thái git dở dang (uncommitted / unpushed) khi kết thúc lượt phản hồi.

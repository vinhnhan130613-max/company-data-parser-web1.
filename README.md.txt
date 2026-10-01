# Company Data Parser (Streamlit Web App)

Ứng dụng Python giúp phân tích **dữ liệu thô** của công ty và tự động đưa vào các trường 1–9.

## 🚀 Tính năng
- **Trường 1**: Tên công ty gốc (Title Case).
- **Trường 2**: Dịch tên công ty sang tiếng Anh (dịch động theo nội dung).
- **Trường 3**: Địa chỉ trước khi gặp Phường/Xã.
- **Trường 4**: Dịch Trường 3 sang tiếng Anh (không dấu + hậu tố St/Quarter/Village/Hamlet).
- **Trường 5**: Phường/Xã từ địa chỉ thuế.
- **Trường 6**: Dịch sang tiếng Anh (Ward/Commune).
- **Trường 7**: Điện thoại (chuẩn hóa).
- **Trường 8**: Người đại diện (Title Case).
- **Trường 9**: Tóm tắt ngày/tháng/năm + phone + xác nhận.

## 📦 Cài đặt
Clone repo về máy:
```bash
git clone https://github.com/your-username/company-data-parser.git
cd company-data-parser

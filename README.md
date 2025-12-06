# 📅 Ứng dụng Quản lý Lịch trình Cá nhân với Xử lý Tiếng Việt

Ứng dụng quản lý lịch trình cá nhân tích hợp xử lý ngôn ngữ tự nhiên tiếng Việt, cho phép người dùng thêm sự kiện bằng cách nhập câu tiếng Việt tự do.

## ✨ Tính năng chính

### 1. **Nhập liệu ngôn ngữ tự nhiên tiếng Việt**
- Nhập sự kiện bằng câu tiếng Việt tự nhiên
- Ví dụ: "Họp nhóm lúc 10 giờ sáng mai ở phòng 302, nhắc trước 15 phút"
- Hỗ trợ cả văn bản có dấu và không dấu

### 2. **Xử lý NLP với 5 Components**

#### Component 1: Tiền xử lý văn bản
- Tách từ tiếng Việt sử dụng `underthesea`
- Chuẩn hóa văn bản (loại bỏ khoảng trắng thừa)
- Hỗ trợ cả văn bản có dấu và không dấu

#### Component 2: Named Entity Recognition (NER)
- Nhận diện thực thể TIME và LOCATION
- Sử dụng pattern matching cho tiếng Việt

#### Component 3: Rule-based Extraction
- Trích xuất tên sự kiện
- Trích xuất địa điểm (pattern: "ở", "tại", "phòng")
- Trích xuất thời gian nhắc nhở (pattern: "nhắc trước X phút/giờ")

#### Component 4: Time Parser
- Chuyển đổi thời gian tương đối thành tuyệt đối:
  - "hôm nay", "mai", "ngày mai"
  - "tuần sau", "tháng sau"
  - "thứ 2", "thứ 3", ..., "chủ nhật"
  - Giờ: "10 giờ", "10h", "10:30", "10h30"
  - Buổi: "sáng", "chiều", "tối", "đêm"
  - Ngày cụ thể: "25/12", "25-12"

#### Component 5: Validation & Merging
- Kiểm tra tính hợp lệ của dữ liệu
- Ghép kết quả từ các component
- Xử lý lỗi và thông báo

### 3. **Quản lý Sự kiện (CRUD)**
- ✅ **Thêm**: Thêm sự kiện từ NLP hoặc form thủ công
- ✅ **Sửa**: Chỉnh sửa thông tin sự kiện
- ✅ **Xóa**: Xóa sự kiện
- ✅ **Tìm kiếm**: Tìm kiếm theo tên, thời gian, địa điểm
- ✅ **Hiển thị**: Xem lịch theo Ngày/Tuần/Tháng

### 4. **Lưu trữ SQLite**
- Database cục bộ với SQLite
- Bảng `events` với các trường đầy đủ
- Hỗ trợ import/export dữ liệu

### 5. **Hệ thống Nhắc nhở Tự động**
- Chạy trong thread riêng (không làm lag app)
- Kiểm tra định kỳ mỗi 60 giây
- Thông báo khi đến giờ nhắc
- Hỗ trợ nhắc trước X phút/giờ

### 6. **Xuất/Nhập Dữ liệu**
- ✅ Xuất ra file `.ics` (iCalendar format)
- ✅ Xuất ra JSON
- ✅ Nhập từ JSON

## 📁 Cấu trúc Project

```
dacn2/
├── app.py                          # File chính chạy Streamlit
├── requirements.txt                # Dependencies
├── README.md                       # Hướng dẫn sử dụng (file này)
├── database/
│   ├── __init__.py
│   └── db_manager.py              # Quản lý SQLite
├── nlp/
│   ├── __init__.py
│   ├── preprocessor.py            # Component 1: Tiền xử lý
│   ├── ner_extractor.py           # Component 2: NER
│   ├── rule_extractor.py          # Component 3: Rule-based
│   ├── time_parser.py             # Component 4: Time parsing
│   └── nlp_pipeline.py            # Component 5: Pipeline tổng hợp
├── reminder/
│   ├── __init__.py
│   └── reminder_system.py         # Hệ thống nhắc nhở
├── utils/
│   ├── __init__.py
│   ├── export_import.py           # Xuất/nhập ICS, JSON
│   └── constants.py               # Hằng số
└── tests/
    ├── __init__.py
    └── test_cases.py              # 30 test cases tiếng Việt
```

## 🚀 Hướng dẫn Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/HuynhCongY/dacn2.git
cd dacn2
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

**Lưu ý:** Lần đầu chạy, `underthesea` sẽ tự động tải các model cần thiết. Quá trình này có thể mất vài phút.

### 3. Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ tự động mở trong trình duyệt tại địa chỉ: `http://localhost:8501`

## 📖 Hướng dẫn Sử dụng

### Trang 1: Thêm Sự kiện

#### Cách 1: Nhập bằng tiếng Việt tự nhiên
1. Vào trang "📅 Thêm sự kiện"
2. Nhập câu tiếng Việt mô tả sự kiện
3. Nhấn "🚀 Thêm sự kiện từ văn bản"
4. Xem thông tin đã trích xuất và xác nhận

**Ví dụ:**
- "Họp nhóm lúc 10 giờ sáng mai ở phòng 302, nhắc trước 15 phút"
- "Đi khám răng 3 giờ chiều thứ 6 này"
- "Sinh nhật bạn vào 8 giờ tối ngày 25/12"
- "Nộp báo cáo deadline 5 giờ chiều mai"
- "Học tiếng Anh 7 giờ sáng hôm nay"

#### Cách 2: Nhập thủ công
1. Sử dụng form nhập thủ công bên dưới
2. Điền đầy đủ thông tin
3. Nhấn "➕ Thêm sự kiện"

### Trang 2: Xem Lịch

#### Tab Ngày
- Chọn ngày muốn xem
- Hiển thị tất cả sự kiện trong ngày đó

#### Tab Tuần
- Chọn ngày trong tuần
- Hiển thị tất cả sự kiện trong tuần đó

#### Tab Tháng
- Chọn tháng và năm
- Hiển thị tất cả sự kiện trong tháng

#### Tab Tìm kiếm
- Nhập từ khóa (tên sự kiện, địa điểm, mô tả)
- Xem kết quả tìm kiếm

### Trang 3: Xuất/Nhập

#### Xuất dữ liệu
- **Xuất ICS**: Xuất ra file .ics để import vào Google Calendar, Outlook, v.v.
- **Xuất JSON**: Xuất ra file JSON để backup hoặc chuyển đổi dữ liệu

#### Nhập dữ liệu
- Upload file JSON để import sự kiện
- Xem preview trước khi import

#### Xóa dữ liệu
- Xóa toàn bộ sự kiện (cẩn thận!)

### Trang 4: Test NLP

#### Test một câu
- Nhập câu tiếng Việt để test
- Xem kết quả trích xuất chi tiết

#### Test 30 test cases
- Chạy test tự động với 30 test cases
- Xem độ chính xác của hệ thống
- Xem chi tiết các case thất bại

## 🧪 Test Cases

Ứng dụng đi kèm với 30 test cases tiếng Việt đa dạng, bao gồm:

1. **Thời gian cơ bản**: "Họp nhóm lúc 10 giờ sáng mai"
2. **Địa điểm**: "Tập gym tại phòng 501 lúc 6 giờ tối"
3. **Nhắc nhở**: "Gặp khách hàng 3 giờ chiều mai, nhắc trước 30 phút"
4. **Thời gian phức tạp**: "Thi cuối kỳ 7h30 sáng thứ 2 tuần sau"
5. **Không dấu**: "Hop nhom luc 10 gio sang mai o phong 302"
6. **Trường hợp đặc biệt**: "Meeting online 9h30 sáng thứ 2, nhắc trước 5 phút"

**Yêu cầu độ chính xác**: ≥90% (27/30 câu trở lên)

## 🎯 Công nghệ Sử dụng

- **Python 3.8+**
- **Streamlit**: Framework UI
- **underthesea**: Thư viện NLP tiếng Việt
- **SQLite**: Database
- **python-dateutil**: Xử lý thời gian
- **pytz**: Múi giờ
- **ics**: Xuất file iCalendar
- **pandas**: Xử lý dữ liệu

## 🔧 Cấu hình

### Múi giờ
Ứng dụng sử dụng múi giờ `Asia/Ho_Chi_Minh` (GMT+7). Có thể thay đổi trong file `utils/constants.py`.

### Khoảng thời gian kiểm tra nhắc nhở
Mặc định: 60 giây. Có thể thay đổi trong file `utils/constants.py`.

### Database
Mặc định lưu tại file `calendar.db` trong thư mục hiện tại.

## 📊 Database Schema

### Bảng `events`

| Trường | Kiểu | Mô tả |
|--------|------|-------|
| id | INTEGER PRIMARY KEY | ID tự động tăng |
| event_name | TEXT | Tên sự kiện (bắt buộc) |
| start_time | TEXT | Thời gian bắt đầu ISO format (bắt buộc) |
| end_time | TEXT | Thời gian kết thúc ISO format (tùy chọn) |
| location | TEXT | Địa điểm (tùy chọn) |
| reminder_minutes | INTEGER | Số phút nhắc trước (tùy chọn) |
| description | TEXT | Mô tả (tùy chọn) |
| created_at | TEXT | Thời gian tạo ISO format |
| notified | INTEGER | Đã thông báo hay chưa (0/1) |

## 🎨 Giao diện

### Screenshots

#### 1. Trang Thêm sự kiện
- Form nhập tiếng Việt tự nhiên
- Preview thông tin đã trích xuất
- Form nhập thủ công (fallback)

#### 2. Trang Xem lịch
- View theo Ngày/Tuần/Tháng
- Tìm kiếm sự kiện
- Sửa/Xóa sự kiện

#### 3. Trang Xuất/Nhập
- Xuất ICS/JSON
- Import từ JSON
- Xóa dữ liệu

#### 4. Trang Test NLP
- Test một câu
- Test 30 cases tự động
- Hiển thị độ chính xác

## 🐛 Xử lý Lỗi

Ứng dụng có xử lý lỗi đầy đủ cho:

- ✅ Văn bản đầu vào rỗng
- ✅ Không trích xuất được thời gian
- ✅ Không trích xuất được tên sự kiện
- ✅ File import không hợp lệ
- ✅ Database errors
- ✅ NLP errors

## 📝 Lưu ý

1. **NLP không hoàn hảo 100%**: Một số câu phức tạp hoặc mơ hồ có thể không parse chính xác. Trong trường hợp đó, sử dụng form nhập thủ công.

2. **Thời gian trong quá khứ**: Nếu chỉ nhập giờ mà giờ đó đã qua trong ngày, hệ thống sẽ tự động chuyển sang ngày hôm sau.

3. **Thread nhắc nhở**: Hệ thống nhắc nhở chạy trong background thread. Streamlit cần phải chạy liên tục để nhắc nhở hoạt động.

4. **Database backup**: Nên thường xuyên export dữ liệu ra JSON để backup.

## 🚧 Phát triển Thêm

### Tính năng có thể mở rộng:

- [ ] Thêm authentication (đăng nhập)
- [ ] Hỗ trợ multi-user
- [ ] Sync với Google Calendar
- [ ] Push notification (web/mobile)
- [ ] Recurring events (sự kiện lặp lại)
- [ ] Attach files vào sự kiện
- [ ] Share events với người khác
- [ ] AI suggestions cho thời gian tối ưu
- [ ] Dark mode
- [ ] Mobile responsive

## 👨‍💻 Tác giả

**Huỳnh Công Ý**

- GitHub: [@HuynhCongY](https://github.com/HuynhCongY)

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🙏 Acknowledgments

- **underthesea**: Thư viện NLP tiếng Việt tuyệt vời
- **Streamlit**: Framework UI đơn giản và mạnh mẽ
- Tất cả các thư viện open source khác được sử dụng trong project

## 📞 Liên hệ & Hỗ trợ

Nếu gặp vấn đề hoặc có câu hỏi, vui lòng:

1. Mở issue trên GitHub
2. Email: [your-email@example.com]

---

**Chúc bạn sử dụng ứng dụng hiệu quả! 📅✨**
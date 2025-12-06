# HƯỚNG DẪN SỬ DỤNG ỨNG DỤNG QUẢN LÝ LỊCH TRÌNH CÁ NHÂN

## 🚀 Khởi động ứng dụng

### 1. Cài đặt môi trường

```bash
# Clone repository
git clone https://github.com/HuynhCongY/dacn2.git
cd dacn2

# Cài đặt thư viện
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run app.py
```

Ứng dụng sẽ tự động mở tại: `http://localhost:8501`

---

## 📅 TRANG 1: THÊM SỰ KIỆN

### Cách 1: Nhập bằng tiếng Việt tự nhiên (Khuyến nghị)

#### Ví dụ câu nhập:

✅ **Có địa điểm + nhắc nhở:**

```
Họp nhóm lúc 10 giờ sáng mai ở phòng 302, nhắc trước 15 phút
```

✅ **Chỉ có thời gian:**

```
Đi khám răng 3 giờ chiều thứ 6 này
```

✅ **Có ngày cụ thể:**

```
Sinh nhật bạn vào 8 giờ tối ngày 25/12
```

✅ **Có deadline:**

```
Nộp báo cáo deadline 5 giờ chiều mai
```

#### Quy tắc nhập:

- **Thời gian**: Hỗ trợ nhiều format

  - Giờ: `10 giờ`, `10h`, `10:30`, `10h30`
  - Buổi: `sáng`, `chiều`, `tối`
  - Ngày: `hôm nay`, `mai`, `thứ 2`, `chủ nhật`, `25/12`
  - Tuần/tháng: `tuần sau`, `tháng sau`

- **Địa điểm**: Dùng từ khóa

  - `ở`, `tại`, `phòng`
  - Ví dụ: `ở trường`, `tại bệnh viện`, `phòng 501`

- **Nhắc nhở**: Format chuẩn
  - `nhắc trước X phút`
  - `nhắc trước X giờ`
  - Ví dụ: `nhắc trước 30 phút`, `nhắc trước 2 giờ`

### Cách 2: Nhập thủ công

Sử dụng form bên dưới nếu:

- NLP không parse chính xác
- Cần nhập chi tiết hơn
- Muốn kiểm soát từng trường

---

## 📆 TRANG 2: XEM LỊCH

### Tab "Ngày"

1. Chọn ngày cần xem
2. Hiển thị tất cả sự kiện trong ngày
3. Sửa/xóa sự kiện trực tiếp

### Tab "Tuần"

1. Chọn bất kỳ ngày nào trong tuần
2. Xem tất cả sự kiện cả tuần (Thứ 2 - Chủ nhật)

### Tab "Tháng"

1. Chọn tháng và năm
2. Xem tổng quan sự kiện trong tháng

### Tab "Tìm kiếm"

- Nhập từ khóa (tên, địa điểm, mô tả)
- Kết quả hiển thị ngay lập tức

### Thao tác với sự kiện

- **Sửa**: Click icon ✏️ → Chỉnh sửa → Lưu
- **Xóa**: Click icon 🗑️ → Xác nhận

---

## ⚙️ TRANG 3: XUẤT/NHẬP

### Xuất dữ liệu

#### Xuất file ICS (iCalendar)

- Format chuẩn quốc tế
- Import vào:
  - Google Calendar
  - Microsoft Outlook
  - Apple Calendar
  - Bất kỳ ứng dụng lịch nào

**Cách dùng:**

1. Click "📤 Xuất ICS"
2. Tải file `.ics`
3. Import vào ứng dụng lịch của bạn

#### Xuất file JSON

**Cách dùng:**

1. Click "📤 Xuất JSON"
2. Tải file `.json`
3. Lưu trữ an toàn

### Nhập dữ liệu

#### Nhập từ JSON

**Cách dùng:**

1. Click "Chọn file JSON để nhập"
2. Chọn file đã xuất trước đó
3. Xem preview số sự kiện
4. Click "📥 Import vào database"

**Format JSON:**

```json
[
  {
    "event": "Họp nhóm",
    "start_time": "2025-11-01T10:00:00",
    "end_time": null,
    "location": "phòng 302",
    "reminder_minutes": 15
  }
]
```

### Xóa dữ liệu

⚠️ **CẢNH BÁO:** Không thể khôi phục!

**Cách dùng:**

1. Tick ✅ "Tôi hiểu và muốn xóa toàn bộ dữ liệu"
2. Click "🗑️ Xóa toàn bộ sự kiện"

---

## 🔔 HỆ THỐNG NHẮC NHỞ

### Cách hoạt động

- Tự động kiểm tra mỗi 60 giây
- Thông báo khi đến giờ nhắc
- Không nhắc lại sau khi đã thông báo

### Trạng thái

- **🔔 Đang chạy**: Hệ thống hoạt động bình thường
- **🔔 Dừng**: Cần khởi động lại ứng dụng

### Lưu ý

- Ứng dụng phải chạy để nhận thông báo
- Đóng trình duyệt = tắt nhắc nhở
- Refresh trang = reset trạng thái nhắc nhở

---

## 💡 MẸO SỬ DỤNG

### 1. Nhập nhanh sự kiện hàng loạt

```
Họp team 10h mai ở phòng A101, nhắc trước 10 phút
Đi gym 6h tối hôm nay
Sinh nhật mẹ 8h tối ngày 15/12, nhắc trước 2 giờ
```

### 2. Tìm kiếm nhanh

- Dùng từ khóa ngắn: `họp`, `khám`, `gym`
- Tìm theo địa điểm: `phòng 302`

---

# Hệ Thống Quản Lý Lịch với NLP Tiếng Việt

## Giới thiệu

Hệ thống quản lý lịch thông minh cho phép người dùng nhập sự kiện bằng **câu tiếng Việt tự nhiên** và tự động trích xuất thông tin (tên sự kiện, thời gian, địa điểm) thông qua NLP Pipeline.

**Ví dụ:**
- Input: *"Họp team lúc 10h sáng mai tại phòng 301"*
- Output: Sự kiện "Họp team" vào 10:00 AM ngày mai, địa điểm "phòng 301"

## Tính năng chính

- ✅ **NLP Pipeline** với 5 components xử lý tiếng Việt
- ✅ **Thêm sự kiện** bằng ngôn ngữ tự nhiên hoặc thủ công
- ✅ **Quản lý CRUD** đầy đủ (Xem, Sửa, Xóa, Tìm kiếm)
- ✅ **Nhắc nhở tự động** trước khi sự kiện diễn ra
- ✅ **Export/Import** dữ liệu (ICS, JSON)
- ✅ **Giao diện Streamlit** thân thiện, dễ sử dụng

## Công nghệ sử dụng

- **Ngôn ngữ:** Python 3.9+
- **UI:** Streamlit
- **Database:** SQLite
- **NLP:** Custom pipeline (Preprocessing, NER, Rule-based, Time Parsing, Validation)

## Cài đặt

```bash
# Clone repository
git clone https://github.com/HuynhCongY/dacn2.git
cd dacn2

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc venv\Scripts\activate trên Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run app.py
```

## Sơ đồ thiết kế hệ thống

📊 **Xem chi tiết các sơ đồ thiết kế:** [docs/diagrams.md](docs/diagrams.md)

Hệ thống bao gồm các sơ đồ sau (sử dụng Mermaid.js):

1. **Sơ đồ khối (Block Diagram)** - Kiến trúc tổng thể 4 layers
2. **Flowchart** - Luồng xử lý NLP và Time Parsing chi tiết
3. **Sequence Diagram** - Tương tác giữa các thành phần (Add Event, Reminder System)
4. **ERD** - Cơ sở dữ liệu (events, notifications)
5. **Use Case Diagram** - 10 chức năng chính
6. **Class Diagram** - Cấu trúc code
7. **State Diagram** - Vòng đời sự kiện

**Hướng dẫn export sơ đồ:** [docs/export_diagrams.md](docs/export_diagrams.md)

## Tài liệu

- 📖 [Báo cáo đồ án đầy đủ](docs/bao_cao_do_an.md)
- 📊 [Sơ đồ thiết kế hệ thống](docs/diagrams.md)
- 🖼️ [Hướng dẫn export diagrams](docs/export_diagrams.md)

## Cấu trúc dự án

```
dacn2/
├── app.py                  # Main Streamlit application
├── requirements.txt
├── README.md
├── docs/                   # Documentation
│   ├── diagrams.md        # System design diagrams
│   ├── export_diagrams.md # Export guide
│   └── bao_cao_do_an.md   # Full project report
├── src/                    # Source code
│   ├── nlp/               # NLP Pipeline components
│   ├── database/          # Database management
│   ├── reminder/          # Reminder system
│   └── utils/             # Utilities
├── tests/                  # Test cases
└── data/                   # SQLite database
```

## NLP Pipeline

Hệ thống xử lý văn bản tiếng Việt qua 5 components:

1. **Component 1: Preprocessing** - Chuẩn hóa, tách từ
2. **Component 2: NER Extraction** - Trích xuất TIME, LOCATION
3. **Component 3: Rule-based Extract** - Tên sự kiện, reminder
4. **Component 4: Time Parsing** - Chuyển đổi thời gian tương đối/tuyệt đối
5. **Component 5: Validation** - Kiểm tra tính hợp lệ

**Độ chính xác:** 87-90% (tested với 30 test cases)

## Ví dụ sử dụng

```python
# Thêm sự kiện bằng NLP
text = "Họp team lúc 10h sáng mai tại phòng 301, nhắc trước 15 phút"

# Hệ thống tự động parse:
{
    "event_name": "Họp team",
    "start_time": "2024-12-07 10:00:00",
    "location": "phòng 301",
    "reminder_minutes": 15
}
```

## Test Cases

Hệ thống đã được test với 30 test cases bao gồm:
- Thời gian tương đối: "mai", "tuần sau", "tháng sau"
- Thời gian tuyệt đối: "25/12/2024", "Chủ nhật này"
- Buổi trong ngày: "sáng", "chiều", "tối"
- Địa điểm đa dạng
- Reminder: "nhắc trước X phút"

**Pass rate:** 90% (27/30 cases)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Liên hệ

- **Tác giả:** Huỳnh Công Ý
- **Repository:** https://github.com/HuynhCongY/dacn2
- **Issues:** https://github.com/HuynhCongY/dacn2/issues

---

**⭐ Nếu project hữu ích, hãy cho một star nhé! ⭐**
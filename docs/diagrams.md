# Sơ Đồ Thiết Kế Hệ Thống - Vietnamese NLP Event Management

## Mục lục
1. [Sơ đồ khối - Kiến trúc tổng thể](#1-sơ-đồ-khối---kiến-trúc-tổng-thể)
2. [Flowchart - Luồng xử lý NLP](#2-flowchart---luồng-xử-lý-nlp)
3. [Sequence Diagram - Tương tác giữa các thành phần](#3-sequence-diagram---tương-tác-giữa-các-thành-phần)
4. [ERD - Entity Relationship Diagram](#4-erd---entity-relationship-diagram)
5. [Use Case Diagram](#5-use-case-diagram)
6. [Class Diagram - Cấu trúc code](#6-class-diagram---cấu-trúc-code)
7. [State Diagram - Trạng thái sự kiện](#7-state-diagram---trạng-thái-sự-kiện)

---

## 1. SƠ ĐỒ KHỐI - KIẾN TRÚC TỔNG THỂ

Sơ đồ này mô tả kiến trúc tổng thể của hệ thống, bao gồm các lớp chính: Presentation, Application, Data và Background Services.

```mermaid
graph TB
    subgraph "Presentation Layer"
        UI[Streamlit UI]
        UI_INPUT[Input: Văn bản tiếng Việt]
        UI_DISPLAY[Display: Danh sách sự kiện]
        UI_EXPORT[Export/Import]
    end
    
    subgraph "Application Layer"
        NLP[NLP Pipeline]
        EVENT_MGR[Event Manager]
        REMINDER[Reminder System]
    end
    
    subgraph "NLP Pipeline Components"
        C1[Component 1:<br/>Preprocessing]
        C2[Component 2:<br/>NER Extraction]
        C3[Component 3:<br/>Rule-based Extract]
        C4[Component 4:<br/>Time Parsing]
        C5[Component 5:<br/>Validation]
        
        C1 --> C2 --> C3 --> C4 --> C5
    end
    
    subgraph "Data Layer"
        DB[(SQLite Database)]
        FILE[File I/O<br/>ICS/JSON]
    end
    
    subgraph "Background Services"
        THREAD[Reminder Thread<br/>Check every 60s]
    end
    
    UI_INPUT --> NLP
    NLP --> C1
    C5 --> EVENT_MGR
    EVENT_MGR --> DB
    DB --> UI_DISPLAY
    UI_EXPORT --> FILE
    FILE --> DB
    
    EVENT_MGR --> REMINDER
    REMINDER --> THREAD
    THREAD -.Notification.-> UI
    
    style NLP fill:#e1f5ff
    style EVENT_MGR fill:#fff4e1
    style DB fill:#f0f0f0
    style REMINDER fill:#ffe1e1
```

**Mô tả:**
- **Presentation Layer**: Giao diện Streamlit cho phép người dùng nhập văn bản, xem danh sách sự kiện, và export/import dữ liệu
- **Application Layer**: Xử lý logic chính bao gồm NLP Pipeline, Event Manager và Reminder System
- **NLP Pipeline**: 5 components xử lý tuần tự từ preprocessing đến validation
- **Data Layer**: SQLite database và file I/O cho import/export
- **Background Services**: Thread chạy nền kiểm tra nhắc nhở mỗi 60 giây

---

## 2. FLOWCHART - LUỒNG XỬ LÝ NLP

### 2.1. Flowchart Tổng Quát

Sơ đồ này mô tả luồng xử lý từ khi người dùng nhập văn bản tiếng Việt đến khi sự kiện được lưu vào database.

```mermaid
flowchart TD
    START([User nhập câu tiếng Việt]) --> INPUT{Input hợp lệ?}
    INPUT -->|Không| ERROR1[Hiển thị lỗi: Input rỗng]
    INPUT -->|Có| PREPROCESS[Component 1:<br/>Preprocessing]
    
    PREPROCESS --> TOKENIZE[Tách từ, chuẩn hóa]
    TOKENIZE --> NER[Component 2:<br/>NER Extraction]
    
    NER --> EXTRACT_TIME[Trích xuất TIME]
    NER --> EXTRACT_LOC[Trích xuất LOCATION]
    
    EXTRACT_TIME --> RULE[Component 3:<br/>Rule-based Extract]
    EXTRACT_LOC --> RULE
    
    RULE --> GET_EVENT[Extract tên sự kiện]
    RULE --> GET_REMINDER[Extract nhắc nhở]
    
    GET_EVENT --> TIMEPARSE[Component 4:<br/>Time Parsing]
    GET_REMINDER --> TIMEPARSE
    
    TIMEPARSE --> RELATIVE{Thời gian<br/>tương đối?}
    RELATIVE -->|Có| CONVERT[Convert: mai → +1 day]
    RELATIVE -->|Không| ABSOLUTE[Parse trực tiếp]
    
    CONVERT --> VALIDATE[Component 5:<br/>Validation]
    ABSOLUTE --> VALIDATE
    
    VALIDATE --> CHECK{Dữ liệu<br/>hợp lệ?}
    CHECK -->|Không| ERROR2[Hiển thị lỗi chi tiết]
    CHECK -->|Có| MERGE[Merge kết quả]
    
    MERGE --> SAVE[Lưu vào Database]
    SAVE --> DISPLAY[Hiển thị sự kiện mới]
    DISPLAY --> END([Hoàn thành])
    
    ERROR1 --> END
    ERROR2 --> END
    
    style START fill:#e1f5ff
    style END fill:#e1ffe1
    style ERROR1 fill:#ffe1e1
    style ERROR2 fill:#ffe1e1
    style VALIDATE fill:#fff4e1
```

**Các bước chính:**
1. Kiểm tra input hợp lệ
2. Preprocessing: Tách từ và chuẩn hóa văn bản
3. NER Extraction: Trích xuất thực thể (TIME, LOCATION)
4. Rule-based Extract: Trích xuất tên sự kiện và thông tin nhắc nhở
5. Time Parsing: Chuyển đổi thời gian tương đối/tuyệt đối
6. Validation: Kiểm tra tính hợp lệ của dữ liệu
7. Lưu vào database và hiển thị

### 2.2. Flowchart Chi Tiết Component 4: Time Parsing

Sơ đồ này chi tiết hóa quá trình phân tích và chuyển đổi thời gian từ văn bản tiếng Việt.

```mermaid
flowchart TD
    START([Input: Text đã xử lý]) --> DETECT{Phát hiện<br/>từ khóa thời gian}
    
    DETECT -->|Tương đối| REL_CHECK{Kiểu tương đối?}
    DETECT -->|Tuyệt đối| ABS_CHECK{Kiểu tuyệt đối?}
    
    REL_CHECK -->|mai, ngày mai| ADD1[now + 1 day]
    REL_CHECK -->|tuần sau| ADD7[now + 7 days]
    REL_CHECK -->|tháng sau| ADD30[now + 30 days]
    REL_CHECK -->|hôm nay| NOW[now]
    
    ABS_CHECK -->|25/12/2025| PARSE_DATE[Parse DD/MM/YYYY]
    ABS_CHECK -->|Chủ nhật này| CALC_WEEK[Tính ngày chủ nhật]
    
    ADD1 --> TIME_CHECK{Có giờ?}
    ADD7 --> TIME_CHECK
    ADD30 --> TIME_CHECK
    NOW --> TIME_CHECK
    PARSE_DATE --> TIME_CHECK
    CALC_WEEK --> TIME_CHECK
    
    TIME_CHECK -->|10h, 10 giờ| PARSE_HOUR[Parse giờ: 10:00]
    TIME_CHECK -->|10:30| PARSE_TIME[Parse giờ:phút]
    TIME_CHECK -->|sáng, chiều| PERIOD{Buổi trong ngày}
    TIME_CHECK -->|Không| DEFAULT[Default: 09:00]
    
    PERIOD -->|sáng| SET_MORNING[06:00 - 12:00]
    PERIOD -->|trưa| SET_NOON[12:00 - 13:00]
    PERIOD -->|chiều| SET_AFTERNOON[13:00 - 18:00]
    PERIOD -->|tối| SET_EVENING[18:00 - 23:00]
    
    PARSE_HOUR --> COMBINE
    PARSE_TIME --> COMBINE
    DEFAULT --> COMBINE
    SET_MORNING --> COMBINE
    SET_NOON --> COMBINE
    SET_AFTERNOON --> COMBINE
    SET_EVENING --> COMBINE
    
    COMBINE[Kết hợp ngày + giờ] --> RESULT([Output: datetime object])
    
    style START fill:#e1f5ff
    style RESULT fill:#e1ffe1
    style COMBINE fill:#fff4e1
```

**Xử lý thời gian tương đối:**
- "mai", "ngày mai" → +1 ngày
- "tuần sau" → +7 ngày
- "tháng sau" → +30 ngày
- "hôm nay" → ngày hiện tại

**Xử lý thời gian tuyệt đối:**
- Format DD/MM/YYYY
- Tính toán ngày trong tuần (VD: "Chủ nhật này")

**Xử lý giờ:**
- Giờ cụ thể: "10h", "10 giờ" → 10:00
- Giờ:phút: "10:30"
- Buổi trong ngày: sáng (6-12h), trưa (12-13h), chiều (13-18h), tối (18-23h)
- Mặc định: 09:00 nếu không có thông tin

---

## 3. SEQUENCE DIAGRAM - TƯƠNG TÁC GIỮA CÁC THÀNH PHẦN

### 3.1. Thêm Sự Kiện

Sơ đồ này mô tả luồng tương tác giữa các thành phần khi người dùng thêm một sự kiện mới.

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant NLP as NLP Pipeline
    participant EM as Event Manager
    participant DB as SQLite DB
    participant RS as Reminder System
    
    User->>UI: Nhập câu tiếng Việt
    UI->>NLP: process(text)
    
    activate NLP
    NLP->>NLP: Component 1: Preprocess
    NLP->>NLP: Component 2: NER Extract
    NLP->>NLP: Component 3: Rule Extract
    NLP->>NLP: Component 4: Time Parse
    NLP->>NLP: Component 5: Validate
    NLP-->>UI: return event_data
    deactivate NLP
    
    UI->>UI: Hiển thị preview
    UI->>User: Xác nhận thông tin?
    User->>UI: Xác nhận
    
    UI->>EM: add_event(event_data)
    activate EM
    EM->>DB: INSERT INTO events
    DB-->>EM: event_id
    EM-->>UI: success
    deactivate EM
    
    UI->>RS: schedule_reminder(event_id)
    RS-->>UI: scheduled
    
    UI->>User: Hiển thị thông báo thành công
```

**Luồng hoạt động:**
1. User nhập câu tiếng Việt vào UI
2. UI gọi NLP Pipeline xử lý văn bản qua 5 components
3. NLP trả về dữ liệu sự kiện đã được trích xuất
4. UI hiển thị preview cho user xác nhận
5. Event Manager lưu vào database và nhận event_id
6. Reminder System lên lịch nhắc nhở
7. UI thông báo thành công

### 3.2. Hệ Thống Nhắc Nhở

Sơ đồ này mô tả cách hoạt động của hệ thống nhắc nhở tự động chạy nền.

```mermaid
sequenceDiagram
    participant Thread as Reminder Thread
    participant RS as Reminder System
    participant DB as SQLite DB
    participant UI as Streamlit UI
    participant User
    
    loop Every 60 seconds
        Thread->>RS: check_reminders()
        activate RS
        RS->>DB: get_upcoming_events(2 hours)
        DB-->>RS: events[]
        
        loop For each event
            RS->>RS: calculate reminder_time
            RS->>RS: now - reminder_time < 60s?
            
            alt Time to remind
                RS->>UI: show_notification(event)
                UI->>User: 🔔 Popup Notification
                RS->>DB: mark_as_notified(event_id)
            else Not yet
                RS->>RS: Skip
            end
        end
        
        deactivate RS
    end
```

**Cơ chế hoạt động:**
1. Reminder Thread chạy vòng lặp mỗi 60 giây
2. Kiểm tra các sự kiện sắp diễn ra trong 2 giờ tới
3. Tính toán thời gian nhắc nhở cho từng sự kiện
4. Nếu đến giờ nhắc (trong vòng 60s), hiển thị notification
5. Đánh dấu đã gửi thông báo trong database
6. Lặp lại quá trình

---

## 4. ERD - ENTITY RELATIONSHIP DIAGRAM

Sơ đồ này mô tả cấu trúc cơ sở dữ liệu của hệ thống.

```mermaid
erDiagram
    EVENTS {
        integer id PK "Auto increment"
        text event_name "NOT NULL"
        text start_time "ISO format, NOT NULL"
        text end_time "ISO format, nullable"
        text location "nullable"
        integer reminder_minutes "Default 0"
        text description "nullable"
        text created_at "ISO format, NOT NULL"
        text updated_at "ISO format, nullable"
    }
    
    EVENTS ||--o{ NOTIFICATIONS : triggers
    
    NOTIFICATIONS {
        integer id PK
        integer event_id FK
        text notification_time "ISO format"
        boolean is_sent "Default false"
        text sent_at "nullable"
    }
```

### SQL Schema

```sql
-- Bảng sự kiện chính
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    start_time TEXT NOT NULL,          -- ISO 8601 format: YYYY-MM-DD HH:MM:SS
    end_time TEXT,                      -- ISO 8601 format, nullable
    location TEXT,                      -- Địa điểm tổ chức
    reminder_minutes INTEGER DEFAULT 0, -- Số phút nhắc trước (0 = không nhắc)
    description TEXT,                   -- Mô tả chi tiết
    created_at TEXT NOT NULL,           -- Thời gian tạo
    updated_at TEXT                     -- Thời gian cập nhật cuối
);

-- Bảng thông báo (tùy chọn, cho hệ thống phức tạp hơn)
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    notification_time TEXT NOT NULL,
    is_sent BOOLEAN DEFAULT 0,
    sent_at TEXT,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

-- Indexes để tối ưu truy vấn
CREATE INDEX idx_start_time ON events(start_time);
CREATE INDEX idx_event_name ON events(event_name);
CREATE INDEX idx_notification_time ON notifications(notification_time);
```

**Mô tả bảng:**

**EVENTS:**
- `id`: ID tự tăng, khóa chính
- `event_name`: Tên sự kiện (bắt buộc)
- `start_time`: Thời gian bắt đầu (bắt buộc, ISO 8601)
- `end_time`: Thời gian kết thúc (tùy chọn)
- `location`: Địa điểm tổ chức
- `reminder_minutes`: Thời gian nhắc trước (phút), 0 = không nhắc
- `description`: Mô tả chi tiết
- `created_at`: Thời gian tạo record
- `updated_at`: Thời gian cập nhật cuối

**NOTIFICATIONS:**
- `id`: ID tự tăng, khóa chính
- `event_id`: Liên kết đến events (khóa ngoại)
- `notification_time`: Thời gian gửi thông báo
- `is_sent`: Đã gửi chưa (boolean)
- `sent_at`: Thời điểm thực tế đã gửi

---

## 5. USE CASE DIAGRAM

Sơ đồ này mô tả các use case (chức năng) mà người dùng có thể thực hiện với hệ thống.

```mermaid
graph LR
    User((Người dùng))
    
    subgraph "Hệ thống Quản lý Lịch"
        UC1[Thêm sự kiện<br/>bằng NLP]
        UC2[Thêm sự kiện<br/>thủ công]
        UC3[Xem danh sách<br/>sự kiện]
        UC4[Sửa sự kiện]
        UC5[Xóa sự kiện]
        UC6[Tìm kiếm sự kiện]
        UC7[Xuất dữ liệu<br/>ICS/JSON]
        UC8[Nhập dữ liệu<br/>JSON]
        UC9[Nhận nhắc nhở]
        UC10[Test NLP<br/>30 cases]
    end
    
    System[Hệ thống Reminder]
    
    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
    User --> UC6
    User --> UC7
    User --> UC8
    User --> UC9
    User --> UC10
    
    UC1 -.include.-> UC2
    UC9 -.trigger.-> System
    
    style User fill:#e1f5ff
    style UC1 fill:#fff4e1
    style UC9 fill:#ffe1e1
    style System fill:#f0f0f0
```

**Các Use Case:**

1. **Thêm sự kiện bằng NLP**: Nhập câu tiếng Việt tự nhiên, hệ thống tự động trích xuất thông tin
2. **Thêm sự kiện thủ công**: Nhập thông tin sự kiện qua form
3. **Xem danh sách sự kiện**: Hiển thị tất cả sự kiện theo lịch
4. **Sửa sự kiện**: Chỉnh sửa thông tin sự kiện đã tạo
5. **Xóa sự kiện**: Xóa sự kiện không cần thiết
6. **Tìm kiếm sự kiện**: Tìm kiếm theo tên, ngày, địa điểm
7. **Xuất dữ liệu (ICS/JSON)**: Export lịch ra file ICS (iCalendar) hoặc JSON
8. **Nhập dữ liệu (JSON)**: Import sự kiện từ file JSON
9. **Nhận nhắc nhở**: Nhận thông báo tự động trước khi sự kiện diễn ra
10. **Test NLP (30 cases)**: Chức năng test với 30 test case mẫu

**Mối quan hệ:**
- UC1 (Thêm bằng NLP) include UC2 (Thêm thủ công) - nếu NLP thất bại, fallback về nhập tay
- UC9 (Nhận nhắc nhở) trigger Hệ thống Reminder tự động

---

## 6. CLASS DIAGRAM - CẤU TRÚC CODE

Sơ đồ này mô tả cấu trúc các class chính trong hệ thống và mối quan hệ giữa chúng.

```mermaid
classDiagram
    class VietnameseNLPEngine {
        -preprocessor: Preprocessor
        -ner_extractor: NERExtractor
        -rule_extractor: RuleExtractor
        -time_parser: TimeParser
        +process(text: str) dict
        +validate(data: dict) bool
    }
    
    class Preprocessor {
        +normalize(text: str) str
        +tokenize(text: str) list
        +remove_stopwords(tokens: list) list
        +lowercase(text: str) str
    }
    
    class NERExtractor {
        +extract_time(text: str) list
        +extract_location(text: str) str
        +extract_entities(text: str) dict
    }
    
    class RuleExtractor {
        -patterns: dict
        +extract_event_name(text: str) str
        +extract_reminder(text: str) int
        +extract_duration(text: str) int
    }
    
    class TimeParser {
        +parse(text: str) datetime
        +parse_relative(text: str) datetime
        +parse_absolute(text: str) datetime
        +parse_time_of_day(text: str) time
        +calculate_offset(keyword: str) timedelta
    }
    
    class DatabaseManager {
        -db_path: str
        -connection: Connection
        +add_event(event: dict) int
        +get_events(start, end) list
        +get_event_by_id(id: int) dict
        +update_event(id: int, data: dict) bool
        +delete_event(id: int) bool
        +search_events(query: str) list
    }
    
    class ReminderSystem {
        -db: DatabaseManager
        -running: bool
        -thread: Thread
        +start() void
        +stop() void
        -check_reminders() void
        -send_notification(event: dict) void
        -calculate_reminder_time(event: dict) datetime
    }
    
    class EventManager {
        -db: DatabaseManager
        -nlp: VietnameseNLPEngine
        +create_from_text(text: str) dict
        +create_manual(data: dict) int
        +get_all() list
        +get_by_id(id: int) dict
        +update(id: int, data: dict) bool
        +delete(id: int) bool
        +search(query: str) list
        +export_ics() str
        +export_json() str
        +import_json(data: str) bool
    }
    
    class StreamlitUI {
        -event_manager: EventManager
        -reminder_system: ReminderSystem
        +render() void
        +show_add_form() void
        +show_event_list() void
        +show_search() void
        +show_import_export() void
    }
    
    VietnameseNLPEngine --> Preprocessor
    VietnameseNLPEngine --> NERExtractor
    VietnameseNLPEngine --> RuleExtractor
    VietnameseNLPEngine --> TimeParser
    
    EventManager --> DatabaseManager
    EventManager --> VietnameseNLPEngine
    
    ReminderSystem --> DatabaseManager
    
    StreamlitUI --> EventManager
    StreamlitUI --> ReminderSystem
```

**Mô tả các class chính:**

**VietnameseNLPEngine**: Class trung tâm xử lý NLP, điều phối 4 components con
- Preprocessor: Tiền xử lý văn bản
- NERExtractor: Trích xuất thực thể có tên
- RuleExtractor: Trích xuất dựa trên luật
- TimeParser: Phân tích và chuyển đổi thời gian

**DatabaseManager**: Quản lý tất cả tương tác với SQLite database

**EventManager**: Class trung gian giữa UI và backend, cung cấp API đầy đủ cho CRUD operations

**ReminderSystem**: Hệ thống nhắc nhở chạy nền với thread riêng

**StreamlitUI**: Giao diện người dùng Streamlit

---

## 7. STATE DIAGRAM - TRẠNG THÁI SỰ KIỆN

Sơ đồ này mô tả vòng đời và các trạng thái của một sự kiện trong hệ thống.

```mermaid
stateDiagram-v2
    [*] --> Draft: User nhập text
    Draft --> Validating: Submit
    
    Validating --> Valid: NLP parse thành công
    Validating --> Invalid: NLP parse thất bại
    
    Invalid --> Draft: Sửa lại
    Invalid --> ManualInput: Nhập thủ công
    
    Valid --> Confirmed: User xác nhận
    ManualInput --> Confirmed: User xác nhận
    
    Confirmed --> Scheduled: Lưu vào DB
    
    Scheduled --> Reminded: Đến giờ nhắc
    Reminded --> Active: Đến giờ bắt đầu
    
    Active --> Completed: Kết thúc
    
    Scheduled --> Editing: User click Sửa
    Editing --> Scheduled: Lưu thay đổi
    
    Scheduled --> Deleted: User click Xóa
    Deleted --> [*]
    
    Completed --> [*]
```

**Các trạng thái:**

1. **Draft**: Người dùng đang nhập văn bản
2. **Validating**: Hệ thống đang xử lý và validate dữ liệu
3. **Valid**: Dữ liệu hợp lệ, chờ xác nhận
4. **Invalid**: Dữ liệu không hợp lệ
5. **ManualInput**: Chuyển sang nhập thủ công
6. **Confirmed**: Người dùng đã xác nhận
7. **Scheduled**: Đã lưu vào DB, đang chờ đến giờ
8. **Reminded**: Đã gửi thông báo nhắc nhở
9. **Active**: Sự kiện đang diễn ra
10. **Editing**: Đang chỉnh sửa
11. **Completed**: Hoàn thành
12. **Deleted**: Đã xóa

**Luồng chuyển đổi:**
- Từ Draft → Validating → Valid/Invalid
- Invalid có thể quay lại Draft hoặc chuyển sang ManualInput
- Valid → Confirmed → Scheduled
- Scheduled có thể chuyển sang Editing (sau đó quay lại Scheduled) hoặc Deleted
- Scheduled → Reminded → Active → Completed

---

## Kết luận

Các sơ đồ trên cung cấp cái nhìn toàn diện về hệ thống quản lý lịch với NLP tiếng Việt:

✅ **Kiến trúc rõ ràng**: 4 layers với trách nhiệm riêng biệt
✅ **Luồng xử lý chi tiết**: Từ input đến output qua 5 components NLP
✅ **Tương tác mạch lạc**: Sequence diagrams mô tả rõ các use case
✅ **Database thiết kế tốt**: ERD đơn giản nhưng đầy đủ
✅ **Use cases đầy đủ**: 10 chức năng chính
✅ **Code structure**: Class diagram hỗ trợ implementation
✅ **Lifecycle quản lý**: State diagram theo dõi vòng đời sự kiện

Tất cả sơ đồ được tạo bằng Mermaid.js, có thể:
- Render trực tiếp trên GitHub
- Export sang PNG/SVG cho báo cáo
- Dễ dàng maintain và version control
- Professional và dễ hiểu

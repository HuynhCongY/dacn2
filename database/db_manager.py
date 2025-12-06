"""
Database Manager cho ứng dụng quản lý lịch trình
Sử dụng SQLite để lưu trữ các sự kiện
"""

import sqlite3
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional, Tuple


class DatabaseManager:
    """Quản lý database SQLite cho ứng dụng lịch"""
    
    def __init__(self, db_path="calendar.db"):
        """
        Khởi tạo database manager
        
        Args:
            db_path: Đường dẫn đến file database
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Tạo bảng events nếu chưa tồn tại"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_name TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                location TEXT,
                reminder_minutes INTEGER,
                description TEXT,
                created_at TEXT NOT NULL,
                notified INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_event(self, event_data: Dict) -> int:
        """
        Thêm sự kiện mới vào database
        
        Args:
            event_data: Dictionary chứa thông tin sự kiện
                - event_name: str (required)
                - start_time: datetime (required)
                - end_time: datetime (optional)
                - location: str (optional)
                - reminder_minutes: int (optional)
                - description: str (optional)
        
        Returns:
            ID của sự kiện vừa thêm
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Chuyển đổi datetime sang ISO format string
        start_time = event_data['start_time']
        if isinstance(start_time, datetime):
            start_time = start_time.isoformat()
        
        end_time = event_data.get('end_time')
        if end_time and isinstance(end_time, datetime):
            end_time = end_time.isoformat()
        
        created_at = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO events (event_name, start_time, end_time, location, 
                              reminder_minutes, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            event_data['event_name'],
            start_time,
            end_time,
            event_data.get('location'),
            event_data.get('reminder_minutes'),
            event_data.get('description'),
            created_at
        ))
        
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return event_id
    
    def get_events(self, start_date: Optional[datetime] = None, 
                   end_date: Optional[datetime] = None) -> List[Dict]:
        """
        Lấy danh sách sự kiện trong khoảng thời gian
        
        Args:
            start_date: Ngày bắt đầu (None = không giới hạn)
            end_date: Ngày kết thúc (None = không giới hạn)
        
        Returns:
            List các dictionary chứa thông tin sự kiện
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM events"
        params = []
        
        if start_date or end_date:
            query += " WHERE"
            if start_date:
                query += " start_time >= ?"
                params.append(start_date.isoformat())
            if end_date:
                if start_date:
                    query += " AND"
                query += " start_time <= ?"
                params.append(end_date.isoformat())
        
        query += " ORDER BY start_time ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        events = []
        for row in rows:
            event = dict(row)
            # Chuyển đổi string thành datetime
            event['start_time'] = datetime.fromisoformat(event['start_time'])
            if event['end_time']:
                event['end_time'] = datetime.fromisoformat(event['end_time'])
            event['created_at'] = datetime.fromisoformat(event['created_at'])
            events.append(event)
        
        conn.close()
        return events
    
    def get_event_by_id(self, event_id: int) -> Optional[Dict]:
        """
        Lấy thông tin sự kiện theo ID
        
        Args:
            event_id: ID của sự kiện
        
        Returns:
            Dictionary chứa thông tin sự kiện hoặc None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        row = cursor.fetchone()
        
        if row:
            event = dict(row)
            event['start_time'] = datetime.fromisoformat(event['start_time'])
            if event['end_time']:
                event['end_time'] = datetime.fromisoformat(event['end_time'])
            event['created_at'] = datetime.fromisoformat(event['created_at'])
            conn.close()
            return event
        
        conn.close()
        return None
    
    def update_event(self, event_id: int, event_data: Dict) -> bool:
        """
        Cập nhật thông tin sự kiện
        
        Args:
            event_id: ID của sự kiện cần cập nhật
            event_data: Dictionary chứa thông tin mới
        
        Returns:
            True nếu cập nhật thành công, False nếu không tìm thấy sự kiện
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Chuyển đổi datetime sang ISO format
        start_time = event_data.get('start_time')
        if start_time and isinstance(start_time, datetime):
            start_time = start_time.isoformat()
        
        end_time = event_data.get('end_time')
        if end_time and isinstance(end_time, datetime):
            end_time = end_time.isoformat()
        
        # Xây dựng câu query UPDATE động
        fields = []
        values = []
        
        if 'event_name' in event_data:
            fields.append("event_name = ?")
            values.append(event_data['event_name'])
        
        if start_time:
            fields.append("start_time = ?")
            values.append(start_time)
        
        if 'end_time' in event_data:
            fields.append("end_time = ?")
            values.append(end_time)
        
        if 'location' in event_data:
            fields.append("location = ?")
            values.append(event_data['location'])
        
        if 'reminder_minutes' in event_data:
            fields.append("reminder_minutes = ?")
            values.append(event_data['reminder_minutes'])
        
        if 'description' in event_data:
            fields.append("description = ?")
            values.append(event_data['description'])
        
        if not fields:
            conn.close()
            return False
        
        values.append(event_id)
        query = f"UPDATE events SET {', '.join(fields)} WHERE id = ?"
        
        cursor.execute(query, values)
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    def delete_event(self, event_id: int) -> bool:
        """
        Xóa sự kiện
        
        Args:
            event_id: ID của sự kiện cần xóa
        
        Returns:
            True nếu xóa thành công, False nếu không tìm thấy
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    def search_events(self, keyword: str) -> List[Dict]:
        """
        Tìm kiếm sự kiện theo tên hoặc mô tả
        
        Args:
            keyword: Từ khóa tìm kiếm
        
        Returns:
            List các sự kiện tìm được
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM events 
            WHERE event_name LIKE ? OR description LIKE ? OR location LIKE ?
            ORDER BY start_time ASC
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        
        rows = cursor.fetchall()
        
        events = []
        for row in rows:
            event = dict(row)
            event['start_time'] = datetime.fromisoformat(event['start_time'])
            if event['end_time']:
                event['end_time'] = datetime.fromisoformat(event['end_time'])
            event['created_at'] = datetime.fromisoformat(event['created_at'])
            events.append(event)
        
        conn.close()
        return events
    
    def get_upcoming_events(self, hours: int = 2) -> List[Dict]:
        """
        Lấy các sự kiện sắp diễn ra trong vài giờ tới
        
        Args:
            hours: Số giờ tính từ hiện tại
        
        Returns:
            List các sự kiện sắp diễn ra
        """
        now = datetime.now()
        future = now + timedelta(hours=hours)
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM events 
            WHERE start_time >= ? AND start_time <= ?
            AND reminder_minutes IS NOT NULL
            ORDER BY start_time ASC
        ''', (now.isoformat(), future.isoformat()))
        
        rows = cursor.fetchall()
        
        events = []
        for row in rows:
            event = dict(row)
            event['start_time'] = datetime.fromisoformat(event['start_time'])
            if event['end_time']:
                event['end_time'] = datetime.fromisoformat(event['end_time'])
            event['created_at'] = datetime.fromisoformat(event['created_at'])
            events.append(event)
        
        conn.close()
        return events
    
    def mark_notified(self, event_id: int):
        """
        Đánh dấu sự kiện đã được thông báo
        
        Args:
            event_id: ID của sự kiện
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE events SET notified = 1 WHERE id = ?", (event_id,))
        
        conn.commit()
        conn.close()
    
    def get_all_events(self) -> List[Dict]:
        """
        Lấy tất cả sự kiện
        
        Returns:
            List tất cả sự kiện
        """
        return self.get_events()
    
    def clear_all_events(self):
        """Xóa toàn bộ sự kiện trong database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM events")
        
        conn.commit()
        conn.close()
    
    def import_events(self, events: List[Dict]) -> Tuple[int, int]:
        """
        Import nhiều sự kiện cùng lúc
        
        Args:
            events: List các dictionary chứa thông tin sự kiện
        
        Returns:
            Tuple (số sự kiện thành công, số sự kiện lỗi)
        """
        success_count = 0
        error_count = 0
        
        for event in events:
            try:
                self.add_event(event)
                success_count += 1
            except Exception as e:
                error_count += 1
                print(f"Lỗi khi import sự kiện: {e}")
        
        return success_count, error_count

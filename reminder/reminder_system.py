"""
Hệ thống nhắc nhở tự động
Chạy trong thread riêng, kiểm tra định kỳ và hiển thị thông báo
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Optional, Callable
import streamlit as st


class ReminderSystem:
    """Hệ thống nhắc nhở tự động"""
    
    def __init__(self, db_manager, check_interval: int = 60):
        """
        Khởi tạo reminder system
        
        Args:
            db_manager: DatabaseManager instance
            check_interval: Khoảng thời gian kiểm tra (giây)
        """
        self.db = db_manager
        self.check_interval = check_interval
        self.running = False
        self.thread = None
        self.notification_callback = None
        self.notified_events = set()  # Lưu ID các sự kiện đã thông báo
    
    def start(self):
        """Khởi động hệ thống nhắc nhở"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._check_reminders, daemon=True)
            self.thread.start()
            print("Reminder system started")
    
    def stop(self):
        """Dừng hệ thống nhắc nhở"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("Reminder system stopped")
    
    def set_notification_callback(self, callback: Callable):
        """
        Đặt callback function để xử lý thông báo
        
        Args:
            callback: Function nhận tham số (event_dict)
        """
        self.notification_callback = callback
    
    def _check_reminders(self):
        """Vòng lặp kiểm tra nhắc nhở (chạy trong thread)"""
        while self.running:
            try:
                self._check_and_notify()
            except Exception as e:
                print(f"Error in reminder system: {e}")
            
            # Chờ trước khi kiểm tra lần tiếp theo
            time.sleep(self.check_interval)
    
    def _check_and_notify(self):
        """Kiểm tra và gửi thông báo cho các sự kiện sắp tới"""
        now = datetime.now()
        
        # Lấy events trong 2 giờ tới
        events = self.db.get_upcoming_events(hours=2)
        
        for event in events:
            # Bỏ qua nếu đã thông báo rồi
            if event['id'] in self.notified_events:
                continue
            
            # Bỏ qua nếu không có thời gian nhắc
            if not event.get('reminder_minutes'):
                continue
            
            # Tính thời gian nhắc nhở
            reminder_time = event['start_time'] - timedelta(minutes=event['reminder_minutes'])
            
            # Kiểm tra nếu đến giờ nhắc (dung sai ±60 giây)
            time_diff = abs((now - reminder_time).total_seconds())
            
            if time_diff < self.check_interval:
                self._send_notification(event)
                self.notified_events.add(event['id'])
                
                # Đánh dấu đã thông báo trong database
                self.db.mark_notified(event['id'])
    
    def _send_notification(self, event: dict):
        """
        Gửi thông báo cho sự kiện
        
        Args:
            event: Dictionary chứa thông tin sự kiện
        """
        # Tạo nội dung thông báo
        message = self._format_notification_message(event)
        
        print(f"\n{'='*60}")
        print(f"🔔 NHẮC NHỞ SỰ KIỆN")
        print(f"{'='*60}")
        print(message)
        print(f"{'='*60}\n")
        
        # Gọi callback nếu có
        if self.notification_callback:
            try:
                self.notification_callback(event)
            except Exception as e:
                print(f"Error in notification callback: {e}")
    
    def _format_notification_message(self, event: dict) -> str:
        """
        Định dạng nội dung thông báo
        
        Args:
            event: Dictionary chứa thông tin sự kiện
        
        Returns:
            Nội dung thông báo đã format
        """
        lines = []
        lines.append(f"Sự kiện: {event['event_name']}")
        lines.append(f"Thời gian: {event['start_time'].strftime('%H:%M - %d/%m/%Y')}")
        
        if event.get('location'):
            lines.append(f"Địa điểm: {event['location']}")
        
        if event.get('description'):
            lines.append(f"Mô tả: {event['description']}")
        
        # Tính thời gian còn lại
        now = datetime.now()
        time_left = event['start_time'] - now
        minutes_left = int(time_left.total_seconds() / 60)
        
        if minutes_left > 0:
            lines.append(f"\n⏰ Còn {minutes_left} phút nữa!")
        else:
            lines.append(f"\n⏰ Sự kiện đang diễn ra!")
        
        return '\n'.join(lines)
    
    def test_notification(self, event_name: str = "Test Event"):
        """
        Test thông báo
        
        Args:
            event_name: Tên sự kiện test
        """
        test_event = {
            'id': 0,
            'event_name': event_name,
            'start_time': datetime.now() + timedelta(minutes=5),
            'location': 'Test Location',
            'description': 'This is a test notification',
            'reminder_minutes': 5
        }
        
        self._send_notification(test_event)
    
    def clear_notified_cache(self):
        """Xóa cache các sự kiện đã thông báo"""
        self.notified_events.clear()
        print("Notification cache cleared")
    
    def get_status(self) -> dict:
        """
        Lấy trạng thái của reminder system
        
        Returns:
            Dictionary chứa trạng thái
        """
        return {
            'running': self.running,
            'check_interval': self.check_interval,
            'notified_count': len(self.notified_events)
        }

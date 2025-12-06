"""
Export và Import dữ liệu
Hỗ trợ format: ICS (iCalendar), JSON
"""

import json
from datetime import datetime
from typing import List, Dict
from ics import Calendar, Event as ICSEvent
import pytz


class ExportImport:
    """Xuất và nhập dữ liệu lịch"""
    
    def __init__(self, timezone='Asia/Ho_Chi_Minh'):
        """
        Khởi tạo export/import handler
        
        Args:
            timezone: Múi giờ
        """
        self.timezone = pytz.timezone(timezone)
    
    def export_to_ics(self, events: List[Dict], filename: str = "calendar.ics") -> str:
        """
        Xuất danh sách sự kiện ra file ICS
        
        Args:
            events: List các sự kiện
            filename: Tên file xuất ra
        
        Returns:
            Nội dung file ICS dạng string
        """
        calendar = Calendar()
        
        for event_data in events:
            event = ICSEvent()
            event.name = event_data['event']
            event.begin = event_data['start_time']
            
            if event_data.get('end_time'):
                event.end = event_data['end_time']
            
            if event_data.get('location'):
                event.location = event_data['location']
            
            if event_data.get('description'):
                event.description = event_data['description']
            
            calendar.events.add(event)
        
        return str(calendar)
    
    def export_to_json(self, events: List[Dict], filename: str = "calendar.json") -> str:
        """
        Xuất danh sách sự kiện ra JSON
        
        Args:
            events: List các sự kiện
            filename: Tên file xuất ra
        
        Returns:
            Nội dung JSON dạng string
        """
        # Chuyển đổi datetime thành string
        export_data = []
        for event in events:
            event_dict = {
                'event': event['event'],
                'start_time': event['start_time'].isoformat(),
                'end_time': event['end_time'].isoformat() if event.get('end_time') else None,
                'location': event.get('location'),
                'reminder_minutes': event.get('reminder_minutes'),
                'description': event.get('description')
            }
            export_data.append(event_dict)
        
        return json.dumps(export_data, ensure_ascii=False, indent=2)
    
    def import_from_json(self, json_content: str) -> List[Dict]:
        """
        Import dữ liệu từ JSON
        
        Args:
            json_content: Nội dung JSON
        
        Returns:
            List các sự kiện
        
        Raises:
            ValueError: Nếu JSON không hợp lệ
        """
        try:
            data = json.loads(json_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON không hợp lệ: {e}")
        
        if not isinstance(data, list):
            raise ValueError("JSON phải là một mảng các sự kiện")
        
        events = []
        for item in data:
            try:
                # Hỗ trợ 2 format:
                # 1. Format export chuẩn: {event, start_time, ...}
                # 2. Format test case: {id, text, expected: {event, start_time, ...}}
                
                # Nếu có trường 'expected', lấy dữ liệu từ đó (test case format)
                if 'expected' in item:
                    item = item['expected']
                
                # Lấy tên sự kiện
                event_value = item.get('event')
                if not event_value:
                    print(f"Lỗi: Thiếu trường 'event'")
                    continue
                
                # Chuyển đổi string thành datetime
                event = {
                    'event': event_value,
                    'start_time': datetime.fromisoformat(item['start_time']),
                    'end_time': datetime.fromisoformat(item['end_time']) if item.get('end_time') else None,
                    'location': item.get('location'),
                    'reminder_minutes': item.get('reminder_minutes'),
                    'description': item.get('description')
                }
                events.append(event)
            except (KeyError, ValueError) as e:
                print(f"Lỗi khi parse sự kiện: {e}")
                continue
        
        return events
    
    def import_from_ics(self, ics_content: str) -> List[Dict]:
        """
        Import dữ liệu từ ICS
        
        Args:
            ics_content: Nội dung file ICS
        
        Returns:
            List các sự kiện
        
        Raises:
            ValueError: Nếu ICS không hợp lệ
        """
        try:
            calendar = Calendar(ics_content)
        except Exception as e:
            raise ValueError(f"File ICS không hợp lệ: {e}")
        
        events = []
        for ics_event in calendar.events:
            event = {
                'event': ics_event.name,
                'start_time': ics_event.begin.datetime,
                'end_time': ics_event.end.datetime if ics_event.end else None,
                'location': ics_event.location if hasattr(ics_event, 'location') else None,
                'description': ics_event.description if hasattr(ics_event, 'description') else None,
                'reminder_minutes': None  # ICS không lưu reminder_minutes
            }
            events.append(event)
        
        return events
    
    def validate_events(self, events: List[Dict]) -> tuple:
        """
        Validate danh sách sự kiện
        
        Args:
            events: List các sự kiện cần validate
        
        Returns:
            Tuple (valid_events, invalid_events)
        """
        valid = []
        invalid = []
        
        for event in events:
            try:
                # Kiểm tra các trường bắt buộc
                if not event.get('event'):
                    raise ValueError("Thiếu tên sự kiện")
                
                if not event.get('start_time'):
                    raise ValueError("Thiếu thời gian bắt đầu")
                
                # Kiểm tra kiểu dữ liệu
                if not isinstance(event['start_time'], datetime):
                    raise ValueError("start_time phải là datetime")
                
                if event.get('end_time') and not isinstance(event['end_time'], datetime):
                    raise ValueError("end_time phải là datetime")
                
                valid.append(event)
            except Exception as e:
                invalid.append({'event': event, 'error': str(e)})
        
        return valid, invalid

"""
Component 4: Time Parser
Phân tích và chuyển đổi thời gian tương đối thành thời gian tuyệt đối
"""

import re
from datetime import datetime, timedelta
from typing import Optional, Dict
import pytz


class TimeParser:
    """Parser cho thời gian tiếng Việt"""
    
    def __init__(self, timezone='Asia/Ho_Chi_Minh'):
        """
        Khởi tạo time parser
        
        Args:
            timezone: Múi giờ (mặc định: Việt Nam)
        """
        self.timezone = pytz.timezone(timezone)
        
        # Mapping cho các từ khóa thời gian tương đối
        self.relative_days = {
            'hôm nay': 0,
            'hom nay': 0,
            'hôm_nay': 0,
            'hom_nay': 0,
            'mai': 1,
            'ngày mai': 1,
            'ngay mai': 1,
            'ngày_mai': 1,
            'ngay_mai': 1,
            'mốt': 2,
            'mot': 2,
            'ngày mốt': 2,
            'ngay mot': 2,
        }
        
        # Mapping cho các buổi trong ngày
        self.time_of_day = {
            'sáng': (6, 11),
            'sang': (6, 11),
            'trưa': (11, 13),
            'trua': (11, 13),
            'chiều': (13, 18),
            'chieu': (13, 18),
            'tối': (18, 22),
            'toi': (18, 22),
            'đêm': (22, 23),
            'dem': (22, 23),
            'khuya': (0, 6),
        }
        
        # Mapping cho thứ trong tuần
        self.weekdays = {
            'thứ hai': 0,
            'thu hai': 0,
            'thứ 2': 0,
            'thu 2': 0,
            't2': 0,
            'thứ ba': 1,
            'thu ba': 1,
            'thứ 3': 1,
            'thu 3': 1,
            't3': 1,
            'thứ tư': 2,
            'thu tu': 2,
            'thứ 4': 2,
            'thu 4': 2,
            't4': 2,
            'thứ năm': 3,
            'thu nam': 3,
            'thứ 5': 3,
            'thu 5': 3,
            't5': 3,
            'thứ sáu': 4,
            'thu sau': 4,
            'thứ 6': 4,
            'thu 6': 4,
            't6': 4,
            'thứ bảy': 5,
            'thu bay': 5,
            'thứ 7': 5,
            'thu 7': 5,
            't7': 5,
            'chủ nhật': 6,
            'chu nhat': 6,
            'cn': 6,
        }
    
    def parse_time(self, text: str) -> Optional[datetime]:
        """
        Parse thời gian từ văn bản tiếng Việt
        
        Args:
            text: Văn bản chứa thông tin thời gian
        
        Returns:
            Datetime object hoặc None
        """
        text_lower = text.lower()
        now = datetime.now(self.timezone)
        
        # Xác định ngày
        target_date = self._parse_date(text_lower, now)
        
        # Xác định giờ
        target_time = self._parse_hour(text_lower)
        
        if target_date and target_time:
            # Kết hợp ngày và giờ
            result = datetime.combine(target_date.date(), target_time.time())
            result = self.timezone.localize(result)
            return result
        elif target_date:
            # Chỉ có ngày, dùng giờ mặc định (9:00 sáng)
            result = datetime.combine(target_date.date(), datetime.min.time().replace(hour=9))
            result = self.timezone.localize(result)
            return result
        elif target_time:
            # Chỉ có giờ, dùng ngày hôm nay
            result = datetime.combine(now.date(), target_time.time())
            result = self.timezone.localize(result)
            
            # Nếu giờ đã qua trong ngày, chuyển sang ngày mai
            if result < now:
                result = result + timedelta(days=1)
            
            return result
        
        return None
    
    def _parse_date(self, text: str, now: datetime) -> Optional[datetime]:
        """Parse phần ngày từ văn bản"""
        
        # Kiểm tra ngày tương đối (hôm nay, mai, ...)
        for keyword, days_offset in self.relative_days.items():
            if keyword in text:
                return now + timedelta(days=days_offset)
        
        # Kiểm tra "tuần sau", "tuần tới"
        if 'tuần sau' in text or 'tuan sau' in text or 'tuần tới' in text or 'tuan toi' in text:
            return now + timedelta(days=7)
        
        # Kiểm tra "tháng sau", "tháng tới"
        if 'tháng sau' in text or 'thang sau' in text or 'tháng tới' in text or 'thang toi' in text:
            return now + timedelta(days=30)
        
        # Kiểm tra thứ trong tuần (thứ 2, thứ 3, ...)
        for keyword, weekday in self.weekdays.items():
            if keyword in text:
                days_ahead = weekday - now.weekday()
                if days_ahead <= 0:  # Target day already happened this week
                    days_ahead += 7
                return now + timedelta(days=days_ahead)
        
        # Kiểm tra ngày cụ thể (25/12, 25-12)
        date_match = re.search(r'(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2,4}))?', text)
        if date_match:
            day = int(date_match.group(1))
            month = int(date_match.group(2))
            year = int(date_match.group(3)) if date_match.group(3) else now.year
            
            try:
                result = datetime(year, month, day)
                result = self.timezone.localize(result)
                
                # Nếu ngày đã qua trong năm, chuyển sang năm sau
                if result < now and not date_match.group(3):
                    result = result.replace(year=year + 1)
                
                return result
            except ValueError:
                pass
        
        # Kiểm tra pattern "ngày X"
        day_match = re.search(r'ngày\s+(\d{1,2})', text)
        if day_match:
            day = int(day_match.group(1))
            try:
                result = datetime(now.year, now.month, day)
                result = self.timezone.localize(result)
                
                # Nếu ngày đã qua trong tháng, chuyển sang tháng sau
                if result < now:
                    if now.month == 12:
                        result = result.replace(year=now.year + 1, month=1)
                    else:
                        result = result.replace(month=now.month + 1)
                
                return result
            except ValueError:
                pass
        
        return None
    
    def _parse_hour(self, text: str) -> Optional[datetime]:
        """Parse phần giờ từ văn bản"""
        
        # Pattern 1: "10 giờ", "10h"
        hour_match = re.search(r'(\d{1,2})\s*(?:giờ|gio|h)\s*(\d{1,2})?\s*(sáng|sang|trưa|trua|chiều|chieu|tối|toi|đêm|dem)?', text)
        if hour_match:
            hour = int(hour_match.group(1))
            minute = int(hour_match.group(2)) if hour_match.group(2) else 0
            period = hour_match.group(3)
            
            # Điều chỉnh giờ dựa trên buổi trong ngày
            if period:
                if period in ['chiều', 'chieu', 'tối', 'toi'] and hour < 12:
                    hour += 12
                elif period in ['sáng', 'sang'] and hour == 12:
                    hour = 0
            
            try:
                return datetime.min.replace(hour=hour, minute=minute)
            except ValueError:
                pass
        
        # Pattern 2: "10:30", "10h30"
        time_match = re.search(r'(\d{1,2})[h:](\d{2})', text)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2))
            
            # Kiểm tra buổi trong ngày
            for period_keyword, (start, end) in self.time_of_day.items():
                if period_keyword in text:
                    if hour < 12 and start >= 12:
                        hour += 12
                    break
            
            try:
                return datetime.min.replace(hour=hour, minute=minute)
            except ValueError:
                pass
        
        # Pattern 3: Chỉ có buổi trong ngày (sáng, chiều, tối)
        for period_keyword, (start, end) in self.time_of_day.items():
            if period_keyword in text:
                # Dùng giờ giữa khoảng
                hour = (start + end) // 2
                return datetime.min.replace(hour=hour, minute=0)
        
        return None
    
    def get_date_range(self, view_type: str, reference_date: Optional[datetime] = None) -> tuple:
        """
        Lấy khoảng thời gian cho view (ngày/tuần/tháng)
        
        Args:
            view_type: 'day', 'week', hoặc 'month'
            reference_date: Ngày tham chiếu (mặc định: hôm nay)
        
        Returns:
            Tuple (start_date, end_date)
        """
        if reference_date is None:
            reference_date = datetime.now(self.timezone)
        
        if view_type == 'day':
            start = reference_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
        elif view_type == 'week':
            # Tuần bắt đầu từ thứ 2
            start = reference_date - timedelta(days=reference_date.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=7)
        elif view_type == 'month':
            start = reference_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            # Ngày cuối tháng
            if start.month == 12:
                end = start.replace(year=start.year + 1, month=1)
            else:
                end = start.replace(month=start.month + 1)
        else:
            raise ValueError(f"Invalid view_type: {view_type}")
        
        return start, end

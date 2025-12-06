"""
Component 3: Rule-based Extraction
Trích xuất thông tin dựa trên rules/patterns cố định
"""

import re
from typing import Optional, Dict


class RuleExtractor:
    """Trích xuất thông tin bằng rules"""
    
    def __init__(self):
        """Khởi tạo rule extractor"""
        pass
    
    def extract_event_name(self, text: str) -> str:
        """
        Trích xuất tên sự kiện (phần đầu câu trước thông tin thời gian)
        
        Args:
            text: Văn bản đầu vào
        
        Returns:
            Tên sự kiện
        """
        # Loại bỏ khoảng trắng thừa
        text = ' '.join(text.split())
        
        # Pattern để tìm vị trí bắt đầu thông tin thời gian
        time_indicators = [
            r'lúc\s+\d',
            r'vào\s+\d',
            r'\d+\s*giờ',
            r'\d+h',
            r'\d+:\d+',
            r'hôm nay',
            r'hom nay',
            r'mai',
            r'ngày mai',
            r'ngay mai',
            r'tuần sau',
            r'tuan sau',
            r'thứ\s+\d',
            r'thu\s+\d',
            r'chủ nhật',
            r'chu nhat',
        ]
        
        # Tìm vị trí đầu tiên xuất hiện thông tin thời gian
        earliest_pos = len(text)
        for pattern in time_indicators:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and match.start() < earliest_pos:
                earliest_pos = match.start()
        
        # Tên sự kiện là phần trước thông tin thời gian
        if earliest_pos < len(text):
            event_name = text[:earliest_pos].strip()
        else:
            # Nếu không tìm thấy thời gian, lấy phần trước dấu phẩy đầu tiên
            if ',' in text:
                event_name = text.split(',')[0].strip()
            else:
                event_name = text.strip()
        
        # Làm sạch tên sự kiện
        event_name = event_name.strip(',').strip()
        
        # Nếu tên quá ngắn hoặc rỗng, trả về toàn bộ text
        if len(event_name) < 2:
            event_name = text.split(',')[0].strip() if ',' in text else text
        
        return event_name
    
    def extract_location(self, text: str) -> Optional[str]:
        """
        Trích xuất địa điểm từ pattern "ở/tại/phòng + [địa điểm]"
        
        Args:
            text: Văn bản đầu vào
        
        Returns:
            Địa điểm hoặc None
        """
        # Pattern cho địa điểm
        patterns = [
            r'(?:ở|o|tại|tai)\s+([^,]+?)(?:\s*,|\s*nhắc|\s*nhac|$)',
            r'phòng\s+(\d+[A-Za-z]?\d*)',
            r'phong\s+(\d+[A-Za-z]?\d*)',
            r'lớp\s+([^,]+?)(?:\s*,|\s*nhắc|\s*nhac|$)',
            r'lop\s+([^,]+?)(?:\s*,|\s*nhắc|\s*nhac|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                # Loại bỏ các từ không liên quan
                location = re.sub(r'\s*nhắc.*$', '', location, flags=re.IGNORECASE)
                location = re.sub(r'\s*nhac.*$', '', location, flags=re.IGNORECASE)
                return location
        
        return None
    
    def extract_reminder(self, text: str) -> Optional[int]:
        """
        Trích xuất thời gian nhắc nhở từ pattern "nhắc trước X phút/giờ"
        
        Args:
            text: Văn bản đầu vào
        
        Returns:
            Số phút nhắc trước hoặc None
        """
        # Pattern cho nhắc nhở
        patterns = [
            r'nhắc\s+trước\s+(\d+)\s*phút',
            r'nhac\s+truoc\s+(\d+)\s*phut',
            r'nhắc\s+trước\s+(\d+)\s*giờ',
            r'nhac\s+truoc\s+(\d+)\s*gio',
            r'nhắc\s+(\d+)\s*phút\s+trước',
            r'nhac\s+(\d+)\s*phut\s+truoc',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = int(match.group(1))
                
                # Nếu là giờ, chuyển sang phút
                if 'giờ' in pattern or 'gio' in pattern:
                    value = value * 60
                
                return value
        
        return None
    
    def extract_description(self, text: str, event_name: str, 
                          location: Optional[str], 
                          reminder: Optional[int]) -> Optional[str]:
        """
        Trích xuất phần mô tả (phần còn lại sau khi loại bỏ các thông tin đã trích xuất)
        
        Args:
            text: Văn bản đầu vào
            event_name: Tên sự kiện đã trích xuất
            location: Địa điểm đã trích xuất
            reminder: Thời gian nhắc đã trích xuất
        
        Returns:
            Mô tả hoặc None
        """
        # Hiện tại chưa implement logic phức tạp
        # Có thể mở rộng sau
        return None

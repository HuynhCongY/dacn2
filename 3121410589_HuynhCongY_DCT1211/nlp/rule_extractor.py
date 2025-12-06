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
            r'luc\s+\d',
            r'vào\s+\d',
            r'vao\s+\d',
            r'\d+\s*giờ',
            r'\d+\s*gio',
            r'\d+h',
            r'\d+:\d+',
            r'hôm nay',
            r'hom nay',
            r'mai\b',
            r'ngày mai',
            r'ngay mai',
            r'tuần sau',
            r'tuan sau',
            r'thứ\s+\d',
            r'thu\s+\d',
            r'chủ nhật',
            r'chu nhat',
        ]
        
        # Pattern để tìm vị trí bắt đầu địa điểm
        location_indicators = [
            r'\s+ở\s+',
            r'\s+o\s+',
            r'\s+tại\s+',
            r'\s+tai\s+',
            r'\s+phòng\s+',
            r'\s+phong\s+',
            r'\s+lớp\s+',
            r'\s+lop\s+',
        ]
        
        # Tìm vị trí đầu tiên xuất hiện thông tin thời gian
        earliest_pos = len(text)
        
        for pattern in time_indicators:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and match.start() < earliest_pos:
                earliest_pos = match.start()
        
        # Tìm vị trí đầu tiên xuất hiện thông tin địa điểm
        for pattern in location_indicators:
            match = re.search(pattern, text, re.IGNORECASE)
            if match and match.start() < earliest_pos:
                earliest_pos = match.start()
        
        # Tên sự kiện là phần trước thông tin thời gian/địa điểm
        if earliest_pos < len(text):
            event = text[:earliest_pos].strip()
        else:
            # Nếu không tìm thấy, lấy phần trước dấu phẩy đầu tiên
            if ',' in text:
                event = text.split(',')[0].strip()
            else:
                event = text.strip()
        
        # Làm sạch tên sự kiện
        event = event.strip(',').strip()
        
        # Nếu tên quá ngắn hoặc rỗng, trả về toàn bộ text
        if len(event) < 2:
            event = text.split(',')[0].strip() if ',' in text else text
        
        return event
    
    def extract_location(self, text: str) -> Optional[str]:
        """
        Trích xuất địa điểm từ pattern "ở/tại/phòng + [địa điểm]"
        
        Args:
            text: Văn bản đầu vào
        
        Returns:
            Địa điểm hoặc None
        """
        # Pattern cho phòng + số (ưu tiên cao nhất)
        phong_pattern = r'(?:phòng|phong)\s+([A-Z]?\d+[A-Za-z]?\d*)'
        match = re.search(phong_pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        
        # Pattern cho "tại phòng + tên phòng" (ví dụ: phòng hội thảo)
        tai_phong_pattern = r'(?:tại|tai)\s+phòng\s+([^\d,]+?)(?:\s*,|\s*nhắc|\s*nhac|$)'
        match = re.search(tai_phong_pattern, text, re.IGNORECASE)
        if match:
            location = match.group(1).strip()
            # Loại bỏ thông tin thời gian
            location = re.sub(r'\s*\d+\s*(?:giờ|gio|h).*$', '', location, flags=re.IGNORECASE)
            if location and len(location) > 1:
                return 'phòng ' + location
        
        # Pattern cho ở/tại + địa điểm (không phải phòng số)
        location_patterns = [
            r'(?:ở|o|tại|tai)\s+([^,]+?)(?:\s*,|\s*nhắc|\s*nhac|\s*lúc|\s*luc|$)',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                
                # Bỏ qua nếu bắt đầu bằng các từ không phải địa điểm
                skip_words = ['báo', 'bao', 'đồ', 'do', 'án', 'an', 'vệ', 've', 'cáo', 'cao']
                if any(location.lower().startswith(word) for word in skip_words):
                    continue
                
                # Loại bỏ thông tin thời gian ở cuối
                location = re.sub(r'\s*\d+\s*(?:giờ|gio|h)\s*.*$', '', location, flags=re.IGNORECASE)
                location = re.sub(r'\s*\d+:\d+.*$', '', location)
                location = re.sub(r'\s*(?:sáng|sang|chiều|chieu|tối|toi|đêm|dem)\s*.*$', '', location, flags=re.IGNORECASE)
                # Loại bỏ "mai", "hôm nay" nhưng giữ lại "Bạch Mai", "Mai Châu" 
                # Chỉ loại bỏ nếu "mai" đứng đầu hoặc đứng sau dấu phẩy/khoảng trắng nhiều
                location = re.sub(r'(?:,\s*|^\s*)(?:hôm nay|hom nay|mai|ngày mai|ngay mai).*$', '', location, flags=re.IGNORECASE)
                location = re.sub(r'\s*(?:thứ|thu)\s*\d+.*$', '', location, flags=re.IGNORECASE)
                location = location.strip()
                
                # Nếu location rỗng hoặc chỉ có số, return None
                if not location or location.isdigit():
                    return None
                    
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
            # Pattern chuẩn: nhắc trước X phút/giờ
            r'nhắc\s+(?:tôi\s+)?trước\s+(\d+)\s*(?:phút|giờ|h\b)',
            r'nhac\s+(?:toi\s+)?truoc\s+(\d+)\s*(?:phut|gio|h\b)',
            # Pattern với "trước Xp/Xh": nhắc tôi trước 30p, nhắc trước 2h
            r'nhắc\s+(?:tôi\s+)?trước\s+(\d+)\s*p\b',
            r'nhac\s+(?:toi\s+)?truoc\s+(\d+)\s*p\b',
            r'nhắc\s+(?:tôi\s+)?trước\s+(\d+)\s*h\b',
            r'nhac\s+(?:toi\s+)?truoc\s+(\d+)\s*h\b',
            # Pattern ngắn gọn: nhắc Xp, nhắc Xh (không có "trước")
            r'nhắc\s+(?:tôi\s+)?(\d+)\s*p\b',
            r'nhac\s+(?:toi\s+)?(\d+)\s*p\b',
            r'nhắc\s+(?:tôi\s+)?(\d+)\s*h\b',
            r'nhac\s+(?:toi\s+)?(\d+)\s*h\b',
            # Pattern có "phút" đầy đủ: nhắc 10 phút, nhắc 45 phút
            r'nhắc\s+(?:tôi\s+)?(\d+)\s*phút',
            r'nhac\s+(?:toi\s+)?(\d+)\s*phut',
            # Pattern đảo: X phút trước
            r'nhắc\s+(?:tôi\s+)?(\d+)\s*(?:phút|p\b)\s+trước',
            r'nhac\s+(?:toi\s+)?(\d+)\s*(?:phut|p\b)\s+truoc',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = int(match.group(1))
                
                # Nếu là giờ (chứa 'giờ', 'gio', hoặc 'h' không theo sau 'p'), chuyển sang phút
                # Kiểm tra xem pattern có chứa 'h\\b' (giờ) hay không
                matched_text = match.group(0).lower()
                if 'giờ' in matched_text or 'gio' in matched_text or (matched_text.endswith('h') and not matched_text.endswith('ph')):
                    value = value * 60
                
                return value
        
        return None

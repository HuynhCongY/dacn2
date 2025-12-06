"""
Component 2: Named Entity Recognition (NER) cho tiếng Việt
Nhận diện các thực thể: TIME, LOCATION
"""

import re
from typing import Dict, List, Optional


class NERExtractor:
    """Trích xuất các thực thể từ văn bản"""
    
    def __init__(self):
        """Khởi tạo NER extractor"""
        # Các từ khóa về thời gian
        self.time_keywords = [
            'giờ', 'phút', 'giây', 'sáng', 'trưa', 'chiều', 'tối', 'đêm',
            'hôm nay', 'hom nay', 'mai', 'ngày mai', 'ngay mai',
            'tuần sau', 'tuan sau', 'tuần tới', 'tuan toi',
            'tháng sau', 'thang sau', 'tháng tới', 'thang toi',
            'năm sau', 'nam sau', 'năm tới', 'nam toi',
            'thứ', 'thu', 'chủ nhật', 'chu nhat', 'cn',
            'lúc', 'luc', 'vào', 'vao'
        ]
        
        # Các từ khóa về địa điểm
        self.location_keywords = [
            'ở', 'o', 'tại', 'tai', 'phòng', 'phong',
            'lớp', 'lop', 'văn phòng', 'van phong',
            'nhà', 'nha', 'công ty', 'cong ty',
            'trường', 'truong', 'bệnh viện', 'benh vien'
        ]
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Trích xuất các thực thể từ văn bản
        
        Args:
            text: Văn bản đầu vào
        
        Returns:
            Dictionary chứa các thực thể tìm được
        """
        text_lower = text.lower()
        
        entities = {
            'TIME': [],
            'LOCATION': []
        }
        
        # Tìm TIME entities
        time_entities = self._find_time_entities(text_lower)
        entities['TIME'].extend(time_entities)
        
        # Tìm LOCATION entities
        location_entities = self._find_location_entities(text, text_lower)
        entities['LOCATION'].extend(location_entities)
        
        return entities
    
    def _find_time_entities(self, text: str) -> List[str]:
        """Tìm các thực thể về thời gian"""
        time_entities = []
        
        # Pattern cho giờ: "10 giờ", "10h", "10:30", "10h30"
        patterns = [
            r'\d{1,2}\s*giờ',
            r'\d{1,2}h\d{0,2}',
            r'\d{1,2}:\d{2}',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            time_entities.extend(matches)
        
        # Tìm các từ khóa thời gian
        for keyword in self.time_keywords:
            if keyword in text:
                time_entities.append(keyword)
        
        # Tìm ngày cụ thể: "25/12", "25-12", "ngày 25/12"
        date_patterns = [
            r'\d{1,2}/\d{1,2}',
            r'\d{1,2}-\d{1,2}',
            r'ngày\s+\d{1,2}/\d{1,2}',
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            time_entities.extend(matches)
        
        return list(set(time_entities))
    
    def _find_location_entities(self, text: str, text_lower: str) -> List[str]:
        """Tìm các thực thể về địa điểm"""
        location_entities = []
        
        # Tìm theo pattern "ở/tại/phòng + [địa điểm]"
        for keyword in self.location_keywords:
            pattern = rf'{keyword}\s+([^\s,]+(?:\s+\d+)?)'
            matches = re.findall(pattern, text_lower)
            
            if matches:
                # Lấy phần text gốc (giữ nguyên chữ hoa/thường)
                for match in matches:
                    # Tìm vị trí trong text gốc
                    idx = text_lower.find(f"{keyword} {match}")
                    if idx != -1:
                        start = idx + len(keyword) + 1
                        end = start + len(match)
                        location_entities.append(text[start:end])
        
        return list(set(location_entities))

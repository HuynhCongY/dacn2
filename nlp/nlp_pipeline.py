"""
Component 5: NLP Pipeline
Tổng hợp tất cả các component và xử lý lỗi
"""

from datetime import datetime
from typing import Dict, Optional
from .preprocessor import VietnamesePreprocessor
from .ner_extractor import NERExtractor
from .rule_extractor import RuleExtractor
from .time_parser import TimeParser


class VietnameseNLPPipeline:
    """Pipeline xử lý NLP tiếng Việt tổng hợp"""
    
    def __init__(self):
        """Khởi tạo NLP pipeline"""
        self.preprocessor = VietnamesePreprocessor()
        self.ner_extractor = NERExtractor()
        self.rule_extractor = RuleExtractor()
        self.time_parser = TimeParser()
    
    def parse(self, text: str) -> Dict:
        """
        Parse câu tiếng Việt và trả về thông tin sự kiện
        
        Args:
            text: Câu tiếng Việt mô tả sự kiện
        
        Returns:
            Dictionary chứa thông tin sự kiện:
            {
                'event_name': str,
                'start_time': datetime,
                'end_time': datetime (optional),
                'location': str (optional),
                'reminder_minutes': int (optional),
                'description': str (optional)
            }
        
        Raises:
            ValueError: Nếu không thể parse được thông tin
        """
        if not text or not text.strip():
            raise ValueError("Văn bản đầu vào rỗng")
        
        # Component 1: Preprocessing
        preprocessed_text = self.preprocessor.preprocess(text)
        
        # Component 2 & 3: Extract entities
        entities = self.ner_extractor.extract_entities(preprocessed_text)
        
        # Trích xuất tên sự kiện
        event_name = self.rule_extractor.extract_event_name(preprocessed_text)
        
        # Trích xuất địa điểm
        location = self.rule_extractor.extract_location(preprocessed_text)
        
        # Trích xuất thời gian nhắc nhở
        reminder_minutes = self.rule_extractor.extract_reminder(preprocessed_text)
        
        # Component 4: Time parsing
        start_time = self.time_parser.parse_time(preprocessed_text)
        
        # Component 5: Validation and merge
        result = self._validate_and_merge({
            'event_name': event_name,
            'start_time': start_time,
            'location': location,
            'reminder_minutes': reminder_minutes
        })
        
        return result
    
    def _validate_and_merge(self, data: Dict) -> Dict:
        """
        Kiểm tra tính hợp lệ và ghép kết quả
        
        Args:
            data: Dictionary chứa các thông tin đã trích xuất
        
        Returns:
            Dictionary đã được validate và làm sạch
        
        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
        """
        # Kiểm tra tên sự kiện
        if not data.get('event_name'):
            raise ValueError("Không thể trích xuất tên sự kiện")
        
        event_name = data['event_name'].strip()
        if len(event_name) < 2:
            raise ValueError("Tên sự kiện quá ngắn")
        
        # Kiểm tra thời gian
        start_time = data.get('start_time')
        if not start_time:
            raise ValueError("Không thể trích xuất thời gian")
        
        # Tạo kết quả
        result = {
            'event_name': event_name,
            'start_time': start_time,
            'end_time': data.get('end_time'),
            'location': data.get('location'),
            'reminder_minutes': data.get('reminder_minutes'),
            'description': data.get('description')
        }
        
        return result
    
    def parse_multiple(self, texts: list) -> list:
        """
        Parse nhiều câu cùng lúc
        
        Args:
            texts: List các câu cần parse
        
        Returns:
            List các kết quả (Dict hoặc None nếu lỗi)
        """
        results = []
        for text in texts:
            try:
                result = self.parse(text)
                results.append(result)
            except Exception as e:
                results.append({'error': str(e), 'text': text})
        
        return results
    
    def test_accuracy(self, test_cases: list) -> Dict:
        """
        Test độ chính xác của pipeline
        
        Args:
            test_cases: List các test case
                Mỗi test case là tuple (text, expected_result)
        
        Returns:
            Dictionary chứa kết quả test:
            {
                'total': int,
                'success': int,
                'failed': int,
                'accuracy': float,
                'failed_cases': list
            }
        """
        total = len(test_cases)
        success = 0
        failed_cases = []
        
        for i, (text, expected) in enumerate(test_cases):
            try:
                result = self.parse(text)
                # Kiểm tra các trường quan trọng
                is_correct = True
                
                if expected.get('event_name'):
                    if result['event_name'].lower() != expected['event_name'].lower():
                        is_correct = False
                
                if expected.get('location'):
                    if result.get('location', '').lower() != expected['location'].lower():
                        is_correct = False
                
                if expected.get('reminder_minutes'):
                    if result.get('reminder_minutes') != expected['reminder_minutes']:
                        is_correct = False
                
                if is_correct:
                    success += 1
                else:
                    failed_cases.append({
                        'index': i + 1,
                        'text': text,
                        'expected': expected,
                        'actual': result
                    })
            except Exception as e:
                failed_cases.append({
                    'index': i + 1,
                    'text': text,
                    'error': str(e)
                })
        
        accuracy = (success / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'success': success,
            'failed': total - success,
            'accuracy': accuracy,
            'failed_cases': failed_cases
        }

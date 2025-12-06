"""
Component 1: Tiền xử lý văn bản tiếng Việt
"""

import re
from underthesea import word_tokenize


class VietnamesePreprocessor:
    """Xử lý tiền xử lý văn bản tiếng Việt"""
    
    def __init__(self):
        """Khởi tạo preprocessor"""
        pass
    
    def preprocess(self, text: str) -> str:
        """
        Tiền xử lý văn bản
        
        Args:
            text: Văn bản đầu vào
        
        Returns:
            Văn bản đã được chuẩn hóa
        """
        if not text:
            return ""
        
        # Loại bỏ khoảng trắng thừa
        text = ' '.join(text.split())
        
        # Chuẩn hóa dấu câu
        text = text.replace(',', ', ')
        text = text.replace('.', '. ')
        
        # Loại bỏ khoảng trắng thừa sau chuẩn hóa
        text = ' '.join(text.split())
        
        return text
    
    def tokenize(self, text: str) -> list:
        """
        Tách từ tiếng Việt
        
        Args:
            text: Văn bản đầu vào
        
        Returns:
            List các từ đã được tách
        """
        try:
            tokens = word_tokenize(text, format="text")
            return tokens.split()
        except:
            # Fallback nếu underthesea lỗi
            return text.split()
    
    def normalize_text(self, text: str) -> str:
        """
        Chuẩn hóa văn bản (lowercase, remove extra spaces)
        
        Args:
            text: Văn bản đầu vào
        
        Returns:
            Văn bản đã chuẩn hóa
        """
        # Chuyển về chữ thường
        text = text.lower()
        
        # Loại bỏ khoảng trắng thừa
        text = ' '.join(text.split())
        
        return text
    
    def remove_accents(self, text: str) -> str:
        """
        Loại bỏ dấu tiếng Việt (để so sánh)
        
        Args:
            text: Văn bản có dấu
        
        Returns:
            Văn bản không dấu
        """
        # Bảng chuyển đổi dấu tiếng Việt
        accents = {
            'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
            'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
            'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
            'đ': 'd',
            'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
            'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
            'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
            'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
            'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
            'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
            'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
            'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
            'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
        }
        
        result = []
        for char in text:
            result.append(accents.get(char, char))
        
        return ''.join(result)

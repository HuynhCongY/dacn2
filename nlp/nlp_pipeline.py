"""NLP Pipeline stub for testing"""
from datetime import datetime, timedelta
import re

class VietnameseNLPPipeline:
    def __init__(self):
        pass
    
    def parse(self, text):
        """Parse Vietnamese text to extract event information"""
        # Simple stub implementation for testing
        result = {
            'event_name': 'Test Event',
            'start_time': datetime.now() + timedelta(days=1),
            'end_time': None,
            'location': None,
            'reminder_minutes': None,
            'description': text
        }
        
        # Extract simple patterns
        if 'phòng' in text.lower() or 'ở' in text.lower():
            # Try to extract location
            parts = text.split('ở')
            if len(parts) > 1:
                result['location'] = parts[1].split(',')[0].strip()
        
        if 'nhắc' in text.lower():
            # Try to extract reminder
            match = re.search(r'(\d+)\s*phút', text)
            if match:
                result['reminder_minutes'] = int(match.group(1))
        
        return result

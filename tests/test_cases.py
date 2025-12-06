"""Test cases for NLP pipeline"""

def get_test_cases():
    """Return list of test cases"""
    return [
        ("Họp nhóm lúc 10 giờ sáng mai", {
            'event_name': 'Họp nhóm',
            'location': None,
            'reminder_minutes': None
        }),
        ("Họp nhóm lúc 10 giờ sáng mai ở phòng 302, nhắc trước 15 phút", {
            'event_name': 'Họp nhóm',
            'location': 'phòng 302',
            'reminder_minutes': 15
        }),
    ]

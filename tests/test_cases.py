"""
30 Test cases cho NLP pipeline
"""

from datetime import datetime, timedelta


def get_test_cases():
    """
    Trả về 30 test cases để test NLP pipeline
    
    Returns:
        List các tuple (text, expected_result)
    """
    now = datetime.now()
    
    test_cases = [
        # Test 1-5: Thời gian cơ bản
        (
            "Họp nhóm lúc 10 giờ sáng mai ở phòng 302, nhắc trước 15 phút",
            {
                'event_name': 'Họp nhóm',
                'location': '302',
                'reminder_minutes': 15
            }
        ),
        (
            "Đi khám răng 3 giờ chiều thứ 6 này",
            {
                'event_name': 'Đi khám răng',
                'location': None,
                'reminder_minutes': None
            }
        ),
        (
            "Sinh nhật bạn vào 8 giờ tối ngày 25/12",
            {
                'event_name': 'Sinh nhật bạn',
                'location': None,
                'reminder_minutes': None
            }
        ),
        (
            "Nộp báo cáo deadline 5 giờ chiều mai",
            {
                'event_name': 'Nộp báo cáo deadline',
                'location': None,
                'reminder_minutes': None
            }
        ),
        (
            "Học tiếng Anh 7 giờ sáng hôm nay",
            {
                'event_name': 'Học tiếng Anh',
                'location': None,
                'reminder_minutes': None
            }
        ),
        
        # Test 6-10: Địa điểm
        (
            "Họp phụ huynh ở trường lúc 2 giờ chiều mai",
            {
                'event_name': 'Họp phụ huynh',
                'location': 'trường',
                'reminder_minutes': None
            }
        ),
        (
            "Tập gym tại phòng 501 lúc 6 giờ tối",
            {
                'event_name': 'Tập gym',
                'location': '501',
                'reminder_minutes': None
            }
        ),
        (
            "Phỏng vấn ở công ty ABC 9 giờ sáng thứ 2",
            {
                'event_name': 'Phỏng vấn',
                'location': 'công ty ABC',
                'reminder_minutes': None
            }
        ),
        (
            "Hẹn bác sĩ tại bệnh viện 10 giờ mai",
            {
                'event_name': 'Hẹn bác sĩ',
                'location': 'bệnh viện',
                'reminder_minutes': None
            }
        ),
        (
            "Học lớp C4K309 vào 1 giờ chiều thứ 4",
            {
                'event_name': 'Học',
                'location': None,
                'reminder_minutes': None
            }
        ),
        
        # Test 11-15: Nhắc nhở
        (
            "Gặp khách hàng 3 giờ chiều mai, nhắc trước 30 phút",
            {
                'event_name': 'Gặp khách hàng',
                'location': None,
                'reminder_minutes': 30
            }
        ),
        (
            "Nộp hồ sơ 9 giờ sáng thứ 3, nhắc trước 1 giờ",
            {
                'event_name': 'Nộp hồ sơ',
                'location': None,
                'reminder_minutes': 60
            }
        ),
        (
            "Họp team 10h30 mai ở phòng A101, nhắc trước 10 phút",
            {
                'event_name': 'Họp team',
                'location': 'A101',
                'reminder_minutes': 10
            }
        ),
        (
            "Bảo vệ đồ án lúc 8 giờ sáng thứ 6, nhắc trước 2 giờ",
            {
                'event_name': 'Bảo vệ đồ án',
                'location': None,
                'reminder_minutes': 120
            }
        ),
        (
            "Đi máy bay 5 giờ sáng mai, nhắc trước 3 giờ",
            {
                'event_name': 'Đi máy bay',
                'location': None,
                'reminder_minutes': 180
            }
        ),
        
        # Test 16-20: Thời gian phức tạp
        (
            "Thi cuối kỳ 7h30 sáng thứ 2 tuần sau",
            {
                'event_name': 'Thi cuối kỳ',
                'location': None,
                'reminder_minutes': None
            }
        ),
        (
            "Dự tiệc cưới 6 giờ tối chủ nhật này",
            {
                'event_name': 'Dự tiệc cưới',
                'location': None,
                'reminder_minutes': None
            }
        ),
        (
            "Làm việc nhóm 2:30 chiều mai ở phòng B203",
            {
                'event_name': 'Làm việc nhóm',
                'location': 'B203',
                'reminder_minutes': None
            }
        ),
        (
            "Đi du lịch 8 giờ sáng ngày 1/1",
            {
                'event_name': 'Đi du lịch',
                'location': None,
                'reminder_minutes': None
            }
        ),
        (
            "Hội nghị khoa học 9h sáng thứ 5",
            {
                'event_name': 'Hội nghị khoa học',
                'location': None,
                'reminder_minutes': None
            }
        ),
        
        # Test 21-25: Không dấu
        (
            "Hop nhom luc 10 gio sang mai o phong 302",
            {
                'event_name': 'Hop nhom',
                'location': '302',
                'reminder_minutes': None
            }
        ),
        (
            "Di kham rang 3 gio chieu thu 6 nay",
            {
                'event_name': 'Di kham rang',
                'location': None,
                'reminder_minutes': None
            }
        ),
        (
            "Hoc tieng Anh 7 gio sang hom nay",
            {
                'event_name': 'Hoc tieng Anh',
                'location': None,
                'reminder_minutes': None
            }
        ),
        (
            "Tap gym tai phong 501 luc 6 gio toi, nhac truoc 15 phut",
            {
                'event_name': 'Tap gym',
                'location': '501',
                'reminder_minutes': 15
            }
        ),
        (
            "Nop bao cao deadline 5 gio chieu mai",
            {
                'event_name': 'Nop bao cao deadline',
                'location': None,
                'reminder_minutes': None
            }
        ),
        
        # Test 26-30: Các trường hợp đặc biệt
        (
            "Seminar AI vào 3 giờ chiều thứ 3 tại phòng hội thảo",
            {
                'event_name': 'Seminar AI',
                'location': 'phòng hội thảo',
                'reminder_minutes': None
            }
        ),
        (
            "Review code 10 giờ sáng mai",
            {
                'event_name': 'Review code',
                'location': None,
                'reminder_minutes': None
            }
        ),
        (
            "Đi shopping 4 giờ chiều chủ nhật",
            {
                'event_name': 'Đi shopping',
                'location': None,
                'reminder_minutes': None
            }
        ),
        (
            "Meeting online 9h30 sáng thứ 2, nhắc trước 5 phút",
            {
                'event_name': 'Meeting online',
                'location': None,
                'reminder_minutes': 5
            }
        ),
        (
            "Kiểm tra sức khỏe định kỳ 8 giờ sáng mai tại phòng khám",
            {
                'event_name': 'Kiểm tra sức khỏe định kỳ',
                'location': 'phòng khám',
                'reminder_minutes': None
            }
        ),
    ]
    
    return test_cases


def print_test_cases():
    """In ra tất cả test cases"""
    test_cases = get_test_cases()
    
    print("=" * 80)
    print("30 TEST CASES CHO NLP PIPELINE")
    print("=" * 80)
    
    for i, (text, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"  Text: {text}")
        print(f"  Expected:")
        print(f"    - Event: {expected['event_name']}")
        print(f"    - Location: {expected['location']}")
        print(f"    - Reminder: {expected['reminder_minutes']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print_test_cases()

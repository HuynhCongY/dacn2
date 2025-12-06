"""
Test NLP pipeline với dữ liệu từ file JSON
"""

import json
import os
import sys
from datetime import datetime

# Thêm thư mục gốc vào sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from nlp.nlp_pipeline import VietnameseNLPPipeline


def load_test_data(json_file='test_data.json'):
    """
    Tải test cases từ file JSON
    
    Args:
        json_file: Đường dẫn đến file JSON chứa test cases
    
    Returns:
        List các test cases
    """
    # Lấy đường dẫn tuyệt đối của file JSON
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, json_file)
    
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Không tìm thấy file: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8-sig') as f:
        test_data = json.load(f)
    
    return test_data


def run_nlp_tests(json_file='test_data.json'):
    """
    Chạy test NLP pipeline với dữ liệu từ file JSON
    
    Args:
        json_file: Đường dẫn đến file JSON chứa test cases
    
    Returns:
        Dict chứa kết quả test
    """
    print("Đang khởi tạo NLP Pipeline...")
    
    # Tải test data
    test_data = load_test_data(json_file)
    
    # Khởi tạo NLP pipeline
    nlp = VietnameseNLPPipeline()
    
    # Biến đếm
    total = len(test_data)
    passed = 0
    failed = 0
    results = []
    
    print("=" * 100)
    print(f"CHẠY {total} TEST CASES CHO NLP PIPELINE")
    print("=" * 100)
    
    for test_case in test_data:
        test_id = test_case['id']
        text = test_case['text']
        expected = test_case['expected']
        
        # Chạy NLP pipeline
        result = nlp.parse(text)
        
        # So sánh kết quả
        is_passed = True
        errors = []
        
        # Kiểm tra event
        actual_event = result.get('event', '')
        expected_event = expected.get('event', '')
        if actual_event != expected_event:
            is_passed = False
            errors.append(f"Event name: expected '{expected_event}', got '{actual_event}'")
        
        # Kiểm tra location
        actual_location = result.get('location')
        expected_location = expected.get('location')
        if actual_location != expected_location:
            is_passed = False
            errors.append(f"Location: expected '{expected_location}', got '{actual_location}'")
        
        # Kiểm tra reminder_minutes
        actual_reminder = result.get('reminder_minutes')
        expected_reminder = expected.get('reminder_minutes')
        if actual_reminder != expected_reminder:
            is_passed = False
            errors.append(f"Reminder: expected '{expected_reminder}', got '{actual_reminder}'")
        
        # Kiểm tra start_time (chỉ so sánh nếu expected có start_time)
        if expected.get('start_time'):
            actual_start = result.get('start_time')
            expected_start = expected.get('start_time')
            if actual_start:
                # So sánh chỉ phần date và time, bỏ qua timezone
                actual_start_str = actual_start.strftime('%Y-%m-%dT%H:%M:%S') if hasattr(actual_start, 'strftime') else str(actual_start)[:19]
                if actual_start_str != expected_start:
                    is_passed = False
                    errors.append(f"Start time: expected '{expected_start}', got '{actual_start_str}'")
            else:
                is_passed = False
                errors.append(f"Start time: expected '{expected_start}', got 'None'")
        
        # Kiểm tra end_time (chỉ so sánh nếu expected có end_time không null)
        if expected.get('end_time') is not None:
            actual_end = result.get('end_time')
            expected_end = expected.get('end_time')
            if actual_end:
                actual_end_str = actual_end.strftime('%Y-%m-%dT%H:%M:%S') if hasattr(actual_end, 'strftime') else str(actual_end)[:19]
                if actual_end_str != expected_end:
                    is_passed = False
                    errors.append(f"End time: expected '{expected_end}', got '{actual_end_str}'")
            elif expected_end is not None:
                is_passed = False
                errors.append(f"End time: expected '{expected_end}', got 'None'")
        
        # Cập nhật kết quả
        if is_passed:
            passed += 1
            status = " PASS"
        else:
            failed += 1
            status = " FAIL"
        
        # Lưu kết quả
        test_result = {
            'id': test_id,
            'text': text,
            'expected': expected,
            'actual': {
                'event': result.get('event'),
                'location': result.get('location'),
                'reminder_minutes': result.get('reminder_minutes'),
                'start_time': result.get('start_time'),
                'end_time': result.get('end_time')
            },
            'status': status,
            'errors': errors
        }
        results.append(test_result)
        
        # In kết quả
        print(f"\n[Test {test_id}] {status}")
        print(f"  Input: {text}")
        if errors:
            print(f"  Errors:")
            for error in errors:
                print(f"    - {error}")
    
    # Tính tỷ lệ
    pass_rate = (passed / total * 100) if total > 0 else 0
    fail_rate = (failed / total * 100) if total > 0 else 0
    
    # In tóm tắt
    print("\n" + "=" * 100)
    print(f"KẾT QUẢ TỔNG HỢP")
    print("=" * 100)
    print(f"Tổng số test:  {total}")
    print(f"Passed:        {passed} ({pass_rate:.1f}%)")
    print(f"Failed:        {failed} ({fail_rate:.1f}%)")
    print("=" * 100)
    
    return {
        'total': total,
        'passed': passed,
        'failed': failed,
        'pass_rate': pass_rate,
        'fail_rate': fail_rate,
        'results': results
    }


def export_results_to_json(test_results, output_file='test_results.json'):
    """
    Xuất kết quả test ra file JSON
    
    Args:
        test_results: Dict chứa kết quả test
        output_file: Tên file JSON để lưu kết quả
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, output_file)
    
    # Chuyển đổi datetime thành string trong results
    clean_results = []
    for result in test_results['results']:
        clean_result = {
            'id': result['id'],
            'text': result['text'],
            'expected': result['expected'],
            'actual': {
                'event': result['actual'].get('event'),
                'location': result['actual'].get('location'),
                'reminder_minutes': result['actual'].get('reminder_minutes'),
                'start_time': result['actual'].get('start_time').isoformat() if result['actual'].get('start_time') else None,
                'end_time': result['actual'].get('end_time').isoformat() if result['actual'].get('end_time') else None
            },
            'status': result['status'],
            'errors': result['errors']
        }
        clean_results.append(clean_result)
    
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total': test_results['total'],
            'passed': test_results['passed'],
            'failed': test_results['failed'],
            'pass_rate': f"{test_results['pass_rate']:.1f}%",
            'fail_rate': f"{test_results['fail_rate']:.1f}%"
        },
        'results': clean_results
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nĐã lưu kết quả vào: {output_path}")


if __name__ == "__main__":
    try:
        # Chạy tests
        test_results = run_nlp_tests()
        
        # Xuất kết quả ra file JSON
        export_results_to_json(test_results)
        
        print("\n✓ Test hoàn tất!")
        
    except Exception as e:
        print(f"\n✗ Lỗi khi chạy test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        # Chạy tests
        test_results = run_nlp_tests()
        
        # Xuất kết quả ra file JSON
        export_results_to_json(test_results)
        
        print("\n✓ Test hoàn tất!")
        
    except Exception as e:
        print(f"\n✗ Lỗi khi chạy test: {e}")
        import traceback
        traceback.print_exc()


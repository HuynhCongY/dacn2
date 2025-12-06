"""
Ứng dụng quản lý lịch trình cá nhân với xử lý tiếng Việt
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json

from database.db_manager import DatabaseManager
from nlp.nlp_pipeline import VietnameseNLPPipeline
from reminder.reminder_system import ReminderSystem
from utils.export_import import ExportImport
from utils.constants import (
    PAGE_TITLE, PAGE_ICON, DEFAULT_DB_PATH,
    DATETIME_FORMAT, ICON_TIME, ICON_LOCATION, ICON_REMINDER, ICON_DESCRIPTION
)
from tests.test_cases import get_test_cases

# Cấu hình trang
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide"
)

# Khởi tạo session state
if 'db' not in st.session_state:
    st.session_state.db = DatabaseManager(DEFAULT_DB_PATH)

if 'nlp' not in st.session_state:
    st.session_state.nlp = VietnameseNLPPipeline()

if 'reminder_system' not in st.session_state:
    st.session_state.reminder_system = ReminderSystem(st.session_state.db)
    st.session_state.reminder_system.start()

if 'export_import' not in st.session_state:
    st.session_state.export_import = ExportImport()

if 'notification_messages' not in st.session_state:
    st.session_state.notification_messages = []


def should_show_reminder(reminder_minutes):
    """Helper function to determine if reminder should be displayed"""
    return reminder_minutes is not None and reminder_minutes > 0


def show_add_event_page():
    """Trang thêm sự kiện"""
    st.title("📅 Thêm sự kiện mới")
    
    # Nhập bằng ngôn ngữ tự nhiên
    st.subheader("🗣️ Nhập bằng tiếng Việt")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_area(
            "Nhập mô tả sự kiện:",
            placeholder="Ví dụ: Họp nhóm lúc 10 giờ sáng mai ở phòng 302, nhắc trước 15 phút",
            height=100,
            key="nlp_input"
        )
    
    with col2:
        st.write("**Ví dụ:**")
        st.caption("• Họp nhóm lúc 10 giờ sáng mai")
        st.caption("• Đi khám răng 3 giờ chiều thứ 6")
        st.caption("• Học tiếng Anh 7h sáng hôm nay")
    
    if st.button("🚀 Thêm sự kiện từ văn bản", type="primary"):
        if user_input.strip():
            try:
                with st.spinner("Đang xử lý..."):
                    result = st.session_state.nlp.parse(user_input)
                
                st.success("✅ Trích xuất thành công!")
                
                # Hiển thị preview
                st.subheader("📋 Thông tin đã trích xuất:")
                
                st.write(f"**Tên sự kiện:** {result['event_name']}")
                st.write(f"{ICON_TIME} **Thời gian:** {result['start_time'].strftime(DATETIME_FORMAT)}")
                
                if result.get('location'):
                    st.write(f"{ICON_LOCATION} **Địa điểm:** {result['location']}")
                
                if should_show_reminder(result.get('reminder_minutes')):
                    st.write(f"{ICON_REMINDER} **Nhắc trước:** {result['reminder_minutes']} phút")
                
                if result.get('description'):
                    st.write(f"{ICON_DESCRIPTION} **Mô tả:** {result['description']}")
                
                # Lưu vào database
                event_id = st.session_state.db.add_event(result)
                st.success(f"✅ Đã thêm sự kiện (ID: {event_id})")
                
            except Exception as e:
                st.error(f"❌ Lỗi: {e}")
                st.info("💡 Vui lòng thử lại hoặc sử dụng form nhập thủ công bên dưới")
        else:
            st.warning("⚠️ Vui lòng nhập mô tả sự kiện")
    
    st.divider()
    
    # Form nhập thủ công
    st.subheader("✍️ Nhập thủ công")
    
    with st.form("manual_event_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            event_name = st.text_input("Tên sự kiện *", placeholder="Ví dụ: Họp nhóm")
            
            start_date = st.date_input("Ngày bắt đầu *", value=datetime.now())
            start_time = st.time_input("Giờ bắt đầu *", value=datetime.now().time())
            
            location = st.text_input("Địa điểm", placeholder="Ví dụ: Phòng 302")
        
        with col2:
            end_date = st.date_input("Ngày kết thúc (tùy chọn)", value=None)
            end_time = st.time_input("Giờ kết thúc (tùy chọn)", value=None)
            
            reminder_minutes = st.number_input(
                "Nhắc trước (phút)", 
                min_value=0, 
                value=15, 
                step=5
            )
        
        description = st.text_area("Mô tả", placeholder="Thông tin bổ sung...")
        
        submitted = st.form_submit_button("➕ Thêm sự kiện", type="primary")
        
        if submitted:
            if event_name and start_date and start_time:
                try:
                    # Tạo datetime
                    start_datetime = datetime.combine(start_date, start_time)
                    
                    end_datetime = None
                    if end_date and end_time:
                        end_datetime = datetime.combine(end_date, end_time)
                    
                    # Tạo event data
                    event_data = {
                        'event_name': event_name,
                        'start_time': start_datetime,
                        'end_time': end_datetime,
                        'location': location if location else None,
                        'reminder_minutes': reminder_minutes if reminder_minutes > 0 else None,
                        'description': description if description else None
                    }
                    
                    # Lưu vào database
                    event_id = st.session_state.db.add_event(event_data)
                    st.success(f"✅ Đã thêm sự kiện thành công! (ID: {event_id})")
                    
                except Exception as e:
                    st.error(f"❌ Lỗi khi thêm sự kiện: {e}")
            else:
                st.error("❌ Vui lòng điền đầy đủ thông tin bắt buộc (*)")


def show_calendar_page():
    """Trang xem lịch"""
    st.title("📆 Xem lịch")
    
    # Tab view
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Ngày", "📆 Tuần", "🗓️ Tháng", "🔍 Tìm kiếm"])
    
    with tab1:
        show_day_view()
    
    with tab2:
        show_week_view()
    
    with tab3:
        show_month_view()
    
    with tab4:
        show_search_view()


def show_day_view():
    """Hiển thị lịch theo ngày"""
    st.subheader("Lịch theo ngày")
    
    selected_date = st.date_input("Chọn ngày", value=datetime.now())
    
    # Lấy events trong ngày
    start = datetime.combine(selected_date, datetime.min.time())
    end = start + timedelta(days=1)
    
    events = st.session_state.db.get_events(start, end)
    
    if events:
        st.write(f"**Có {len(events)} sự kiện trong ngày {selected_date.strftime('%d/%m/%Y')}**")
        
        for event in events:
            show_event_card(event, key_prefix="day")
    else:
        st.info("📭 Không có sự kiện nào trong ngày này")


def show_week_view():
    """Hiển thị lịch theo tuần"""
    st.subheader("Lịch theo tuần")
    
    selected_date = st.date_input("Chọn ngày trong tuần", value=datetime.now(), key="week_date")
    
    # Tính ngày đầu và cuối tuần
    start = selected_date - timedelta(days=selected_date.weekday())
    end = start + timedelta(days=7)
    
    start_dt = datetime.combine(start, datetime.min.time())
    end_dt = datetime.combine(end, datetime.min.time())
    
    events = st.session_state.db.get_events(start_dt, end_dt)
    
    st.write(f"**Tuần từ {start.strftime('%d/%m/%Y')} đến {end.strftime('%d/%m/%Y')}**")
    
    if events:
        st.write(f"**Có {len(events)} sự kiện trong tuần**")
        
        for event in events:
            show_event_card(event, key_prefix="week")
    else:
        st.info("📭 Không có sự kiện nào trong tuần này")


def show_month_view():
    """Hiển thị lịch theo tháng"""
    st.subheader("Lịch theo tháng")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_month = st.selectbox(
            "Chọn tháng",
            range(1, 13),
            index=datetime.now().month - 1,
            format_func=lambda x: f"Tháng {x}"
        )
    
    with col2:
        current_year = datetime.now().year
        selected_year = st.number_input("Chọn năm", min_value=current_year - 5, max_value=current_year + 5, value=current_year)
    
    # Tính ngày đầu và cuối tháng
    start = datetime(selected_year, selected_month, 1)
    if selected_month == 12:
        end = datetime(selected_year + 1, 1, 1)
    else:
        end = datetime(selected_year, selected_month + 1, 1)
    
    events = st.session_state.db.get_events(start, end)
    
    st.write(f"**Tháng {selected_month}/{selected_year}**")
    
    if events:
        st.write(f"**Có {len(events)} sự kiện trong tháng**")
        
        for event in events:
            show_event_card(event, key_prefix="month")
    else:
        st.info("📭 Không có sự kiện nào trong tháng này")


def show_search_view():
    """Hiển thị tìm kiếm"""
    st.subheader("Tìm kiếm sự kiện")
    
    keyword = st.text_input("Nhập từ khóa tìm kiếm", placeholder="Tên sự kiện, địa điểm...")
    
    if keyword:
        events = st.session_state.db.search_events(keyword)
        
        if events:
            st.write(f"**Tìm thấy {len(events)} sự kiện**")
            
            for event in events:
                show_event_card(event, key_prefix="search")
        else:
            st.info("📭 Không tìm thấy sự kiện nào")


def show_event_card(event, key_prefix=""):
    """Hiển thị card cho một sự kiện"""
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"### {event['event_name']}")
            st.write(f"{ICON_TIME} **Thời gian:** {event['start_time'].strftime(DATETIME_FORMAT)}")
            
            if event.get('location'):
                st.write(f"{ICON_LOCATION} **Địa điểm:** {event['location']}")
            
            if should_show_reminder(event.get('reminder_minutes')):
                st.write(f"{ICON_REMINDER} **Nhắc trước:** {event['reminder_minutes']} phút")
            
            if event.get('description'):
                st.write(f"{ICON_DESCRIPTION} **Mô tả:** {event['description']}")
        
        with col2:
            if st.button("✏️ Sửa", key=f"{key_prefix}_edit_{event['id']}"):
                st.session_state.editing_event = event['id']
                st.rerun()
            
            if st.button("🗑️ Xóa", key=f"{key_prefix}_delete_{event['id']}"):
                if st.session_state.db.delete_event(event['id']):
                    st.success("✅ Đã xóa sự kiện")
                    st.rerun()
                else:
                    st.error("❌ Không thể xóa sự kiện")
        
        st.divider()


def show_settings_page():
    """Trang cài đặt và xuất/nhập"""
    st.title("⚙️ Cài đặt & Xuất/Nhập")
    
    # Xuất dữ liệu
    st.subheader("📤 Xuất dữ liệu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Xuất ra ICS (iCalendar)", type="primary"):
            events = st.session_state.db.get_all_events()
            
            if events:
                try:
                    ics_content = st.session_state.export_import.export_to_ics(events)
                    
                    st.download_button(
                        label="⬇️ Download file ICS",
                        data=ics_content,
                        file_name=f"calendar_{datetime.now().strftime('%Y%m%d')}.ics",
                        mime="text/calendar"
                    )
                    
                    st.success(f"✅ Đã xuất {len(events)} sự kiện")
                except Exception as e:
                    st.error(f"❌ Lỗi khi xuất ICS: {e}")
            else:
                st.warning("⚠️ Không có sự kiện nào để xuất")
    
    with col2:
        if st.button("📋 Xuất ra JSON", type="primary"):
            events = st.session_state.db.get_all_events()
            
            if events:
                try:
                    json_content = st.session_state.export_import.export_to_json(events)
                    
                    st.download_button(
                        label="⬇️ Download file JSON",
                        data=json_content,
                        file_name=f"calendar_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
                    
                    st.success(f"✅ Đã xuất {len(events)} sự kiện")
                except Exception as e:
                    st.error(f"❌ Lỗi khi xuất JSON: {e}")
            else:
                st.warning("⚠️ Không có sự kiện nào để xuất")
    
    st.divider()
    
    # Nhập dữ liệu
    st.subheader("📥 Nhập dữ liệu")
    
    uploaded_file = st.file_uploader("Chọn file JSON để nhập", type=['json'])
    
    if uploaded_file is not None:
        try:
            json_content = uploaded_file.read().decode('utf-8')
            events = st.session_state.export_import.import_from_json(json_content)
            
            st.write(f"**Tìm thấy {len(events)} sự kiện trong file**")
            
            if st.button("📥 Import vào database"):
                success, errors = st.session_state.db.import_events(events)
                st.success(f"✅ Đã import {success} sự kiện")
                
                if errors > 0:
                    st.warning(f"⚠️ {errors} sự kiện bị lỗi")
                
        except Exception as e:
            st.error(f"❌ Lỗi khi đọc file: {e}")
    
    st.divider()
    
    # Xóa dữ liệu
    st.subheader("🗑️ Xóa dữ liệu")
    
    st.warning("⚠️ **Cảnh báo:** Thao tác này sẽ xóa toàn bộ dữ liệu và không thể khôi phục!")
    
    if st.button("🗑️ Xóa toàn bộ sự kiện", type="secondary"):
        if st.checkbox("Tôi hiểu và muốn xóa toàn bộ dữ liệu"):
            st.session_state.db.clear_all_events()
            st.success("✅ Đã xóa toàn bộ dữ liệu")
            st.rerun()


def show_test_nlp_page():
    """Trang test NLP"""
    st.title("🧪 Test NLP Pipeline")
    
    st.write("Kiểm tra độ chính xác của hệ thống xử lý ngôn ngữ tự nhiên với 30 test cases")
    
    # Test đơn lẻ
    st.subheader("🔬 Test một câu")
    
    test_input = st.text_area(
        "Nhập câu test:",
        placeholder="Ví dụ: Họp nhóm lúc 10 giờ sáng mai ở phòng 302, nhắc trước 15 phút",
        height=80
    )
    
    if st.button("🧪 Test câu này"):
        if test_input.strip():
            try:
                with st.spinner("Đang xử lý..."):
                    result = st.session_state.nlp.parse(test_input)
                
                st.success("✅ Trích xuất thành công!")
                st.json(result)
                
            except Exception as e:
                st.error(f"❌ Lỗi: {e}")
        else:
            st.warning("⚠️ Vui lòng nhập câu test")
    
    st.divider()
    
    # Test tất cả 30 cases
    st.subheader("📊 Test 30 test cases")
    
    if st.button("🚀 Chạy test tất cả 30 cases", type="primary"):
        test_cases = get_test_cases()
        
        with st.spinner(f"Đang test {len(test_cases)} cases..."):
            success_count = 0
            failed_cases = []
            
            progress_bar = st.progress(0)
            
            for i, (text, expected) in enumerate(test_cases):
                try:
                    result = st.session_state.nlp.parse(text)
                    
                    # Kiểm tra tên sự kiện
                    event_name_match = result['event_name'].lower().strip() == expected['event_name'].lower().strip()
                    
                    # Kiểm tra địa điểm
                    location_match = True
                    if expected.get('location'):
                        location_match = result.get('location', '').lower().find(expected['location'].lower()) >= 0
                    elif result.get('location') is None:
                        location_match = True
                    
                    # Kiểm tra reminder
                    reminder_match = result.get('reminder_minutes') == expected.get('reminder_minutes')
                    
                    if event_name_match and location_match and reminder_match:
                        success_count += 1
                    else:
                        failed_cases.append({
                            'index': i + 1,
                            'text': text,
                            'expected': expected,
                            'actual': result,
                            'event_name_match': event_name_match,
                            'location_match': location_match,
                            'reminder_match': reminder_match
                        })
                
                except Exception as e:
                    failed_cases.append({
                        'index': i + 1,
                        'text': text,
                        'error': str(e)
                    })
                
                progress_bar.progress((i + 1) / len(test_cases))
            
            # Hiển thị kết quả
            accuracy = (success_count / len(test_cases)) * 100
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Tổng số test", len(test_cases))
            
            with col2:
                st.metric("Thành công", success_count, delta=f"{success_count - (len(test_cases) - success_count)}")
            
            with col3:
                st.metric("Độ chính xác", f"{accuracy:.1f}%")
            
            if accuracy >= 90:
                st.success(f"🎉 Đạt yêu cầu! Độ chính xác: {accuracy:.1f}% (≥90%)")
            else:
                st.warning(f"⚠️ Chưa đạt yêu cầu. Độ chính xác: {accuracy:.1f}% (cần ≥90%)")
            
            # Hiển thị các case failed
            if failed_cases:
                st.subheader(f"❌ {len(failed_cases)} test cases thất bại:")
                
                for case in failed_cases:
                    with st.expander(f"Test {case['index']}: {case['text'][:50]}..."):
                        st.write(f"**Câu test:** {case['text']}")
                        
                        if 'error' in case:
                            st.error(f"**Lỗi:** {case['error']}")
                        else:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("**Expected:**")
                                st.json(case['expected'])
                            
                            with col2:
                                st.write("**Actual:**")
                                st.json(case['actual'])
                            
                            if not case.get('event_name_match'):
                                st.error("❌ Tên sự kiện không khớp")
                            if not case.get('location_match'):
                                st.error("❌ Địa điểm không khớp")
                            if not case.get('reminder_match'):
                                st.error("❌ Nhắc nhở không khớp")


def main():
    """Main function"""
    
    # Sidebar navigation
    st.sidebar.title("🧭 Điều hướng")
    
    page = st.sidebar.radio(
        "Chọn trang:",
        ["📅 Thêm sự kiện", "📆 Xem lịch", "⚙️ Xuất/Nhập", "🧪 Test NLP"]
    )
    
    st.sidebar.divider()
    
    # Thông tin hệ thống
    st.sidebar.subheader("ℹ️ Thông tin")
    
    total_events = len(st.session_state.db.get_all_events())
    st.sidebar.write(f"**Tổng số sự kiện:** {total_events}")
    
    reminder_status = st.session_state.reminder_system.get_status()
    if reminder_status['running']:
        st.sidebar.success("🔔 Hệ thống nhắc nhở: Đang chạy")
    else:
        st.sidebar.error("🔔 Hệ thống nhắc nhở: Dừng")
    
    st.sidebar.divider()
    st.sidebar.caption("© 2024 Calendar App with Vietnamese NLP")
    
    # Hiển thị trang được chọn
    if page == "📅 Thêm sự kiện":
        show_add_event_page()
    elif page == "📆 Xem lịch":
        show_calendar_page()
    elif page == "⚙️ Xuất/Nhập":
        show_settings_page()
    elif page == "🧪 Test NLP":
        show_test_nlp_page()


if __name__ == "__main__":
    main()

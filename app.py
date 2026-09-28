import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px

# -----------------------------------------------------------------------------
# CẤU HÌNH TRANG & CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Hệ Thống Quản Lý Khách Sạn",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .room-card {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: white;
        text-align: center;
        font-weight: bold;
    }
    .status-available { background-color: #2e7d32; }
    .status-occupied { background-color: #c62828; }
    .status-dirty { background-color: #f57f17; }
    .status-maintenance { background-color: #424242; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DỮ LIỆU MẪU & KHỞI TẠO STATE
# -----------------------------------------------------------------------------
def init_data():
    if "rooms" not in st.session_state:
        st.session_state.rooms = pd.DataFrame([
            {"room_number": "101", "type": "Đơn", "price": 500000, "status": "Trống"},
            {"room_number": "102", "type": "Đơn", "price": 500000, "status": "Có khách"},
            {"room_number": "103", "type": "Đôi", "price": 800000, "status": "Chưa dọn"},
            {"room_number": "104", "type": "VIP", "price": 1500000, "status": "Bảo trì"},
            {"room_number": "201", "type": "Đơn", "price": 500000, "status": "Trống"},
            {"room_number": "202", "type": "Đôi", "price": 800000, "status": "Có khách"},
            {"room_number": "203", "type": "Đôi", "price": 800000, "status": "Trống"},
            {"room_number": "204", "type": "VIP", "price": 1500000, "status": "Trống"},
        ])

    if "bookings" not in st.session_state:
        st.session_state.bookings = pd.DataFrame([
            {
                "booking_id": 1,
                "customer_name": "Nguyễn Văn A",
                "phone": "0901234567",
                "room_number": "102",
                "check_in": date(2026, 9, 27),
                "check_out": date(2026, 9, 29),
                "status": "Đang ở",
                "total_price": 1000000
            },
            {
                "booking_id": 2,
                "customer_name": "Trần Thị B",
                "phone": "0987654321",
                "room_number": "202",
                "check_in": date(2026, 9, 28),
                "check_out": date(2026, 9, 30),
                "status": "Đang ở",
                "total_price": 1600000
            }
        ])

init_data()

# -----------------------------------------------------------------------------
# THANH ĐIỀU HƯỚNG (SIDEBAR)
# -----------------------------------------------------------------------------
st.sidebar.title("🏨 QL Khách Sạn")
menu = st.sidebar.radio(
    "Danh mục quản lý",
    ["Sơ đồ phòng", "Đặt phòng & Check-in", "Check-out & Thanh toán", "Thống kê & Báo cáo"]
)

# -----------------------------------------------------------------------------
# 1. SƠ ĐỒ PHÒNG (DASHBOARD TRỰC QUAN)
# -----------------------------------------------------------------------------
if menu == "Sơ đồ phòng":
    st.title("📌 Sơ Đồ Trạng Thái Phòng")

    # Bảng thống kê nhanh
    c1, c2, c3, c4 = st.columns(4)
    total_rooms = len(st.session_state.rooms)
    available = len(st.session_state.rooms[st.session_state.rooms['status'] == 'Trống'])
    occupied = len(st.session_state.rooms[st.session_state.rooms['status'] == 'Có khách'])
    dirty = len(st.session_state.rooms[st.session_state.rooms['status'] == 'Chưa dọn'])

    c1.metric("Tổng số phòng", total_rooms)
    c2.metric("Phòng trống", available)
    c3.metric("Đang có khách", occupied)
    c4.metric("Cần dọn dẹp", dirty)

    st.markdown("---")

    # Bộ lọc trạng thái
    status_filter = st.multiselect(
        "Lọc theo trạng thái:",
        ["Trống", "Có khách", "Chưa dọn", "Bảo trì"],
        default=["Trống", "Có khách", "Chưa dọn", "Bảo trì"]
    )

    filtered_rooms = st.session_state.rooms[st.session_state.rooms['status'].isin(status_filter)]

    # Hiển thị sơ đồ lưới (Grid System)
    cols = st.columns(4)
    status_classes = {
        "Trống": "status-available",
        "Có khách": "status-occupied",
        "Chưa dọn": "status-dirty",
        "Bảo trì": "status-maintenance"
    }

    for idx, row in filtered_rooms.iterrows():
        col = cols[idx % 4]
        bg_class = status_classes.get(row['status'], "")
        with col:
            st.markdown(f"""
                <div class="room-card {bg_class}">
                    <h3>Phòng {row['room_number']}</h3>
                    <p>Loại: {row['type']}</p>
                    <p>Giá: {row['price']:,} VNĐ</p>
                    <p>Trạng thái: <b>{row['status']}</b></p>
                </div>
            """, unsafe_allow_html=True)
            
            # Nút đổi nhanh trạng thái phòng (vd: Dọn dẹp xong)
            if row['status'] == 'Chưa dọn':
                if st.button(f"Đã dọn xong P.{row['room_number']}", key=f"clean_{row['room_number']}"):
                    st.session_state.rooms.loc[st.session_state.rooms['room_number'] == row['room_number'], 'status'] = 'Trống'
                    st.rerun()

# -----------------------------------------------------------------------------
# 2. ĐẶT PHÒNG & CHECK-IN
# -----------------------------------------------------------------------------
elif menu == "Đặt phòng & Check-in":
    st.title("📝 Đặt Phòng / Check-in Mới")

    available_rooms = st.session_state.rooms[st.session_state.rooms['status'] == 'Trống']['room_number'].tolist()

    if not available_rooms:
        st.warning("Hiện tại không có phòng nào trống!")
    else:
        with st.form("checkin_form"):
            col1, col2 = st.columns(2)

            with col1:
                customer_name = st.text_input("Họ và tên khách hàng *")
                phone = st.text_input("Số điện thoại *")
                selected_room = st.selectbox("Chọn phòng trống *", available_rooms)

            with col2:
                check_in = st.date_input("Ngày nhận phòng", value=date.today())
                check_out = st.date_input("Ngày trả phòng (dự kiến)", value=date.today())

            submitted = st.form_submit_button("Xác nhận Check-in")

            if submitted:
                if not customer_name or not phone:
                    st.error("Vui lòng điền đầy đủ thông tin khách hàng.")
                elif check_out <= check_in:
                    st.error("Ngày trả phòng phải sau ngày nhận phòng.")
                else:
                    # Tính tổng tiền dự kiến
                    room_price = st.session_state.rooms.loc[
                        st.session_state.rooms['room_number'] == selected_room, 'price'
                    ].values[0]
                    days = (check_out - check_in).days
                    total = days * room_price

                    # Cập nhật thông tin đặt phòng mới
                    new_id = len(st.session_state.bookings) + 1
                    new_booking = pd.DataFrame([{
                        "booking_id": new_id,
                        "customer_name": customer_name,
                        "phone": phone,
                        "room_number": selected_room,
                        "check_in": check_in,
                        "check_out": check_out,
                        "status": "Đang ở",
                        "total_price": total
                    }])
                    st.session_state.bookings = pd.concat([st.session_state.bookings, new_booking], ignore_index=True)

                    # Cập nhật trạng thái phòng sang 'Có khách'
                    st.session_state.rooms.loc[
                        st.session_state.rooms['room_number'] == selected_room, 'status'
                    ] = 'Có khách'

                    st.success(f"Check-in thành công cho phòng {selected_room}!")
                    st.rerun()

# -----------------------------------------------------------------------------
# 3. CHECK-OUT & THANH TOÁN
# -----------------------------------------------------------------------------
elif menu == "Check-out & Thanh toán":
    st.title("💳 Check-out & Lập Hóa Đơn")

    active_bookings = st.session_state.bookings[st.session_state.bookings['status'] == 'Đang ở']

    if active_bookings.empty:
        st.info("Hiện không có phòng nào đang sử dụng.")
    else:
        booking_options = {
            f"Phòng {row['room_number']} - {row['customer_name']}": row['booking_id']
            for _, row in active_bookings.iterrows()
        }
        
        selected_option = st.selectbox("Chọn lượt ở cần thanh toán:", list(booking_options.keys()))
        selected_id = booking_options[selected_option]

        booking_detail = active_bookings[active_bookings['booking_id'] == selected_id].iloc[0]

        st.markdown("### Chi Tiết Hóa Đơn")
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Khách hàng:** {booking_detail['customer_name']}")
            st.write(f"**Số điện thoại:** {booking_detail['phone']}")
            st.write(f"**Phòng:** {booking_detail['room_number']}")
        with c2:
            st.write(f"**Ngày nhận:** {booking_detail['check_in']}")
            st.write(f"**Ngày trả:** {booking_detail['check_out']}")
            
            days = (booking_detail['check_out'] - booking_detail['check_in']).days
            days = max(days, 1) # Tối thiểu 1 ngày
            st.write(f"**Số đêm lưu trú:** {days} đêm")

        st.markdown(f"### 💰 Tổng tiền thanh toán: `{booking_detail['total_price']:,} VNĐ`")

        if st.button("Xác nhận Check-out & Thanh toán"):
            # Cập nhật trạng thái lượt đặt phòng
            st.session_state.bookings.loc[
                st.session_state.bookings['booking_id'] == selected_id, 'status'
            ] = 'Đã thanh toán'

            # Chuyển trạng thái phòng sang 'Chưa dọn'
            st.session_state.rooms.loc[
                st.session_state.rooms['room_number'] == booking_detail['room_number'], 'status'
            ] = 'Chưa dọn'

            st.balloons()
            st.success("Thanh toán hoàn tất! Phòng đã chuyển sang trạng thái 'Chưa dọn'.")
            st.rerun()

# -----------------------------------------------------------------------------
# 4. THỐNG KÊ & BÁO CÁO
# -----------------------------------------------------------------------------
elif menu == "Thống kê & Báo cáo":
    st.title("📊 Báo Cáo Doanh Thu & Hiệu Suất")

    completed_bookings = st.session_state.bookings[st.session_state.bookings['status'] == 'Đã thanh toán']
    total_revenue = completed_bookings['total_price'].sum()

    m1, m2 = st.columns(2)
    m1.metric("Tổng doanh thu thực tế", f"{total_revenue:,} VNĐ")
    m2.metric("Lượt phòng đã phục vụ", len(completed_bookings))

    st.markdown("---")

    if not st.session_state.bookings.empty:
        st.subheader("Biểu đồ doanh thu theo phòng")
        revenue_by_room = st.session_state.bookings.groupby('room_number')['total_price'].sum().reset_index()
        fig = px.bar(
            revenue_by_room,
            x='room_number',
            y='total_price',
            labels={'room_number': 'Số phòng', 'total_price': 'Doanh thu (VNĐ)'},
            color='total_price',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Lịch sử giao dịch")
        st.dataframe(st.session_state.bookings, use_container_width=True)

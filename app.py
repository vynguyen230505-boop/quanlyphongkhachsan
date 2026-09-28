import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_page_title="Hệ Thống Quản Lý Khách Sạn",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Khởi tạo dữ liệu mẫu trong Session State (chạy khi ứng dụng khởi chạy lần đầu)
# -----------------------------------------------------------------------------
if "rooms" not in st.session_state:
    st.session_state.rooms = pd.DataFrame(
        [
            {
                "Số Phòng": "101",
                "Loại Phòng": "Đơn",
                "Giá (VNĐ/đêm)": 500000,
                "Trạng Thái": "Trống",
            },
            {
                "Số Phòng": "102",
                "Loại Phòng": "Đơn",
                "Giá (VNĐ/đêm)": 500000,
                "Trạng Thái": "Đang Có Khách",
            },
            {
                "Số Phòng": "103",
                "Loại Phòng": "Đôi",
                "Giá (VNĐ/đêm)": 800000,
                "Trạng Thái": "Đang Đang Dọn",
            },
            {
                "Số Phòng": "201",
                "Loại Phòng": "VIP",
                "Giá (VNĐ/đêm)": 1500000,
                "Trạng Thái": "Trống",
            },
            {
                "Số Phòng": "202",
                "Loại Phòng": "VIP",
                "Giá (VNĐ/đêm)": 1500000,
                "Trạng Thái": "Đang Có Khách",
            },
            {
                "Số Phòng": "301",
                "Loại Phòng": "Gia Đình",
                "Giá (VNĐ/đêm)": 1200000,
                "Trạng Thái": "Trống",
            },
        ]
    )

if "bookings" not in st.session_state:
    st.session_state.bookings = pd.DataFrame(
        [
            {
                "Mã Đặt Phòng": "BK001",
                "Tên Khách Hàng": "Nguyễn Văn A",
                "Số Điện Thoại": "0901234567",
                "Số Phòng": "102",
                "Ngày Nhận": datetime.date.today() - datetime.timedelta(days=1),
                "Ngày Trả": datetime.date.today() + datetime.timedelta(days=1),
                "Tổng Tiền (VNĐ)": 1000000,
                "Trạng Thái Thanh Toán": "Chưa Thanh Toán",
            },
            {
                "Mã Đặt Phòng": "BK002",
                "Tên Khách Hàng": "Trần Thị B",
                "Số Điện Thoại": "0987654321",
                "Số Phòng": "202",
                "Ngày Nhận": datetime.date.today(),
                "Ngày Trả": datetime.date.today() + datetime.timedelta(days=2),
                "Tổng Tiền (VNĐ)": 3000000,
                "Trạng Thái Thanh Toán": "Đã Thanh Toán",
            },
        ]
    )

# -----------------------------------------------------------------------------
# Thanh Menu Bên Tái (Sidebar Navigation)
# -----------------------------------------------------------------------------
st.sidebar.title("🏨 QL Khách Sạn")
menu = st.sidebar.radio(
    "Danh mục quản lý",
    [
        "📊 Tổng Quan & Sơ Đồ",
        "📝 Đặt Phòng Mới",
        "🛏️ Quản Lý Phòng",
        "📋 Danh Sách Đặt Phòng",
        "💰 Doanh Thu & Báo Cáo",
    ],
)

# -----------------------------------------------------------------------------
# Trang 1: Tổng Quan & Sơ Đồ Phòng
# -----------------------------------------------------------------------------
if menu == "📊 Tổng Quan & Sơ Đồ":
    st.title("📊 Tổng Quan Trang Trạng Thái Khách Sạn")

    df_rooms = st.session_state.rooms

    # Các chỉ số Metric
    total_rooms = len(df_rooms)
    occupied_rooms = len(df_rooms[df_rooms["Trạng Thái"] == "Đang Có Khách"])
    available_rooms = len(df_rooms[df_rooms["Trạng Thái"] == "Trống"])
    cleaning_rooms = len(df_rooms[df_rooms["Trạng Thái"] == "Đang Đang Dọn"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng Số Phòng", total_rooms)
    col2.metric("Phòng Trống", available_rooms)
    col3.metric("Đang Có Khách", occupied_rooms)
    col4.metric("Đang Dọn Dẹp", cleaning_rooms)

    st.markdown("---")
    st.subheader("🗺️ Sơ Đồ Trạng Thái Phòng")

    # Hiển thị dạng thẻ (Cards) trực quan
    cols = st.columns(3)
    status_colors = {
        "Trống": "#28a745",
        "Đang Có Khách": "#dc3545",
        "Đang Đang Dọn": "#ffc107",
    }

    for idx, row in df_rooms.iterrows():
        col = cols[idx % 3]
        color = status_colors.get(row["Trạng Thái"], "#6c757d")
        with col:
            st.markdown(
                f"""
                <div style="
                    border: 2px solid {color};
                    border-radius: 10px;
                    padding: 15px;
                    margin-bottom: 15px;
                    background-color: rgba(255,255,255,0.05);
                ">
                    <h3 style="margin: 0; color: {color};">Phòng {row['Số Phòng']}</h3>
                    <p style="margin: 5px 0;"><b>Loại:</b> {row['Loại Phòng']}</p>
                    <p style="margin: 5px 0;"><b>Giá:</b> {row['Giá (VNĐ/đêm)']:,.0f} VNĐ</p>
                    <p style="margin: 5px 0;"><b>Trạng thái:</b> <span style="color:{color}; font-weight:bold;">{row['Trạng Thái']}</span></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# -----------------------------------------------------------------------------
# Trang 2: Đặt Phòng Mới
# -----------------------------------------------------------------------------
elif menu == "📝 Đặt Phòng Mới":
    st.title("📝 Đặt Phòng Cho Khách")

    df_rooms = st.session_state.rooms
    available_room_list = df_rooms[df_rooms["Trạng Thái"] == "Trống"][
        "Số Phòng"
    ].tolist()

    if not available_room_list:
        st.warning("⚠️ Hiện tại không có phòng nào trống!")
    else:
        with st.form("booking_form", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                guest_name = st.text_input("Họ và Tên Khách Hàng*")
                phone = st.text_input("Số Điện Thoại*")
                selected_room = st.selectbox(
                    "Chọn Phòng Trống*", available_room_list
                )

            with col2:
                checkin_date = st.date_input(
                    "Ngày Nhận Phòng", min_value=datetime.date.today()
                )
                checkout_date = st.date_input(
                    "Ngày Trả Phòng",
                    min_value=checkin_date + datetime.timedelta(days=1),
                )
                payment_status = st.selectbox(
                    "Trạng Thái Thanh Toán",
                    ["Chưa Thanh Toán", "Đã Thanh Toán"],
                )

            # Tính toán tổng tiền
            room_price = df_rooms[df_rooms["Số Phòng"] == selected_room][
                "Giá (VNĐ/đêm)"
            ].values[0]
            nights = (checkout_date - checkin_date).days
            total_price = nights * room_price

            st.markdown(
                f"**Số đêm ở:** {nights} đêm | **Tổng tiền tạm tính:** `{total_price:,.0f} VNĐ`"
            )

            submitted = st.form_submit_button("Xác Nhận Đặt Phòng")

            if submitted:
                if not guest_name or not phone:
                    st.error("Vui lòng điền đầy đủ thông tin bắt buộc (*)")
                else:
                    new_id = f"BK{len(st.session_state.bookings) + 1:03d}"
                    new_booking = {
                        "Mã Đặt Phòng": new_id,
                        "Tên Khách Hàng": guest_name,
                        "Số Điện Thoại": phone,
                        "Số Phòng": selected_room,
                        "Ngày Nhận": checkin_date,
                        "Ngày Trả": checkout_date,
                        "Tổng Tiền (VNĐ)": total_price,
                        "Trạng Thái Thanh Toán": payment_status,
                    }

                    # Thêm đơn đặt phòng
                    st.session_state.bookings = pd.concat(
                        [
                            st.session_state.bookings,
                            pd.DataFrame([new_booking]),
                        ],
                        ignore_index=True,
                    )

                    # Cập nhật trạng thái phòng thành "Đang Có Khách"
                    st.session_state.rooms.loc[
                        st.session_state.rooms["Số Phòng"] == selected_room,
                        "Trạng Thái",
                    ] = "Đang Có Khách"

                    st.success(
                        f"🎉 Đặt phòng thành công cho khách {guest_name}! Mã đặt: **{new_id}**"
                    )
                    st.rerun()

# -----------------------------------------------------------------------------
# Trang 3: Quản Lý Phòng
# -----------------------------------------------------------------------------
elif menu == "🛏️ Quản Lý Phòng":
    st.title("🛏️ Quản Lý Danh Sách & Trạng Thái Phòng")

    tab1, tab2 = st.tabs(["Cập Nhật Trạng Thái", "Thêm Phòng Mới"])

    with tab1:
        st.subheader("Thay Đổi Trạng Thái Phòng")
        df_rooms = st.session_state.rooms

        edited_df = st.data_editor(
            df_rooms,
            column_config={
                "Trạng Thái": st.column_config.SelectboxColumn(
                    "Trạng Thái",
                    options=["Trống", "Đang Có Khách", "Đang Đang Dọn"],
                    required=True,
                ),
                "Giá (VNĐ/đêm)": st.column_config.NumberColumn(
                    "Giá (VNĐ/đêm)", format="%d"
                ),
            },
            num_rows="dynamic",
            use_container_width=True,
        )

        if st.button("Lưu Thay Đổi Phòng"):
            st.session_state.rooms = edited_df
            st.success("Đã cập nhật danh sách phòng thành công!")
            st.rerun()

    with tab2:
        st.subheader("Thêm Phòng Mới")
        with st.form("add_room_form"):
            room_no = st.text_input("Số Phòng (Ví dụ: 302)")
            room_type = st.selectbox(
                "Loại Phòng", ["Đơn", "Đôi", "VIP", "Gia Đình"]
            )
            room_price = st.number_input(
                "Giá Phòng (VNĐ/đêm)", min_value=100000, step=50000, value=500000
            )

            if st.form_submit_button("Thêm Phòng"):
                if room_no in st.session_state.rooms["Số Phòng"].values:
                    st.error("Số phòng này đã tồn tại!")
                elif not room_no:
                    st.error("Vui lòng nhập số phòng!")
                else:
                    new_room = {
                        "Số Phòng": room_no,
                        "Loại Phòng": room_type,
                        "Giá (VNĐ/đêm)": room_price,
                        "Trạng Thái": "Trống",
                    }
                    st.session_state.rooms = pd.concat(
                        [st.session_state.rooms, pd.DataFrame([new_room])],
                        ignore_index=True,
                    )
                    st.success(f"Đã thêm phòng {room_no} thành công!")
                    st.rerun()

# -----------------------------------------------------------------------------
# Trang 4: Danh Sách Đặt Phòng & Check-out
# -----------------------------------------------------------------------------
elif menu == "📋 Danh Sách Đặt Phòng":
    st.title("📋 Quản Lý Đặt Phòng & Check-out")

    df_bookings = st.session_state.bookings

    if df_bookings.empty:
        st.info("Chưa có đơn đặt phòng nào.")
    else:
        st.dataframe(df_bookings, use_container_width=True)

        st.markdown("---")
        st.subheader("🚪 Xử Lý Check-out / Trả Phòng")

        active_bookings = df_bookings[
            df_bookings["Số Phòng"].isin(
                st.session_state.rooms[
                    st.session_state.rooms["Trạng Thái"] == "Đang Có Khách"
                ]["Số Phòng"]
            )
        ]

        if active_bookings.empty:
            st.info("Không có phòng nào đang có khách cần Check-out.")
        else:
            selected_bk = st.selectbox(
                "Chọn Mã Đặt Phòng Cần Check-out",
                active_bookings["Mã Đặt Phòng"].tolist(),
            )
            bk_info = active_bookings[
                active_bookings["Mã Đặt Phòng"] == selected_bk
            ].iloc[0]

            st.write(
                f"**Khách hàng:** {bk_info['Tên Khách Hàng']} | **Phòng:** {bk_info['Số Phòng']} | **Tổng tiền:** {bk_info['Tổng Tiền (VNĐ)']:,.0f} VNĐ"
            )

            col_btn1, col_btn2 = st.columns(2)

            if col_btn1.button("✅ Trả Phòng (Chuyển sang Đang Dọn Dẹp)"):
                room_num = bk_info["Số Phòng"]
                st.session_state.rooms.loc[
                    st.session_state.rooms["Số Phòng"] == room_num,
                    "Trạng Thái",
                ] = "Đang Đang Dọn"
                st.session_state.bookings.loc[
                    st.session_state.bookings["Mã Đặt Phòng"] == selected_bk,
                    "Trạng Thái Thanh Toán",
                ] = "Đã Thanh Toán"
                st.success(
                    f"Đã check-out phòng {room_num}. Phòng chuyển sang trạng thái 'Đang Đang Dọn'!"
                )
                st.rerun()

# -----------------------------------------------------------------------------
# Trang 5: Doanh Thu & Báo Cáo
# -----------------------------------------------------------------------------
elif menu == "💰 Doanh Thu & Báo Cáo":
    st.title("💰 Báo Cáo Doanh Thu & Thống Kê")

    df_bookings = st.session_state.bookings

    if df_bookings.empty:
        st.info("Chưa có dữ liệu thống kê.")
    else:
        total_revenue = df_bookings[
            df_bookings["Trạng Thái Thanh Toán"] == "Đã Thanh Toán"
        ]["Tổng Tiền (VNĐ)"].sum()
        pending_revenue = df_bookings[
            df_bookings["Trạng Thái Thanh Toán"] == "Chưa Thanh Toán"
        ]["Tổng Tiền (VNĐ)"].sum()

        col1, col2 = st.columns(2)
        col1.metric("Doanh Thu Thực Thu", f"{total_revenue:,.0f} VNĐ")
        col2.metric("Doanh Thu Chờ Thanh Toán", f"{pending_revenue:,.0f} VNĐ")

        st.markdown("---")
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.subheader("Phân Bố Loại Phòng")
            fig_room_type = px.pie(
                st.session_state.rooms,
                names="Loại Phòng",
                title="Tỷ lệ các loại phòng trong khách sạn",
                hole=0.4,
            )
            st.plotly_chart(fig_room_type, use_container_width=True)

        with col_chart2:
            st.subheader("Tỷ Lệ Trạng Thái Phòng")
            fig_status = px.bar(
                st.session_state.rooms["Trạng Thái"].value_counts().reset_index(),
                x="Trạng Thái",
                y="count",
                labels={"count": "Số lượng", "Trạng Thái": "Trạng Thái"},
                color="Trạng Thái",
                title="Số lượng phòng theo trạng thái",
            )
            st.plotly_chart(fig_status, use_container_width=True)

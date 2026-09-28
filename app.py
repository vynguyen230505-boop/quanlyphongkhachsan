customer_name,
                        phone,
                        check_in.strftime("%d/%m/%Y"),
                        check_out.strftime("%d/%m/%Y"),
                        note
                    )

                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

# =========================================================
# CÀI ĐẶT
# =========================================================

elif page == "⚙️ Cài đặt":

    st.title("⚙️ Cài đặt")

    st.subheader("🗄️ Cơ sở dữ liệu")

    st.write(
        f"Database hiện tại: `{DB_FILE}`"
    )

    st.write(
        f"Tổng số phòng: **{len(df)}**"
    )

    st.divider()

    st.subheader("📊 Thống kê")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Theo loại phòng**")

        type_stats = (
            df["room_type"]
            .value_counts()
            .reset_index()
        )

        type_stats.columns = [
            "Loại phòng",
            "Số lượng"
        ]

        st.dataframe(
            type_stats,
            use_container_width=True,
            hide_index=True
        )

    with col2:

        st.write("**Theo trạng thái**")

        status_stats = (
            df["status"]
            .value_counts()
            .reset_index()
        )

        status_stats.columns = [
            "Trạng thái",
            "Số lượng"
        ]

        st.dataframe(
            status_stats,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader("🔄 Làm mới dữ liệu")

    if st.button(
        "🔄 Tải lại dữ liệu",
        use_container_width=True
    ):
        st.rerun()

    st.divider()

    st.caption(
        "Hotel Room Manager — Streamlit + SQLite"
    )

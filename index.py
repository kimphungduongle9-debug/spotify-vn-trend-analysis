import streamlit as st
from app import changes, overview, potential, ranking, model_results, data_view
from components.filters import render_filters
from components.layout import (
    load_css,
    render_footer,
    render_hero,
)
from components.metric_cards import render_metric_cards
from data_loader import load_project_data
from components.navigation import render_top_navigation

# =========================================================
# 1. CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Spotify Việt Nam Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. NẠP CSS
# =========================================================
load_css()


# =========================================================
# 3. ĐỌC DỮ LIỆU
# =========================================================
try:
    project_data = load_project_data()
except Exception as error:
    st.error(f"Không thể đọc dữ liệu: {error}")
    st.stop()


main_data = project_data["cleaned"]


# =========================================================
# 4. MENU SIDEBAR
# =========================================================
selected_page = render_top_navigation()

# =========================================================
# 5. BỘ LỌC DÙNG CHUNG
# =========================================================
filtered_data, filter_state = render_filters(main_data)

# =========================================================
# 6. ĐIỀU HƯỚNG TRANG
# =========================================================
if selected_page == "🏠 Trang chủ":
    render_hero()

    render_metric_cards(filtered_data)

    st.write("")

    st.subheader("Nội dung phân tích")

    st.markdown("""
        Ứng dụng hỗ trợ trình bày kết quả phân tích
        bảng xếp hạng Spotify Top 200 Việt Nam trong
        12 tuần, bao gồm:

        - Xu hướng tổng lượt nghe theo tuần.
        - Top bài hát và nghệ sĩ nổi bật.
        - Biến động tăng hoặc giảm thứ hạng.
        - Nhận diện bài hát tiềm năng.
        - Đánh giá kết quả mô hình dự đoán lượt nghe.
        """)

    st.info(
        "Chọn mục **Tổng quan** trong thanh bên trái " "để xem các biểu đồ phân tích."
    )

if selected_page == "Trang chủ":
    render_hero()
    render_metric_cards(filtered_data)

elif selected_page == "Tổng quan":
    overview.render(filtered_data)

elif selected_page == "Bảng xếp hạng":
    ranking.render(filtered_data)

elif selected_page == "Biến động":
    changes.render(filtered_data)

elif selected_page == "Bài hát tiềm năng":
    potential.render(
        potential_data=project_data["potential"],
        final_potential_data=project_data["final_potential"],
    )

elif selected_page == "Kết quả mô hình":
    model_results.render(
        metrics_data=project_data["metrics"],
        linear_predictions=project_data["linear_predictions"],
        rf_predictions=project_data["rf_predictions"],
        train_data=project_data["train"],
        test_data=project_data["test"],
    )

elif selected_page == "Dữ liệu":
    data_view.render(project_data)
# =========================================================
# 7. CHÂN TRANG
# =========================================================
render_footer()

import streamlit as st

NAVIGATION_OPTIONS = [
    "Trang chủ",
    "Tổng quan",
    "Bảng xếp hạng",
    "Biến động",
    "Bài hát tiềm năng",
    "Kết quả mô hình",
    "Dữ liệu",
]


def select_page(page_name: str) -> None:
    """Lưu trang đang chọn."""

    st.session_state["selected_page"] = page_name


def render_top_navigation() -> str:
    """Hiển thị thanh điều hướng giống website."""

    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "Trang chủ"

    current_page = st.session_state["selected_page"]

    with st.container(
        key="top_navigation",
        border=False,
    ):
        columns = st.columns(
            [
                2.2,
                0.9,
                0.9,
                1.2,
                0.9,
                1.5,
                1.4,
                0.8,
            ],
            gap="small",
            vertical_alignment="center",
        )

        with columns[0]:
            st.html("""
                <div class="top-nav-brand">
                    <strong>Spotify VN Analytics</strong>
                    <span>Phân tích dữ liệu âm nhạc</span>
                </div>
                """)

        for index, page_name in enumerate(NAVIGATION_OPTIONS):
            with columns[index + 1]:
                st.button(
                    page_name,
                    key=f"navigation_button_{index}",
                    type=("primary" if current_page == page_name else "secondary"),
                    width="stretch",
                    on_click=select_page,
                    args=(page_name,),
                )

    return st.session_state["selected_page"]

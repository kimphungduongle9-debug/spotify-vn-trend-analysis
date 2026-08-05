from html import escape
from pathlib import Path

import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parents[1]
STYLE_PATH = PROJECT_DIR / "style.css"


def load_css() -> None:
    """Nạp file CSS dùng chung cho toàn bộ ứng dụng."""

    if not STYLE_PATH.exists():
        st.error(f"Không tìm thấy file CSS: {STYLE_PATH}")
        st.stop()

    css_content = STYLE_PATH.read_text(encoding="utf-8")

    st.html(f"<style>{css_content}</style>")


def render_sidebar_brand() -> None:
    """Hiển thị thương hiệu phía trên sidebar."""

    st.html("""
        <div class="sidebar-brand">
            <div class="sidebar-icon">🎧</div>

            <div>
                <h3>Spotify VN Analytics</h3>

                <p>
                    Dashboard phân tích
                    Spotify Top 200 Việt Nam
                </p>
            </div>
        </div>
        """)


def render_hero() -> None:
    """Hiển thị banner chính tại trang chủ."""

    st.html("""
        <div class="hero">
            <div class="hero-content">
                <span class="hero-badge">
                    PHÂN TÍCH DỮ LIỆU & MACHINE LEARNING
                </span>

                <h1>
                    Phân tích Spotify Top 200 Việt Nam
                </h1>

                <p>
                    Phân tích xu hướng bảng xếp hạng,
                    đánh giá mô hình dự đoán lượt nghe
                    và nhận diện bài hát tiềm năng.
                </p>
            </div>

            <div class="hero-decoration">♫</div>
        </div>
        """)


def render_page_header(
    title: str,
    description: str,
    icon: str = "",
) -> None:
    """Hiển thị tiêu đề trang, không dùng icon."""

    safe_title = escape(title)
    safe_description = escape(description)

    st.html(f"""
        <div class="page-header-simple">
            <h1>{safe_title}</h1>
            <p>{safe_description}</p>
        </div>
        """)


def render_info_box(
    message: str,
) -> None:
    """Hiển thị khung ghi chú."""

    safe_message = escape(message)

    st.html(f"""
        <div class="info-box">
            {safe_message}
        </div>
        """)


def render_footer() -> None:
    """Hiển thị chân trang dùng chung."""

    st.html("""
        <div class="footer">
            <p>
                Phân tích dữ liệu bảng xếp hạng
                Spotify Việt Nam nhằm dự đoán lượt nghe
                và nhận diện bài hát tiềm năng.
            </p>
        </div>
        """)

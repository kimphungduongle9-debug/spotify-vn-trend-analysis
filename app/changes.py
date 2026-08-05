import pandas as pd
import plotly.express as px
import streamlit as st

from components.layout import (
    render_info_box,
    render_page_header,
)
from helpers import (
    PLOTLY_CONFIG,
    format_date,
    style_chart,
)


def render(data: pd.DataFrame) -> None:
    """Hiển thị bài tăng hạng, tụt hạng và bài mới."""

    render_page_header(
        title="Biến động bảng xếp hạng",
        description=(
            "Phân tích các bài hát tăng hạng, "
            "tụt hạng và mới xuất hiện theo từng tuần."
        ),
        icon="📈",
    )

    if data.empty:
        st.warning("Không có dữ liệu phù hợp với bộ lọc hiện tại.")
        return

    available_weeks = sorted(
        data["chart_week"].dropna().unique(),
        reverse=True,
    )

    if not available_weeks:
        st.warning("Không tìm thấy dữ liệu tuần.")
        return

    selected_week = st.selectbox(
        "Chọn tuần cần phân tích",
        options=available_weeks,
        format_func=format_date,
        key="changes_selected_week",
    )

    week_data = data[data["chart_week"] == pd.Timestamp(selected_week)].copy()

    week_data["rank_change"] = pd.to_numeric(
        week_data["rank_change"],
        errors="coerce",
    ).fillna(0)

    render_info_box(
        "Đang phân tích biến động tại tuần "
        f"{format_date(selected_week)}. "
        "Giá trị dương là tăng hạng, "
        "giá trị âm là tụt hạng."
    )

    rising_songs = week_data[week_data["rank_change"] > 0].copy()

    falling_songs = week_data[week_data["rank_change"] < 0].copy()

    new_entry_values = week_data["is_new_entry"].astype(str).str.strip().str.lower()

    new_songs = week_data[new_entry_values.isin(["true", "1", "yes"])].copy()

    metric_1, metric_2, metric_3 = st.columns(3)

    metric_1.metric(
        "Bài tăng hạng",
        f"{len(rising_songs):,}",
    )

    metric_2.metric(
        "Bài tụt hạng",
        f"{len(falling_songs):,}",
    )

    metric_3.metric(
        "Bài mới/quay lại",
        f"{len(new_songs):,}",
    )

    st.write("")

    rise_column, fall_column = st.columns(2)

    # =====================================================
    # BÀI TĂNG HẠNG
    # =====================================================
    with rise_column:
        top_risers = rising_songs.nlargest(
            10,
            "rank_change",
        ).sort_values("rank_change")

        if top_risers.empty:
            st.info("Không có bài hát tăng hạng " "trong tuần đã chọn.")
        else:
            rising_figure = px.bar(
                top_risers,
                x="rank_change",
                y="track_name",
                orientation="h",
                title="Top 10 bài tăng hạng mạnh",
                color="rank_change",
                color_continuous_scale=[
                    [0, "#DDD6FE"],
                    [1, "#7C3AED"],
                ],
                hover_data={
                    "artist_names": True,
                    "rank": True,
                    "streams": ":,.0f",
                    "rank_change": True,
                },
            )

            rising_figure.update_coloraxes(showscale=False)

            rising_figure.update_xaxes(title="Số hạng tăng")

            rising_figure.update_yaxes(title="")

            st.plotly_chart(
                style_chart(
                    rising_figure,
                    height=510,
                ),
                width="stretch",
                config=PLOTLY_CONFIG,
            )

    # =====================================================
    # BÀI TỤT HẠNG
    # =====================================================
    with fall_column:
        top_fallers = falling_songs.nsmallest(
            10,
            "rank_change",
        ).copy()

        top_fallers["Số hạng tụt"] = top_fallers["rank_change"].abs()

        top_fallers = top_fallers.sort_values("Số hạng tụt")

        if top_fallers.empty:
            st.info("Không có bài hát tụt hạng " "trong tuần đã chọn.")
        else:
            falling_figure = px.bar(
                top_fallers,
                x="Số hạng tụt",
                y="track_name",
                orientation="h",
                title="Top 10 bài tụt hạng mạnh",
                color="Số hạng tụt",
                color_continuous_scale=[
                    [0, "#FCE7F3"],
                    [1, "#DB2777"],
                ],
                hover_data={
                    "artist_names": True,
                    "rank": True,
                    "streams": ":,.0f",
                    "Số hạng tụt": True,
                },
            )

            falling_figure.update_coloraxes(showscale=False)

            falling_figure.update_xaxes(title="Số hạng tụt")

            falling_figure.update_yaxes(title="")

            st.plotly_chart(
                style_chart(
                    falling_figure,
                    height=510,
                ),
                width="stretch",
                config=PLOTLY_CONFIG,
            )

    # =====================================================
    # BẢNG BÀI MỚI HOẶC QUAY LẠI
    # =====================================================
    st.subheader("Bài mới hoặc quay lại bảng xếp hạng")

    if new_songs.empty:
        st.info("Không có bài mới hoặc quay lại " "trong tuần đã chọn.")
    else:
        new_song_table = (
            new_songs[
                [
                    "rank",
                    "track_name",
                    "artist_names",
                    "genre",
                    "streams",
                    "weeks_on_chart",
                ]
            ]
            .sort_values("rank")
            .rename(
                columns={
                    "rank": "Hạng",
                    "track_name": "Bài hát",
                    "artist_names": "Nghệ sĩ",
                    "genre": "Thể loại",
                    "streams": "Lượt nghe",
                    "weeks_on_chart": ("Số tuần trên BXH"),
                }
            )
        )

        st.dataframe(
            new_song_table,
            width="stretch",
            hide_index=True,
        )

import pandas as pd
import streamlit as st

from components.layout import render_page_header
from helpers import format_date


def render(data: pd.DataFrame) -> None:
    """Hiển thị bảng xếp hạng Spotify theo từng tuần."""

    render_page_header(
        title="Bảng xếp hạng",
        description=(
            "Theo dõi thứ hạng, lượt nghe và biến động "
            "của các bài hát trong từng tuần."
        ),
        icon="🏆",
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

    week_column, amount_column = st.columns([2, 1])

    with week_column:
        selected_week = st.selectbox(
            "Chọn tuần bảng xếp hạng",
            options=available_weeks,
            format_func=format_date,
            key="ranking_selected_week",
        )

    with amount_column:
        top_n = st.selectbox(
            "Số bài hiển thị",
            options=[10, 20, 50, 100, 200],
            index=1,
            key="ranking_top_n",
        )

    ranking_data = (
        data[data["chart_week"] == pd.Timestamp(selected_week)]
        .sort_values("rank")
        .head(top_n)
        .copy()
    )

    if ranking_data.empty:
        st.info("Không có bài hát phù hợp trong tuần đã chọn.")
        return

    top_song = ranking_data.iloc[0]

    metric_1, metric_2, metric_3 = st.columns(3)

    metric_1.metric(
        "Bài hát hạng 1",
        top_song["track_name"],
    )

    metric_2.metric(
        "Nghệ sĩ",
        top_song["artist_names"],
    )

    metric_3.metric(
        "Lượt nghe hạng 1",
        f"{top_song['streams']:,.0f}",
    )

    st.write("")

    display_columns = [
        "rank",
        "track_name",
        "artist_names",
        "genre",
        "streams",
        "peak_rank",
        "previous_rank",
        "rank_change",
        "weeks_on_chart",
        "is_new_entry",
    ]

    display_columns = [
        column for column in display_columns if column in ranking_data.columns
    ]

    ranking_table = ranking_data[display_columns].rename(
        columns={
            "rank": "Hạng",
            "track_name": "Bài hát",
            "artist_names": "Nghệ sĩ",
            "genre": "Thể loại",
            "streams": "Lượt nghe",
            "peak_rank": "Hạng cao nhất",
            "previous_rank": "Hạng tuần trước",
            "rank_change": "Thay đổi hạng",
            "weeks_on_chart": "Số tuần trên BXH",
            "is_new_entry": "Mới/quay lại",
        }
    )

    st.dataframe(
        ranking_table,
        width="stretch",
        hide_index=True,
        column_config={
            "Hạng": st.column_config.NumberColumn(
                format="%d",
            ),
            "Lượt nghe": st.column_config.NumberColumn(
                format="%d",
            ),
            "Hạng cao nhất": st.column_config.NumberColumn(
                format="%d",
            ),
            "Hạng tuần trước": st.column_config.NumberColumn(
                format="%d",
            ),
            "Thay đổi hạng": st.column_config.NumberColumn(
                format="%+d",
            ),
            "Số tuần trên BXH": st.column_config.NumberColumn(
                format="%d",
            ),
            "Mới/quay lại": st.column_config.CheckboxColumn(),
        },
    )

    csv_data = ranking_table.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Tải bảng xếp hạng CSV",
        data=csv_data,
        file_name=(
            "spotify_ranking_"
            + pd.Timestamp(selected_week).strftime("%Y-%m-%d")
            + ".csv"
        ),
        mime="text/csv",
    )

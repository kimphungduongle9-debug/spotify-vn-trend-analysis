import pandas as pd
import streamlit as st

from helpers import format_number


def render_metric_cards(
    data: pd.DataFrame,
) -> None:
    """Hiển thị 5 thẻ thống kê tổng quan."""

    total_rows = len(data)

    total_weeks = data["chart_week"].nunique() if "chart_week" in data.columns else 0

    total_songs = data["song_key"].nunique() if "song_key" in data.columns else 0

    total_artists = (
        data["artist_names"].nunique() if "artist_names" in data.columns else 0
    )

    total_streams = data["streams"].sum() if "streams" in data.columns else 0

    (
        row_column,
        week_column,
        song_column,
        artist_column,
        stream_column,
    ) = st.columns(5)

    row_column.metric(
        label="Dòng dữ liệu",
        value=f"{total_rows:,}",
    )

    week_column.metric(
        label="Số tuần",
        value=f"{total_weeks:,}",
    )

    song_column.metric(
        label="Bài hát",
        value=f"{total_songs:,}",
    )

    artist_column.metric(
        label="Nghệ sĩ",
        value=f"{total_artists:,}",
    )

    stream_column.metric(
        label="Tổng lượt nghe",
        value=format_number(total_streams),
    )

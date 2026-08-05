import pandas as pd
import streamlit as st

from helpers import format_date


def render_filters(
    data: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """
    Hiển thị bộ lọc trong sidebar.

    Trả về:
    - Dữ liệu sau khi lọc.
    - Thông tin các lựa chọn hiện tại.
    """

    st.sidebar.markdown("### Bộ lọc dữ liệu")

    available_weeks = sorted(
        data["chart_week"].dropna().unique(),
        reverse=True,
    )

    week_options = {
        "Tất cả 12 tuần": None,
    }

    for week in available_weeks:
        week_options[format_date(week)] = pd.Timestamp(week)

    selected_week_label = st.sidebar.selectbox(
        "Tuần bảng xếp hạng",
        options=list(week_options.keys()),
        key="filter_week",
    )

    selected_week = week_options[selected_week_label]

    genre_options = sorted(data["genre"].dropna().astype(str).unique())

    selected_genres = st.sidebar.multiselect(
        "Thể loại",
        options=genre_options,
        placeholder="Chọn thể loại",
        key="filter_genres",
    )

    artist_options = sorted(data["artist_names"].dropna().astype(str).unique())

    selected_artists = st.sidebar.multiselect(
        "Nghệ sĩ",
        options=artist_options,
        placeholder="Chọn nghệ sĩ",
        key="filter_artists",
    )

    rank_range = st.sidebar.slider(
        "Khoảng thứ hạng",
        min_value=1,
        max_value=200,
        value=(1, 200),
        key="filter_rank",
    )

    filtered_data = data.copy()

    if selected_week is not None:
        filtered_data = filtered_data[filtered_data["chart_week"] == selected_week]

    if selected_genres:
        filtered_data = filtered_data[filtered_data["genre"].isin(selected_genres)]

    if selected_artists:
        filtered_data = filtered_data[
            filtered_data["artist_names"].isin(selected_artists)
        ]

    filtered_data = filtered_data[
        filtered_data["rank"].between(
            rank_range[0],
            rank_range[1],
        )
    ].copy()

    st.sidebar.divider()

    st.sidebar.caption(f"Đang hiển thị {len(filtered_data):,} dòng dữ liệu.")

    filter_state = {
        "week_label": selected_week_label,
        "week": selected_week,
        "genres": selected_genres,
        "artists": selected_artists,
        "rank_range": rank_range,
    }

    return filtered_data, filter_state

import pandas as pd
import plotly.express as px
import streamlit as st

from components.layout import render_page_header
from components.metric_cards import render_metric_cards
from helpers import PLOTLY_CONFIG, style_chart

PASTEL_COLORS = [
    "#7C3AED",
    "#8B5CF6",
    "#A78BFA",
    "#C4B5FD",
    "#D8B4FE",
    "#F0ABFC",
    "#F9A8D4",
]


def render(data: pd.DataFrame) -> None:
    """Hiển thị trang phân tích tổng quan."""

    render_page_header(
        title="Phân tích tổng quan",
        description=(
            "Theo dõi xu hướng lượt nghe, " "bài hát, nghệ sĩ và thể loại nổi bật."
        ),
        icon="📊",
    )

    if data.empty:
        st.warning("Không có dữ liệu phù hợp với bộ lọc hiện tại.")
        return

    render_metric_cards(data)

    st.write("")

    # =====================================================
    # 1. XU HƯỚNG LƯỢT NGHE VÀ THỂ LOẠI
    # =====================================================
    stream_column, genre_column = st.columns([1.6, 1])

    with stream_column:
        weekly_streams = (
            data.groupby(
                "chart_week",
                as_index=False,
            )["streams"]
            .sum()
            .sort_values("chart_week")
        )

        weekly_figure = px.area(
            weekly_streams,
            x="chart_week",
            y="streams",
            markers=True,
            title="Xu hướng tổng lượt nghe theo tuần",
            color_discrete_sequence=["#8B5CF6"],
        )

        weekly_figure.update_traces(
            line={
                "width": 3,
            },
            fillcolor=("rgba(139, 92, 246, 0.18)"),
            hovertemplate=(
                "Tuần: %{x|%d/%m/%Y}" "<br>Lượt nghe: %{y:,.0f}" "<extra></extra>"
            ),
        )

        weekly_figure.update_xaxes(title="")

        weekly_figure.update_yaxes(title="Lượt nghe")

        st.plotly_chart(
            style_chart(
                weekly_figure,
                height=440,
            ),
            width="stretch",
            config=PLOTLY_CONFIG,
        )

    with genre_column:
        genre_summary = (
            data.groupby(
                "genre",
                as_index=False,
            )["streams"]
            .sum()
            .sort_values(
                "streams",
                ascending=False,
            )
        )

        genre_figure = px.pie(
            genre_summary,
            names="genre",
            values="streams",
            hole=0.58,
            title="Tỷ trọng lượt nghe theo thể loại",
            color_discrete_sequence=PASTEL_COLORS,
        )

        genre_figure.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "%{label}"
                "<br>%{value:,.0f} lượt nghe"
                "<br>%{percent}"
                "<extra></extra>"
            ),
        )

        st.plotly_chart(
            style_chart(
                genre_figure,
                height=440,
            ),
            width="stretch",
            config=PLOTLY_CONFIG,
        )

    # =====================================================
    # 2. TOP BÀI HÁT VÀ NGHỆ SĨ
    # =====================================================
    song_column, artist_column = st.columns(2)

    with song_column:
        top_songs = (
            data.groupby(
                [
                    "track_name",
                    "artist_names",
                ],
                as_index=False,
            )["streams"]
            .sum()
            .nlargest(
                10,
                "streams",
            )
            .sort_values("streams")
        )

        top_songs["Bài hát"] = (
            top_songs["track_name"] + " — " + top_songs["artist_names"]
        )

        song_figure = px.bar(
            top_songs,
            x="streams",
            y="Bài hát",
            orientation="h",
            title="Top 10 bài hát theo tổng lượt nghe",
            color="streams",
            color_continuous_scale=[
                [0, "#E9D5FF"],
                [1, "#7C3AED"],
            ],
        )

        song_figure.update_coloraxes(showscale=False)

        song_figure.update_xaxes(title="Lượt nghe")

        song_figure.update_yaxes(title="")

        song_figure.update_traces(
            hovertemplate=("%{y}" "<br>%{x:,.0f} lượt nghe" "<extra></extra>")
        )

        st.plotly_chart(
            style_chart(
                song_figure,
                height=510,
            ),
            width="stretch",
            config=PLOTLY_CONFIG,
        )

    with artist_column:
        top_artists = (
            data.groupby(
                "artist_names",
                as_index=False,
            )["streams"]
            .sum()
            .nlargest(
                10,
                "streams",
            )
            .sort_values("streams")
        )

        artist_figure = px.bar(
            top_artists,
            x="streams",
            y="artist_names",
            orientation="h",
            title="Top 10 nghệ sĩ theo tổng lượt nghe",
            color="streams",
            color_continuous_scale=[
                [0, "#F5D0FE"],
                [1, "#9333EA"],
            ],
        )

        artist_figure.update_coloraxes(showscale=False)

        artist_figure.update_xaxes(title="Lượt nghe")

        artist_figure.update_yaxes(title="")

        artist_figure.update_traces(
            hovertemplate=("%{y}" "<br>%{x:,.0f} lượt nghe" "<extra></extra>")
        )

        st.plotly_chart(
            style_chart(
                artist_figure,
                height=510,
            ),
            width="stretch",
            config=PLOTLY_CONFIG,
        )

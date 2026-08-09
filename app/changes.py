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
            "tụt hạng và mới xuất hiện trong phạm vi dữ liệu đã chọn."
        ),
        icon="📈",
    )

    if data.empty:
        st.warning("Không có dữ liệu phù hợp với bộ lọc hiện tại.")
        return

    # =====================================================
    # XÁC ĐỊNH PHẠM VI PHÂN TÍCH
    # Dữ liệu đã được lọc từ sidebar trước khi truyền vào đây
    # =====================================================
    analysis_data = data.copy()

    analysis_data["rank_change"] = pd.to_numeric(
        analysis_data["rank_change"],
        errors="coerce",
    )

    available_weeks = sorted(
        analysis_data["chart_week"].dropna().unique(),
        reverse=True,
    )

    if not available_weeks:
        st.warning("Không tìm thấy dữ liệu tuần.")
        return

    if len(available_weeks) == 1:
        period_label = f"tuần {format_date(available_weeks[0])}"

        render_info_box(
            f"Đang phân tích biến động tại {period_label}. "
            "Giá trị dương là tăng hạng, "
            "giá trị âm là tụt hạng."
        )
    else:
        period_label = f"toàn bộ {len(available_weeks)} tuần"

        render_info_box(
            f"Đang phân tích biến động trên {period_label}. "
            "Giá trị dương là tăng hạng, "
            "giá trị âm là tụt hạng."
        )

    # =====================================================
    # PHÂN LOẠI BIẾN ĐỘNG
    # =====================================================
    rising_songs = analysis_data[analysis_data["rank_change"] > 0].copy()

    falling_songs = analysis_data[analysis_data["rank_change"] < 0].copy()

    new_entry_values = analysis_data["is_new_entry"].astype(str).str.strip().str.lower()

    new_songs = analysis_data[new_entry_values.isin(["true", "1", "yes"])].copy()

    # =====================================================
    # KPI
    # =====================================================
    metric_1, metric_2, metric_3 = st.columns(3)

    if len(available_weeks) == 1:
        rise_label = "Bài tăng hạng"
        fall_label = "Bài tụt hạng"
        new_label = "Bài mới/quay lại"
    else:
        rise_label = "Lượt tăng hạng"
        fall_label = "Lượt tụt hạng"
        new_label = "Lượt mới/quay lại"

    metric_1.metric(
        rise_label,
        f"{len(rising_songs):,}",
    )

    metric_2.metric(
        fall_label,
        f"{len(falling_songs):,}",
    )

    metric_3.metric(
        new_label,
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
            st.info("Không có bài hát tăng hạng " "trong phạm vi đã chọn.")
        else:
            rising_figure = px.bar(
                top_risers,
                x="rank_change",
                y="track_name",
                orientation="h",
                title=(f"Top 10 bài tăng hạng mạnh - " f"{period_label}"),
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
            st.info("Không có bài hát tụt hạng " "trong phạm vi đã chọn.")
        else:
            falling_figure = px.bar(
                top_fallers,
                x="Số hạng tụt",
                y="track_name",
                orientation="h",
                title=(f"Top 10 bài tụt hạng mạnh - " f"{period_label}"),
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
        st.info("Không có bài mới hoặc quay lại " "trong phạm vi đã chọn.")
    else:
        # Nếu xem nhiều tuần thì cần thêm cột Tuần
        if len(available_weeks) > 1:
            table_columns = [
                "chart_week",
                "rank",
                "track_name",
                "artist_names",
                "genre",
                "streams",
                "weeks_on_chart",
            ]

            new_song_table = (
                new_songs[table_columns]
                .sort_values(
                    ["chart_week", "rank"],
                    ascending=[False, True],
                )
                .rename(
                    columns={
                        "chart_week": "Tuần",
                        "rank": "Hạng",
                        "track_name": "Bài hát",
                        "artist_names": "Nghệ sĩ",
                        "genre": "Thể loại",
                        "streams": "Lượt nghe",
                        "weeks_on_chart": ("Số tuần trên BXH"),
                    }
                )
            )

            new_song_table["Tuần"] = new_song_table["Tuần"].dt.strftime("%d/%m/%Y")

        else:
            table_columns = [
                "rank",
                "track_name",
                "artist_names",
                "genre",
                "streams",
                "weeks_on_chart",
            ]

            new_song_table = (
                new_songs[table_columns]
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

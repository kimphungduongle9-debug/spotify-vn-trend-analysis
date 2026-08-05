import pandas as pd
import plotly.express as px
import streamlit as st

from components.layout import (
    render_info_box,
    render_page_header,
)
from helpers import (
    PLOTLY_CONFIG,
    format_number,
    style_chart,
)


def render(potential_data: pd.DataFrame | None) -> None:
    """Hiển thị danh sách bài hát tiềm năng từ notebook."""

    render_page_header(
        title="Bài hát tiềm năng",
        description=(
            "Nhận diện các bài hát nổi bật dựa trên "
            "lượt nghe, mức tăng hạng, thứ hạng hiện tại "
            "và thời gian xuất hiện trên bảng xếp hạng."
        ),
        icon="✨",
    )

    render_info_box(
        "Điểm tiềm năng được notebook tính sẵn. "
        "Đây là điểm hỗ trợ sàng lọc bài hát nổi bật, "
        "không phải xác suất thành công trong tương lai."
    )

    if potential_data is None:
        st.warning("Không tìm thấy file outputs/potential_songs.csv.")
        return

    if potential_data.empty:
        st.info("Danh sách bài hát tiềm năng đang trống.")
        return

    data = potential_data.copy()

    numeric_columns = [
        "Hạng hiện tại",
        "Số hạng tăng",
        "Số tuần trên BXH",
        "Lượt nghe",
        "Điểm tiềm năng",
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce",
            )

    if "Điểm tiềm năng" in data.columns:
        data = data.sort_values(
            "Điểm tiềm năng",
            ascending=False,
        ).reset_index(drop=True)

    best_song = data.iloc[0]

    song_name = best_song.get(
        "Tên bài hát",
        "Không xác định",
    )

    artist_name = best_song.get(
        "Nghệ sĩ",
        "Không xác định",
    )

    potential_score = pd.to_numeric(
        best_song.get("Điểm tiềm năng", 0),
        errors="coerce",
    )

    streams = pd.to_numeric(
        best_song.get("Lượt nghe", 0),
        errors="coerce",
    )

    if pd.isna(potential_score):
        potential_score = 0

    if pd.isna(streams):
        streams = 0

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    metric_1.metric(
        "Bài tiềm năng nhất",
        song_name,
    )

    metric_2.metric(
        "Nghệ sĩ",
        artist_name,
    )

    metric_3.metric(
        "Điểm tiềm năng",
        f"{potential_score:.2f}/100",
    )

    metric_4.metric(
        "Lượt nghe hiện tại",
        format_number(streams),
    )

    st.write("")

    required_chart_columns = {
        "Tên bài hát",
        "Số hạng tăng",
        "Lượt nghe",
        "Điểm tiềm năng",
    }

    if required_chart_columns.issubset(data.columns):
        hover_columns = [
            column
            for column in [
                "Nghệ sĩ",
                "Hạng hiện tại",
                "Số tuần trên BXH",
            ]
            if column in data.columns
        ]

        potential_figure = px.scatter(
            data,
            x="Số hạng tăng",
            y="Lượt nghe",
            size="Điểm tiềm năng",
            color="Điểm tiềm năng",
            hover_name="Tên bài hát",
            hover_data=hover_columns,
            title=("Mối quan hệ giữa tăng hạng, " "lượt nghe và điểm tiềm năng"),
            color_continuous_scale=[
                [0, "#DDD6FE"],
                [0.5, "#A78BFA"],
                [1, "#6D28D9"],
            ],
            size_max=55,
        )

        potential_figure.update_xaxes(title="Số hạng tăng")

        potential_figure.update_yaxes(title="Lượt nghe")

        st.plotly_chart(
            style_chart(
                potential_figure,
                height=520,
            ),
            width="stretch",
            config=PLOTLY_CONFIG,
        )
    else:
        st.info("File bài hát tiềm năng chưa đủ cột " "để tạo biểu đồ bong bóng.")

    st.subheader("Danh sách bài hát tiềm năng")

    st.dataframe(
        data,
        width="stretch",
        hide_index=True,
        column_config={
            "Hạng hiện tại": (
                st.column_config.NumberColumn(
                    format="%d",
                )
            ),
            "Số hạng tăng": (
                st.column_config.NumberColumn(
                    format="%+d",
                )
            ),
            "Số tuần trên BXH": (
                st.column_config.NumberColumn(
                    format="%d",
                )
            ),
            "Lượt nghe": (
                st.column_config.NumberColumn(
                    format="%d",
                )
            ),
            "Điểm tiềm năng": (
                st.column_config.ProgressColumn(
                    min_value=0,
                    max_value=100,
                    format="%.2f",
                )
            ),
        },
    )

    st.download_button(
        label="⬇️ Tải danh sách bài hát tiềm năng",
        data=data.to_csv(index=False).encode("utf-8-sig"),
        file_name="potential_songs.csv",
        mime="text/csv",
    )

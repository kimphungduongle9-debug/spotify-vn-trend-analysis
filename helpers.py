from datetime import date, datetime

import pandas as pd

# Cấu hình chung cho biểu đồ Plotly
PLOTLY_CONFIG = {
    "displaylogo": False,
    "scrollZoom": False,
    "responsive": True,
}


def format_number(value) -> str:
    """Rút gọn số thành K hoặc M."""

    number = pd.to_numeric(
        value,
        errors="coerce",
    )

    if pd.isna(number):
        return "0"

    if abs(number) >= 1_000_000:
        return f"{number / 1_000_000:,.2f}M"

    if abs(number) >= 1_000:
        return f"{number / 1_000:,.1f}K"

    return f"{number:,.0f}"


def format_date(value) -> str:
    """Định dạng ngày thành dd/mm/yyyy."""

    if value is None:
        return ""

    if isinstance(value, (date, datetime)):
        return value.strftime("%d/%m/%Y")

    converted_date = pd.to_datetime(
        value,
        errors="coerce",
    )

    if pd.isna(converted_date):
        return str(value)

    return converted_date.strftime("%d/%m/%Y")


def style_chart(
    figure,
    height: int = 430,
):
    """Áp dụng kiểu giao diện chung cho biểu đồ."""

    figure.update_layout(
        height=height,
        margin={
            "l": 20,
            "r": 20,
            "t": 60,
            "b": 20,
        },
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(255, 255, 255, 0)",
        font={
            "color": "#35264D",
        },
        title_font={
            "size": 18,
            "color": "#35264D",
        },
        legend_title_text="",
        hoverlabel={
            "bgcolor": "white",
            "font_size": 13,
        },
    )

    figure.update_xaxes(
        gridcolor="rgba(139, 92, 246, 0.09)",
        zeroline=False,
    )

    figure.update_yaxes(
        gridcolor="rgba(139, 92, 246, 0.09)",
        zeroline=False,
    )

    return figure

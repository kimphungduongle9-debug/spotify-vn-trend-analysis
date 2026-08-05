import pandas as pd
import streamlit as st

from components.layout import (
    render_info_box,
    render_page_header,
)


def render(project_data: dict) -> None:
    """Hiển thị các tập dữ liệu đã xuất từ notebook."""

    render_page_header(
        title="Dữ liệu",
        description=(
            "Xem dữ liệu đã làm sạch, tập huấn luyện "
            "và tập kiểm tra được notebook tạo ra."
        ),
        icon="🗂️",
    )

    render_info_box(
        "Các tập train và test được tạo trong notebook "
        "theo cách chia dữ liệu của mô hình."
    )

    dataset_options = {}

    cleaned_data = project_data.get("cleaned")
    train_data = project_data.get("train")
    test_data = project_data.get("test")

    if cleaned_data is not None:
        dataset_options["Dữ liệu đã làm sạch"] = cleaned_data

    if train_data is not None:
        dataset_options["Tập train"] = train_data

    if test_data is not None:
        dataset_options["Tập test"] = test_data

    if not dataset_options:
        st.warning("Không tìm thấy dữ liệu để hiển thị.")
        return

    selected_dataset_name = st.selectbox(
        "Chọn tập dữ liệu",
        options=list(dataset_options.keys()),
        key="data_view_dataset",
    )

    selected_data = dataset_options[selected_dataset_name].copy()

    if selected_data.empty:
        st.info("Tập dữ liệu đã chọn đang trống.")
        return

    row_column, column_column, missing_column = st.columns(3)

    row_column.metric(
        "Số dòng",
        f"{len(selected_data):,}",
    )

    column_column.metric(
        "Số cột",
        f"{len(selected_data.columns):,}",
    )

    missing_column.metric(
        "Giá trị thiếu",
        f"{selected_data.isna().sum().sum():,}",
    )

    st.write("")

    available_columns = list(selected_data.columns)

    default_columns = available_columns[: min(10, len(available_columns))]

    selected_columns = st.multiselect(
        "Chọn các cột cần hiển thị",
        options=available_columns,
        default=default_columns,
        key="data_view_columns",
    )

    if not selected_columns:
        st.warning("Hãy chọn ít nhất một cột để hiển thị.")
        return

    maximum_rows = min(
        500,
        len(selected_data),
    )

    row_options = [
        option for option in [10, 20, 50, 100, 200, 500] if option <= maximum_rows
    ]

    if maximum_rows not in row_options:
        row_options.append(maximum_rows)

    row_options = sorted(set(row_options))

    number_of_rows = st.selectbox(
        "Số dòng hiển thị",
        options=row_options,
        index=min(
            2,
            len(row_options) - 1,
        ),
        key="data_view_rows",
    )

    display_data = selected_data[selected_columns].head(number_of_rows).copy()

    st.dataframe(
        display_data,
        width="stretch",
        hide_index=True,
    )

    st.caption(f"Đang hiển thị {len(display_data):,}/" f"{len(selected_data):,} dòng.")

    download_data = selected_data.drop(
        columns=["song_key"],
        errors="ignore",
    )

    download_file_name = (
        selected_dataset_name.lower()
        .replace(" ", "_")
        .replace("ữ", "u")
        .replace("ậ", "a")
    )

    st.download_button(
        label="⬇️ Tải toàn bộ dữ liệu CSV",
        data=download_data.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{download_file_name}.csv",
        mime="text/csv",
    )

    with st.expander("Xem kiểu dữ liệu của các cột"):
        column_information = pd.DataFrame(
            {
                "Tên cột": selected_data.columns,
                "Kiểu dữ liệu": [str(data_type) for data_type in selected_data.dtypes],
                "Số giá trị thiếu": [
                    int(value) for value in selected_data.isna().sum()
                ],
            }
        )

        st.dataframe(
            column_information,
            width="stretch",
            hide_index=True,
        )

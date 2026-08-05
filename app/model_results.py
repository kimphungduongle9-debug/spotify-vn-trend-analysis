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


def render(
    metrics_data: pd.DataFrame | None,
    linear_predictions: pd.DataFrame | None,
    rf_predictions: pd.DataFrame | None,
    train_data: pd.DataFrame | None = None,
    test_data: pd.DataFrame | None = None,
) -> None:
    """Hiển thị kết quả đánh giá các mô hình dự đoán."""

    render_page_header(
        title="Kết quả mô hình",
        description=(
            "So sánh Baseline, Linear Regression "
            "và Random Forest trong dự đoán "
            "lượt nghe tuần tiếp theo."
        ),
        icon="🤖",
    )

    render_info_box(
        "Trang này chỉ đọc kết quả notebook đã xuất. "
        "Mô hình không được huấn luyện lại khi mở giao diện."
    )

    # =====================================================
    # 1. BẢNG SO SÁNH MÔ HÌNH
    # =====================================================
    if metrics_data is None:
        st.warning("Không tìm thấy file outputs/model_metrics.csv.")
    elif metrics_data.empty:
        st.info("Bảng kết quả mô hình đang trống.")
    else:
        metrics = metrics_data.copy()

        required_metric_columns = {
            "Mô hình",
            "MAE",
            "RMSE",
            "R²",
        }

        missing_columns = required_metric_columns - set(metrics.columns)

        if missing_columns:
            st.error(
                "File model_metrics.csv thiếu các cột: "
                + ", ".join(sorted(missing_columns))
            )
        else:
            for column in ["MAE", "RMSE", "R²"]:
                metrics[column] = pd.to_numeric(
                    metrics[column],
                    errors="coerce",
                )

            metrics = metrics.dropna(subset=["MAE", "RMSE", "R²"])

            if metrics.empty:
                st.warning("Các chỉ số mô hình không hợp lệ.")
            else:
                best_model = metrics.sort_values(
                    by=["MAE", "RMSE", "R²"],
                    ascending=[True, True, False],
                ).iloc[0]

                (
                    model_column,
                    mae_column,
                    rmse_column,
                    r2_column,
                ) = st.columns(4)

                model_column.metric(
                    "Mô hình tốt nhất",
                    best_model["Mô hình"],
                )

                mae_column.metric(
                    "MAE",
                    format_number(best_model["MAE"]),
                )

                rmse_column.metric(
                    "RMSE",
                    format_number(best_model["RMSE"]),
                )

                r2_column.metric(
                    "R²",
                    f"{best_model['R²']:.4f}",
                )

                st.write("")

                error_column, r2_chart_column = st.columns([1.5, 1])

                with error_column:
                    error_chart_data = metrics.melt(
                        id_vars="Mô hình",
                        value_vars=["MAE", "RMSE"],
                        var_name="Chỉ số",
                        value_name="Giá trị",
                    )

                    error_figure = px.bar(
                        error_chart_data,
                        x="Mô hình",
                        y="Giá trị",
                        color="Chỉ số",
                        barmode="group",
                        title="So sánh MAE và RMSE",
                        color_discrete_sequence=[
                            "#7C3AED",
                            "#C084FC",
                        ],
                    )

                    error_figure.update_xaxes(title="")
                    error_figure.update_yaxes(title="Mức sai số")

                    st.plotly_chart(
                        style_chart(
                            error_figure,
                            height=430,
                        ),
                        width="stretch",
                        config=PLOTLY_CONFIG,
                    )

                with r2_chart_column:
                    r2_figure = px.bar(
                        metrics.sort_values("R²"),
                        x="Mô hình",
                        y="R²",
                        color="R²",
                        title="So sánh hệ số R²",
                        color_continuous_scale=[
                            [0, "#DDD6FE"],
                            [1, "#6D28D9"],
                        ],
                    )

                    r2_figure.update_coloraxes(showscale=False)

                    r2_figure.update_xaxes(title="")
                    r2_figure.update_yaxes(
                        title="R²",
                        range=[0, 1],
                    )

                    st.plotly_chart(
                        style_chart(
                            r2_figure,
                            height=430,
                        ),
                        width="stretch",
                        config=PLOTLY_CONFIG,
                    )

                display_metrics = metrics.copy()

                display_metrics["MAE"] = display_metrics["MAE"].round(2)
                display_metrics["RMSE"] = display_metrics["RMSE"].round(2)
                display_metrics["R²"] = display_metrics["R²"].round(4)

                st.dataframe(
                    display_metrics,
                    width="stretch",
                    hide_index=True,
                    column_config={
                        "MAE": st.column_config.NumberColumn(
                            format="%.2f",
                        ),
                        "RMSE": st.column_config.NumberColumn(
                            format="%.2f",
                        ),
                        "R²": st.column_config.NumberColumn(
                            format="%.4f",
                        ),
                    },
                )

    # =====================================================
    # 2. THÔNG TIN TẬP TRAIN VÀ TEST
    # =====================================================
    train_column, test_column = st.columns(2)

    with train_column:
        if train_data is not None:
            st.metric(
                "Số dòng tập train",
                f"{len(train_data):,}",
            )
        else:
            st.metric(
                "Số dòng tập train",
                "Chưa có dữ liệu",
            )

    with test_column:
        if test_data is not None:
            st.metric(
                "Số dòng tập test",
                f"{len(test_data):,}",
            )
        else:
            st.metric(
                "Số dòng tập test",
                "Chưa có dữ liệu",
            )

    # =====================================================
    # 3. CHI TIẾT DỰ ĐOÁN
    # =====================================================
    st.subheader("Chi tiết kết quả dự đoán")

    selected_model = st.radio(
        "Chọn mô hình cần xem",
        options=[
            "Linear Regression",
            "Random Forest",
        ],
        horizontal=True,
        key="model_result_choice",
    )

    if selected_model == "Linear Regression":
        prediction_data = linear_predictions
        prediction_column = "Linear Regression dự đoán"
    else:
        prediction_data = rf_predictions
        prediction_column = "Random Forest dự đoán"

    actual_column = "Lượt nghe thực tế tuần sau"
    error_column_name = "Sai lệch tuyệt đối"

    if prediction_data is None:
        st.warning("Không tìm thấy file dự đoán " "của mô hình đã chọn.")
        return

    if prediction_data.empty:
        st.info("Bảng dự đoán đang trống.")
        return

    predictions = prediction_data.copy()

    required_prediction_columns = {
        actual_column,
        prediction_column,
    }

    missing_prediction_columns = required_prediction_columns - set(predictions.columns)

    if missing_prediction_columns:
        st.error(
            "File dự đoán thiếu các cột: "
            + ", ".join(sorted(missing_prediction_columns))
        )
        return

    for column in [
        "Lượt nghe hiện tại",
        actual_column,
        prediction_column,
        error_column_name,
    ]:
        if column in predictions.columns:
            predictions[column] = pd.to_numeric(
                predictions[column],
                errors="coerce",
            )

    valid_predictions = predictions.dropna(
        subset=[
            actual_column,
            prediction_column,
        ]
    ).copy()

    if valid_predictions.empty:
        st.warning("Không có giá trị dự đoán hợp lệ.")
        return

    prediction_figure = px.scatter(
        valid_predictions,
        x=actual_column,
        y=prediction_column,
        hover_name=("Bài hát" if "Bài hát" in valid_predictions.columns else None),
        hover_data=[
            column
            for column in [
                "Nghệ sĩ",
                "Tuần hiện tại",
                "Tuần cần dự đoán",
                error_column_name,
            ]
            if column in valid_predictions.columns
        ],
        title=("So sánh lượt nghe thực tế " "và lượt nghe dự đoán"),
        color_discrete_sequence=["#7C3AED"],
    )

    minimum_value = min(
        valid_predictions[actual_column].min(),
        valid_predictions[prediction_column].min(),
    )

    maximum_value = max(
        valid_predictions[actual_column].max(),
        valid_predictions[prediction_column].max(),
    )

    prediction_figure.add_shape(
        type="line",
        x0=minimum_value,
        y0=minimum_value,
        x1=maximum_value,
        y1=maximum_value,
        line={
            "color": "#DB2777",
            "dash": "dash",
            "width": 2,
        },
    )

    prediction_figure.update_xaxes(title="Lượt nghe thực tế")

    prediction_figure.update_yaxes(title="Lượt nghe dự đoán")

    st.plotly_chart(
        style_chart(
            prediction_figure,
            height=540,
        ),
        width="stretch",
        config=PLOTLY_CONFIG,
    )

    if error_column_name in predictions.columns:
        predictions = predictions.sort_values(
            error_column_name,
            ascending=False,
        )

    number_of_rows = st.selectbox(
        "Số kết quả hiển thị",
        options=[10, 20, 50, 100],
        index=1,
        key="prediction_rows",
    )

    st.dataframe(
        predictions.head(number_of_rows),
        width="stretch",
        hide_index=True,
        column_config={
            "Lượt nghe hiện tại": (
                st.column_config.NumberColumn(
                    format="%d",
                )
            ),
            actual_column: (
                st.column_config.NumberColumn(
                    format="%d",
                )
            ),
            prediction_column: (
                st.column_config.NumberColumn(
                    format="%d",
                )
            ),
            error_column_name: (
                st.column_config.NumberColumn(
                    format="%d",
                )
            ),
        },
    )

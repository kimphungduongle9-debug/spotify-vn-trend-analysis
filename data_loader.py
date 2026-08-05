from pathlib import Path

import pandas as pd
import streamlit as st

# Thư mục gốc của project
PROJECT_DIR = Path(__file__).resolve().parent

DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "outputs"


RAW_DATA_PATH = DATA_DIR / "spotify_vn_12_weeks.csv"
CLEANED_DATA_PATH = OUTPUT_DIR / "spotify_cleaned.csv"
TRAIN_DATA_PATH = OUTPUT_DIR / "train_data.csv"
TEST_DATA_PATH = OUTPUT_DIR / "test_data.csv"
MODEL_METRICS_PATH = OUTPUT_DIR / "model_metrics.csv"
LINEAR_PREDICTIONS_PATH = OUTPUT_DIR / "linear_predictions.csv"
RF_PREDICTIONS_PATH = OUTPUT_DIR / "random_forest_predictions.csv"
POTENTIAL_SONGS_PATH = OUTPUT_DIR / "potential_songs.csv"


DATE_COLUMNS = [
    "chart_week",
    "next_chart_week",
    "Tuần",
    "Tuần hiện tại",
    "Tuần cần dự đoán",
]


@st.cache_data(show_spinner=False)
def read_csv(path: Path) -> pd.DataFrame:
    """Đọc một file CSV và tự chuyển các cột ngày."""

    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {path}")

    data = pd.read_csv(
        path,
        encoding="utf-8-sig",
    )

    for column in DATE_COLUMNS:
        if column in data.columns:
            data[column] = pd.to_datetime(
                data[column],
                errors="coerce",
            )

    return data


def read_optional_csv(
    path: Path,
) -> pd.DataFrame | None:
    """Đọc file nếu tồn tại, nếu không thì trả về None."""

    if not path.exists():
        return None

    return read_csv(path)


def prepare_main_data(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """Chuẩn hóa dữ liệu chính dùng trên giao diện."""

    required_columns = {
        "rank",
        "artist_names",
        "track_name",
        "streams",
        "chart_week",
    }

    missing_columns = required_columns.difference(data.columns)

    if missing_columns:
        raise ValueError("Dữ liệu thiếu các cột: " + ", ".join(sorted(missing_columns)))

    default_columns = {
        "genre": "Không xác định",
        "rank_change": 0,
        "is_new_entry": False,
        "weeks_on_chart": 0,
        "peak_rank": 0,
        "previous_rank": 0,
    }

    for column, default_value in default_columns.items():
        if column not in data.columns:
            data[column] = default_value

    numeric_columns = [
        "rank",
        "streams",
        "rank_change",
        "weeks_on_chart",
        "peak_rank",
        "previous_rank",
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce",
        )

    text_columns = [
        "track_name",
        "artist_names",
        "genre",
    ]

    for column in text_columns:
        data[column] = data[column].fillna("Không xác định").astype(str).str.strip()

    if data["is_new_entry"].dtype != bool:
        data["is_new_entry"] = (
            data["is_new_entry"]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["true", "1", "yes"])
        )

    data = data.dropna(
        subset=[
            "chart_week",
            "rank",
            "streams",
        ]
    ).copy()

    data["song_key"] = data["track_name"] + " — " + data["artist_names"]

    return data.sort_values(["chart_week", "rank"]).reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_project_data() -> dict:
    """Đọc toàn bộ dữ liệu và kết quả notebook."""

    if CLEANED_DATA_PATH.exists():
        main_data = read_csv(CLEANED_DATA_PATH)
    else:
        main_data = read_csv(RAW_DATA_PATH)

    main_data = prepare_main_data(main_data)

    return {
        "cleaned": main_data,
        "train": read_optional_csv(TRAIN_DATA_PATH),
        "test": read_optional_csv(TEST_DATA_PATH),
        "metrics": read_optional_csv(MODEL_METRICS_PATH),
        "linear_predictions": read_optional_csv(LINEAR_PREDICTIONS_PATH),
        "rf_predictions": read_optional_csv(RF_PREDICTIONS_PATH),
        "potential": read_optional_csv(POTENTIAL_SONGS_PATH),
    }

import pandas as pd
import os

DATASET_PATH = 'psychological_state_dataset.csv'

_dataframe = None
_data_iterator = None


def _load_dataset():
    global _dataframe
    if os.path.exists(DATASET_PATH):
        try:
            _dataframe = pd.read_csv(DATASET_PATH)
            _dataframe = _dataframe.dropna(subset=['HRV (ms)', 'GSR (μS)'])
        except Exception:
            _dataframe = None


def get_simulated_data() -> dict:
    global _dataframe, _data_iterator

    if _dataframe is None:
        _load_dataset()

    if _dataframe is None or _dataframe.empty:
        return {"hrv_raw": 70.0, "gsr_raw": 2.5}

    if _data_iterator is None:
        _data_iterator = _dataframe.iterrows()

    try:
        index, row = next(_data_iterator)
    except StopIteration:
        _data_iterator = _dataframe.iterrows()
        index, row = next(_data_iterator)

    return {
        "hrv_raw": float(row['HRV (ms)']),
        "gsr_raw": float(row['GSR (μS)'])
    }
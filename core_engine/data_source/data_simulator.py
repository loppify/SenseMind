import os
import pandas as pd

DATASET_FILENAME = 'psychological_state_dataset.csv'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASET_PATH = os.path.join(BASE_DIR, DATASET_FILENAME)

COL_HRV = 'HRV (ms)'
COL_GSR = 'GSR (μS)'

DEFAULT_HRV = 70.0
DEFAULT_GSR = 2.5


class BioSensorSimulator:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._dataframe = None
        self._data_iterator = None
        self._load_dataset()

    def _load_dataset(self):
        if os.path.exists(self.file_path):
            try:
                df = pd.read_csv(self.file_path)
                self._dataframe = df.dropna(subset=[COL_HRV, COL_GSR])
                self._data_iterator = self._dataframe.iterrows()
                print(f"Dataset loaded successfully: {len(self._dataframe)} records.")
            except Exception as e:
                print(f"Error loading dataset: {e}")
                self._dataframe = None
        else:
            print(f"Warning: Dataset not found at {self.file_path}")

    def get_next_reading(self) -> dict:
        if self._dataframe is None or self._dataframe.empty:
            return {"hrv_raw": DEFAULT_HRV, "gsr_raw": DEFAULT_GSR}

        try:
            _, row = next(self._data_iterator)
        except StopIteration:
            self._data_iterator = self._dataframe.iterrows()
            _, row = next(self._data_iterator)

        return {
            "hrv_raw": float(row[COL_HRV]),
            "gsr_raw": float(row[COL_GSR])
        }


sensor_simulator = BioSensorSimulator(DATASET_PATH)


def get_simulated_data() -> dict:
    return sensor_simulator.get_next_reading()
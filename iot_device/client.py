import json
import os
import time
from collections import deque

import pandas as pd
import requests

#
DATASET_FILENAME = 'psychological_state_dataset.csv'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, DATASET_FILENAME)

COL_HRV = 'HRV (ms)'
COL_GSR = 'GSR (μS)'

DEFAULT_HRV = 70.0
DEFAULT_GSR = 2.5


class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.settings = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                print(f"[INIT] Config loaded from {self.config_path}")
                return json.load(f)
        else:
            print("[ERROR] Config file not found! Using defaults.")
            return {
                "server_url": "http://127.0.0.1:5000/api/v1/data/raw",
                "polling_interval_sec": 3,
                "smoothing_window": 3
            }

    def get(self, key):
        return self.settings.get(key)


class SmartBandDevice:
    def __init__(self, config: ConfigManager, file_path: str = DATASET_PATH):
        self.config = config
        self.server_url = config.get("server_url")
        self.interval = config.get("polling_interval_sec")
        self.window_size = config.get("smoothing_window")

        self.hrv_buffer = deque(maxlen=self.window_size)
        self.gsr_buffer = deque(maxlen=self.window_size)

        # For simulating data collecting
        self.file_path = file_path
        self._dataframe = None
        self._data_iterator = None
        self._load_dataset()

    def _load_dataset(self):  # For simulating data collecting
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

    def _read_raw_sensor_data(self) -> dict:  # For simulating data collecting
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

    def _process_data(self, raw_data):
        self.hrv_buffer.append(raw_data['hrv_raw'])
        self.gsr_buffer.append(raw_data['gsr_raw'])

        avg_hrv = sum(self.hrv_buffer) / len(self.hrv_buffer)
        avg_gsr = sum(self.gsr_buffer) / len(self.gsr_buffer)

        return {
            "hrv_raw": round(avg_hrv, 2),
            "gsr_raw": round(avg_gsr, 3),
            "device_id": self.config.get("device_id"),
            "timestamp": time.time()
        }

    def send_to_server(self, processed_data):
        try:
            response = requests.post(self.server_url, json=processed_data)
            if response.status_code == 201:
                print(f"[SUCCESS] Data sent: {processed_data}")
            else:
                print(f"[WARNING] Server error: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")

    def run(self):
        print("--- IoT Device Started ---")
        print(f"Target Server: {self.server_url}")

        while True:
            raw = self._read_raw_sensor_data()
            payload = self._process_data(raw)
            self.send_to_server(payload)
            time.sleep(self.interval)


if __name__ == "__main__":
    cfg = ConfigManager()
    device = SmartBandDevice(cfg)
    device.run()

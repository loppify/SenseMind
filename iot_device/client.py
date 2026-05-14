import json
import os
import time
import random
from collections import deque

import pandas as pd
import requests

DATASET_FILENAME = 'psychological_state_dataset.csv'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, DATASET_FILENAME)

COL_HRV = 'HRV (ms)'
COL_GSR = 'GSR (μS)'

DEFAULT_HRV = 70.0
DEFAULT_GSR = 2.5


class ConfigManager:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self.config_path = config_path
        self._last_mtime = 0
        self.settings = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            self._last_mtime = os.path.getmtime(self.config_path)
            with open(self.config_path, 'r') as f:
                print(f"[CONFIG] Loaded from {self.config_path}")
                return json.load(f)
        else:
            print("[ERROR] Config file not found! Using defaults.")
            return {
                "server_url": "http://127.0.0.1:5000/api/v1/data/raw",
                "polling_interval_sec": 3,
                "smoothing_window": 3,
                "device_serial_id": "SN-001",
                "device_password": "device-secret-pass"
            }

    def check_for_updates(self):
        if os.path.exists(self.config_path):
            mtime = os.path.getmtime(self.config_path)
            if mtime > self._last_mtime:
                self.settings = self._load_config()
                return True
        return False

    def get(self, key):
        return self.settings.get(key)


class SmartBandDevice:
    def __init__(self, config: ConfigManager, file_path: str = DATASET_PATH):
        self.config = config
        self._sync_settings()

        self.hrv_buffer = deque(maxlen=self.window_size)
        self.gsr_buffer = deque(maxlen=self.window_size)

        self.file_path = file_path
        self._dataframe = None
        
        self.current_hrv = DEFAULT_HRV
        self.current_gsr = DEFAULT_GSR
        self.target_hrv = DEFAULT_HRV
        self.target_gsr = DEFAULT_GSR
        self.current_state = "Neutral"
        self.ticks_in_state = 0
        self.max_state_duration = random.randint(15, 30)

        self._load_dataset_initial()

    def _sync_settings(self):
        self.server_url = self.config.get("server_url")
        self.interval = self.config.get("polling_interval_sec")
        self.window_size = self.config.get("smoothing_window")
        print(f"[DEVICE] Settings synced. Interval: {self.interval}s")

    def _load_dataset_initial(self):
        if os.path.exists(self.file_path):
            try:
                df = pd.read_csv(self.file_path)
                self._dataframe = df.dropna(subset=[COL_HRV, COL_GSR])
                if not self._dataframe.empty:
                    row = self._dataframe.sample(n=1).iloc[0]
                    self.current_hrv = float(row[COL_HRV])
                    self.current_gsr = float(row[COL_GSR])
                print(f"[SIMULATION] Baseline loaded: HRV={self.current_hrv:.1f}, GSR={self.current_gsr:.2f}")
            except Exception as e:
                print(f"Error loading dataset: {e}")
        
        self.target_hrv = self.current_hrv
        self.target_gsr = self.current_gsr

    def _simulate_human_biology(self):
        self.ticks_in_state += 1

        force_change = self.ticks_in_state > self.max_state_duration
        
        if random.random() < 0.08 or force_change:
            self.ticks_in_state = 0
            self.max_state_duration = random.randint(15, 40)
            
            if self.current_state != "Neutral" and force_change:
                self.current_state = "Neutral"
                self.target_hrv = random.uniform(55.0, 75.0)
                self.target_gsr = random.uniform(1.5, 3.5)
            else:
                chance = random.random()
                if chance < 0.25:
                    self.current_state = "Stressed"
                    self.target_hrv = random.uniform(25.0, 45.0)
                    self.target_gsr = random.uniform(5.0, 9.0)
                elif chance < 0.50:
                    self.current_state = "Relaxed"
                    self.target_hrv = random.uniform(75.0, 110.0)
                    self.target_gsr = random.uniform(0.3, 1.2)
                else:
                    self.current_state = "Focused"
                    self.target_hrv = random.uniform(50.0, 65.0)
                    self.target_gsr = random.uniform(2.0, 4.5)
            
            print(f"[SIMULATION EVENT] Shifted to {self.current_state} (Target HRV: {self.target_hrv:.1f})")

        self.current_hrv += (self.target_hrv - self.current_hrv) * 0.12 + random.uniform(-1.0, 1.0)
        self.current_gsr += (self.target_gsr - self.current_gsr) * 0.12 + random.uniform(-0.1, 0.1)

        # Biological clamps (Safety limits)
        self.current_hrv = max(15.0, min(160.0, self.current_hrv))
        self.current_gsr = max(0.05, min(15.0, self.current_gsr))

    def _process_data(self):
        self._simulate_human_biology()
        self.hrv_buffer.append(self.current_hrv)
        self.gsr_buffer.append(self.current_gsr)

        return {
            "hrv_raw": round(sum(self.hrv_buffer)/len(self.hrv_buffer), 2),
            "gsr_raw": round(sum(self.gsr_buffer)/len(self.gsr_buffer), 3),
            "device_serial_id": self.config.get("device_serial_id"),
            "device_password": self.config.get("device_password")
        }

    def send_to_server(self, payload):
        try:
            res = requests.post(self.server_url, json=payload, timeout=5)
            if res.status_code == 201:
                print(f"[SENT] {self.current_state} | HRV: {payload['hrv_raw']} | GSR: {payload['gsr_raw']}")
            else:
                print(f"[FAIL] Server returned {res.status_code}")
        except Exception as e:
            print(f"[ERROR] {e}")

    def run(self):
        print(f"--- IoT Simulation Started ({self.config.get('device_serial_id')}) ---")
        while True:
            if self.config.check_for_updates():
                self._sync_settings()
            
            self.send_to_server(self._process_data())
            time.sleep(self.interval)


if __name__ == "__main__":
    SmartBandDevice(ConfigManager()).run()

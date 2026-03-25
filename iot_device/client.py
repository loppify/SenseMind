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
                "smoothing_window": 3,
                "device_serial_id": "SN-001",
                "device_password": "device-secret-pass"
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

        self.file_path = file_path
        self._dataframe = None
        
        self.current_hrv = DEFAULT_HRV
        self.current_gsr = DEFAULT_GSR
        self.target_hrv = DEFAULT_HRV
        self.target_gsr = DEFAULT_GSR
        self.current_state = "Neutral"

        self._load_dataset_initial()

    def _load_dataset_initial(self):
        """Loads a single random row from dataset to act as the baseline biological state"""
        if os.path.exists(self.file_path):
            try:
                df = pd.read_csv(self.file_path)
                self._dataframe = df.dropna(subset=[COL_HRV, COL_GSR])
                if not self._dataframe.empty:
                    row = self._dataframe.sample(n=1).iloc[0]
                    self.current_hrv = float(row[COL_HRV])
                    self.current_gsr = float(row[COL_GSR])
                print(f"[SIMULATION] Initial biological baseline loaded: HRV={self.current_hrv:.1f}, GSR={self.current_gsr:.2f}")
            except Exception as e:
                print(f"Error loading dataset: {e}")
        else:
            print(f"Warning: Dataset not found at {self.file_path}. Using hardcoded defaults.")
            
        self.target_hrv = self.current_hrv
        self.target_gsr = self.current_gsr

    def _simulate_human_biology(self):
        """Chance-stained system mimicking real physiological state changes"""
        # 10% chance on each tick to randomly change psychological state
        if random.random() < 0.10:
            chance = random.random()
            if chance < 0.3:
                self.current_state = "Stressed"
                self.target_hrv = random.uniform(20.0, 45.0)  # HRV drops during stress
                self.target_gsr = random.uniform(4.0, 8.0)    # GSR (sweating) rises
            elif chance < 0.6:
                self.current_state = "Relaxed"
                self.target_hrv = random.uniform(65.0, 95.0)  # High HRV means relaxed
                self.target_gsr = random.uniform(0.5, 2.5)    # Low GSR
            else:
                self.current_state = "Focused/Neutral"
                self.target_hrv = random.uniform(50.0, 70.0)
                self.target_gsr = random.uniform(2.0, 4.0)
                
            print(f"[SIMULATION EVENT] User state shifted to {self.current_state}")

        # Interpolate current values towards the target (creates smooth biological transitions)
        hrv_step = (self.target_hrv - self.current_hrv) * 0.15
        gsr_step = (self.target_gsr - self.current_gsr) * 0.15

        # Add biological noise (jitter) on every single tick
        self.current_hrv += hrv_step + random.uniform(-1.5, 1.5)
        self.current_gsr += gsr_step + random.uniform(-0.15, 0.15)

        # Clamp values to extreme biological limits
        self.current_hrv = max(10.0, min(150.0, self.current_hrv))
        self.current_gsr = max(0.1, min(20.0, self.current_gsr))

    def _process_data(self):
        self._simulate_human_biology()
        
        self.hrv_buffer.append(self.current_hrv)
        self.gsr_buffer.append(self.current_gsr)

        avg_hrv = sum(self.hrv_buffer) / len(self.hrv_buffer)
        avg_gsr = sum(self.gsr_buffer) / len(self.gsr_buffer)

        return {
            "hrv_raw": round(avg_hrv, 2),
            "gsr_raw": round(avg_gsr, 3),
            "device_serial_id": self.config.get("device_serial_id"),
            "device_password": self.config.get("device_password"),
            "timestamp": time.time()
        }

    def send_to_server(self, processed_data):
        try:
            response = requests.post(self.server_url, json=processed_data)
            if response.status_code == 201:
                print(f"[SUCCESS] Data sent: HRV={processed_data['hrv_raw']} | GSR={processed_data['gsr_raw']}")
            elif response.status_code == 401:
                print(f"[WARNING] 401 Unauthorized. Check device_serial_id or device_password!")
            else:
                print(f"[WARNING] Server error: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")

    def run(self):
        print("--- IoT Device Started ---")
        print(f"Target Server: {self.server_url}")

        while True:
            payload = self._process_data()
            self.send_to_server(payload)
            time.sleep(self.interval)


if __name__ == "__main__":
    cfg = ConfigManager()
    device = SmartBandDevice(cfg)
    device.run()

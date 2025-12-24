import os
import joblib
import pandas as pd
from core_engine.database.db_storage import create_state_record, create_recommendation_log

MODEL_FILENAME = 'sensemind_model.pkl'
BASE_DIR = os.getcwd()
MODEL_PATH = os.path.join(BASE_DIR, "core_engine", "models", MODEL_FILENAME)

STATE_STRESSED = "Stressed"
STATE_ANXIOUS = "Anxious"
STATE_RELAXED = "Relaxed"
STATE_FOCUSED = "Focused"
STATE_UNKNOWN = "Unknown"


class EmotionClassifier:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                return joblib.load(self.model_path)
            except Exception as e:
                print(f"Error loading model: {e}")
                return None
        else:
            print(f"Warning: Model file not found at {self.model_path}")
            return None

    def predict(self, hrv: float, gsr: float) -> str:
        if self.model:
            features = pd.DataFrame([[hrv, gsr]], columns=['HRV (ms)', 'GSR (μS)'])
            try:
                prediction = self.model.predict(features)
                return prediction[0]
            except Exception as e:
                print(f"Prediction error: {e}")
                return STATE_UNKNOWN

        if hrv < 40:
            return STATE_STRESSED
        return STATE_RELAXED


classifier_service = EmotionClassifier(MODEL_PATH)


def generate_recommendation(state: str) -> str:
    recommendations = {
        STATE_STRESSED: "Виявлено стрес. Зробіть дихальні вправи.",
        STATE_ANXIOUS: "Виявлено тривожність. Спробуйте техніку заземлення.",
        STATE_RELAXED: "Стан стабільний. Продовжуйте в тому ж дусі.",
        STATE_FOCUSED: "Чудова концентрація!",
        STATE_UNKNOWN: "Рівень показників у нормі."
    }
    return recommendations.get(state, "Рівень показників у нормі.")


def process_and_store_data(raw_data: dict, session_id: str) -> dict:
    hrv = raw_data.get("hrv_raw", 60.0)
    gsr = raw_data.get("gsr_raw", 1.0)

    state = classifier_service.predict(hrv, gsr)

    record = create_state_record(session_id, state, hrv, gsr)

    rec_text = generate_recommendation(state)
    create_recommendation_log(record["record_id"], rec_text)

    return record

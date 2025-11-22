import joblib
import os
import pandas as pd
from core_engine.database.db_storage import create_state_record, create_recommendation_log

MODEL_PATH = 'sensemind_model.pkl'
_model = None


def load_model():
    global _model
    if os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)


load_model()


def classify_state_logic(hrv: float, gsr: float) -> str:
    global _model
    if _model:
        df = pd.DataFrame([[hrv, gsr]], columns=['HRV (ms)', 'GSR (μS)'])
        return _model.predict(df)[0]

    if hrv < 40: return "Stressed"
    return "Relaxed"


def generate_recommendation(state: str) -> str:
    if state == "Stressed" or state == "Anxious":
        return "Виявлено стрес. Зробіть дихальні вправи."
    elif state == "Relaxed":
        return "Стан стабільний. Продовжуйте в тому ж дусі."
    elif state == "Focused":
        return "Чудова концентрація!"
    return "Рівень показників у нормі."


def process_and_store_data(raw_data: dict, session_id: str):
    hrv = raw_data.get("hrv_raw", 60.0)
    gsr = raw_data.get("gsr_raw", 1.0)

    state = classify_state_logic(hrv, gsr)

    record = create_state_record(session_id, state, hrv, gsr)
    rec_text = generate_recommendation(state)
    create_recommendation_log(record["record_id"], rec_text)

    return record

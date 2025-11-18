from core_engine.database.db_storage import create_state_record, create_recommendation_log


def classify_state_logic(hrv: float, gsr: float) -> str:
    if hrv < 40 and gsr > 2.0:
        return "Stress"
    elif hrv > 60 and gsr < 1.5:
        return "Calm"
    else:
        return "Focus"


def generate_recommendation(state: str) -> str:
    if state == "Stress":
        return "Виявлено стрес. Зробіть дихальні вправи."
    elif state == "Calm":
        return "Стан стабільний. Продовжуйте в тому ж дусі."
    return "Рівень концентрації в нормі."


def process_and_store_data(raw_data: dict, session_id: str):
    hrv = raw_data["hrv_raw"]
    gsr = raw_data["gsr_raw"]

    state = classify_state_logic(hrv, gsr)

    record = create_state_record(session_id, state, hrv, gsr)

    rec_text = generate_recommendation(state)
    create_recommendation_log(record["record_id"], rec_text)

    return record
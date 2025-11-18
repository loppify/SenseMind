import uuid
from datetime import datetime

STATE_RECORDS_IN_MEMORY = []
RECOMMENDATION_LOG_IN_MEMORY = []


def create_state_record(session_id: str, classified_state: str, hrv_score: float, gsr_score: float) -> dict:
    record_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    new_record = {
        "record_id": record_id,
        "session_id": session_id,
        "timestamp": timestamp,
        "classified_state": classified_state,
        "hrv_score": hrv_score,
        "gsr_score": gsr_score
    }

    STATE_RECORDS_IN_MEMORY.append(new_record)
    return new_record


def create_recommendation_log(record_id: str, text: str) -> dict:
    log_id = str(uuid.uuid4())

    new_log = {
        "log_id": log_id,
        "record_id": record_id,
        "recommendation_text": text
    }

    RECOMMENDATION_LOG_IN_MEMORY.append(new_log)
    return new_log


def get_latest_record() -> dict or None:
    if STATE_RECORDS_IN_MEMORY:
        return STATE_RECORDS_IN_MEMORY[-1]
    return None


def get_records_by_time(limit: int = 60) -> list:
    return STATE_RECORDS_IN_MEMORY[-limit:]

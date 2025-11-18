import uuid
from datetime import datetime

STATE_RECORDS_IN_MEMORY = []


def create_state_record(session_id: str, classified_state: str, hrv_score: float, gsr_score: float) -> dict:
    """Створює та зберігає новий запис стану в імітованій БД."""
    new_record = {
        "record_id": str(uuid.uuid4()),
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "classified_state": classified_state,
        "hrv_score": hrv_score,
        "gsr_score": gsr_score
    }
    STATE_RECORDS_IN_MEMORY.append(new_record)
    return new_record


def get_latest_record() -> dict or None:
    """Повертає останній запис стану (імітація SELECT)."""
    if STATE_RECORDS_IN_MEMORY:
        return STATE_RECORDS_IN_MEMORY[-1]
    return None


def get_records_by_time(limit: int = 60) -> list:
    """Повертає останні записи для побудови графіка трендів."""
    return STATE_RECORDS_IN_MEMORY[-limit:]


def test_db_interaction(session_id: str):
    """Тестування взаємодії: Запис -> Читання."""
    record = create_state_record(
        session_id=session_id,
        classified_state="Testing_Stress",
        hrv_score=35.5,
        gsr_score=0.9
    )
    latest = get_latest_record()
    if latest and latest["classified_state"] == "Testing_Stress":
        print(f"✅ БД Test PASS: Записано та прочитано запис {latest['record_id']}")
    else:
        print("❌ БД Test FAIL")


if __name__ == "__main__":
    print("--- Перевірка функцій роботи з БД ---")
    test_db_interaction("TestSession123")

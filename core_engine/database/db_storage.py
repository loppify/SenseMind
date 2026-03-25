from core_engine.database.models import db, StateRecord, RecommendationLog, Device
from datetime import datetime

def create_state_record(device_id: int, classified_state: str, hrv_score: float, gsr_score: float) -> dict:
    new_record = StateRecord(
        device_id=device_id,
        classified_state=classified_state,
        hrv_score=hrv_score,
        gsr_score=gsr_score
    )
    db.session.add(new_record)
    db.session.commit()
    
    return {
        "record_id": new_record.id,
        "device_id": new_record.device_id,
        "timestamp": new_record.timestamp.isoformat(),
        "classified_state": new_record.classified_state,
        "hrv_score": new_record.hrv_score,
        "gsr_score": new_record.gsr_score
    }

def create_recommendation_log(record_id: int, text: str) -> dict:
    new_log = RecommendationLog(
        record_id=record_id,
        recommendation_text=text
    )
    db.session.add(new_log)
    db.session.commit()
    
    return {
        "log_id": new_log.id,
        "record_id": new_log.record_id,
        "recommendation_text": new_log.recommendation_text
    }

def get_recommendation_for_record(record_id: int) -> str or None:
    log = RecommendationLog.query.filter_by(record_id=record_id).first()
    return log.recommendation_text if log else None

def get_latest_record_for_device(device_id: int) -> dict or None:
    latest_record = StateRecord.query.filter_by(device_id=device_id).order_by(StateRecord.timestamp.desc()).first()
    
    if latest_record is None:
        return None

    recommendation = get_recommendation_for_record(latest_record.id)
    
    return {
        "timestamp": latest_record.timestamp.isoformat(),
        "classified_state": latest_record.classified_state,
        "hrv_score": latest_record.hrv_score,
        "gsr_score": latest_record.gsr_score,
        "recommendation": recommendation if recommendation else "No recommendation found"
    }

def get_records_by_device(device_id: int, limit: int = 60) -> list:
    records = StateRecord.query.filter_by(device_id=device_id).order_by(StateRecord.timestamp.desc()).limit(limit).all()
    return [
        {
            "timestamp": r.timestamp.isoformat(),
            "classified_state": r.classified_state,
            "hrv_score": r.hrv_score,
            "gsr_score": r.gsr_score
        } for r in records
    ]

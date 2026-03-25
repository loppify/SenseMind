import os
from flask import Blueprint, jsonify, request
from core_engine.database.models import db, StateRecord, RecommendationLog
import dotenv

admin_bp = Blueprint('admin_v1', __name__)

dotenv.load_dotenv()
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN')


def check_admin_auth():
    token = request.headers.get("X-Admin-Token")
    if token != ADMIN_TOKEN:
        return False
    return True


@admin_bp.route('/export/data', methods=['GET'])
def export_system_data():
    """
        Експорт усіх даних системи (Адмін)
        ---
        tags:
          - Адміністрування
        security:
          - APIKeyHeader: []
        description: Повертає всі записи станів та логів рекомендацій з бази даних.
        responses:
          200:
            description: Повний пакет даних системи
          401:
            description: Помилка авторизації (Unauthorized)
    """
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    records = StateRecord.query.all()
    logs = RecommendationLog.query.all()

    export_package = {
        "state_records": [
            {
                "id": r.id,
                "device_id": r.device_id,
                "timestamp": r.timestamp.isoformat(),
                "classified_state": r.classified_state,
                "hrv_score": r.hrv_score,
                "gsr_score": r.gsr_score
            } for r in records
        ],
        "logs": [
            {
                "id": l.id,
                "record_id": l.record_id,
                "recommendation_text": l.recommendation_text,
                "created_at": l.created_at.isoformat()
            } for l in logs
        ],
        "record_count": len(records)
    }

    return jsonify(export_package), 200


@admin_bp.route('/system/clear', methods=['DELETE'])
def clear_system_data():
    """
        Очищення системи (Адмін)
        ---
        tags:
          - Адміністрування
        security:
          - APIKeyHeader: []
        description: Видаляє всі поточні записи станів та рекомендацій з бази даних.
        responses:
          200:
            description: Дані успішно видалені
          401:
            description: Помилка авторизації
    """
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    try:
        db.session.query(RecommendationLog).delete()
        db.session.query(StateRecord).delete()
        db.session.commit()
        return jsonify({"message": "System data cleared successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

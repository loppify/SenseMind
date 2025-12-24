from flask import Blueprint, jsonify, request
from core_engine.database.db_storage import get_records_by_time, \
    get_latest_record_with_recommendation
from core_engine.services.ml_classifier import process_and_store_data

api_bp = Blueprint('api_v1', __name__)

CURRENT_SESSION_ID = "SESSION_DEMO_001"


@api_bp.route('/status/current', methods=['GET'])
def get_current_status():
    """
        Отримати останній класифікований стан та рекомендацію
        ---
        tags:
          - Аналітика
        responses:
          200:
            description: Повертає останній запис стану SenseMind
            schema:
              id: StateRecord
              properties:
                classified_state:
                  type: string
                  example: Stress
                recommendation:
                  type: string
                  example: Try deep breathing exercises.
        """
    latest_record = get_latest_record_with_recommendation()
    if latest_record:
        response = latest_record.copy()
        del response['record_id']
        del response['session_id']
        return jsonify(response), 200

    return jsonify({
        "status": "waiting_for_data",
        "message": "No data received from IoT device yet."
    }), 404


@api_bp.route('/history/last_hour', methods=['GET'])
def get_history():
    """
        Отримати історію станів за останню годину
        ---
        tags:
          - Аналітика
        responses:
          200:
            description: Список записів станів (без технічних ID) за останні 60 хвилин
            schema:
              type: array
              items:
                properties:
                  timestamp:
                    type: string
                    example: "2025-11-24T15:30:00Z"
                  classified_state:
                    type: string
                    example: "Stress"
                  hrv_score:
                    type: number
                    example: 55.4
                  gsr_score:
                    type: number
                    example: 0.12
        """
    history = get_records_by_time(limit=60)
    cleaned_history = []

    for record in history:
        rec_copy = record.copy()
        del rec_copy['record_id']
        del rec_copy['session_id']
        cleaned_history.append(rec_copy)

    return jsonify(cleaned_history), 200


@api_bp.route('/data/raw', methods=['POST'])
def receive_raw_data():
    """
        Передати сирі дані для обробки та класифікації
        ---
        tags:
          - Обробка даних
        parameters:
          - in: body
            name: body
            required: true
            schema:
              properties:
                hrv_raw:
                  type: number
                  description: Сирий показник HRV
                  example: 65.2
                gsr_raw:
                  type: number
                  description: Сирий показник GSR
                  example: 0.45
        responses:
          201:
            description: Дані успішно оброблені
            schema:
              properties:
                message:
                  type: string
                  example: "Data processed"
                record_id:
                  type: string
                  example: "uuid-v4-identifier"
                classified_state:
                  type: string
                  description: Результат класифікації ML-моделі
                  example: "Calm"
          400:
            description: Порожній або невалідний запит
        """
    data = request.json
    if not data:
        return jsonify({"error": "Empty payload"}), 400
    saved_record = process_and_store_data(data, CURRENT_SESSION_ID)

    return jsonify({
        "message": "Data processed",
        "record_id": saved_record['record_id'],
        "classified_state": saved_record['classified_state'],
    }), 201

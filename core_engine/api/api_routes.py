from flask import Blueprint, jsonify, request
from core_engine.database.db_storage import get_latest_record, get_records_by_time
from core_engine.services.ml_classifier import process_and_store_data

api_bp = Blueprint('api_v1', __name__)

CURRENT_SESSION_ID = "SESSION_DEMO_001"


@api_bp.route('/status/current', methods=['GET'])
def get_current_status():
    latest_record = get_latest_record()
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
    data = request.json
    if not data:
        return jsonify({"error": "Empty payload"}), 400
    saved_record = process_and_store_data(data, CURRENT_SESSION_ID)
    process_and_store_data(data, CURRENT_SESSION_ID)
    return jsonify({
        "message": "Data processed",
        "record_id": saved_record['record_id'],
        "classified_state": saved_record['classified_state']
    }), 201

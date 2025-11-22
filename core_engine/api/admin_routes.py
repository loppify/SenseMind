from flask import Blueprint, jsonify, request
from core_engine.database.db_storage import STATE_RECORDS_IN_MEMORY, RECOMMENDATION_LOG_IN_MEMORY

admin_bp = Blueprint('admin_v1', __name__)

ADMIN_TOKEN = "SECRET_ADMIN_123"


def check_admin_auth():
    token = request.headers.get("X-Admin-Token")
    if token != ADMIN_TOKEN:
        return False
    return True


@admin_bp.route('/export/data', methods=['GET'])
def export_system_data():
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    export_package = {
        "state_records": STATE_RECORDS_IN_MEMORY,
        "logs": RECOMMENDATION_LOG_IN_MEMORY,
        "record_count": len(STATE_RECORDS_IN_MEMORY)
    }

    return jsonify(export_package), 200


@admin_bp.route('/system/clear', methods=['DELETE'])
def clear_system_data():
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    STATE_RECORDS_IN_MEMORY.clear()
    RECOMMENDATION_LOG_IN_MEMORY.clear()

    return jsonify({"message": "System data cleared successfully"}), 200
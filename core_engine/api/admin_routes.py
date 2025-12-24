import os

from flask import Blueprint, jsonify, request
from core_engine.database.db_storage import STATE_RECORDS_IN_MEMORY, RECOMMENDATION_LOG_IN_MEMORY
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
        description: Повертає всі записи станів та логів рекомендацій, що зберігаються в пам'яті.
        responses:
          200:
            description: Повний пакет даних системи
            schema:
              properties:
                state_records:
                  type: array
                  items:
                    $ref: '#/definitions/StateRecord'
                logs:
                  type: array
                  items:
                    properties:
                      log_id: {type: string}
                      recommendation_text: {type: string}
                record_count:
                  type: integer
                  example: 15
          401:
            description: Помилка авторизації (Unauthorized)
        """
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
    """
        Очищення пам'яті системи (Адмін)
        ---
        tags:
          - Адміністрування
        security:
          - APIKeyHeader: []
        description: Видаляє всі поточні записи станів та рекомендацій. Використовується для скидання сесії.
        responses:
          200:
            description: Дані успішно видалені
            schema:
              properties:
                message:
                  type: string
                  example: "System data cleared successfully"
          401:
            description: Помилка авторизації
        """
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    STATE_RECORDS_IN_MEMORY.clear()
    RECOMMENDATION_LOG_IN_MEMORY.clear()

    return jsonify({"message": "System data cleared successfully"}), 200

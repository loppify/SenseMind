from flask import Flask, jsonify
from core_engine.database.db_storage import get_latest_record, get_records_by_time
from core_engine.services.ml_classifier import classify_new_data
from core_engine.data_source.data_simulator import get_simulated_data

app = Flask(__name__)
SESSION_ID = "DEMO_SESSION_001"


@app.route('/api/v1/status/current', methods=['GET'])
def get_current_status():
    """Endpoint для отримання поточного класифікованого стану."""

    # 1. Імітуємо отримання нових даних
    simulated_raw_data = get_simulated_data()

    # 2. Обробка та класифікація
    # (Ця функція повинна викликати БД-функцію всередині)
    classify_new_data(simulated_raw_data, SESSION_ID)

    # 3. Отримання останнього результату з БД
    latest_record = get_latest_record()

    if latest_record:
        # Видаляємо внутрішні технічні поля для чистоти API
        del latest_record['record_id']
        del latest_record['session_id']
        return jsonify(latest_record), 200

    return jsonify({"error": "No data records found."}), 404


@app.route('/api/v1/history/last_hour', methods=['GET'])
def get_history():
    """Endpoint для отримання історії записів для графіків трендів."""
    history = get_records_by_time(limit=60)
    return jsonify(history), 200


if __name__ == '__main__':
    # Сюди можна додати ініціалізацію, наприклад, перше читання датасету
    app.run(debug=True, port=5000)
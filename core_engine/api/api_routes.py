from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from core_engine.database.db_storage import get_records_by_device, \
    get_latest_record_for_device
from core_engine.database.models import Device
from core_engine.services.ml_classifier import process_and_store_data

api_bp = Blueprint('api_v1', __name__)

@api_bp.route('/status/current/<int:device_id>', methods=['GET'])
@jwt_required()
def get_current_status(device_id):
    """
        Get latest state and recommendation for a device
        ---
        tags:
          - Analytics
        security:
          - APIKeyHeader: []
        responses:
          200:
            description: Returns last record
          404:
            description: No data
    """
    user_id = int(get_jwt_identity())
    device = Device.query.filter_by(id=device_id, user_id=user_id).first()
    if not device:
        return jsonify({"error": "Device not found or access denied"}), 404
        
    latest_record = get_latest_record_for_device(device.id)
    if latest_record:
        return jsonify(latest_record), 200

    return jsonify({
        "status": "waiting_for_data",
        "message": "No data received from IoT device yet."
    }), 404

@api_bp.route('/history/<int:device_id>', methods=['GET'])
@jwt_required()
def get_history(device_id):
    """
        Get last 60 records for a device
        ---
        tags:
          - Analytics
        security:
          - APIKeyHeader: []
    """
    user_id = int(get_jwt_identity())
    device = Device.query.filter_by(id=device_id, user_id=user_id).first()
    if not device:
        return jsonify({"error": "Device not found"}), 404
        
    history = get_records_by_device(device.id, limit=60)
    return jsonify(history), 200

@api_bp.route('/data/raw', methods=['POST'])
def receive_raw_data():
    """
        Submit raw data from device
        ---
        tags:
          - Data Collection
        parameters:
          - in: body
            name: body
            schema:
              properties:
                device_serial_id: {type: string}
                device_password: {type: string}
                hrv_raw: {type: number}
                gsr_raw: {type: number}
    """
    data = request.json
    if not data or 'device_serial_id' not in data or 'device_password' not in data:
        return jsonify({"error": "Missing device credentials"}), 400
        
    device = Device.query.filter_by(device_serial_id=data['device_serial_id']).first()
    if not device or not device.check_password(data['device_password']):
        return jsonify({"error": "Unauthorized device"}), 401
        
    saved_record = process_and_store_data(data, device.id)

    return jsonify({
        "message": "Data processed",
        "record_id": saved_record['record_id'],
        "classified_state": saved_record['classified_state'],
    }), 201

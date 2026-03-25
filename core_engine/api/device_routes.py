from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from core_engine.database.models import db, Device, User

device_bp = Blueprint('devices', __name__)

@device_bp.route('/register', methods=['POST'])
@jwt_required()
def register_device():
    """
    Register a new device for current user
    ---
    tags:
      - Devices
    security:
      - APIKeyHeader: []
    parameters:
      - in: body
        name: body
        schema:
          properties:
            device_serial_id: {type: string}
            name: {type: string}
            device_password: {type: string}
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if Device.query.filter_by(device_serial_id=data['device_serial_id']).first():
        return jsonify({"msg": "Device already registered"}), 400
    
    device = Device(
        device_serial_id=data['device_serial_id'],
        name=data.get('name', 'My Device'),
        user_id=user_id
    )
    device.set_password(data['device_password'])
    db.session.add(device)
    db.session.commit()
    return jsonify({"msg": "Device registered", "id": device.id}), 201

@device_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_devices():
    """
    List current user's devices
    ---
    tags:
      - Devices
    security:
      - APIKeyHeader: []
    """
    user_id = int(get_jwt_identity())
    devices = Device.query.filter_by(user_id=user_id).all()
    return jsonify([
        {"id": d.id, "device_serial_id": d.device_serial_id, "name": d.name} 
        for d in devices
    ]), 200

@device_bp.route('/<int:device_id>/change-password', methods=['PUT'])
@jwt_required()
def change_device_password(device_id):
    """
    Change device password
    ---
    tags:
      - Devices
    security:
      - APIKeyHeader: []
    parameters:
      - in: body
        name: body
        schema:
          properties:
            new_password: {type: string}
    """
    user_id = int(get_jwt_identity())
    device = Device.query.filter_by(id=device_id, user_id=user_id).first()
    if not device:
        return jsonify({"msg": "Device not found"}), 404
    
    data = request.get_json()
    device.set_password(data['new_password'])
    db.session.commit()
    return jsonify({"msg": "Password changed"}), 200

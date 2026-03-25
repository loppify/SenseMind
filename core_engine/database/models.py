from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    devices = db.relationship('Device', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = sha256.hash(password)

    def check_password(self, password):
        return sha256.verify(password, self.password_hash)

class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    device_serial_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    records = db.relationship('StateRecord', backref='device', lazy=True)

    def set_password(self, password):
        self.password_hash = sha256.hash(password)

    def check_password(self, password):
        return sha256.verify(password, self.password_hash)

class StateRecord(db.Model):
    __tablename__ = 'state_records'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    classified_state = db.Column(db.String(50))
    hrv_score = db.Column(db.Float)
    gsr_score = db.Column(db.Float)
    
    recommendations = db.relationship('RecommendationLog', backref='record', lazy=True)

class RecommendationLog(db.Model):
    __tablename__ = 'recommendation_logs'
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('state_records.id'), nullable=False)
    recommendation_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

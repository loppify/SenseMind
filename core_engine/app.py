import os
from datetime import timedelta

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from core_engine.api.admin_routes import admin_bp
from core_engine.api.api_routes import api_bp
from core_engine.api.auth_routes import auth_bp
from core_engine.api.device_routes import device_bp
from core_engine.database.models import db
from waitress import serve

load_dotenv()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///sensemind.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

with app.app_context():
    try:
        db.create_all()
        print("Database sync: Tables checked/created successfully.")
    except Exception as e:
        print(f"Database sync skipped or failed: {e}")

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda model: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "securityDefinitions": {
        "APIKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Bearer <JWT Token>"
        }
    }
}
swagger = Swagger(app, config=swagger_config)

app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(device_bp, url_prefix='/api/v1/devices')
app.register_blueprint(api_bp, url_prefix='/api/v1')
app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if os.getenv('FLASK_DEBUG') == '1':
        app.run(debug=True, host='0.0.0.0', port=port)
    else:
        print(f"Starting waitress server on http://0.0.0.0:{port}")
        serve(app, host='0.0.0.0', port=port)

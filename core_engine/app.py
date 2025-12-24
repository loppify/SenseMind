from flask import Flask
from flasgger import Swagger
from core_engine.api.admin_routes import admin_bp
from core_engine.api.api_routes import api_bp

app = Flask(__name__)

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
            "name": "X-Admin-Token",
            "description": "Введіть ваш адмін-пароль або токен у форматі: <token>"
        }
    }
}
swagger = Swagger(app, config=swagger_config)

app.register_blueprint(api_bp, url_prefix='/api/v1')
app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

from flask import Flask

from core_engine.api.admin_routes import admin_bp
from core_engine.api.api_routes import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix='/api/v1')
app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

if __name__ == '__main__':
    print("Starting SenseMind Server...")
    print("API available at http://127.0.0.1:5000/api/v1/status/current")
    app.run(debug=True, port=5000)

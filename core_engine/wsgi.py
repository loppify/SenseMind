import os

from core_engine.app import app

if __name__ == "__main__":
    from waitress import serve

    port = int(os.environ.get("PORT", 5000))
    print(f"Starting SenseMind WSGI Server on 0.0.0.0:{port}")
    serve(app, host='0.0.0.0', port=port)

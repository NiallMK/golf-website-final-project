# app.py
from flask import Flask
from routes.bookings import bookings_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(bookings_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return {"status": "Golf API running"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)

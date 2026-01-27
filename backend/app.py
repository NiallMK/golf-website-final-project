# app.py
from flask import Flask
from flask_cors import CORS

from routes.bookings import bookings_bp
from routes.rounds import rounds_bp
from routes.handicap import handicap_bp
from routes.courses import courses_bp
from routes.users import users_bp


def create_app():
    app = Flask(__name__)

    # ✅ ENABLE CORS (this fixes Angular)
    CORS(app)

    app.register_blueprint(bookings_bp, url_prefix="/api")
    app.register_blueprint(rounds_bp, url_prefix="/api")
    app.register_blueprint(handicap_bp, url_prefix="/api")
    app.register_blueprint(courses_bp, url_prefix="/api")
    app.register_blueprint(users_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return {"status": "Golf API running"}

    @app.route("/debug/routes")
    def debug_routes():
        return str(app.url_map)

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)

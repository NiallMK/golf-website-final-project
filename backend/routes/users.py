from flask import Blueprint, jsonify
from db import get_db

users_bp = Blueprint("users", __name__)

@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("""
            SELECT id, name, email, current_handicap
            FROM users
            WHERE id = ?
        """, (user_id,))
        user = cur.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(dict(user)), 200
    finally:
        db.close()

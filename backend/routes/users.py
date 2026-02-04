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

@users_bp.route("/users/<int:user_id>/profile", methods=["GET"])
def get_user_profile(user_id):
    db = get_db()
    try:
        cur = db.cursor()

        # Basic user info
        cur.execute("""
            SELECT name, current_handicap
            FROM users
            WHERE id = ?
        """, (user_id,))
        user = cur.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Round counts
        cur.execute("""
            SELECT
              COUNT(*) AS total,
              SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) AS completed
            FROM rounds
            WHERE user_id = ?
        """, (user_id,))
        stats = cur.fetchone()

        return jsonify({
            "name": user["name"],
            "current_handicap": user["current_handicap"],
            "total_rounds": stats["total"],
            "completed_rounds": stats["completed"],
            "in_progress_rounds": stats["total"] - stats["completed"]
        }), 200

    finally:
        db.close()
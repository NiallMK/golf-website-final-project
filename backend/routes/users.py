from flask import Blueprint, jsonify, session
from db import get_db
from .auth_utils import login_required

users_bp = Blueprint("users", __name__)

# -------------------------------------------------
# GET CURRENT USER PROFILE (LOGGED-IN USER ONLY)
# -------------------------------------------------
@users_bp.route("/users/profile", methods=["GET"])
@login_required
def get_user_profile():
    user_id = session["user_id"]

    db = get_db()
    try:
        cur = db.cursor()

        # -------------------------------
        # Basic user info
        # -------------------------------
        cur.execute("""
            SELECT name, email, current_handicap
            FROM users
            WHERE id = ?
        """, (user_id,))
        user = cur.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        # -------------------------------
        # Round statistics
        # -------------------------------
        cur.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) AS completed
            FROM rounds
            WHERE user_id = ?
        """, (user_id,))
        stats = cur.fetchone()

        total_rounds = stats["total"]
        completed_rounds = stats["completed"] or 0
        in_progress_rounds = total_rounds - completed_rounds

        return jsonify({
            "name": user["name"],
            "email": user["email"],
            "current_handicap": user["current_handicap"],
            "total_rounds": total_rounds,
            "completed_rounds": completed_rounds,
            "in_progress_rounds": in_progress_rounds
        }), 200

    finally:
        db.close()

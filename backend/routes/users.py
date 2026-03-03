from flask import Blueprint, jsonify, session, request
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

@users_bp.route("/admin/users", methods=["GET"])
def get_all_users():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    try:
        cur = db.cursor()

        cur.execute(
            "SELECT role FROM users WHERE id = ?",
            (session["user_id"],)
        )
        current_user = cur.fetchone()

        if not current_user or current_user["role"] != "admin":
            return jsonify({"error": "Forbidden"}), 403

        cur.execute("SELECT id, name, email, role FROM users")
        rows = cur.fetchall()

        return jsonify([dict(row) for row in rows])

    finally:
        db.close()

@users_bp.route("/admin/users/<int:user_id>/role", methods=["PUT"])
def update_user_role(user_id):

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    try:
        cur = db.cursor()

        cur.execute(
            "SELECT role FROM users WHERE id = ?",
            (session["user_id"],)
        )
        current_user = cur.fetchone()

        if not current_user or current_user["role"] != "admin":
            return jsonify({"error": "Forbidden"}), 403

        data = request.get_json()
        new_role = data.get("role")

        if new_role not in ["admin", "user"]:
            return jsonify({"error": "Invalid role"}), 400

        cur.execute(
            "UPDATE users SET role = ? WHERE id = ?",
            (new_role, user_id)
        )

        db.commit()

        return jsonify({"message": "Role updated"}), 200

    finally:
        db.close()

@users_bp.route("/admin/stats", methods=["GET"])
def admin_stats():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    try:
        cur = db.cursor()

        cur.execute(
            "SELECT role FROM users WHERE id = ?",
            (session["user_id"],)
        )
        current_user = cur.fetchone()

        if not current_user or current_user["role"] != "admin":
            return jsonify({"error": "Forbidden"}), 403

        cur.execute("SELECT COUNT(*) as count FROM users")
        users_count = cur.fetchone()["count"]

        cur.execute("SELECT COUNT(*) as count FROM courses")
        courses_count = cur.fetchone()["count"]

        cur.execute("SELECT COUNT(*) as count FROM rounds")
        rounds_count = cur.fetchone()["count"]

        cur.execute("SELECT COUNT(*) as count FROM bookings")
        bookings_count = cur.fetchone()["count"]

        return jsonify({
            "users": users_count,
            "courses": courses_count,
            "rounds": rounds_count,
            "bookings": bookings_count
        })

    finally:
        db.close()

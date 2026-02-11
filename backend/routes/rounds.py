from flask import Blueprint, request, jsonify, session
from db import get_db
from .auth_utils import login_required


rounds_bp = Blueprint("rounds", __name__)

# -------------------------------------------------
# CREATE ROUND FROM BOOKING
# -------------------------------------------------
@rounds_bp.route("/rounds", methods=["POST"])
@login_required
def create_round():
    data = request.get_json()
    booking_id = data.get("booking_id")

    if not booking_id:
        return jsonify({"error": "booking_id is required"}), 400

    user_id = session["user_id"]

    db = get_db()
    try:
        cur = db.cursor()

        # Get booking (must belong to logged-in user)
        cur.execute("""
            SELECT t.course_id, t.id AS teetime_id
            FROM bookings b
            JOIN tee_times t ON t.id = b.teetime_id
            WHERE b.id = ? AND b.user_id = ?
        """, (booking_id, user_id))

        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Booking not found"}), 404

        course_id = row["course_id"]
        teetime_id = row["teetime_id"]

        # Handicap snapshot
        cur.execute(
            "SELECT current_handicap FROM users WHERE id = ?",
            (user_id,)
        )
        h = cur.fetchone()
        handicap = h["current_handicap"] if h else None

        cur.execute("""
            INSERT INTO rounds (
                user_id,
                course_id,
                teetime_id,
                date_played,
                handicap_at_time
            )
            VALUES (?, ?, ?, date('now'), ?)
        """, (user_id, course_id, teetime_id, handicap))

        db.commit()

        return jsonify({
            "round_id": cur.lastrowid,
            "type": "booked"
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()

# -------------------------------------------------
# CREATE MANUAL ROUND (NO BOOKING)
# -------------------------------------------------
@rounds_bp.route("/rounds/manual", methods=["POST"])
@login_required
def create_manual_round():
    data = request.get_json()

    user_id = session["user_id"]
    course_id = data.get("course_id")
    date_played = data.get("date_played")

    if not course_id or not date_played:
        return jsonify({
            "error": "course_id and date_played are required"
        }), 400

    db = get_db()
    try:
        cur = db.cursor()

        cur.execute(
            "SELECT current_handicap FROM users WHERE id = ?",
            (user_id,)
        )
        h = cur.fetchone()
        handicap = h["current_handicap"] if h else None

        cur.execute("""
            INSERT INTO rounds (
                user_id,
                course_id,
                date_played,
                handicap_at_time
            )
            VALUES (?, ?, ?, ?)
        """, (user_id, course_id, date_played, handicap))

        db.commit()

        return jsonify({
            "round_id": cur.lastrowid,
            "type": "manual"
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()

# -------------------------------------------------
# SUBMIT HOLE SCORES FOR A ROUND
# -------------------------------------------------
@rounds_bp.route("/rounds/<int:round_id>/scores", methods=["POST"])
@login_required
def submit_scores(round_id):
    user_id = session["user_id"]
    data = request.get_json()
    scores = data.get("scores")

    if not scores or not isinstance(scores, list):
        return jsonify({"error": "scores list required"}), 400

    db = get_db()
    try:
        cur = db.cursor()

        cur.execute("""
            SELECT id, is_completed
            FROM rounds
            WHERE id = ? AND user_id = ?
        """, (round_id, user_id))

        r = cur.fetchone()
        if not r:
            return jsonify({"error": "Round not found"}), 404

        if r["is_completed"] == 1:
            return jsonify({"error": "Scores already submitted"}), 409

        total = 0
        cur.execute("BEGIN")

        for s in scores:
            cur.execute("""
                INSERT INTO hole_scores (round_id, hole_id, strokes)
                VALUES (?, ?, ?)
            """, (round_id, s["hole_id"], s["strokes"]))
            total += s["strokes"]

        cur.execute("""
            UPDATE rounds
            SET gross_score = ?, is_completed = 1
            WHERE id = ?
        """, (total, round_id))

        db.commit()

        return jsonify({
            "round_id": round_id,
            "gross_score": total
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()


# -------------------------------------------------
# GET ROUND DETAILS + SCORES
# -------------------------------------------------
@rounds_bp.route("/rounds/<int:round_id>", methods=["GET"])
@login_required
def get_round(round_id):
    user_id = session["user_id"]

    db = get_db()
    try:
        cur = db.cursor()

        cur.execute("""
            SELECT r.id,
                   r.course_id,
                   r.date_played,
                   r.gross_score,
                   r.handicap_at_time,
                   c.name AS course
            FROM rounds r
            JOIN courses c ON c.id = r.course_id
            WHERE r.id = ? AND r.user_id = ?
        """, (round_id, user_id))

        r = cur.fetchone()
        if not r:
            return jsonify({"error": "Round not found"}), 404

        cur.execute("""
            SELECT h.hole_number, hs.strokes
            FROM hole_scores hs
            JOIN holes h ON h.id = hs.hole_id
            WHERE hs.round_id = ?
            ORDER BY h.hole_number
        """, (round_id,))

        return jsonify({
            "round": dict(r),
            "scores": [dict(row) for row in cur.fetchall()]
        }), 200

    finally:
        db.close()

    
# -------------------------------------------------
# GET A USERS ROUND HISTORY
# -------------------------------------------------

@rounds_bp.route("/rounds", methods=["GET"])
@login_required
def get_user_rounds():
    user_id = session["user_id"]

    db = get_db()
    try:
        cur = db.cursor()

        cur.execute("""
            SELECT
                r.id,
                r.date_played,
                r.gross_score,
                r.is_completed,
                c.name AS course
            FROM rounds r
            JOIN courses c ON c.id = r.course_id
            WHERE r.user_id = ?
            ORDER BY r.date_played DESC
        """, (user_id,))

        return jsonify([dict(row) for row in cur.fetchall()]), 200

    finally:
        db.close()


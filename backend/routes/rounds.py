from flask import Blueprint, request, jsonify
from db import get_db

rounds_bp = Blueprint("rounds", __name__)

# -------------------------------------------------
# CREATE ROUND FROM BOOKING
# -------------------------------------------------
@rounds_bp.route("/rounds", methods=["POST"])
def create_round():
    data = request.get_json()
    booking_id = data.get("booking_id")

    if not booking_id:
        return jsonify({"error": "booking_id is required"}), 400

    db = get_db()
    try:
        cur = db.cursor()

        # Get booking, user, course, and tee time
        cur.execute("""
            SELECT b.user_id, t.course_id, t.id AS teetime_id
            FROM bookings b
            JOIN tee_times t ON t.id = b.teetime_id
            WHERE b.id = ?
        """, (booking_id,))
        row = cur.fetchone()

        if not row:
            return jsonify({"error": "Booking not found"}), 404

        user_id = row["user_id"]
        course_id = row["course_id"]
        teetime_id = row["teetime_id"]

        # Get current handicap snapshot
        cur.execute(
            "SELECT current_handicap FROM users WHERE id = ?",
            (user_id,)
        )
        h = cur.fetchone()
        handicap = h["current_handicap"] if h else None

        cur.execute("BEGIN")
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

        round_id = cur.lastrowid
        db.commit()

        return jsonify({
            "round_id": round_id,
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
def create_manual_round():
    data = request.get_json()

    user_id = data.get("user_id")
    course_id = data.get("course_id")
    date_played = data.get("date_played")

    if not user_id or not course_id or not date_played:
        return jsonify({
            "error": "user_id, course_id, and date_played are required"
        }), 400

    db = get_db()
    try:
        cur = db.cursor()

        # Get current handicap snapshot
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

        round_id = cur.lastrowid
        db.commit()

        return jsonify({
            "round_id": round_id,
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
def submit_scores(round_id):
    data = request.get_json()
    scores = data.get("scores")

    if not scores or not isinstance(scores, list):
        return jsonify({"error": "scores list required"}), 400

    db = get_db()
    try:
        cur = db.cursor()

        # Ensure round exists
        cur.execute("SELECT id FROM rounds WHERE id = ?", (round_id,))
        if not cur.fetchone():
            return jsonify({"error": "Round not found"}), 404

        cur.execute("BEGIN")

        total = 0
        for s in scores:
            hole_id = s.get("hole_id")
            strokes = s.get("strokes")

            if hole_id is None or strokes is None:
                return jsonify({
                    "error": "Each score needs hole_id and strokes"
                }), 400

            cur.execute("""
                INSERT INTO hole_scores (round_id, hole_id, strokes)
                VALUES (?, ?, ?)
            """, (round_id, hole_id, strokes))

            total += strokes

        # Update gross score
        cur.execute("""
            UPDATE rounds
            SET gross_score = ?
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
def get_round(round_id):
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
            WHERE r.id = ?
        """, (round_id,))
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
        holes = [
            {
                "hole": row["hole_number"],
                "strokes": row["strokes"]
            }
            for row in cur.fetchall()
        ]

        return jsonify({
            "round": dict(r),
            "scores": holes
        }), 200

    finally:
        db.close()

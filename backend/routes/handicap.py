from flask import Blueprint, jsonify, session
from db import get_db
from .auth_utils import login_required

handicap_bp = Blueprint("handicap", __name__)


@handicap_bp.route("/handicap/recalculate", methods=["POST"])
@login_required
def recalculate_handicap():
    user_id = session["user_id"]

    db = get_db()
    try:
        cur = db.cursor()

        # --------------------------------
        # Get last 5 completed rounds
        # --------------------------------
        cur.execute("""
            SELECT r.gross_score, c.par
            FROM rounds r
            JOIN courses c ON c.id = r.course_id
            WHERE r.user_id = ?
              AND r.is_completed = 1
              AND r.gross_score IS NOT NULL
            ORDER BY r.date_played DESC
            LIMIT 5
        """, (user_id,))

        rounds = cur.fetchall()

        if len(rounds) < 3:
            return jsonify({
                "message": "Not enough rounds to calculate handicap",
                "rounds_used": len(rounds)
            }), 200

        # --------------------------------
        # Calculate differentials
        # --------------------------------
        differentials = [
            r["gross_score"] - r["par"]
            for r in rounds
        ]

        new_handicap = round(
            sum(differentials) / len(differentials),
            1
        )

        # --------------------------------
        # Update user
        # --------------------------------
        cur.execute("""
            UPDATE users
            SET current_handicap = ?
            WHERE id = ?
        """, (new_handicap, user_id))

        # Insert into history
        cur.execute("""
            INSERT INTO handicap_history (user_id, handicap)
            VALUES (?, ?)
        """, (user_id, new_handicap))

        db.commit()

        return jsonify({
            "new_handicap": new_handicap,
            "rounds_used": len(differentials)
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()

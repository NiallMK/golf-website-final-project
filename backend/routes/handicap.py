from flask import Blueprint, jsonify
from db import get_db

handicap_bp = Blueprint("handicap", __name__)

@handicap_bp.route("/handicap/recalculate/<int:user_id>", methods=["POST"])
def recalculate_handicap(user_id):
    db = get_db()
    try:
        cur = db.cursor()

        # --------------------------------
        # Get completed rounds for user
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
        differentials = []
        for r in rounds:
            diff = r["gross_score"] - r["par"]
            differentials.append(diff)

        # Average of differentials
        new_handicap = round(sum(differentials) / len(differentials), 1)

        # --------------------------------
        # Update user handicap
        # --------------------------------
        cur.execute("""
            UPDATE users
            SET current_handicap = ?
            WHERE id = ?
        """, (new_handicap, user_id))

        db.commit()

        return jsonify({
            "user_id": user_id,
            "new_handicap": new_handicap,
            "rounds_used": len(differentials)
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()




from flask import Blueprint, jsonify
from db import get_db

handicap_bp = Blueprint("handicap", __name__)

@handicap_bp.route("/handicap/<int:user_id>", methods=["POST"])
def calculate_handicap(user_id):
    db = get_db()
    try:
        cur = db.cursor()

        # Get last 5 completed rounds from a user
        cur.execute("""
            SELECT r.gross_score, c.par
            FROM rounds r
            JOIN courses c ON c.id = r.course_id
            WHERE r.user_id = ?
              AND r.gross_score IS NOT NULL
            ORDER BY r.date_played DESC
            LIMIT 5
        """, (user_id,))
        rows = cur.fetchall()

        if len(rows) < 3:
            return jsonify({
                "error": "Not enough completed rounds to calculate handicap"
            }), 400

        differentials = [
            row["gross_score"] - row["par"]
            for row in rows
        ]

        handicap = round(sum(differentials) / len(differentials), 1)

        cur.execute("""
            UPDATE users
            SET current_handicap = ?
            WHERE id = ?
        """, (handicap, user_id))

        db.commit()

        return jsonify({
            "user_id": user_id,
            "handicap": handicap,
            "rounds_used": len(differentials)
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()

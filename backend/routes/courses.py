from flask import Blueprint, jsonify
from db import get_db

courses_bp = Blueprint("courses", __name__)

# --------------------------------------
# GET ALL COURSES
# --------------------------------------
@courses_bp.route("/courses", methods=["GET"])
def get_courses():
    db = get_db()
    try:
        cur = db.cursor()

        cur.execute("""
            SELECT id, name, par
            FROM courses
            ORDER BY name
        """)
        rows = cur.fetchall()

        courses = [
            {
                "id": row["id"],
                "name": row["name"],
                "par": row["par"]
            }
            for row in rows
        ]

        return jsonify(courses), 200

    finally:
        db.close()


# --------------------------------------
# GET SINGLE COURSE (OPTIONAL)
# --------------------------------------
@courses_bp.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    db = get_db()
    try:
        cur = db.cursor()

        cur.execute("""
            SELECT id, name, par
            FROM courses
            WHERE id = ?
        """, (course_id,))
        row = cur.fetchone()

        if not row:
            return jsonify({"error": "Course not found"}), 404

        return jsonify({
            "id": row["id"],
            "name": row["name"],
            "par": row["par"]
        }), 200

    finally:
        db.close()
#------------------------------------------------------------------
#GET the individual holes 
@courses_bp.route("/courses/<int:course_id>/holes", methods=["GET"])
def get_course_holes(course_id):
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("""
            SELECT id, hole_number, par
            FROM holes
            WHERE course_id = ?
            ORDER BY hole_number
        """, (course_id,))
        rows = cur.fetchall()

        return jsonify([
            {
                "id": r["id"],
                "hole_number": r["hole_number"],
                "par": r["par"]
            }
            for r in rows
        ]), 200
    finally:
        db.close()

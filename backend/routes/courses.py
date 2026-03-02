from flask import Blueprint, jsonify, request, session
from db import get_db
import json

courses_bp = Blueprint("courses", __name__)

# --------------------------------------
# GET ALL COURSES
# --------------------------------------
@courses_bp.route("/courses", methods=["GET"])
def get_courses():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, name, location, par,
               slope_rating, image_url
        FROM courses
    """)

    rows = cur.fetchall()

    courses = []

    for row in rows:
        images = []
        if row["image_url"]:
            images = json.loads(row["image_url"])

        courses.append({
            "id": row["id"],
            "name": row["name"],
            "location": row["location"],
            "par": row["par"],
            "slope_rating": row["slope_rating"],
            "images": images
        })

    return jsonify(courses)



# --------------------------------------
# GET SINGLE COURSE (OPTIONAL)
# --------------------------------------
import json

@courses_bp.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    db = get_db()
    try:
        cur = db.cursor()

        cur.execute("""
            SELECT id, name, location, par,
                   course_rating, slope_rating, image_url, latitude, longitude, description
            FROM courses
            WHERE id = ?
        """, (course_id,))
        row = cur.fetchone()

        if not row:
            return jsonify({"error": "Course not found"}), 404

        images = []
        if row["image_url"]:
            images = json.loads(row["image_url"])

        return jsonify({
            "id": row["id"],
            "name": row["name"],
            "location": row["location"],
            "par": row["par"],
            "course_rating": row["course_rating"],
            "slope_rating": row["slope_rating"],
            "images": images,
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "description": row["description"]
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

#-------------------------------------------------------------------
# LEADERBOARD FOR EACH COURSE
#-------------------------------------------------------------------

@courses_bp.route("/leaderboard/course/<int:course_id>", methods=["GET"])
def course_leaderboard(course_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT u.name AS player_name,
               MIN(rt.total_score) AS best_score
        FROM (
            SELECT r.id,
                   r.course_id,
                   r.user_id,
                   SUM(hs.strokes) AS total_score
            FROM rounds r
            JOIN hole_scores hs ON r.id = hs.round_id
            WHERE r.course_id = ?
            GROUP BY r.id
        ) rt
        JOIN users u ON rt.user_id = u.id
        GROUP BY rt.user_id
        ORDER BY best_score ASC
    """, (course_id,))

    rows = cur.fetchall()

    return jsonify([
        {
            "player": row["player_name"],
            "score": row["best_score"]
        }
        for row in rows
    ])

# --------------------------------------
# ADMIN: ADD COURSE
# --------------------------------------
@courses_bp.route("/courses", methods=["POST"])
def add_course():
    # check if a user is logged in
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    try:
        cur = db.cursor()

        # Check user role, are they an admin?
        cur.execute(
            "SELECT role FROM users WHERE id = ?",
            (session["user_id"],)
        )
        user = cur.fetchone()

        if not user or user["role"] != "admin":
            return jsonify({"error": "Forbidden - Admins only"}), 403

        # Get request data
        data = request.get_json()

        name = data.get("name")
        location = data.get("location")
        par = data.get("par")
        course_rating = data.get("course_rating")
        slope_rating = data.get("slope_rating")
        images = data.get("images", [])
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        description = data.get("description")

        if not name or par is None or course_rating is None or slope_rating is None:
            return jsonify({"error": "Missing required fields"}), 400
        
        images = [img for img in images if img]

        #store images as JSON strings
        image_json = json.dumps(images) if images else None

        # insert into golf-website.db
        cur.execute("""
            INSERT INTO courses
            (name, location, par, course_rating, slope_rating,
             image_url, latitude, longitude, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            location,
            par,
            course_rating,
            slope_rating,
            image_json,
            latitude,
            longitude,
            description
        ))

        db.commit()

        return jsonify({"message": "Course added successfully"}), 201

    finally:
        db.close()

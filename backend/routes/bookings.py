from flask import Blueprint, request, jsonify, session
from db import get_db
from .auth_utils import login_required

bookings_bp = Blueprint("bookings", __name__)

# -------------------------
# CREATE BOOKING (POST)
# -------------------------
@bookings_bp.route("/bookings", methods=["POST"])
@login_required
def book_teetime():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    teetime_id = data.get("teetime_id")
    user_id = session["user_id"]

    if not teetime_id:
        return jsonify({"error": "teetime_id is required"}), 400

    db = get_db()
    try:
        cursor = db.cursor()

        # Check tee time exists and is free
        cursor.execute(
            "SELECT is_booked FROM tee_times WHERE id = ?",
            (teetime_id,)
        )
        tee_time = cursor.fetchone()

        if tee_time is None:
            return jsonify({"error": "Tee time not found"}), 404

        if tee_time["is_booked"] == 1:
            return jsonify({"error": "Tee time already booked"}), 409

        cursor.execute("BEGIN")

        # Create booking
        cursor.execute(
            "INSERT INTO bookings (user_id, teetime_id) VALUES (?, ?)",
            (user_id, teetime_id)
        )

        # Lock tee time
        cursor.execute(
            "UPDATE tee_times SET is_booked = 1 WHERE id = ?",
            (teetime_id,)
        )

        db.commit()

        return jsonify({"message": "Tee time booked successfully"}), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()


# -------------------------
# CANCEL BOOKING (DELETE)
# -------------------------
@bookings_bp.route("/bookings/<int:booking_id>", methods=["DELETE"])
@login_required
def cancel_booking(booking_id):
    user_id = session["user_id"]

    db = get_db()
    try:
        cursor = db.cursor()

        # Booking must belong to logged-in user
        cursor.execute("""
            SELECT teetime_id
            FROM bookings
            WHERE id = ? AND user_id = ?
        """, (booking_id, user_id))

        booking = cursor.fetchone()

        if booking is None:
            return jsonify({"error": "Booking not found"}), 404

        teetime_id = booking["teetime_id"]

        cursor.execute("BEGIN")

        # Delete booking
        cursor.execute(
            "DELETE FROM bookings WHERE id = ?",
            (booking_id,)
        )

        # Free tee time
        cursor.execute(
            "UPDATE tee_times SET is_booked = 0 WHERE id = ?",
            (teetime_id,)
        )

        db.commit()

        return jsonify({"message": "Booking cancelled successfully"}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()


# -------------------------
# GET AVAILABLE TEE TIMES (PUBLIC)
# -------------------------
@bookings_bp.route("/teetimes/available", methods=["GET"])
def get_available_teetimes():
    course_id = request.args.get("course_id")
    date = request.args.get("date")

    if not course_id or not date:
        return jsonify({"error": "course_id and date required"}), 400

    db = get_db()
    try:
        cur = db.cursor()

        cur.execute("""
            SELECT id, time
            FROM tee_times
            WHERE course_id = ?
              AND date = ?
              AND is_booked = 0
            ORDER BY time
        """, (course_id, date))

        return jsonify([dict(row) for row in cur.fetchall()]), 200

    finally:
        db.close()


# -------------------------
# GET LOGGED-IN USER BOOKINGS
# -------------------------
@bookings_bp.route("/bookings", methods=["GET"])
@login_required
def get_user_bookings():
    user_id = session["user_id"]

    db = get_db()
    try:
        cur = db.cursor()

        cur.execute("""
            SELECT
                b.id,
                t.date,
                t.time,
                c.name AS course_name
            FROM bookings b
            JOIN tee_times t ON b.teetime_id = t.id
            JOIN courses c ON t.course_id = c.id
            WHERE b.user_id = ?
            ORDER BY t.date DESC, t.time DESC
        """, (user_id,))

        return jsonify([dict(row) for row in cur.fetchall()]), 200

    finally:
        db.close()

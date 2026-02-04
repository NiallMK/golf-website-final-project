# routes/bookings.py
from flask import Blueprint, request, jsonify
from db import get_db

bookings_bp = Blueprint("bookings", __name__)

# -------------------------
# CREATE BOOKING (POST)
# -------------------------
@bookings_bp.route("/bookings", methods=["POST"])
def book_teetime():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    user_id = data.get("user_id")
    teetime_id = data.get("teetime_id")

    if not user_id or not teetime_id:
        return jsonify({"error": "user_id and teetime_id are required"}), 400

    db = get_db()
    try:
        cursor = db.cursor()

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

        cursor.execute(
            "INSERT INTO bookings (user_id, teetime_id) VALUES (?, ?)",
            (user_id, teetime_id)
        )

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
def cancel_booking(booking_id):
    db = get_db()
    try:
        cursor = db.cursor()

        # 1. Find booking
        cursor.execute(
            "SELECT teetime_id FROM bookings WHERE id = ?",
            (booking_id,)
        )
        booking = cursor.fetchone()

        if booking is None:
            return jsonify({"error": "Booking not found"}), 404

        teetime_id = booking["teetime_id"]

        # 2. Begin transaction
        cursor.execute("BEGIN")

        # 3. Delete booking
        cursor.execute(
            "DELETE FROM bookings WHERE id = ?",
            (booking_id,)
        )

        # 4. Free tee time
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
# GET AVAILABLE TEE TIMES
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

        teetimes = [dict(row) for row in cur.fetchall()]
        return jsonify(teetimes), 200

    finally:
        db.close()

#------------------------
# GET USER BOOKING HISTORY
#------------------------

@bookings_bp.route("/bookings/user/<int:user_id>", methods=["GET"])
def get_user_bookings(user_id):
    db = get_db()
    try:
        cur = db.cursor()

        cur.execute("""
            SELECT
                b.id,
                t.date,
                t.time,
                c.name AS course_name,
                t.is_booked
            FROM bookings b
            JOIN tee_times t ON b.teetime_id = t.id
            JOIN courses c ON t.course_id = c.id
            WHERE b.user_id = ?
            ORDER BY t.date DESC, t.time DESC
        """, (user_id,))

        bookings = [dict(row) for row in cur.fetchall()]
        return jsonify(bookings), 200

    finally:
        db.close()



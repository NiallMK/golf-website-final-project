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

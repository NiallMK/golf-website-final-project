from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db

auth_bp = Blueprint("auth", __name__)


#REGISTRATION ENDPOINT
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password or not name:
        return jsonify({"error": "All fields required"}), 400

    db = get_db()
    try:
        cur = db.cursor()

        # Check email uniqueness
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cur.fetchone():
            return jsonify({"error": "Email already registered"}), 409

        password_hash = generate_password_hash(password)

        cur.execute("""
            INSERT INTO users (email, password_hash, name)
            VALUES (?, ?, ?)
        """, (email, password_hash, name))

        user_id = cur.lastrowid
        db.commit()

        # Log user in
        session["user_id"] = user_id

        return jsonify({
            "user": {
                "id": user_id,
                "email": email,
                "name": name
            }
        }), 201

    finally:
        db.close()



#LOGIN ENDPOINT
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, password_hash, name
        FROM users
        WHERE email = ?
    """, (email,))
    user = cur.fetchone()

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Store user in session
    session["user_id"] = user["id"]

    return jsonify({
        "message": "Logged in",
        "user": {
            "id": user["id"],
            "name": user["name"]
        }
    })

#who is using this website right now?
@auth_bp.route("/auth/me", methods=["GET"])
def me():
    if "user_id" not in session:
        return jsonify({"user": None}), 401

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT id, name, email, current_handicap
        FROM users
        WHERE id = ?
    """, (session["user_id"],))

    user = cur.fetchone()
    if not user:
        return jsonify({"user": None}), 401

    return jsonify({"user": dict(user)}), 200

#LOGOUT ENDPOINT
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

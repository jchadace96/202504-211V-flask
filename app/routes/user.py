from flask import Blueprint, request, jsonify
from app.database import get_db_connection

user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route("/", methods=["GET"])
def get_all_users():
    db = get_db_connection()
    users = db.execute("SELECT * FROM users;").fetchall()
    return jsonify([dict(u) for u in users]), 200


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_single_user(user_id):
    db = get_db_connection()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(dict(user)), 200


@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    db = get_db_connection()
    db.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        (username, email, password)
    )
    db.commit()
    return jsonify({"message": "Usuario creado"}), 201


@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    db = get_db_connection()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    db.execute(
        "UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?",
        (username, email, password, user_id)
    )
    db.commit()
    return jsonify({"message": "Usuario actualizado"}), 200


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    db = get_db_connection()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    return jsonify({"message": "Usuario eliminado"}), 200
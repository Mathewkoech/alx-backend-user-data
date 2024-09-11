#!/usr/bin/env python3
"""Main module
"""
from sqlite3 import IntegrityError
from flask import Flask, jsonify, request
from auth import Auth
app = Flask(__name__)

AUTH = Auth()

@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """GET /
    Return:
      - welcome message
    """
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """POST /users
    Return:
      - user information
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        # Register the user using the Auth object
        new_user = AUTH.register_user(email, password)

        return jsonify({"email": new_user.email, "message": "user created"}), 201
    
    except IntegrityError:
        return jsonify({"message": "email already registered"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

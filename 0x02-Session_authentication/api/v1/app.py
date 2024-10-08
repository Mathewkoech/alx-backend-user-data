#!/usr/bin/env python3
from flask import Flask, jsonify
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.session_auth import SessionAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize the authentication variable
auth = SessionAuth()
AUTH_TYPE = os.getenv('AUTH_TYPE')

# Load the authentication class based on the environmental variables
if AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def before_request():
    """ Filter each requests before it is processed.
    """
    if auth is None:
        return

    excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None and \
            auth.session_cookie(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)

    request.current_user = auth.current_user(request)
    if request.current_user is None:
        abort(403)


@app.route('/api/v1/status', methods=['GET'])
@app.route('/api/v1/status/', methods=['GET'])
def status():
    """
    Return the status of the API.
    """
    return jsonify({"status": "OK"})


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

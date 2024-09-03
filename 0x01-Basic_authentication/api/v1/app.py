#!/usr/bin/env python3
from flask import Flask, jsonify

app = Flask(__name__)

@app.errorhandler(401)
def unauthorized_error(error):
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response

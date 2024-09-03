#!/usr/bin/env python3
from flask import Flask, jsonify
"""
Route module for the API
"""
app = Flask(__name__)

@app.errorhandler(401)
def unauthorized(error) -> str:
     """ Unauthorized handler
     """
    return jsonify({"error": "Unauthorized"})401

@app.errorhandler(403)
def forbidden(error) -> str:
     """ forbidden handler                                                                                      
     """
    return jsonify({"error": "Forbidden"})403


@app.errorhandler(404)
def not_found(error) -> str:
     """ forbidden handler                                                                                                   
     """
    return jsonify({"error": "Not found"})404


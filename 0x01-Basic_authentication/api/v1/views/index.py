"""Module of Index views.
"""
from flask import jsonify, abort
from api.v1.views import app_views

@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """GET /api/v1/unauthorized
    Return:
      - Unauthorized error.
    """
    abort(401)

@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """GET /api/v1/forbidden
    Return:
      - Unauthorized error.
    """
    abort(403)

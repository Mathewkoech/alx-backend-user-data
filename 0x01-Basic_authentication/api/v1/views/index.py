#!/usr/bin/env python3
from flask import Blueprint, abort

bp = Blueprint('index', __name__)

@bp.route('/api/v1/unauthorized', methods=['GET'])
def unauthorized():
    abort(401)

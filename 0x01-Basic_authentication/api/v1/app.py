#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from api.v1.auth.auth import Auth
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = os.getenv('AUTH_TYPE')
if auth_type == 'auth':
    auth = Auth()


@app.before_request
def before_request():
    """Feltering user request
    """
    global auth
    if auth is None:
        return

    secure_paths = ['/api/v1/status/',
                    '/api/v1/unauthorized/',
                    '/api/v1/forbidden/']
    if auth.require.auth(request.path, secure_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    unauthorised 401 error
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(403)
def forbidden_data(error) -> str:
    """
    403 forbidden error handler
    """
    res = jsonify({"error": "Forbidden"})
    res.status_code = 403
    return res


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
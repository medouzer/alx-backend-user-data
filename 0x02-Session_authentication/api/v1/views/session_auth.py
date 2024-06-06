#!/usr/bin/env python3
""" Module of session_auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
import os

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """session_authentication"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({ "error": "email missing" }), 400
    if password is None:
        return jsonify({ "error": "password missing" }), 400
    user_list = User.search({'email': email})
    if not user_list:
        return jsonify({ "error": "no user found for this email" }), 404
    user = user_list[0]
    if not user.is_valid_password(password):
        return jsonify({ "error": "wrong password" }), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = make_response(user.to_json())
    session_name = os.getenv("SESSION_NAME", "_my_session_id")
    print(session_name)
    print(session_id)
    response.set_cookie(session_name, session_id)
    return response

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """logout"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200

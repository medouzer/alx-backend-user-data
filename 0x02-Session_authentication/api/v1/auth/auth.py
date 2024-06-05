#!/usr/bin/env python3
"""
Auth class
"""

from flask import request
from typing import List, TypeVar
import os


class Auth():
    """the class Auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method require_auth"""
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        for excluded_path in excluded_paths:
            if path.startswith(excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """public method authorization_header"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """public method current_user"""
        return None
    
    def session_cookie(self, request=None):
        """session_cookie"""
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)

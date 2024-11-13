#!/usr/bin/env python3
"""
MODULE MANAGES  API AUTHENTICATION
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    AUTH implements Api authentication

    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns False
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path.rstrip('/')
        for excluded_path in excluded_paths:
            if path == excluded_path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns None
        """
        if request and request.headers:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns NONE
        """
        return None

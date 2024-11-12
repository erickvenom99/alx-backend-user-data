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
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns NONE
        """
        return None
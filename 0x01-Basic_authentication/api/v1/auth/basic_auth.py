#!/usr/bin/env python3
"""
MODULE MANAGES  BASIC AUTHENTICATION
0;10;1c"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64


class BasicAuth(Auth):
    """
    Basic_Auth implements Api authentication

    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
           Retrieve the Base64 part of the Authorization
              header
           Args:
               authorization_header: the header string
            Returns:
                the value after Basic(after the space) or None
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
           Retrieve the Base64 part of the Authorization
              header
           Args:
               authorization_header: the header string
            Returns:
                the value after Basic(after the space) or None
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_string = base64.b64decode(
                base64_authorization_header).decode('utf-8')
            return decoded_string
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Retrieve user email and password from the decoded Base64 value.

        Args:
            decoded_base64_authorization_header (str): The decoded
            Base64 string.
        Returns:
            tuple: A tuple containing the user email and password (str, str),
             or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        try:
            email, password = decoded_base64_authorization_header.split(":", 1)
            return email, password
        except ValueError:
            return None, None

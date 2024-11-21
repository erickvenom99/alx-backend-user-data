#!/usr/bin/env python3
"""
    Auth
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


class Auth:
    """Authentication class.
    """
    def __init__(self):
        """init"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user if it does not already exist.
        Args:
            email (str): user email .
            password (str): user password.
        Returns:
            User: The newly created User object.
        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hash_pass = self._hash_password(password)
            new_user = self._db.add_user(email, hash_pass)
            return new_user
        else:
            raise ValueError(f"User {email} already exists")

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hash password
        """
        salt_pwd = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt_pwd)
        return hashed_pwd

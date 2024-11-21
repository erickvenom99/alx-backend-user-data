#!/usr/bin/env python3
"""
    Auth
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> str:
    """
    Hash password
    """
    salt_pwd = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt_pwd)
    return hashed_pwd


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
            hash_pass = _hash_password(password)
            new_user = self._db.add_user(email, hash_pass)
            return new_user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login.

        Args:
            email (str): User email.
            password (str): User password.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(
                    password.encode('utf-8'), user.hashed_password)
            return False
        except (NoResultFound, InvalidRequestError):
            return False

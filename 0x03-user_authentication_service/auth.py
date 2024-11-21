#!/usr/bin/env python3
"""
    Auth
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid


def _hash_password(password: str) -> str:
    """
    Hash password
    """
    salt_pwd = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt_pwd)
    return hashed_pwd


def _generate_uuid() -> str:
    """
    Generate a UUID.

    Returns:
        str: The generated UUID.
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """
        Create a session for a user.

        Args:
            email (str): User email.

        Returns:
            str: The session ID.

        Raises:
            ValueError: If the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Finds a user from database using session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            User or None: The corresponding User or None if not found.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        method remove sesssions
        Args:
            user_id (int): user ID.
        Returns:
            None
        """
        return self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for the given email.

        Args:
            email (str): The email of the user to generate the token for.

        Returns:
            str: The generated reset token.

        Raises:
            ValueError: If the user with the given email does not exist.
        """
        if email:
            try:
                user = self._db.find_user_by(email=email)
            except NoResultFound:
                raise ValueError
            else:
                set_token = _generate_uuid()
                self._db.update_user(user.id, reset_token=set_token)
                return set_token

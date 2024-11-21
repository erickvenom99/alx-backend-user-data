#!/usr/bin/env python3
"""
    Auth
"""

import bcrypt


def _hash_password(password: str) -> str:
    """
        Hash password
    """
    salt_pwd = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt_pwd)
    return hashed_pwd

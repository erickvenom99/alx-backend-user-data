#!/usr/bin/env python3
"""
main module
"""

import requests

BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    res = requests.post(
        f"{BASE_URL}/users",
        data={"email": email, "password": password})
    assert res.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    res = requests.post(
        f"{BASE_URL}/sessions",
        data={"email": email, "password": password})
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    res = requests.post(
        f"{BASE_URL}/sessions",
        data={"email": email, "password": password})
    assert res.status_code == 200
    return res.json().get("session_id", "")


def profile_unlogged() -> None:
    res = requests.get(f"{BASE_URL}/profile")
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    res = requests.get(
        f"{BASE_URL}/profile",
        cookies={"session_id": session_id})
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.json()}")
    assert res.status_code == 200


def log_out(session_id: str) -> None:
    res = requests.delete(
        f"{BASE_URL}/sessions",
        cookies={"session_id": session_id})
    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    res = requests.post(
        f"{BASE_URL}/reset_password",
        data={"email": email})
    assert res.status_code == 200
    return res.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    res = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email, "reset_token": reset_token,
              "new_password": new_password})
    assert res.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

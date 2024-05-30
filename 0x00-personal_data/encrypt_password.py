#!/usr/bin/env python3
"""Encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Encrypting passwords"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash

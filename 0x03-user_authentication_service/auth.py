#!/usr/bin/env python3
"""Auth module
"""
from sqlalchemy.orm.exc import NoResultFound
from db import DB
import bcrypt
from user import User

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> str:
        """Hashes a password
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    def register_user(self, email: str, password: str) -> User:
        """Register a user
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, self._hash_password(password))  
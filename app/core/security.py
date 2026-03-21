# Security-related functions and utilities

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# This function hashes the password using bcrypt algorithm.
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
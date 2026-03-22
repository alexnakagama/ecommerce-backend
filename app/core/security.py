# Security-related functions and utilities

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# This function hashes the password using bcrypt algorithm.
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# This function verifies a password against a hashed password.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# This function authenticates a user by verifying the provided password against the stored hashed password.
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"error": "User not found"}
    if not verify_password(password, user.hashed_password):
        return {"error": "Invalid password"}
    return user

# This function creates a JWT access token for a given user ID.
def create_access_token(user_data: dict):
    to_encode = user_data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
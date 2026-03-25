from sqlalchemy.orm import Session

from app.models.user_model import User

from app.core.security import hash_password

# This function creates a new user with the provided username, email, and password.
def create_user(username, email, password, role, db: Session):
    password_hash = hash_password(password)
    new_user = User(username=username, email=email, password_hash=password_hash, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": new_user}
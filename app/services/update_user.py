from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.user_model import User

def update_user_info(db: Session, user_id: int, username: str, email: str) -> dict:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.username = username
        db_user.email = email
        db.commit()
        db.refresh(db_user)
        return {"message": "User information updated successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
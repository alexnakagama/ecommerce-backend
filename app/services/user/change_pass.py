from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.user_model import User

from app.core.security import verify_password, hash_password

def change_pass(db: Session, current_user: User, old_password: str, new_password: str) -> dict:
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if db_user and verify_password(old_password, db_user.password_hash):
        db_user.password_hash = hash_password(new_password)
        db.commit()
        return {"message": "Password changed successfully"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")
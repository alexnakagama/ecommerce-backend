from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.user_model import User

def update_user_role(db: Session, user_id: int, new_role: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.role = new_role
    db.commit()
    db.refresh(user)
    return {"message": f"User role updated to {new_role} successfully"}
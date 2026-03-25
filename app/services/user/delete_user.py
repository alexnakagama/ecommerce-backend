from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.models.user_model import User

def delete_user(db: Session, user_id: int) -> dict:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"message": "User account deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found, could not be deleted")
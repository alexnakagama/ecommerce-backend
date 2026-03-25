from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.models.user_model import User

from app.schemas.user.user_response import UserResponse

def get_user_by_id(db : Session, user_id : int):    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"user": UserResponse.model_validate(user)}
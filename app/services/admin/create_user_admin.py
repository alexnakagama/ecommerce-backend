from sqlalchemy.orm import Session

from app.schemas.user.user_create import UserCreate

from app.services.user.create_user import create_user as create_user_service

def create_user_admin(db: Session, user_data: UserCreate):
    return create_user_service(user_data.username, user_data.email, user_data.password, user_data.role, db)
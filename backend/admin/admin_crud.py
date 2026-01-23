# from datetime import datetime, timedelta, timezone
# from typing import Annotated

import jwt 
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from starlette.config import Config
from sqlalchemy.orm import Session

from models import Admin
from database import get_db
from admin.admin_schema import (
    AdminCreate,
    AdminUpdate,
)

config = Config(".env")
SECRET_KEY = config("SECRET_KEY", default="SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("TIMEOUT", default=1))

router = APIRouter(prefix="/spm/admin")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/spm/admin/login")

ADMINS = [
    config("ADMIN1", default="default1")
]

# find different hashing?
password_hash = PasswordHash.recommended()


def create_admin(db: Session, create_admin: AdminCreate) -> Admin:
    """
    create new admin
    """
    new_admin = Admin(
        id=str(uuid.uuid4()),
        username=create_admin.username,
        password=password_hash.hash(create_admin.password),
        is_admin=create_admin.is_admin,
    )
    db.add(new_admin)
    db.commit()

    return get_admin_by_username(db, new_admin.username)


def update_admin(
        db: Session, 
        update_admin: AdminUpdate, 
        current_admin: Admin
) -> Admin:
    """
    update admin (password only)
    """
    admin = get_admin_by_id(current_admin.id)
    # can only update password
    admin.username = admin.username
    admin.password = password_hash.hash(update_admin.password)
    admin.is_admin = True

    return get_admin_by_id(db, admin.id)


def delete_admin(db: Session, current_admin: Admin) -> None:
    """
    remove admin
    """
    db.delete(current_admin)
    db.commit()


#  - - - - - - - - - -
#   UTILITIES
#  - - - - - - - - - -


def get_admin_by_id(db: Session, admin_id: str) -> Admin | None:
    """
    Retrieve admin by id
    """
    return db.query(Admin).filter(Admin.id == admin_id).first()


def get_admin_by_username(db: Session, username: str) -> Admin | None:
    """
    Retrieve admin by username
    """
    return db.query(Admin).filter(Admin.username == username).first()


def get_all_admins(db: Session):
    return db.query(Admin).all()


async def get_current_admin(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        # token = Token(username=username)
    except PyJWTError:
        raise credentials_exception
    
    admin = get_admin_by_username(db=db, username=username)
    if admin is None:
        return credentials_exception
    return admin

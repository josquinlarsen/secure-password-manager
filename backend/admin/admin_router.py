from fastapi import (
    APIRouter, 
    HTTPException,
    Depends,
)
from fastapi.security import (
    OAuth2PasswordBearer, 
    OAuth2PasswordRequestForm,
    )
from sqlalchemy.orm import (
    Session,
)
from starlette import status
from starlette.config import Config
from datetime import datetime, timedelta, timezone

from database import get_db
from admin.admin_crud import (
    password_hash, 
    create_admin,
    update_admin,
    delete_admin,
    get_admin_by_id,
    get_admin_by_username,
    get_current_admin,
)
from admin.admin_schema import (
    AdminCreate,
    AdminUpdate,
    AdminResponse,
    Token,
)
from models import (
    Admin,
)

from auth import (
    create_access_token,
)

config = Config(".env")
router = APIRouter(prefix="/spm/admin")

SECRET_KEY = config("SECRET_KEY", default="SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("TIMEOUT", default=1))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/spm/admin/login")


@router.post("/register")
def register_admin(
    admin_create: AdminCreate,
    db: Session = Depends(get_db),
) -> AdminResponse:
    # verify that admin doesn't already exist before registering

    new_admin = create_admin(db=db, create_admin=admin_create)

    return AdminResponse(
        id=new_admin.id,
        username=new_admin.username,
        password=new_admin.password,
        is_admin=new_admin.is_admin
    )

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    admin = get_admin_by_username(db, form_data.username)
    if not admin: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    return Token(
        access_token=access_token, 
        token_type="bearer", 
        username=admin.username
    )


@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin_route(
    admin_id: str,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    admin = get_admin_by_id(db, admin_id)
    return delete_admin(db, admin) 

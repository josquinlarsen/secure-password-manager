from pydantic import BaseModel, field_validator


class AdminCreate(BaseModel):
    username: str
    password: str
    is_admin: bool

    @field_validator("username", "password")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Required field!")
        return v


class AdminUpdate(BaseModel):
    username: str
    password: str
    is_admin: bool

    @field_validator("username", "password")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Required field!")
        return v


class AdminResponse(BaseModel):
    id: str
    username: str
    password: str
    is_admin: bool


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

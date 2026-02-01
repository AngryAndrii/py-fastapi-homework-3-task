from pydantic import BaseModel, EmailStr, field_validator

from database import accounts_validators


class UserBase(BaseModel):
    email: EmailStr


class UserRegistrationRequestSchema(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserRegistrationResponseSchema(UserRead):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str

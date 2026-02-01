from datetime import datetime, timezone, timedelta
from typing import cast

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from crud.crud import get_user_by_email, create_user
from database import get_db


from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from config import get_jwt_auth_manager, get_settings, BaseAppSettings
from database import (
    get_db,
    UserModel,
    UserGroupModel,
    UserGroupEnum,
    ActivationTokenModel,
    PasswordResetTokenModel,
    RefreshTokenModel
)
from exceptions import BaseSecurityError
from schemas import UserRegistrationResponseSchema, \
    UserRegistrationRequestSchema
from security.interfaces import JWTAuthManagerInterface

router = APIRouter()

# Write your code here



router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register/", response_model=UserRegistrationResponseSchema, status_code=201)
async def register(user: UserRegistrationRequestSchema, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=409, detail=f"A user with this email {db_user.email} already exists.")
    return await create_user(db, user)
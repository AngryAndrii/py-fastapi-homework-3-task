from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import UserModel, UserGroupEnum, UserGroupModel
from schemas.accounts import UserRegistrationRequestSchema
from security.passwords import hash_password


async def create_user(db: AsyncSession, user: UserRegistrationRequestSchema):
    result = await db.execute(
        select(UserGroupModel).where(UserGroupModel.name == UserGroupEnum.USER)
    )
    user_group = result.scalar_one_or_none()

    hashed = hash_password(user.password)

    db_user = UserModel(email=user.email, _hashed_password=hashed, group_id=user_group.id)

    cur_user = await get_user_by_email(db, db_user.email)

    if cur_user:
        raise HTTPException(status_code=409, detail=f"A user with this email {cur_user.email} already exists.")

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(UserModel).where(UserModel.email == email))
    return result.scalar_one_or_none()

import strawberry
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info
from .models import User
from .db import get_db


@strawberry.type
class UserType:
    id: int
    name: str
    email: str


@strawberry.type
class Query:
    @strawberry.field
    async def users(self, info: Info) -> List[UserType]:
        db: AsyncSession = next(get_db())
        result = db.execute(select(User))
        return result.scalars().all()


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, name: str, email: str, info: Info) -> UserType:
        db: AsyncSession = next(get_db())
        new_user = User(name=name, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

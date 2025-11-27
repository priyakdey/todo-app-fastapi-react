import time
from typing import Optional

from sqlmodel import SQLModel, Field


class Profile(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(nullable=False, min_length=3, max_length=20)
    password: str = Field(nullable=False, min_length=3, max_length=20)
    name: str = Field(nullable=False, min_length=1, max_length=100)
    created_on: int = Field(nullable=False)
    modified_on: int = Field(nullable=False)

    @staticmethod
    def create(username: str, password: str, name: Optional[str]) -> "Profile":
        instant = int(time.time())
        return Profile(username=username, password=password,
                       name=name, created_on=instant,
                       modified_on=instant)


class Todo(SQLModel, table=True):
    id: int = Field(primary_key=True)
    profile_id: int = Field(foreign_key="profile.id", nullable=False)
    title: str = Field(nullable=False, min_length=1, max_length=50)
    description: Optional[str] = Field(nullable=True)
    is_completed: bool = Field(nullable=False, default=False)
    created_on: int = Field(nullable=False)
    modified_on: int = Field(nullable=False)


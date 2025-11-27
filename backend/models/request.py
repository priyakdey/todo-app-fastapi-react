from typing import Any

from pydantic import BaseModel, field_validator


class NewProfileRequest(BaseModel, arbitrary_types_allowed=True):
    username: str
    password: bytearray
    name: str

    @field_validator("password", mode="before")
    @classmethod
    def to_bytearray(cls, v: Any) -> bytearray | Any:
        if isinstance(v, str):
            return bytearray(v, encoding="utf-8")
        return v


class SigninRequest(BaseModel, arbitrary_types_allowed=True):
    username: str
    password: bytearray

    @field_validator("password", mode="before")
    @classmethod
    def to_bytearray(cls, v: Any) -> bytearray | Any:
        if isinstance(v, str):
            return bytearray(v, encoding="utf-8")
        return v


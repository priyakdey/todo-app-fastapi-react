from typing import Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlmodel import Session
from starlette import status
from starlette.responses import Response, JSONResponse

from .db import get_session
from .db.entity import Profile

server = FastAPI()

SessionDep = Annotated[Session, Depends(get_session)]


class NewProfileRequest(BaseModel):
    username: str
    password: str
    name: str


@server.post("/signup")
async def signup_profile(new_profile_req: NewProfileRequest,
                         session: SessionDep):
    profile = Profile.create(new_profile_req.username, new_profile_req.password,
                             new_profile_req.name)
    session.add(profile)
    session.commit()
    return JSONResponse(content=None, status_code=status.HTTP_201_CREATED)


import time
from typing import Annotated, Any

import jwt
from fastapi import Depends
from fastapi import FastAPI
from pwdlib import PasswordHash
from sqlalchemy.exc import IntegrityError, DataError
from sqlmodel import Session, select
from starlette import status
from starlette.responses import JSONResponse

from .db import get_session
from .db.entity import Profile
from .models.request import NewProfileRequest, SigninRequest

ISSUER = "todo-backend"
SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
EXPIRATION_TIME = 60 * 24

SALT = b"PASS_SALT"

SessionDep = Annotated[Session, Depends(get_session)]

password_hasher = PasswordHash.recommended()
server = FastAPI()



@server.post("/signup")
async def signup_profile(new_profile_req: NewProfileRequest,
                         session: SessionDep):
    try:
        pass_hash = password_hasher.hash(bytes(new_profile_req.password),
                                         salt=SALT)
        print("hash = ", pass_hash)
        new_profile_req.password.clear()
        profile = Profile.create(new_profile_req.username, pass_hash,
                                 new_profile_req.name)
        session.add(profile)
        session.commit()
        return JSONResponse(content=None, status_code=status.HTTP_201_CREATED)
    except IntegrityError as e:
        # TODO: learn how to log properly, normie!
        print(e)
        return JSONResponse(content={"err": "integrity issue"},
                            status_code=status.HTTP_409_CONFLICT)
    except DataError as e:
        # TODO: learn how to log properly, normie!
        print(e)
        return JSONResponse(content={"err": "data issue"},
                            status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return JSONResponse(content={"err": "check logs"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@server.post("/signin")
async def signin(session: SessionDep, signin_req: SigninRequest,
                 response: JSONResponse):
    res = session.exec(
        select(Profile).where(Profile.username == signin_req.username))
    profile = res.one_or_none()

    if not profile:
        return JSONResponse(content={"err": "no such user"},
                            status_code=status.HTTP_401_UNAUTHORIZED)

    if not password_hasher.verify(bytes(signin_req.password),
                                  profile.password):
        return JSONResponse(content={"err": "no such user"},
                            status_code=status.HTTP_401_UNAUTHORIZED)
    iat = int(time.time())
    exp = iat + 1440

    headers: dict[str, Any] = {
        "alg": ALGORITHM,
        "typ": "JWT",

    }

    payload: dict[str, Any] = {
        "iss": ISSUER,
        "aud": profile.id,
        "iat": iat,
        "exp": exp,
        "name": profile.name,
        "sub": profile.id,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM,
                       headers=headers)

    # the cookie config should be env driven
    response.set_cookie(key="access_token", value=token, path="/",
                        httponly=True, secure=False, samesite="lax",
                        max_age=EXPIRATION_TIME)
    return JSONResponse(content=None, status_code=status.HTTP_200_OK)


# TODO: add middleware for security
@server.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: JSONResponse, ):
    response.delete_cookie(key="access_token")
    return JSONResponse(content=None, status_code=status.HTTP_200_OK)

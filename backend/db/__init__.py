from typing import Any

from sqlalchemy import create_engine
from sqlmodel import Session

db_username: str = "postgres"
db_password: str = "password"
db_url: str = f"postgresql+psycopg2://{db_username}:{db_password}@localhost:5432/postgres"

connect_args: dict[str, Any] = {}
engine = create_engine(db_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


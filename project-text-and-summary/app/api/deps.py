from typing import Generator

from app.db import session


def get_db() -> Generator:
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

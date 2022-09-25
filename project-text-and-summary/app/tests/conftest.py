from typing import Generator

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api import deps
from app.db.base import Base
from app.main import app
from app.tests.factories import DocumentFactory


TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker()

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    transaction = connection.begin()
    session = Session(autocommit=False, autoflush=False, bind=connection)
    DocumentFactory._meta.sqlalchemy_session = session
    yield lambda: (yield session)
    session.close()
    transaction.rollback()


@pytest.fixture()
def client(session) -> Generator:
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_db] = session
        yield client
        app.dependency_overrides = {}

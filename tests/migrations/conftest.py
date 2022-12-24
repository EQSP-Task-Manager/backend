import uuid
from argparse import Namespace

import pytest
from alembic.config import Config
from sqlalchemy_utils import create_database
from sqlalchemy_utils import drop_database

from backend.storage.db import setup_alembic_config


@pytest.fixture()
def db_url() -> str:
    db_name = uuid.uuid4().hex
    db_url = f'postgresql://postgres:postgres@localhost:5432/{db_name}'
    create_database(db_url)
    try:
        yield f'postgresql+asyncpg://postgres:postgres@localhost:5432/{db_name}'
    finally:
        drop_database(db_url)


@pytest.fixture()
def alembic_config(db_url: str) -> Config:
    args = Namespace(config='alembic.ini', name='alembic', db_url=db_url)
    return setup_alembic_config(args)

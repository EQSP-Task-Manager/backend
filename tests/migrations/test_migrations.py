from argparse import Namespace

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory

from backend.storage.db import setup_alembic_config


def get_revisions() -> list[Script]:
    args = Namespace(config='alembic.ini', name='alembic', db_url='postgresql://postgres:postgres@localhost:5432/db')
    config = setup_alembic_config(args)
    revisions_dir = ScriptDirectory.from_config(config)
    revisions = list(revisions_dir.walk_revisions('base', 'heads'))
    revisions.reverse()
    return revisions


@pytest.mark.parametrize('revision', get_revisions())
def test_migrations_stairway(alembic_config: Config, revision: Script):
    upgrade(alembic_config, revision.revision)
    downgrade(alembic_config, revision.down_revision or '-1')
    upgrade(alembic_config, revision.revision)

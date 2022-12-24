from sqlalchemy import MetaData, Table, Column, Index, Text, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import ARRAY, ENUM, UUID

naming_convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': (
        'fk__%(table_name)s__'
        '%(all_column_names)s__'
        '%(referred_table_name)s'
    ),
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=naming_convention)

tasks_table = Table(
    'tasks',
    metadata,

    # Identifiers
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('uuid', UUID, nullable=False),
    Column('user_id', Text, nullable=False),

    # Main fields
    Column('title', Text, nullable=False),
    Column('description', Text, nullable=False),
    Column('done', Boolean, nullable=False),
    Column('importance', ENUM('low', 'basic', 'important', name='task_importance'), nullable=False),
    Column('tags', ARRAY(Text), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('changed_at', DateTime, nullable=False),

    # Optional fields
    Column('deadline', DateTime),
    Column('color', Text),

    Index('ix__user_id_id', 'user_id', 'id'),
    Index('ix__user_id_uuid', 'user_id', 'uuid', unique=True)
)

revisions_table = Table(
    'revisions',
    metadata,

    Column('user_id', Text, primary_key=True),
    Column('revision', Integer, nullable=False)
)

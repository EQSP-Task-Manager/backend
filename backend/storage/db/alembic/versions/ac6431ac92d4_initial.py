"""Initial

Revision ID: ac6431ac92d4
Revises: 
Create Date: 2022-12-25 02:21:42.969866

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ac6431ac92d4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'revisions',
        sa.Column('user_id', sa.Text(), nullable=False),
        sa.Column('revision', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('user_id', name=op.f('pk__revisions'))
    )
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('uuid', postgresql.UUID(), nullable=False),
        sa.Column('user_id', sa.Text(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('done', sa.Boolean(), nullable=False),
        sa.Column('importance', postgresql.ENUM('low', 'basic', 'important', name='task_importance'), nullable=False),
        sa.Column('tags', postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('changed_at', sa.DateTime(), nullable=False),
        sa.Column('deadline', sa.DateTime(), nullable=True),
        sa.Column('color', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__tasks'))
    )
    op.create_index('ix__user_id_id', 'tasks', ['user_id', 'id'], unique=False)
    op.create_index('ix__user_id_uuid', 'tasks', ['user_id', 'uuid'], unique=True)


def downgrade() -> None:
    op.drop_index('ix__user_id_uuid', table_name='tasks')
    op.drop_index('ix__user_id_id', table_name='tasks')
    op.drop_table('tasks')
    op.drop_table('revisions')
    op.execute('DROP TYPE task_importance')

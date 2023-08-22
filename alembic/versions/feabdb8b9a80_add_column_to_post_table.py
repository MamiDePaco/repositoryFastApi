"""add column to post table

Revision ID: feabdb8b9a80
Revises: 416fdc7e2e11
Create Date: 2023-08-21 12:26:16.391588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'feabdb8b9a80'
down_revision: Union[str, None] = '416fdc7e2e11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Post',sa.Column('content',sa.Integer(),nullable=False))
    pass


def downgrade() -> None:
    pass
    op.drop_column('Post','content')

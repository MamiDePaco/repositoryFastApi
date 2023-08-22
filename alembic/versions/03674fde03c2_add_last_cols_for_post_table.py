"""add last cols for post table

Revision ID: 03674fde03c2
Revises: 54ecf8015b44
Create Date: 2023-08-21 16:27:20.566274

"""
from typing import Sequence, Union
from sqlalchemy.sql.expression import text


from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03674fde03c2'
down_revision: Union[str, None] = '54ecf8015b44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Post',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('Post',sa.Column('create_at',sa.DATETIME(timezone=True),nullable=False,server_default=sa.text('GETDATE()')))
    pass


def downgrade() -> None:
    op.drop_column('Post','published')
    op.drop_column('Post','create_at')
    pass

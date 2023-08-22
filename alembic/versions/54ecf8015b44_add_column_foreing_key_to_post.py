"""add column foreing key to Post

Revision ID: 54ecf8015b44
Revises: a3b1c10f6cf8
Create Date: 2023-08-21 16:15:46.689443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54ecf8015b44'
down_revision: Union[str, None] = 'a3b1c10f6cf8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Post',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('Post_User_foreingKey',source_table='Post',local_cols=['owner_id'],referent_table='User',remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('Post_User_foreingKey','Post',sa.Integer())
    op.drop_column('Post','owner_id')
    pass

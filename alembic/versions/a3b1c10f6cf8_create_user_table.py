"""create user table

Revision ID: a3b1c10f6cf8
Revises: feabdb8b9a80
Create Date: 2023-08-21 15:59:58.257158

"""
from typing import Sequence, Union
from sqlalchemy.sql.expression import text


from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3b1c10f6cf8'
down_revision: Union[str, None] = 'feabdb8b9a80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('User',sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(100),nullable=False),
                    sa.Column('password',sa.String(50),nullable=False),
                    sa.Column('create_at',sa.DATETIME(timezone=True),nullable=False,server_default=text('GETDATE()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('User')
    pass

"""create post

Revision ID: 416fdc7e2e11
Revises: 7898fbc1c463
Create Date: 2023-08-21 12:17:58.026983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '416fdc7e2e11'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.create_table('Post', 
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False))
    pass

def downgrade() -> None:
    op.drop_table('Post')
    pass

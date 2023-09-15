"""add content title to post table

Revision ID: fe1f8f7574b5
Revises: 89eb95bacab4
Create Date: 2023-09-15 13:06:07.812587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe1f8f7574b5'
down_revision: Union[str, None] = '89eb95bacab4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')

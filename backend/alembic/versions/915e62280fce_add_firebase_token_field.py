"""Add firebase_token field

Revision ID: 915e62280fce
Revises: a9d2f6bdbb5a
Create Date: 2024-11-19 20:15:25.795713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '915e62280fce'
down_revision: Union[str, None] = 'a9d2f6bdbb5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('firebase_token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'firebase_token')
    # ### end Alembic commands ###

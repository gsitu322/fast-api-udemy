"""add phone number to user model

Revision ID: 51a98e7bb425
Revises: 
Create Date: 2025-09-02 16:48:59.682634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51a98e7bb425'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column("users", "phone_number")

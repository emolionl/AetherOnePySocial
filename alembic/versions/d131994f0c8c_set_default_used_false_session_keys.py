"""set_default_used_false_session_keys

Revision ID: d131994f0c8c
Revises: 6c3de43e4575
Create Date: 2025-01-31 12:10:59.861150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd131994f0c8c'
down_revision: Union[str, None] = '6c3de43e4575'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

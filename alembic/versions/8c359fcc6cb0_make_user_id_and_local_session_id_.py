"""Make user_id and local_session_id unique together in session_keys

Revision ID: 8c359fcc6cb0
Revises: 9febcb9c9db2
Create Date: 2025-06-12 10:50:54.341890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c359fcc6cb0'
down_revision: Union[str, None] = '9febcb9c9db2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the old unique constraint on user_id
    op.drop_constraint('session_keys_user_id_key', 'session_keys', type_='unique')
    # Add a new unique constraint on (user_id, local_session_id)
    op.create_unique_constraint(
        'session_keys_user_id_local_session_id_key',
        'session_keys',
        ['user_id', 'local_session_id']
    )


def downgrade() -> None:
    # Remove the new unique constraint
    op.drop_constraint('session_keys_user_id_local_session_id_key', 'session_keys', type_='unique')
    # Re-add the old unique constraint on user_id
    op.create_unique_constraint(
        'session_keys_user_id_key',
        'session_keys',
        ['user_id']
    )

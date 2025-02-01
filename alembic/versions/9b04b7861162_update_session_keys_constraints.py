"""Update session_keys constraints

Revision ID: 9b04b7861162
Revises: c35295a018f7
Create Date: 2025-01-31 15:04:42.564062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b04b7861162'
down_revision: Union[str, None] = 'c35295a018f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # First drop the existing unique constraint on user_id
    op.drop_constraint('session_keys_user_id_key', 'session_keys', type_='unique')
    
    # Create new composite unique constraint
    op.create_unique_constraint(
        'uix_session_keys_user_key_local',
        'session_keys',
        ['user_id', 'key', 'local_session_id']
    )


def downgrade() -> None:
    # Drop the composite constraint
    op.drop_constraint('uix_session_keys_user_key_local', 'session_keys', type_='unique')
    
    # Recreate the original constraint
    op.create_unique_constraint('session_keys_user_id_key', 'session_keys', ['user_id'])

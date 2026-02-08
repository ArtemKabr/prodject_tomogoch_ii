"""add unique index memories (user_id, type, lower(text))

Revision ID: f8c9c6daf96b
Revises: 74ecf4a3cc59
Create Date: 2026-02-08 14:13:35.011468

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8c9c6daf96b'
down_revision: Union[str, Sequence[str], None] = '74ecf4a3cc59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(  # (я добавил)
        """
        CREATE UNIQUE INDEX IF NOT EXISTS uq_memories_user_type_text_lower
        ON memories (user_id, type, lower(text));
        """
    )  # (я добавил)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS uq_memories_user_type_text_lower;")  # (я добавил)


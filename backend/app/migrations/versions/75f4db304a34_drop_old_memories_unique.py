# backend/alembic/versions/75f4db304a34_drop_old_memories_unique.py — удалить старый unique индекс memories
"""drop old memories unique

Revision ID: 75f4db304a34
Revises: c22930396f86
Create Date: 2026-02-08 14:59:16.124146

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa: F401  # (я добавил)


# revision identifiers, used by Alembic.
revision: str = "75f4db304a34"
down_revision: Union[str, Sequence[str], None] = "c22930396f86"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP INDEX IF EXISTS uq_memories_user_type_text_lower;")  # (я добавил)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(  # (я добавил)
        """
        CREATE UNIQUE INDEX IF NOT EXISTS uq_memories_user_type_text_lower
        ON memories (user_id, type, lower(text));
        """
    )  # (я добавил)

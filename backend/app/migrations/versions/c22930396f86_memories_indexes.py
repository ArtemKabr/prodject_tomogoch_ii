# backend/alembic/versions/c22930396f86_memories_indexes.py — индексы/уникальность memories
"""memories indexes

Revision ID: c22930396f86
Revises: f8c9c6daf96b
Create Date: 2026-02-08 14:56:10.617382

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa: F401  # (я добавил)


# revision identifiers, used by Alembic.
revision: str = "c22930396f86"
down_revision: Union[str, Sequence[str], None] = "f8c9c6daf96b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # unique: один и тот же текст (trim/lower) на пользователя  # (я добавил)
    op.execute(  # (я добавил)
        """
        CREATE UNIQUE INDEX IF NOT EXISTS uq_memories_user_text_norm
        ON memories (user_id, (lower(btrim(text))));
        """
    )  # (я добавил)

    # ускорение сортировок/выборок (top memories)  # (я добавил)
    op.execute(  # (я добавил)
        """
        CREATE INDEX IF NOT EXISTS ix_memories_user_importance_updated_created
        ON memories (user_id, importance DESC, updated_at DESC, created_at DESC);
        """
    )  # (я добавил)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX IF EXISTS ix_memories_user_importance_updated_created;")  # (я добавил)
    op.execute("DROP INDEX IF EXISTS uq_memories_user_text_norm;")  # (я добавил)

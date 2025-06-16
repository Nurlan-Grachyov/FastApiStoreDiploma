"""add ORM and pydentic models for products

Revision ID: 9e72d9d69364
Revises: 6cb402d1ea2e
Create Date: 2025-06-16 12:13:56.610872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e72d9d69364'
down_revision: Union[str, None] = '6cb402d1ea2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

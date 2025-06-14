"""adiciona campo syllabus_url em course

Revision ID: 5dc09a969795
Revises: 651f08302963
Create Date: 2025-06-11 14:14:53.278676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5dc09a969795'
down_revision: Union[str, None] = '651f08302963'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courses', sa.Column('syllabus_url', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('courses', 'syllabus_url')
    # ### end Alembic commands ###

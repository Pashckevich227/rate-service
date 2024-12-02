"""Add rate and price tables

Revision ID: 6ff6553cf4ab
Revises:
Create Date: 2024-12-02 14:00:00

"""
from typing import Union, Sequence
from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision = '6ff6553cf4ab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'price',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('price', sa.Float, nullable=False)
    )

    op.create_table(
        'rate',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('date', sa.String(length=10), nullable=False),
        sa.Column('cargo_type', sa.String, nullable=False),
        sa.Column('rate', sa.String, nullable=False),
        sa.Column('price_id', sa.Integer, sa.ForeignKey('price.id'), nullable=True)
    )


def downgrade() -> None:
    op.drop_table('rate')
    op.drop_table('price')

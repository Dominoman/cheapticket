"""Add route index

Revision ID: 6201c75a4852
Revises: 4488a85481d8
Create Date: 2024-09-12 13:10:13.277222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6201c75a4852'
down_revision: Union[str, None] = '4488a85481d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(op.f('route_idx'), 'itinerary2route', ['route_id'], unique=False)



def downgrade() -> None:
    op.drop_index(op.f('route_idx'), table_name='itinerary2route')


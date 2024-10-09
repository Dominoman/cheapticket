"""Foreign key change

Revision ID: 26ea3feffe8a
Revises: 8f8e7793bd21
Create Date: 2024-10-04 13:57:06.450174

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '26ea3feffe8a'
down_revision: Union[str, None] = '8f8e7793bd21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('PRAGMA foreign_keys=off')
    op.rename_table('itinerary2route', '_itinerary2route_new')
    op.create_table(
        'itinerary2route',
        sa.Column('search_id', sa.String(36), nullable=False),
        sa.Column('itinerary_id', sa.String(255), nullable=False),
        sa.Column('route_id', sa.String(26), nullable=False),
        sa.PrimaryKeyConstraint('search_id', 'itinerary_id', 'route_id'),
        sa.ForeignKeyConstraint(['search_id', 'itinerary_id'], ['itinerary.search_id', 'itinerary.id']),
        sa.ForeignKeyConstraint(['route_id'], ['route.id'])
    )
    op.execute('INSERT INTO itinerary2route SELECT * FROM _itinerary2route_new')
    op.drop_table('_itinerary2route_new')
    op.execute('PRAGMA foreign_keys=on')

    bind = op.get_bind()
    bind.connection.commit()
    if bind.dialect.name == 'sqlite':
        # Execute the VACUUM command for SQLite
        op.execute('VACUUM')


def downgrade() -> None:
   pass

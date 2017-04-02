"""add icon column to MQTTItem

Revision ID: eef456f73654
Revises: f4c55277bc6f
Create Date: 2017-04-02 19:12:24.467709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eef456f73654'
down_revision = 'f4c55277bc6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mqtt_items', sa.Column('icon', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mqtt_items', 'icon')
    # ### end Alembic commands ###

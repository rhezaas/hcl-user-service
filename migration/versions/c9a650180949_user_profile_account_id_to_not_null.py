"""user.profile.account_id to not null

Revision ID: c9a650180949
Revises: aa9df77734d0
Create Date: 2021-01-16 18:59:34.100371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9a650180949'
down_revision = 'aa9df77734d0'
branch_labels = None
depends_on = None


def upgrade():
    # add constraint not null to account_id in user.profile
    op.alter_column('profile', 'account_id', False, schema='user')


def downgrade():
    # rollback add constraint not null to account_id in user.profile
    op.alter_column('profile', 'account_id', True, schema='user')

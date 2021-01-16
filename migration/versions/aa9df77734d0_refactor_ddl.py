"""refactor ddl

Revision ID: aa9df77734d0
Revises: 617d6d1ed309
Create Date: 2021-01-16 18:11:52.327982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa9df77734d0'
down_revision = '617d6d1ed309'
branch_labels = None
depends_on = None


def upgrade():
    # rename table user to profile
    op.rename_table('user', 'profile', schema='user')

    # add column account_id
    op.add_column('profile', sa.Column('account_id', sa.Integer, sa.ForeignKey('user.account.id'), unique=True, nullable=True), schema='user')

    # drop column user_id in table user.account
    op.drop_column('account', 'user_id', schema='user')

    # rename user_id to profile_id in table user.image
    op.alter_column('image', 'user_id', new_column_name='profile_id', schema='user')

    # drop constraint user_id in table user.image
    op.drop_constraint('image_user_id_fkey', 'image', schema='user')

    # create foreign_key for profile_id in table user.image
    op.create_foreign_key('image_profile_id_fkey', 'image', 'profile', ['profile_id'], ['id'], source_schema='user', referent_schema='user')

def downgrade():
    # rollback rename
    op.rename_table('profile', 'user', schema='user')

    # drop column account_id
    op.drop_column('profile', 'account_id', schema='user')

    # add column user_id in table user.account
    op.add_column('account', sa.Column('user_id', sa.Integer, sa.ForeignKey('user.user.id'), unique=True, nullable=False), schema='user')

    # alter back relation profile_id to user_id in table user.image
    op.alter_column('image', 'profile_id', new_column_name='user_id', schema='user')

    # drop constraint profile_id in table user.image
    op.drop_constraint('image_profile_id_fkey', 'image', schema='user')

    # create foreign_key for profile_id in table user.image
    op.create_foreign_key('image_user_id_fkey', 'image', 'user', ['user_id'], ['id'], source_schema='user', referent_schema='user')

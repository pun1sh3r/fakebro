"""empty message

Revision ID: 68520cda0d93
Revises: 
Create Date: 2022-01-11 15:51:20.585090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68520cda0d93'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fakefollower',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('follower_handle', sa.String(length=100), nullable=True),
    sa.Column('follower_score', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('follower_id')
    )
    op.create_index(op.f('ix_fakefollower_follower_handle'), 'fakefollower', ['follower_handle'], unique=False)
    op.create_table('handle',
    sa.Column('handle_id', sa.Integer(), nullable=False),
    sa.Column('ig_handle', sa.String(length=100), nullable=True),
    sa.Column('ig_follower_count', sa.Integer(), nullable=True),
    sa.Column('ig_followed_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('handle_id')
    )
    op.create_index(op.f('ix_handle_ig_handle'), 'handle', ['ig_handle'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('joined_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_joined_at'), 'user', ['joined_at'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.String(length=20), nullable=True),
    sa.Column('like_count', sa.Integer(), nullable=True),
    sa.Column('comment_count', sa.Integer(), nullable=True),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['handle.handle_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('comment_count'),
    sa.UniqueConstraint('like_count')
    )
    op.create_index(op.f('ix_comments_post_id'), 'comments', ['post_id'], unique=True)
    op.create_table('rel',
    sa.Column('handle_id', sa.Integer(), nullable=True),
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['follower_id'], ['fakefollower.follower_id'], ),
    sa.ForeignKeyConstraint(['handle_id'], ['handle.handle_id'], )
    )
    op.create_table('task',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_name'), 'task', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_name'), table_name='task')
    op.drop_table('task')
    op.drop_table('rel')
    op.drop_index(op.f('ix_comments_post_id'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_user_joined_at'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_handle_ig_handle'), table_name='handle')
    op.drop_table('handle')
    op.drop_index(op.f('ix_fakefollower_follower_handle'), table_name='fakefollower')
    op.drop_table('fakefollower')
    # ### end Alembic commands ###

"""init

Revision ID: bc08f9de3587
Revises: 
Create Date: 2022-10-26 11:21:08.672237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc08f9de3587'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_companies_id'), 'companies', ['id'], unique=False)
    op.create_index(op.f('ix_companies_name'), 'companies', ['name'], unique=True)
    op.create_index(op.f('ix_companies_owner_id'), 'companies', ['owner_id'], unique=False)
    op.create_table('members',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('company_id', 'user_id')
    )
    op.create_table('quizzes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('frequency', sa.Integer(), nullable=True),
    sa.Column('quiz', sa.JSON(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quizzes_company_id'), 'quizzes', ['company_id'], unique=False)
    op.create_index(op.f('ix_quizzes_id'), 'quizzes', ['id'], unique=False)
    op.create_table('requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('side', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requests_company_id'), 'requests', ['company_id'], unique=False)
    op.create_index(op.f('ix_requests_id'), 'requests', ['id'], unique=False)
    op.create_index(op.f('ix_requests_user_id'), 'requests', ['user_id'], unique=False)
    op.create_table('results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('quiz_id', sa.Integer(), nullable=True),
    sa.Column('overall_questions', sa.Integer(), nullable=True),
    sa.Column('correct_answers', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_results_id'), 'results', ['id'], unique=False)
    op.create_index(op.f('ix_results_quiz_id'), 'results', ['quiz_id'], unique=False)
    op.create_index(op.f('ix_results_user_id'), 'results', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_results_user_id'), table_name='results')
    op.drop_index(op.f('ix_results_quiz_id'), table_name='results')
    op.drop_index(op.f('ix_results_id'), table_name='results')
    op.drop_table('results')
    op.drop_index(op.f('ix_requests_user_id'), table_name='requests')
    op.drop_index(op.f('ix_requests_id'), table_name='requests')
    op.drop_index(op.f('ix_requests_company_id'), table_name='requests')
    op.drop_table('requests')
    op.drop_index(op.f('ix_quizzes_id'), table_name='quizzes')
    op.drop_index(op.f('ix_quizzes_company_id'), table_name='quizzes')
    op.drop_table('quizzes')
    op.drop_table('members')
    op.drop_index(op.f('ix_companies_owner_id'), table_name='companies')
    op.drop_index(op.f('ix_companies_name'), table_name='companies')
    op.drop_index(op.f('ix_companies_id'), table_name='companies')
    op.drop_table('companies')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###

"""create documents table

Revision ID: ac983f083b19
Revises: 
Create Date: 2022-09-04 20:32:28.799488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac983f083b19'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'document',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('text', sa.Text, nullable=False),
        sa.Column('summary', sa.Text, nullable=True),
    )
    op.create_index(op.f('ix_document_id'), 'document', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_document_id'), table_name='document')
    op.drop_table('document')

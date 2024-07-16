"""Add hashed_password to users

Revision ID: 384c777a0fa0
Revises: 
Create Date: 2024-07-16 09:27:22.289086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '384c777a0fa0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('instruments', 'name',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=50),
               nullable=False)
    op.alter_column('instruments', 'price',
               existing_type=mysql.DECIMAL(precision=10, scale=0),
               nullable=False)
    op.alter_column('levels', 'instruments_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('levels', 'level',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=50),
               nullable=False)
    op.alter_column('packs', 'pack',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=50),
               nullable=False)
    op.alter_column('packs', 'discount_1',
               existing_type=mysql.DECIMAL(precision=10, scale=0),
               nullable=False)
    op.alter_column('packs', 'discount_2',
               existing_type=mysql.DECIMAL(precision=10, scale=0),
               nullable=False)
    op.alter_column('packs_instruments', 'instrument_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('packs_instruments', 'packs_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'packs_instruments', 'instruments', ['instrument_id'], ['id'])
    op.create_foreign_key(None, 'packs_instruments', 'packs', ['packs_id'], ['id'])
    op.alter_column('students', 'family_id',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    op.alter_column('teachers', 'first_name',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=50),
               nullable=False)
    op.alter_column('teachers', 'last_name',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=50),
               nullable=False)
    op.alter_column('teachers', 'phone',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=50),
               nullable=False)
    op.alter_column('teachers', 'mail',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=255),
               nullable=True)
    op.alter_column('teachers_instruments', 'teacher_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('teachers_instruments', 'instrument_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'teachers_instruments', 'teachers', ['teacher_id'], ['id'])
    op.create_foreign_key(None, 'teachers_instruments', 'instruments', ['instrument_id'], ['id'])
    op.add_column('users', sa.Column('hashed_password', sa.String(length=300), nullable=False))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'users', ['username'])
    op.drop_column('users', 'email')
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', mysql.VARCHAR(length=50), nullable=False))
    op.add_column('users', sa.Column('email', mysql.VARCHAR(length=50), nullable=False))
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'hashed_password')
    op.drop_constraint(None, 'teachers_instruments', type_='foreignkey')
    op.drop_constraint(None, 'teachers_instruments', type_='foreignkey')
    op.alter_column('teachers_instruments', 'instrument_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('teachers_instruments', 'teacher_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('teachers', 'mail',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('teachers', 'phone',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('teachers', 'last_name',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('teachers', 'first_name',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('students', 'family_id',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    op.drop_constraint(None, 'packs_instruments', type_='foreignkey')
    op.drop_constraint(None, 'packs_instruments', type_='foreignkey')
    op.alter_column('packs_instruments', 'packs_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('packs_instruments', 'instrument_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('packs', 'discount_2',
               existing_type=mysql.DECIMAL(precision=10, scale=0),
               nullable=True)
    op.alter_column('packs', 'discount_1',
               existing_type=mysql.DECIMAL(precision=10, scale=0),
               nullable=True)
    op.alter_column('packs', 'pack',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('levels', 'level',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('levels', 'instruments_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.alter_column('instruments', 'price',
               existing_type=mysql.DECIMAL(precision=10, scale=0),
               nullable=True)
    op.alter_column('instruments', 'name',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###

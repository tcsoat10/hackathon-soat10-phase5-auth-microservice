"""populate admin user

Revision ID: 9d34ec9bfc70
Revises: 690a8cddf862
Create Date: 2025-08-25 22:18:24.522161

"""
import os
import bcrypt
from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer


# revision identifiers, used by Alembic.
revision: str = '9d34ec9bfc70'
down_revision: Union[str, None] = '690a8cddf862'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

users_table = table(
    'users',
    column('id', Integer),
    column('name', String),
    column('password_hash', String),
    column('profile_id', Integer)
)

users = [
    {
        'name': 'administrator',
        'password_hash': bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        'profile_id': 1
    }
]

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    op.bulk_insert(users_table, users)

def downgrade():
    op.execute(
        "DELETE FROM users WHERE name IN ('administrator')"
    )
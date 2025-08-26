"""populate profiles

Revision ID: 1c1b831480d4
Revises: 3a830bf3f7c9
Create Date: 2025-08-25 20:51:51.528706

"""
import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String


# revision identifiers, used by Alembic.
revision: str = '1c1b831480d4'
down_revision: Union[str, None] = '3a830bf3f7c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


profiles_table = table(
    'profiles',
    column('id', String),
    column('name', String),
    column('description', String)
)

profiles = [
    {"name": "administrator", "description": "Manager with full access."},
    {"name": "manager", "description": "Manager with full access."},
    {"name": "employee", "description": "Employee with restricted access."},
    {"name": "customer", "description": "Customer with limited access."},
]

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return

    op.bulk_insert(profiles_table, profiles)

def downgrade():
    op.execute(
        "DELETE FROM profiles WHERE name IN ('administrator', 'manager', 'employee', 'customer')"
    )

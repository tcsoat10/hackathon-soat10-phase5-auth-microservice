"""populate admin person

Revision ID: 38fafd36c87d
Revises: 9d34ec9bfc70
Create Date: 2025-08-25 22:21:30.146712

"""
from typing import Sequence, Union

import os
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Date
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '38fafd36c87d'
down_revision: Union[str, None] = '9d34ec9bfc70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


persons_table = table(
    'persons',
    column('id', Integer),
    column('cpf', String),
    column('name', String),
    column('email', String),
    column('birth_date', Date)
)


persons = [
    {
        'name': 'administrator', 
        'cpf': None,
        'email': None,
        'birth_date': datetime(1900, 1, 1)
    }
]
    

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    op.bulk_insert(persons_table, persons)

def downgrade():
    op.execute(
        "DELETE FROM persons WHERE name IN ('administrator')"
    )
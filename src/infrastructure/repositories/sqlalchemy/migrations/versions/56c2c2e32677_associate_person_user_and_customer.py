"""associate person, user and customer

Revision ID: 56c2c2e32677
Revises: a44a6bea63c9
Create Date: 2025-08-25 22:28:21.266920

"""
import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column, select
from sqlalchemy import String, Integer, MetaData


# revision identifiers, used by Alembic.
revision: str = '56c2c2e32677'
down_revision: Union[str, None] = '38fafd36c87d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


customer_table = table(
    'customers',
    column('id', Integer),
    column('person_id', Integer),
    column('user_id', Integer)
)

persons_table = table(
    'persons',
    column('id', Integer),
    column('name', String)
)

users_table = table(
    'users',
    column('id', Integer),
    column('name', String)
)


employees = [
    {
        'name': 'administrator',
        'user': 'administrator',
    }
]
    

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    connection = op.get_bind()
    metadata = MetaData()
    metadata.reflect(bind=connection)

    persons_mapping = {}
    result = connection.execute(select(persons_table.c.id, persons_table.c.name))
    for row in result:
        persons_mapping[row[1]] = row[0]

    users_mapping = {}
    result = connection.execute(select(users_table.c.id, users_table.c.name))
    for row in result:
        users_mapping[row[1]] = row[0]

    insert_data = []
    for employee in employees:
        person_id = persons_mapping.get(employee['name'])
        user_id = users_mapping.get(employee['user'])
        if person_id and user_id:
            insert_data.append({
                'person_id': person_id,
                'user_id': user_id
            })
    
    op.bulk_insert(customer_table, insert_data)

def downgrade():
    connection = op.get_bind()
    metadata = MetaData()
    metadata.reflect(bind=connection)

    persons_mapping = {}
    result = connection.execute(select(persons_table.c.id, persons_table.c.name))
    for row in result:
        persons_mapping[row[1]] = row[0]
    
    persons_id_list = []
    for employee in employees:
        person_id = persons_mapping.get(employee['name'])
        if person_id:
            persons_id_list.append(person_id)

    if persons_id_list:
        ids = ', '.join(map(str, persons_id_list))
        op.execute(
            f"DELETE FROM customers WHERE person_id IN ({ids})"
        )

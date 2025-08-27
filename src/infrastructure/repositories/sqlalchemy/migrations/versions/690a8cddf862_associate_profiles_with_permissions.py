"""associate profiles with permissions

Revision ID: 690a8cddf862
Revises: 1c1b831480d4
Create Date: 2025-08-25 20:53:29.079479

"""
import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column, select
from sqlalchemy import Integer, String, DateTime, MetaData
from datetime import datetime, timezone
from src.core.constants.permissions import (
    CustomerPermissions,
    PermissionPermissions,
    ProfilePermissions,
    ProfilePermissionPermissions,
    UserPermissions,
    UserProfilePermissions,
    PersonPermissions,
)

# revision identifiers, used by Alembic.
revision: str = '690a8cddf862'
down_revision: Union[str, None] = '1c1b831480d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Tabela de referência
profile_permissions_table = table(
    'profile_permissions',
    column('profile_id', String),
    column('permission_id', String),
    column('created_at', DateTime)
)

permissions_table = table(
    'permissions',
    column('id', Integer),
    column('name', String)
)

# Perfis e permissões associadas
profile_permissions = {
    "1": [  # Administrator: todas as permissões
        *PermissionPermissions.values(),
        *ProfilePermissions.values(),
        *ProfilePermissionPermissions.values(),
        *UserPermissions.values(),
        *UserProfilePermissions.values(),
        *CustomerPermissions.values(),
        *PersonPermissions.values(),
    ],
    "2": [  # Manager
        *PermissionPermissions.values(),
        *ProfilePermissions.values(),
        *ProfilePermissionPermissions.values(),
        *UserPermissions.values(),
        *UserProfilePermissions.values(),
        *CustomerPermissions.values(),
        *PersonPermissions.values(),
    ],
    "3": [  # Employee
        *PermissionPermissions.list_only_values(only=["CAN_VIEW"]),
        *ProfilePermissions.list_only_values(only=["CAN_VIEW"]),
        *ProfilePermissionPermissions.list_only_values(only=["CAN_VIEW"]),
        *UserPermissions.list_only_values(only=["CAN_VIEW"]),
        *UserProfilePermissions.list_only_values(only=["CAN_VIEW"]),
        *CustomerPermissions.list_only_values(only=["CAN_VIEW"]),
        *PersonPermissions.list_only_values(only=["CAN_VIEW", "CAN_UPDATE"]),
    ],
    "4": [  # Customer: acesso mínimo
        *CustomerPermissions.list_only_values(only=["CAN_VIEW", "CAN_UPDATE"])
    ]
}

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return

    connection = op.get_bind()
    metadata = MetaData()
    metadata.reflect(bind=connection)

    permissions_mapping = {}
    result = connection.execute(select(permissions_table.c.id, permissions_table.c.name))
    for row in result:
        permissions_mapping[row[1]] = row[0]

    
    insert_data = []
    for profile_id, permissions in profile_permissions.items():
        for permission_name in permissions:
            permission_id = permissions_mapping.get(permission_name)
            if permission_id:
                insert_data.append({
                    "profile_id": int(profile_id),
                    "permission_id": permission_id,
                    "created_at": datetime.now(timezone.utc)
                })

    op.bulk_insert(profile_permissions_table, insert_data)
    pass


def downgrade():
    op.execute("DELETE FROM profile_permissions WHERE profile_id IN ('1', '2', '3', '4')")
    # pass

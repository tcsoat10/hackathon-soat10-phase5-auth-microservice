"""populate permissions

Revision ID: 3a830bf3f7c9
Revises: e4229cbd5f9f
Create Date: 2025-08-25 00:49:26.143285

"""
import os
from typing import Sequence, Union

from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, DateTime

from src.core.constants.permissions import (
    CustomerPermissions,
    PermissionPermissions,
    PersonPermissions,
    ProfilePermissionPermissions,
    ProfilePermissions,
    UserPermissions,
    UserProfilePermissions
)


# revision identifiers, used by Alembic.
revision: str = '3a830bf3f7c9'
down_revision: Union[str, None] = 'e4229cbd5f9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


permissions_table = table(
    'permissions',
    column('id', String),
    column('name', String),
    column('description', String),
    column('created_at', DateTime),
    column('updated_at', DateTime),
    column('inactivated_at', DateTime),
)

permissions = [
    # Permissions
    *PermissionPermissions.values_and_descriptions(),

    # Profile
    *ProfilePermissions.values_and_descriptions(),

    # Profile Permissions
    *ProfilePermissionPermissions.values_and_descriptions(),

    # Users
    *UserPermissions.values_and_descriptions(),

    # User Profiles
    *UserProfilePermissions.values_and_descriptions(),

    # Customers
    *CustomerPermissions.values_and_descriptions(),

    # Person
    *PersonPermissions.values_and_descriptions(),
]


def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return

    op.bulk_insert(permissions_table, permissions)


def downgrade():
    op.execute("DELETE FROM permissions WHERE name LIKE 'can_%'")

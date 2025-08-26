from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from src.infrastructure.repositories.sqlalchemy.models.base_model import BaseModel
from src.core.domain.entities.permission import Permission
from src.core.shared.identity_map import IdentityMap


class PermissionModel(BaseModel):
    __tablename__ = "permissions"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))

    profile_associations = relationship(
        "ProfilePermissionModel",
        back_populates="permission",
        cascade="all, delete-orphan"
    )

    profiles = association_proxy("profile_associations", "profile")

    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            inactivated_at=entity.inactivated_at
        )

    def to_entity(self) -> Permission:
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing = identity_map.get(Permission, self.id)
        if existing:
            return existing

        permission = Permission(
            id=self.id,
            name=self.name,
            description=self.description,
            profiles=None,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at
        )
        identity_map.add(permission)
        
        permission.profiles = [profile.to_entity() for profile in self.profiles]
        
        return permission


__all__ = ["PermissionModel"]

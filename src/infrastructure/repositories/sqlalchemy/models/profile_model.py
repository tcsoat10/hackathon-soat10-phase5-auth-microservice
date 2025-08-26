from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from src.infrastructure.repositories.sqlalchemy.models.base_model import BaseModel
from src.core.domain.entities.profile import Profile
from src.core.shared.identity_map import IdentityMap


class ProfileModel(BaseModel):
    __tablename__ = "profiles"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))

    permission_associations = relationship(
        "ProfilePermissionModel",
        back_populates="profile",
        cascade="all, delete-orphan"
    )

    permissions = association_proxy("permission_associations", "permission")

    users = relationship("UserModel", back_populates="profile")

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

    def to_entity(self):
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing = identity_map.get(Profile, self.id)
        if existing:
            return existing

        profile = Profile(
            id=self.id,
            name=self.name,
            permissions=[permission.to_entity() for permission in self.permissions],
            users=[user.to_entity() for user in self.users],
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at
        )
        identity_map.add(profile)
        return profile


__all__ = ["ProfileModel"]

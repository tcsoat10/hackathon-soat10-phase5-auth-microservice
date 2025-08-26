from src.infrastructure.repositories.sqlalchemy.models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship


class ProfilePermissionModel(BaseModel):
    __tablename__ = 'profile_permissions'

    profile_id = Column(ForeignKey('profiles.id'), nullable=False)
    permission_id = Column(ForeignKey('permissions.id'), nullable=False)

    profile = relationship('ProfileModel', back_populates='permission_associations')
    permission = relationship('PermissionModel', back_populates='profile_associations')

__all__ = ['ProfilePermissionModel']

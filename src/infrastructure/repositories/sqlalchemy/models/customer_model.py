
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.customer import Customer
from src.infrastructure.repositories.sqlalchemy.models.base_model import BaseModel


class CustomerModel(BaseModel):
    __tablename__ = 'customers'

    person_id = Column(ForeignKey('persons.id'), nullable=True)
    person = relationship('PersonModel')
    
    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('UserModel')

    @classmethod
    def from_entity(cls, customer: Customer):
        return cls(
            id=getattr(customer, 'id', None),
            created_at=getattr(customer, 'created_at', None),
            updated_at=getattr(customer, 'updated_at', None),
            inactivated_at=getattr(customer, 'inactivated_at', None),
            person_id=customer.person.id,
            user_id=customer.user.id,
        )
    
    def to_entity(self):
        identity_map = IdentityMap.get_instance()

        existing = identity_map.get(Customer, self.id)
        if existing:
            return existing
        
        person = self._get_person(identity_map)
        user = self._get_user(identity_map)
        
        customer_entity = Customer(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at,
            person=person,
            user=user,            
        )
        identity_map.add(customer_entity)
        return customer_entity

    def _get_person(self, identity_map: IdentityMap):
        from src.core.domain.entities.person import Person
        
        existing = identity_map.get(Person, self.person_id)
        if existing:
            return existing
        return self.person.to_entity()
    
    def _get_user(self, identity_map: IdentityMap):
        from src.core.domain.entities.user import User
        
        existing = identity_map.get(User, self.user_id)
        if existing:
            return existing

        return self.user.to_entity()

__all__ = ['CustomerModel']

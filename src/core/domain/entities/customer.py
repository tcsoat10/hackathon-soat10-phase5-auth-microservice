from src.core.domain.entities.base_entity import BaseEntity
from src.core.domain.entities.person import Person
from src.core.domain.entities.user import User
from typing import Optional



class Customer(BaseEntity):
    def __init__(
        self,
        person: Person,
        user: User,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        inactivated_at: Optional[str] = None
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self._person: Person = person
        self._user: User = user

    @property
    def person(self) -> Person:
        return self._person
    
    @person.setter
    def person(self, value: Person):
        self._person = value

    @property
    def user(self) -> User:
        return self._user
    
    @user.setter
    def user(self, value: User):
        self._user = value


__all__ = ['Customer']

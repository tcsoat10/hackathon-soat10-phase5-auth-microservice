from pydantic import BaseModel, ConfigDict
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO
from src.core.domain.dtos.user.create_user_dto import CreateUserDTO


class CreateCustomerDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    person: CreatePersonDTO
    user: CreateUserDTO


__all__ = ['CreateCustomerDTO']
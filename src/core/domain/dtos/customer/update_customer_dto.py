from pydantic import BaseModel, ConfigDict

from src.core.domain.dtos.person.update_person_dto import UpdatePersonDTO

class UpdateCustomerDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    person: UpdatePersonDTO


__all__ = ['UpdateCustomerDTO']

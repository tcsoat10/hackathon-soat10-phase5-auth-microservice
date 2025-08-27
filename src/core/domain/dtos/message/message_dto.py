from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class MessageDTO(BaseModel):
    message: Optional[str] = Field(None, min_length=3, max_length=100)
    status: Optional[str] = Field(None, min_length=3, max_length=100)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MessageDTO':
        return cls(**data)

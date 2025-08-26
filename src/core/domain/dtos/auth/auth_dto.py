from pydantic import BaseModel


class LoginDTO(BaseModel):
    username: str
    password: str

class TokenDTO(BaseModel):
    access_token: str
    token_type: str
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            access_token=data.get("access_token"),
            token_type=data.get("token_type")
        )

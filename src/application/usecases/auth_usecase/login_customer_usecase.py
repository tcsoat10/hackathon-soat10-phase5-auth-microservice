
from typing import Any, Dict
from src.core.domain.dtos.auth.auth_dto import LoginDTO
from src.core.domain.entities.customer import Customer
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.invalid_credentials_exception import InvalidCredentialsException
from src.core.utils.jwt_util import JWTUtil
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository


class LoginCustomerUseCase:
    
    def __init__(
        self,
        customer_gateway: ICustomerRepository,
        profile_gateway: IProfileRepository,
    ):
        self.customer_gateway = customer_gateway
        self.profile_gateway = profile_gateway
        
    @classmethod
    def build(
        cls,
        customer_gateway: ICustomerRepository,
        profile_gateway: IProfileRepository
    ) -> 'LoginCustomerUseCase':
        return cls(customer_gateway, profile_gateway)
    
    def execute(self, dto: LoginDTO) -> Dict[str, Any]:
        customer: Customer = self.customer_gateway.get_by_username(dto.username)
        if not customer or not customer.user.verify_password(dto.password):
            raise InvalidCredentialsException()
        
        if customer.is_deleted():
            raise InvalidCredentialsException()

        permissions = [permission.name for permission in customer.user.profile.permissions]
        if not permissions:
            raise EntityNotFoundException(entity_name="Customer permissions")

        token_payload = {
            "person": {
                "id": str(customer.id),
                "name": customer.person.name,
                "cpf": customer.person.cpf,
                "email": customer.person.email,
            },
            "profile": {
                "name": customer.user.profile.name,
                "permissions": permissions,
            },
        }

        token = JWTUtil.create_token(token_payload)
        return {
            "token_type": "Bearer",
            "access_token": token,
        }

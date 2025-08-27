from src.core.exceptions.unauthorized_access_exception import UnauthorizedAccessException
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.dtos.user.update_user_dto import UpdateUserDTO
from src.core.domain.entities.user import User
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class UpdateUserPasswordUsecase:
    def __init__(self, user_gateway: IUserRepository, customer_gateway: ICustomerRepository):
        self.user_gateway = user_gateway
        self.customer_gateway = customer_gateway

    @classmethod
    def build(cls, user_gateway: IUserRepository, customer_gateway: ICustomerRepository) -> 'UpdateUserPasswordUsecase':
        return cls(user_gateway, customer_gateway)
    
    def execute(self, user_id: int, dto: UpdateUserDTO) -> User:
        customer = self.customer_gateway.get_by_id(user_id)
        if not customer:
            raise EntityNotFoundException(entity_name='Customer')
        
        user = customer.user
        if user.verify_password(dto.old_password) is False:
            raise UnauthorizedAccessException('Wrong password')
        
        user.name = user.name
        user.password = dto.password
        updated_user = self.user_gateway.update(user)

        return updated_user
    
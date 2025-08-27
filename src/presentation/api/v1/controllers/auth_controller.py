from src.application.usecases.auth_usecase.login_customer_usecase import LoginCustomerUseCase
from src.presentation.api.v1.presenters.dto_presenter import DTOPresenter
from src.core.domain.dtos.auth.auth_dto import LoginDTO, TokenDTO
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository

class AuthController:
    def __init__(
        self,
        profile_gateway: IProfileRepository,
        customer_gateway: ICustomerRepository
    ):
        self.profile_gateway: IProfileRepository = profile_gateway
        self.customer_gateway: ICustomerRepository = customer_gateway
        
    def login_customer(self, dto: LoginDTO) -> TokenDTO:
        login_customer_by_cpf_use_case = LoginCustomerUseCase.build(
            self.customer_gateway,
            self.profile_gateway,
        )
        token = login_customer_by_cpf_use_case.execute(dto)
        return DTOPresenter.transform_from_dict(token, TokenDTO)

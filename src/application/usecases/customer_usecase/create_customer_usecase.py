from src.core.domain.entities.user import User
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.domain.dtos.customer.create_customer_dto import CreateCustomerDTO
from src.core.domain.entities.customer import Customer
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.entities.person import Person
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.ports.user.i_user_repository import IUserRepository


class CreateCustomerUsecase:
    def __init__(
        self,
        customer_gateway: ICustomerRepository,
        person_gateway: IPersonRepository,
        user_gateway: IUserRepository,
        profile_gateway: IProfileRepository
    ):
        self.customer_gateway = customer_gateway
        self.person_gateway = person_gateway
        self.user_gateway = user_gateway
        self.profile_gateway = profile_gateway

    @classmethod
    def build(
        cls,
        customer_gateway: ICustomerRepository,
        person_gateway: IPersonRepository,
        user_gateway: IUserRepository,
        profile_gateway: IProfileRepository
    ) -> 'CreateCustomerUsecase':
        return cls(customer_gateway, person_gateway, user_gateway, profile_gateway)
    
    def execute(self, dto: CreateCustomerDTO) -> Customer:
        person = self.person_gateway.get_by_cpf(dto.person.cpf)
        if not person:
            if self.person_gateway.exists_by_email(dto.person.email):
                raise EntityDuplicatedException(entity_name='Customer')
            
            person = Person(
                name=dto.person.name,
                cpf=dto.person.cpf,
                email=dto.person.email,
                birth_date=dto.person.birth_date
            )
            person = self.person_gateway.create(person)
        else:
            person.name = dto.person.name
            person.email = dto.person.email
            person.birth_date = dto.person.birth_date
            if person.is_deleted():
                person.reactivate()
            person = self.person_gateway.update(person)
        
        
        user = self.user_gateway.get_by_name(dto.user.name)
        if user:
            raise EntityDuplicatedException(entity_name='User')

        user = User(name=dto.user.name, password=dto.user.password)
        customer_profile = self.profile_gateway.get_by_name('customer')

        if not customer_profile:
            raise EntityNotFoundException(entity_name='Customer profile')

        user.profile = customer_profile
        user = self.user_gateway.create(user)

        customer = self.customer_gateway.get_by_person_id(person.id)
        if customer:
            if not customer.is_deleted():
                raise EntityDuplicatedException(entity_name='Customer')
            
            customer.reactivate()
            self.customer_gateway.update(customer)
        else:
            customer = Customer(person=person, user=user)
            customer = self.customer_gateway.create(customer)

        return customer

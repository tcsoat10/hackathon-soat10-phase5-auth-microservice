import pytest
from datetime import datetime
from src.core.domain.dtos.person.update_person_dto import UpdatePersonDTO
from src.core.domain.dtos.user.create_user_dto import CreateUserDTO
from src.core.domain.dtos.user.update_user_dto import UpdateUserDTO
from src.infrastructure.repositories.sqlalchemy.customer_repository import CustomerRepository
from src.infrastructure.repositories.sqlalchemy.person_repository import PersonRepository
from src.infrastructure.repositories.sqlalchemy.profile_repository import ProfileRepository
from src.infrastructure.repositories.sqlalchemy.user_repository import UserRepository
from src.application.usecases.customer_usecase.create_customer_usecase import CreateCustomerUsecase
from src.application.usecases.customer_usecase.get_all_customers_usecase import GetAllCustomersUsecase
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.dtos.customer.create_customer_dto import CreateCustomerDTO
from src.core.domain.dtos.customer.update_customer_dto import UpdateCustomerDTO
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO
from src.application.usecases.customer_usecase.delete_customer_usecase import DeleteCustomerUsecase
from src.application.usecases.customer_usecase.update_customer_usecase import UpdateCustomerUsecase
from pycpfcnpj import gen

from tests.factories.customer_factory import CustomerFactory
from tests.factories.profile_factory import ProfileFactory

class TestCustomerUsecases:

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.customer_gateway = CustomerRepository(db_session)
        self.person_gateway = PersonRepository(db_session)
        self.user_gateway = UserRepository(db_session)
        self.profile_gateway = ProfileRepository(db_session)

        self.create_customer_usecase = CreateCustomerUsecase(
            self.customer_gateway,
            self.person_gateway,
            self.user_gateway,
            self.profile_gateway,
        )
        self.update_customer_usecase = UpdateCustomerUsecase(
            self.customer_gateway,
            self.person_gateway,
            self.user_gateway,
            self.profile_gateway,
        )
        self.get_all_customers_usecase = GetAllCustomersUsecase(self.customer_gateway)
        self.delete_customer_usecase = DeleteCustomerUsecase(self.customer_gateway)

    def test_create_customer_usecase(self):
        cpf = gen.cpf()
        person_dto = CreatePersonDTO(
            name='John Doe',
            cpf=cpf,
            email='john@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )
        
        ProfileFactory(name='customer')
        user_dto = CreateUserDTO(name='john.doe', password='12345678')

        dto = CreateCustomerDTO(person=person_dto, user=user_dto)
        customer = self.create_customer_usecase.execute(dto)

        assert customer.id is not None
        assert customer.user.id == 1
        assert customer.person.name == 'John Doe'
        assert customer.person.cpf == cpf
        assert customer.person.email == 'john@example.com'
        assert customer.person.birth_date is not None
        assert customer.user.verify_password('12345678') is True

    def test_update_customer_usecase(self):
        customer = CustomerFactory()

        update_person_dto = UpdatePersonDTO(
            id=customer.person.id,
            name='Jane Doe',
            cpf=customer.person.cpf,
            email='jane@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )

        updated_customer_dto = UpdateCustomerDTO(
            id=customer.person.id,
            person=update_person_dto
        )

        current_user = {
            'profile': {'name': 'manager'},
            'person': {
                'id': customer.person.id,
                'cpf': customer.person.cpf,
                'name': customer.person.name,
                'email': customer.person.email
            }
        }
        updated_customer = self.update_customer_usecase.execute(customer.id, updated_customer_dto, current_user)

        assert updated_customer.person.name == 'Jane Doe'
        assert updated_customer.person.email == 'jane@example.com'
        assert updated_customer.person.birth_date is not None
        assert updated_customer.person.cpf == customer.person.cpf

    def test_create_duplicate_customer_usecase(self):
        customer = CustomerFactory()
        ProfileFactory(name='customer')

        person_dto = CreatePersonDTO(
            name='John Doe',
            cpf=customer.person.cpf,
            email='john@example.com',
            birth_date=datetime.now().strftime('%Y-%m-%d')
        )
        
        user_dto = CreateUserDTO(
            name='john.doe',
            password='12345678'
        )

        dto = CreateCustomerDTO(person=person_dto, user=user_dto)

        with pytest.raises(EntityDuplicatedException):
            self.create_customer_usecase.execute(dto)

    def test_get_all_customers_usecase(self):        
        CustomerFactory()
        CustomerFactory()

        current_user = {
            'profile': {'name': 'manager'},
            'person': {'id': '1'}
        }

        customers = self.get_all_customers_usecase.execute(current_user)
        assert len(customers) == 2

    def test_delete_customer_usecase(self):
        customer = CustomerFactory()

        current_user = {
            'profile': {'name': 'manager'},
            'person': {'id': '1'}
        }

        self.delete_customer_usecase.execute(customer.id, current_user)
        
        customer = self.customer_gateway.get_by_id(customer.id)
        assert customer.is_deleted() is True

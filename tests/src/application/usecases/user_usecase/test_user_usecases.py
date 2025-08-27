import pytest
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.user.update_user_dto import UpdateUserDTO
from src.infrastructure.repositories.sqlalchemy.customer_repository import CustomerRepository
from src.infrastructure.repositories.sqlalchemy.user_repository import UserRepository
from src.application.usecases.user_usecase.get_all_users_usecase import GetAllUsersUsecase
from src.application.usecases.user_usecase.delete_user_usecase import DeleteUserUsecase
from src.application.usecases.user_usecase.update_user_password_usecase import UpdateUserPasswordUsecase
from tests.factories.customer_factory import CustomerFactory
from tests.factories.user_factory import UserFactory


class TestUserUsecases:
    
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.user_gateway = UserRepository(db_session)
        self.customer_gateway = CustomerRepository(db_session)
        self.get_all_users_usecase = GetAllUsersUsecase(self.user_gateway)
        self.delete_user_usecase = DeleteUserUsecase(self.user_gateway)
        self.update_user_password_usecase = UpdateUserPasswordUsecase(self.user_gateway, self.customer_gateway)

    def test_get_all_users_usecase(self):
        
        UserFactory(name='testuser1', password='testpassuser1')
        UserFactory(name='testuser2', password='testpassuser2')

        users = self.get_all_users_usecase.execute()
        assert len(users) == 2
        assert users[0].name == 'testuser1'
        assert users[1].name == 'testuser2'

    def test_delete_user_usecase(self):
        user = UserFactory(name='testuser', password='testpass123')

        self.delete_user_usecase.execute(user.id)
        
        user = self.user_gateway.get_by_id(user.id)
        assert user.is_deleted() is True

    def test_update_user_password_usecase(self):
        customer = CustomerFactory(user__name='testuser', user__password='testpass123')

        update_dto = UpdateUserDTO(old_password="testpass123", password='newpass123')
        updated_user = self.update_user_password_usecase.execute(customer.user.id, update_dto)

        assert updated_user.name == 'testuser'
        assert updated_user.verify_password('newpass123')

    def test_update_user_not_found_usecase(self):
        update_dto = UpdateUserDTO(old_password='updateduser', password='newpass123')
        
        with pytest.raises(EntityNotFoundException):
            self.update_user_password_usecase.execute(1, update_dto)

from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
import factory

from src.infrastructure.repositories.sqlalchemy.models.customer_model import CustomerModel
from tests.factories.person_factory import PersonFactory
from tests.factories.user_factory import UserFactory


fake = Faker()


class CustomerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = CustomerModel
        sqlalchemy_session_persistence = 'commit'

    person = factory.SubFactory(PersonFactory)
    person_id = factory.SelfAttribute('person.id')
    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute('user.id')

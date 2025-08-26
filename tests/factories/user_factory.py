import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from src.core.domain.entities.user import User
from src.infrastructure.repositories.sqlalchemy.models.user_model import UserModel
from tests.factories.profile_factory import ProfileFactory

fake = Faker()

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = UserModel
        sqlalchemy_session_persistence = "flush"

    name = factory.LazyAttribute(lambda _: fake.name())
    password_hash = factory.LazyAttribute(lambda _: User.hash_password(fake.password()))
    
    profile = factory.SubFactory(ProfileFactory)
    profile_id = factory.SelfAttribute('profile.id')

    class Params:
        user_entity = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        plain = kwargs.pop("password", None)
        if plain:
            kwargs["password_hash"] = User.hash_password(plain)

        return super()._create(model_class, *args, **kwargs)

__all__ = ["UserFactory"]


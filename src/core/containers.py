from dependency_injector import containers, providers

from src.config.database import get_db
from src.core.shared.identity_map import IdentityMap
from src.infrastructure.repositories.sqlalchemy.customer_repository import CustomerRepository
from src.infrastructure.repositories.sqlalchemy.permission_repository import PermissionRepository
from src.infrastructure.repositories.sqlalchemy.person_repository import PersonRepository
from src.infrastructure.repositories.sqlalchemy.profile_repository import ProfileRepository
from src.infrastructure.repositories.sqlalchemy.user_repository import UserRepository
from src.presentation.api.v1.controllers.auth_controller import AuthController
from src.presentation.api.v1.controllers.customer_controller import CustomerController
from src.presentation.api.v1.controllers.permission_controller import PermissionController
from src.presentation.api.v1.controllers.person_controller import PersonController
from src.presentation.api.v1.controllers.profile_controller import ProfileController
from src.presentation.api.v1.controllers.user_controller import UserController


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "src.presentation.api.v1.controllers.permission_controller",
        "src.presentation.api.v1.routes.permission_routes",
        "src.presentation.api.v1.controllers.profile_controller",
        "src.presentation.api.v1.routes.profile_routes",
        "src.presentation.api.v1.controllers.user_controller",
        "src.presentation.api.v1.routes.user_routes",
        "src.presentation.api.v1.controllers.person_controller",
        "src.presentation.api.v1.routes.person_routes",
        "src.presentation.api.v1.controllers.customer_controller",
        "src.presentation.api.v1.routes.customer_routes",
        "src.presentation.api.v1.controllers.auth_controller",
        "src.presentation.api.v1.routes.auth_routes",
    ])
    
    identity_map = providers.Singleton(IdentityMap)

    db_session = providers.Resource(get_db)

    permission_gateway = providers.Factory(PermissionRepository, db_session=db_session)
    permission_controller = providers.Factory(PermissionController, permission_gateway=permission_gateway)

    profile_gateway = providers.Factory(ProfileRepository, db_session=db_session)
    profile_controller = providers.Factory(ProfileController, profile_gateway=profile_gateway)


    person_gateway = providers.Factory(PersonRepository, db_session=db_session)
    person_controller = providers.Factory(PersonController, person_gateway=person_gateway)
    
    user_gateway = providers.Factory(UserRepository, db_session=db_session)

    customer_gateway = providers.Factory(CustomerRepository, db_session=db_session)
    customer_controller = providers.Factory(
        CustomerController,
        customer_gateway=customer_gateway,
        person_gateway=person_gateway,
        user_gateway=user_gateway,
        profile_gateway=profile_gateway
    )
    user_controller = providers.Factory(UserController, user_gateway=user_gateway, customer_gateway=customer_gateway)
    
    auth_controller = providers.Factory(
        AuthController,
        profile_gateway=profile_gateway,
        customer_gateway=customer_gateway
    )

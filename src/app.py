from fastapi import FastAPI

from src.core.containers import Container
from src.presentation.api.v1.middleware.auth_middleware import AuthMiddleware
from src.presentation.api.v1.middleware.custom_error_middleware import CustomErrorMiddleware
from src.presentation.api.v1.middleware.identity_map_middleware import IdentityMapMiddleware
from src.presentation.api.v1.routes.health_check import router as health_check_router
from src.presentation.api.v1.routes.auth_routes import router as auth_routes
from src.presentation.api.v1.routes.permission_routes import router as permission_routes
from src.presentation.api.v1.routes.profile_routes import router as profile_routes
from src.presentation.api.v1.routes.user_routes import router as user_routes
from src.presentation.api.v1.routes.person_routes import router as person_routes
from src.presentation.api.v1.routes.customer_routes import router as customer_routes


app = FastAPI(title="Hackathon SOAT10 - Auth Microservice - FIAP")

container = Container()
app.container = container

app.add_middleware(CustomErrorMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(IdentityMapMiddleware)

app.include_router(health_check_router, prefix="/api/v1")
app.include_router(auth_routes, prefix="/api/v1", tags=['auth'])
app.include_router(permission_routes, prefix="/api/v1", tags=["permissions"])
app.include_router(profile_routes, prefix="/api/v1", tags=["profiles"])
app.include_router(user_routes, prefix="/api/v1", tags=["user"])
app.include_router(person_routes, prefix="/api/v1", tags=["persons"])
app.include_router(customer_routes, prefix="/api/v1", tags=["customers"])

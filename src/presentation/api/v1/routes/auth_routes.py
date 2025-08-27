from typing import Annotated
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from src.core.containers import Container
from src.presentation.api.v1.controllers.auth_controller import AuthController
from src.core.auth.oauth2_password_request_form_custom import OAuth2PasswordRequestFormCustom
from src.core.domain.dtos.auth.auth_dto import LoginDTO, TokenDTO

router = APIRouter()
    

@router.post("/auth/token", response_model=TokenDTO)
@inject
def get_oauth_token(
    form_data: Annotated[OAuth2PasswordRequestFormCustom, Depends()],
    auth_controller: AuthController = Depends(Provide[Container.auth_controller])
):    
    return auth_controller.login_customer(LoginDTO(username=form_data.username, password=form_data.password))

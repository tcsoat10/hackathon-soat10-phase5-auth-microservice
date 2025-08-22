from fastapi import FastAPI

from src.presentation.api.v1.routes.health_check import router as health_check_router


app = FastAPI(title="Hackathon SOAT10 - Auth Microservice - FIAP")

app.include_router(health_check_router, prefix="/api/v1")

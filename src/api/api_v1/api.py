from fastapi import APIRouter

from api.api_v1.endpoints import health_check, water_solenoid

api_router = APIRouter()
api_router.include_router(health_check.router, prefix="/health_check", tags=["health_check"])
api_router.include_router(water_solenoid.router, prefix="/water_solenoid", tags=["water_solenoid"])
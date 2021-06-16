from fastapi import APIRouter

from weather_api.app import scheme
from weather_api.business import callbacks

router = APIRouter()


@router.get('')
async def weather(city: str, country: str) -> scheme.WeatherResponse:
    return scheme.WeatherResponse(**await callbacks.weather(city, country))

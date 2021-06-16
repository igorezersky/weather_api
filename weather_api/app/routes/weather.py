from fastapi import APIRouter

from weather_api.app.scheme import WeatherResponse

router = APIRouter()


@router.get('')
async def weather(city: str, country: str) -> WeatherResponse:
    return WeatherResponse()

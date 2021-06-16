from fastapi import APIRouter, Query

from weather_api.app import scheme
from weather_api.business import callbacks

router = APIRouter()


@router.get('')
async def weather(
    city: str = Query(..., example='Minsk'),
    country: str = Query(..., example='by', max_length=2, min_length=2)
) -> scheme.WeatherResponse:
    return await callbacks.weather(city, country.lower())

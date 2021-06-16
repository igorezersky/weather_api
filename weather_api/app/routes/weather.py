from fastapi import APIRouter, Query

from weather_api.business import callbacks, scheme

router = APIRouter()


@router.get(
    '',
    summary='Get weather for specified city',
    response_model=scheme.WeatherResponse
)
async def weather(
    city: str = Query(..., example='Bogota'),
    country: str = Query(..., example='co', max_length=2, min_length=2)
) -> scheme.WeatherResponse:
    return await callbacks.weather(city, country.lower())

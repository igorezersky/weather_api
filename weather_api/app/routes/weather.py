from fastapi import APIRouter, Query, status

from weather_api.app.core import exceptions
from weather_api.business import callbacks, scheme, errors

router = APIRouter(
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {'model': exceptions.ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': exceptions.ErrorResponse}
    }
)


@router.get(
    '',
    summary='Get weather for specified city',
    response_model=scheme.WeatherResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': errors.NotFound}
    }
)
async def weather(
    city: str = Query(..., example='Bogota'),
    country: str = Query(..., example='co', max_length=2, min_length=2)
) -> scheme.WeatherResponse:
    return await callbacks.weather(city, country.lower())

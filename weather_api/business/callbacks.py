import logging
from datetime import datetime
from typing import Dict

import aiohttp

from weather_api.business import converters
from weather_api.processors import configs

_logger = logging.getLogger(__name__)


async def weather(city: str, country: str) -> Dict:
    """ Callback for `weather` endpoint """

    requested_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url=configs.weather.api_url_format.format(
                    city=city,
                    country_code=country,
                    api_key=configs.weather.api_key.get_secret_value()
                )
        ) as resp:
            response_status = resp.status
            if response_status != 200:
                raise ValueError(resp.text())
            result = await resp.json()
    return dict(
        location_name=f'{city}, {country.upper()}',
        temperature=converters.kelvin2celsius(result['main']['temp']),
        wind=f'{result["wind"]["speed"]} m/s',
        cloudiness=converters.clouds2condition(result['clouds']['all']),
        pressure=f'{result["main"]["pressure"]} hpa',
        humidity=f'{result["main"]["humidity"]}%',
        sunrise=converters.utc2time(result['sys']['sunrise'] + result['timezone']),
        sunset=converters.utc2time(result['sys']['sunset'] + result['timezone']),
        geo_coordinates=f'[{result["coord"]["lon"]}, {result["coord"]["lat"]}]',
        requested_time=requested_time,
        forecast=''
    )

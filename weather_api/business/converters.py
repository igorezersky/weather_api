from datetime import datetime


def kelvin2celsius(temperature: float) -> str:
    """ Convert `temperature` from Kelvin to Celsius """

    return f'{int(temperature - 273.15)} °C'


def kelvin2fahrenheit(temperature: float) -> str:
    """ Convert `temperature` from Kelvin to Fahrenheit """

    return f'{int((temperature - 273.15) * 9/5) + 32} °F'


def utc2time(utctime: int) -> str:
    """ Convert UTC timestamp to current time """

    return datetime.utcfromtimestamp(utctime).strftime('%H:%M')


def clouds2condition(clouds: int) -> str:
    """ Convert clouds percentage to condition """

    clouds /= 100
    if clouds <= 1 / 8:
        condition = 'Sunny'
    elif clouds <= 3 / 8:
        condition = 'Mostly Sunny'
    elif clouds <= 5 / 8:
        condition = 'Partly Sunny'
    elif clouds <= 7 / 8:
        condition = 'Mostly Cloudy'
    else:
        condition = 'Cloudy'
    return condition

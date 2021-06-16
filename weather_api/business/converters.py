import time


def kelvin2celsius(temperature: float) -> str:
    """ Convert `temperature` from Kelvin to Celsius """

    return f'{int(temperature - 273.15)} °C'


def kelvin2fahrenheit(temperature: float) -> str:
    """ Convert `temperature` from Kelvin to Fahrenheit """

    return f'{int((temperature - 273.15) * 9/5) + 32} °F'


def utc2time(utctime: int) -> str:
    """ Convert UTC timestamp to current time """

    return time.strftime('%H:%M', time.localtime(utctime))

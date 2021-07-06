from pathlib import Path

from weather_api.app.core import App, ExceptionsHandler
from weather_api.configs import Configs

# main server processors
configs = Configs(package_dir=Path(__file__).parent)
exceptions_handler = ExceptionsHandler()
app = App(configs=configs, exceptions_handler=exceptions_handler)

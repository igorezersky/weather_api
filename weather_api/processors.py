from pathlib import Path

from weather_api.app.core import App
from weather_api.configs import Configs

# main server processors
configs = Configs(package_dir=Path(__file__).parent)
app = App(configs=configs)

from pathlib import Path

from weather_api.app import App, Configs, ExceptionsHandler

# main server processors
configs = Configs(package_dir=Path(__file__).parent)
exceptions_handler = ExceptionsHandler()
app = App(configs=configs, exceptions_handler=exceptions_handler)

""" This module contains settings containers. Different settings are stored in different containers, main access is
provided with `Configs` class help.
"""

import logging.config
from pathlib import Path
from typing import Any, Union

from pydantic import BaseModel, SecretStr
from ruamel.yaml import YAML
from starlette.config import Config as StarletteConfig

__all__ = ['ServerConfigs', 'WeatherConfigs', 'PathConfigs', 'Configs']


class Context(BaseModel):
    yml: Any
    env: Any

    @classmethod
    def load(
        cls,
        package_dir: Union[str, Path],
        yml_path: Union[str, Path] = None,
        env_path: Union[str, Path] = None
    ) -> 'Context':
        """ Load configs from environment and YAML file """

        package_dir = Path(package_dir)
        if not package_dir.exists():
            raise FileNotFoundError(package_dir)

        env_path = Path(env_path or f'{package_dir.parent}/.env')
        env_config = StarletteConfig(env_path if env_path.exists() else '')

        yaml = YAML()
        yml_path = Path(yml_path or f'{package_dir}/configs/configs.yml')
        with yml_path.open('r', encoding='utf-8') as fp:
            yml_config = yaml.load(fp)
        return cls(yml=yml_config, env=env_config)


class ServerConfigs(BaseModel):
    host: str
    port: int
    enable_cors: bool

    @classmethod
    def from_context(cls, context: Context) -> 'ServerConfigs':
        return cls(
            host=context.env.get('HOST', default=context.yml['server']['host'], cast=str),
            port=context.env.get('PORT', default=context.yml['server']['port'], cast=int),
            enable_cors=context.env.get('ENABLE_CORS', default=context.yml['server']['enable_cors'], cast=bool)
        )


class PathConfigs(BaseModel):
    logs: Path

    @classmethod
    def from_context(cls, context: Context) -> 'PathConfigs':
        obj = cls(logs=Path(context.yml['path']['logs']))
        obj.logs.mkdir(parents=True, exist_ok=True)
        return obj


class WeatherConfigs(BaseModel):
    api_key: SecretStr
    api_url_format: str

    @classmethod
    def from_context(cls, context: Context) -> 'WeatherConfigs':
        return cls(
            api_key=SecretStr(context.env.get('API_KEY')),
            **context.yml['weather']
        )


class Configs:
    """ Container of all system configs """

    def __init__(self, package_dir: Union[str, Path], **kwargs) -> None:
        self._context = Context.load(package_dir, **kwargs)

        self.server = ServerConfigs.from_context(self._context)
        self.path = PathConfigs.from_context(self._context)
        self.weather = WeatherConfigs.from_context(self._context)

        self.configure_logging()

    def configure_logging(self) -> 'Configs':
        """ Add logs directory path to all file handlers and apply logging configs """

        if 'handlers' in self._context.yml['logging']:
            for key in self._context.yml['logging']['handlers']:
                handler_fname = self._context.yml['logging']['handlers'][key].get('filename')
                if handler_fname:
                    self._context.yml['logging']['handlers'][key]['filename'] = f'{self.path.logs}/{handler_fname}'
        logging.config.dictConfig(self._context.yml['logging'])
        return self

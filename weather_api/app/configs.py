""" This module contains settings containers. Different settings are stored in different containers, main access is
provided with `Configs` class help.
"""

import logging.config
from pathlib import Path
from typing import Any, Dict, Union

from pydantic import BaseModel, SecretStr
from ruamel.yaml import YAML
from starlette.config import Config as StarletteConfig


class ServerConfigs(BaseModel):
    protocol: str
    host: str
    port: int
    exceptions: Dict[str, str]
    enable_cors: bool


class PathConfigs(BaseModel):
    logs: Path


class WeatherConfigs(BaseModel):
    api_key: SecretStr
    api_url_format: str


class SystemConfigs(BaseModel):
    yml: Any
    env: Any

    @classmethod
    def load(
        cls,
        package_dir: Union[str, Path],
        yml_path: Union[str, Path] = None,
        env_path: Union[str, Path] = None
    ):
        """ Load configs from environment and YAML file """

        package_dir = Path(package_dir)
        if not package_dir.exists():
            raise FileNotFoundError(package_dir)

        env_path = Path(env_path or f'{package_dir.parent}/.env')
        env_config = StarletteConfig(env_path if env_path.exists() else '')

        yaml = YAML()
        yml_path = Path(yml_path or f'{package_dir}/app/configs.yml')
        with yml_path.open('r', encoding='utf-8') as fp:
            yml_config = yaml.load(fp)
        return cls(yml=yml_config, env=env_config)


class Configs:
    """ Container of all system configs """

    def __init__(self, package_dir: Union[str, Path], **kwargs) -> None:
        self._raw = SystemConfigs.load(package_dir, **kwargs)

        self.server = ServerConfigs(
            protocol=self._raw.env.get('PROTOCOL', default=self._raw.yml['server']['protocol'], cast=str),
            host=self._raw.env.get('HOST', default=self._raw.yml['server']['host'], cast=str),
            port=self._raw.env.get('PORT', default=self._raw.yml['server']['port'], cast=int),
            enable_cors=self._raw.env.get('ENABLE_CORS', default=self._raw.yml['server']['enable_cors'], cast=bool),
            exceptions=self._raw.yml['server']['exceptions']
        )
        self.path = PathConfigs(logs=Path(self._raw.yml['path']['logs']))
        self.path.logs.mkdir(parents=True, exist_ok=True)
        self.weather = WeatherConfigs(
            api_key=SecretStr(self._raw.env.get('API_KEY')),
            **self._raw.yml['weather']
        )
        self.configure_logging()

    def configure_logging(self) -> 'Configs':
        """ Add logs directory path to all file handlers and apply logging configs """

        if 'handlers' in self._raw.yml['logging']:
            for key in self._raw.yml['logging']['handlers']:
                handler_fname = self._raw.yml['logging']['handlers'][key].get('filename')
                if handler_fname:
                    self._raw.yml['logging']['handlers'][key]['filename'] = f'{self.path.logs}/{handler_fname}'
        logging.config.dictConfig(self._raw.yml['logging'])
        return self

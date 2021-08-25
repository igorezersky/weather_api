import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.routing import NoMatchFound

from weather_api.configs import Configs


class App:
    def __init__(self, configs: Configs) -> None:
        self.server = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)  # trick to handle documentation hosting
        self.configs = configs.server

        if self.configs.enable_cors:
            self.enable_cors()

    def enable_cors(self) -> 'App':
        """ Enable CORS for all origins, methods and headers. Do not enable CORS on production servers

        Notes
        -----

        Read more about CORS: https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
        """

        self.server.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
        return self

    def run(self):
        """ Start `uvicorn` server from code """

        uvicorn.run(
            self.server,
            host=self.configs.host,
            port=self.configs.port,
            proxy_headers=True,
            forwarded_allow_ips='*'
        )

    def url_for(self, endpoint: str, **kwargs) -> str:
        """ Generate relative URL for `endpoint` """

        endpoint_parts = endpoint.split('.')
        endpoint_tags = endpoint_parts[:-1]
        endpoint_name = endpoint_parts[-1]
        if not endpoint_tags or not endpoint_name:
            raise NoMatchFound(endpoint)
        for route in self.server.routes:
            if endpoint_name != route.name or any(tag not in getattr(route, 'tags', []) for tag in endpoint_tags):
                continue
            try:
                url = route.url_path_for(endpoint_name, **kwargs)
                return url
            except NoMatchFound:
                pass
        raise NoMatchFound()

    def include_routers(self) -> 'App':
        """ Main application method: connect all exceptions handlers, endpoints and blueprints to app """

        from weather_api.app.routes import index, weather
        from weather_api.app.core import exceptions as _  # required for exceptions handlers connection

        self.server.include_router(weather.router, prefix='/weather', tags=['weather'])
        self.server.include_router(index.router, prefix='', tags=['index'])

        return self

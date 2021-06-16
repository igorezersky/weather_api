import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.routing import NoMatchFound

from weather_api.app.configs import Configs
from weather_api.app.exceptions import ExceptionsHandler


class App:
    def __init__(self, configs: Configs, exceptions_handler: ExceptionsHandler) -> None:
        self.server = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
        self.configs = configs.server

        if self.configs.enable_cors:
            self.enable_cors()

        if exceptions_handler:
            exceptions_handler.app = self
            for handler in exceptions_handler.handlers:
                self.server.add_exception_handler(handler.exception, handler.callback)

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

    async def handle_exception(self, status_code: int):
        """ Return formatted response for received exception """

        return JSONResponse(
            content=dict(
                status_code=status_code,
                message=dict(text=self.configs.exceptions[f'{status_code}'])
            ),
            status_code=status_code
        )

    def include_routers(self) -> 'App':
        from weather_api.app.routes import index, weather

        self.server.include_router(weather.router, prefix='/weather', tags=['weather'])
        self.server.include_router(index.router, prefix='', tags=['index'])

        return self

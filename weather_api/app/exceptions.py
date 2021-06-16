import logging
from dataclasses import dataclass
from typing import Callable, Union, Type

from fastapi import status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request

Exceptions = Union[HTTPException, Type[Exception], Exception, RequestValidationError]
_logger = logging.getLogger(__name__)


@dataclass
class Handler:
    exception: Union[int, Exceptions]
    callback: Callable


class ExceptionsHandler:
    def __init__(self, app=None) -> None:
        self.app = app
        self.handlers = [
            Handler(exception=RequestValidationError, callback=self.validation),
            Handler(exception=Exception, callback=self.system),
            Handler(exception=status.HTTP_404_NOT_FOUND, callback=self.http404),
            Handler(exception=status.HTTP_500_INTERNAL_SERVER_ERROR, callback=self.http500),
        ]

    async def validation(self, request: Request, exc: Exceptions):
        return await self.system(request, exc)

    async def system(self, _: Request, exc: Exceptions):
        _logger.error(exc)
        return await self.app.handle_exception(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def http404(self, _: Request, exc: Exceptions):
        _logger.debug(exc)
        return await self.app.handle_exception(status_code=status.HTTP_404_NOT_FOUND)

    async def http500(self, request: Request, exc: Exceptions):
        return await self.system(request, exc)

import logging
from dataclasses import dataclass
from typing import Callable, Union, Type

from fastapi import status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

Exceptions = Union[HTTPException, Type[Exception], Exception, RequestValidationError]
_logger = logging.getLogger(__name__)


class ErrorResponse(BaseModel):
    error: str


@dataclass
class Handler:
    exception: Union[int, Exceptions]
    callback: Callable


class ExceptionsHandler:
    def __init__(self) -> None:
        self.handlers = [
            Handler(exception=RequestValidationError, callback=self.validation),
            Handler(exception=Exception, callback=self.system),
            Handler(exception=HTTPException, callback=self.http)
        ]

    @staticmethod
    async def handle_exception(status_code: int, message: str) -> JSONResponse:
        """ Return formatted response for received exception """

        return JSONResponse(content=dict(error=message), status_code=status_code)

    async def validation(self, _: Request, exc: Exceptions):
        return await self.handle_exception(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=exc.detail
        )

    async def system(self, _: Request, exc: Exceptions):
        _logger.error(exc)
        return await self.handle_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message='Internal server error'
        )

    async def http(self, _: Request, exc: Exceptions):
        _logger.debug(exc)
        return await self.handle_exception(status_code=exc.status_code, message=exc.detail)

from fastapi import APIRouter, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse

from weather_api.processors import app

router = APIRouter()


@router.get('/', include_in_schema=False)
async def index() -> RedirectResponse:
    return RedirectResponse(app.url_for('index.healthcheck'), status_code=308)


@router.get('/openapi.json', include_in_schema=False)
async def openapi():
    return JSONResponse(get_openapi(title='Weather API', version='1.0.0', routes=app.server.routes))


@router.get('/docs', include_in_schema=False)
async def documentation():
    return get_swagger_ui_html(openapi_url=app.url_for('index.openapi'), title='docs')


@router.get('/healthcheck')
async def healthcheck():
    return HTMLResponse(
        content=f'It works. Explore the documentation at <a href="{app.url_for("index.documentation")}">/docs</a>',
        status_code=status.HTTP_200_OK
    )

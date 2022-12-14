import json

from celery import Celery
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.endpoints.document import api_router
from app.core.config import settings, setup_app_logging
from app.core.middlewares import ProcessTimeMiddleware


setup_app_logging(config=settings)
app = FastAPI(title="Document API")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origin_regex=settings.BACKEND_CORS_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(ProcessTimeMiddleware)

app.include_router(api_router)

@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(error['loc'][-1]+f": {error['msg']}")

    return JSONResponse(response, status_code=422)


###### Celery #######
celery = Celery(
    __name__,
    broker=settings.celery.brocker,
    backend=settings.celery.backend
)


celery.conf.imports = [
    'app.tasks.document_tasks'
]
#####################


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")

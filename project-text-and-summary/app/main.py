from fastapi import FastAPI

from app.api.endpoints.document import api_router


app = FastAPI(title="Document API")

app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")

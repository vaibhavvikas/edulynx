# Main file for the project
import logging

import uvicorn
from fastapi import APIRouter, FastAPI

from edulynx.routers.course_router import router

app = FastAPI()

api_router = APIRouter()
log = logging.getLogger(__name__)


@api_router.get("/", status_code=200)
def root():
    """
    Root Get
    """
    return {"msg": "Welcome to Edulynx!"}


app.include_router(api_router)
app.include_router(router)


def start():
    """Launched with `poetry run start` at root level"""
    print("App is Starting:", "http://localhost:8000")
    print("Swagger:", "http://localhost:8000/docs")
    log.info("App is Starting")
    uvicorn.run("edulynx.__main__:app", host="0.0.0.0", port=8000, log_config="log.ini")


if __name__ == "__main__":
    start()

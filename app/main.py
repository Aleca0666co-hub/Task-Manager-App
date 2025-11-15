from fastapi import FastAPI
from app.utils.logging import logger
from app.api.v2 import task_api 
from app.settings import settings

app = FastAPI(title=settings.APP_NAME,version=settings.VERSION,description="Task Management API")
app.include_router(task_api.router)

logger.info("------>☼.....Server Runing")

@app.get("/")
def root():
    return {"message":"Welcome to TodoAPP"}
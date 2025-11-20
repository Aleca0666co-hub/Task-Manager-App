from fastapi import FastAPI
from app.utils.logging import logger
from app.api.v3 import task_api 
from app.settings import settings

from app.models.base import Base,BaseTask
from app.models.task import Task
from app.database import engine

Base.metadata.create_all(bind=engine)



app = FastAPI(title=settings.APP_NAME,version=settings.VERSION,description="Task Management API")
app.include_router(task_api.router)

logger.info("------>☼.....Server Runing")

@app.get("/")
def root():
    return {"message":"Welcome to TodoAPP"}
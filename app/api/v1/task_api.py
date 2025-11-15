from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import TaskCreate, TaskRead
from app.crud.task import create_task, get_tasks 
from app.database import get_db
from fastapi import status

router = APIRouter(prefix="/task",tags=["Task"])

@router.post("/", response_model=TaskRead ,status_code=status.HTTP_201_CREATED )
def create(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db, task)

@router.get("/", response_model=list[TaskRead] ,status_code=status.HTTP_200_OK  )
def read(db: Session = Depends(get_db)):
    return get_tasks(db)
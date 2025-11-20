from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import TaskCreate, TaskRead
from app.database import get_db
from app.crud.v2.task import create_task,get_tasks,get_task_by_id,get_tasks_by_name,update_tasks,delete_task
from fastapi import status,HTTPException


router = APIRouter(prefix="/task",tags=["Task"])

@router.post("/", response_model=TaskRead ,status_code=status.HTTP_201_CREATED )
def create(task: TaskCreate, db: Session = Depends(get_db)):
    try: 
        return create_task(db, task)
    except RuntimeError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Inconsistency in the database")
        

@router.get("/", response_model=list[TaskRead] ,status_code=status.HTTP_200_OK  )
def read(db: Session = Depends(get_db)):
    return get_tasks(db)

@router.get("/{task_id}",response_model=TaskRead,status_code=status.HTTP_200_OK)
def get_task_id(task_id:int,db:Session=Depends(get_db)):
    entity=get_task_by_id(db,task_id)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
    return entity 
    
@router.put("/{task_id}",response_model=TaskRead, status_code=status.HTTP_202_ACCEPTED)
def update(task_id:int ,task:TaskCreate,db:Session=Depends(get_db)):
    entity=update_tasks(db,task_id,task)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
    return entity 
        
from app.utils.exceptions import TaskNotFoundError, DatabaseError

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete(task_id: int, db: Session = Depends(get_db)) -> dict:
    try:
        return delete_task(db, task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    except DatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")        

@router.get("/search/{name}", response_model=list[TaskRead], status_code=status.HTTP_200_OK)
def search_by_name(name: str, db: Session = Depends(get_db)):
    tasks = get_tasks_by_name(db, name)
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found with that name")
    return tasks
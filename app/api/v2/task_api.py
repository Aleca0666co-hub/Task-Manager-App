from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import TaskCreate, TaskRead
from todo_app.app.crud.v1.task import create_task, get_tasks,update_tasks ,delete_task 
from app.utils.exceptions import TaskNotFoundError
from app.database import get_db
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
    
@router.put("/{task_id}",response_model=TaskRead, status_code=status.HTTP_202_ACCEPTED)
def update(task_id:int ,task:TaskCreate,db:Session=Depends(get_db)):
    entity=update_tasks(db,task_id,task)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
    return entity 
        
@router.delete("/{task_id}",status_code=status.HTTP_200_OK)
def delete(task_id:int ,db:Session=Depends(get_db))->dict:
    deleted = delete_task(db,task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
        